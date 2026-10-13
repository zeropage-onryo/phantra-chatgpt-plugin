#!/usr/bin/env python3
"""Check the package against OpenAI's submission limits and the /mcp tool list.

    python3 scripts/check.py            # the manifest, the icons, every skill
    python3 scripts/check.py --tools    # also print which tools each skill names

Standard library only. Exit 0 when nothing failed; warnings do not fail.

The limits are the ones OpenAI's pages stated on 2026-10-13 (the FINAL
submission limits, which are tighter than package validation):
  https://developers.openai.com/plugins/deploy/submission
  https://developers.openai.com/plugins/deploy/submission-errors
The two pages disagree on the root `description` (4,000 against 1,024
characters); the smaller one is checked.

The tool list is scripts/mcp-tools.txt, read off the studio server's code.
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = ("Productivity", "Creativity", "Developer Tools", "Business & Operations",
              "Data & Analytics", "Communication", "Education & Research", "Security",
              "Finance", "Healthcare", "Travel", "Entertainment", "Other")
SKILL_LINES = 100          # this package's own rule; OpenAI says only "keep it concise"
SKILL_DESCRIPTION = 1024
IDENTITY = 64              # "plugin-name:skill-name"
PRICE = re.compile(r"\b\d+\s+credits?\b|\$\s?\d", re.I)

fails: list[str] = []
warns: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def names(path: str) -> tuple[list[str], list[str]]:
    """(names, names marked "?") from a one-per-line list with # comments."""
    plain, soft = [], []
    for line in (ROOT / path).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        name, _, mark = line.partition(" ")
        (soft if mark.strip() == "?" else plain).append(name)
    return plain, soft


def luminance(hex_colour: str) -> float:
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def https(label: str, url, limit: int = 1024) -> None:
    if not isinstance(url, str) or not url.startswith("https://"):
        fail(f"{label} must be an https URL, got {url!r}")
    elif len(url) > limit or "@" in url.split("/")[2]:
        fail(f"{label} is over {limit} characters or carries credentials")


def png_size(path: Path) -> tuple[int, int]:
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", head[16:24])


def check_manifest(tools: set[str]) -> dict:
    manifest = json.loads((ROOT / "plugin.json").read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())
    if len(mcp.get("mcpServers", {})) != 1:
        fail("mcp.json must declare exactly one MCP server")
    for server in mcp.get("mcpServers", {}).values():
        https("mcp.json url", server.get("url"), 2048)

    name = manifest.get("name", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name):
        fail(f"name {name!r}: 1-64 of letters, digits, _ and -, starting with a letter or digit")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        fail("version must be semantic (1.0.0)")
    desc = manifest.get("description", "")
    if not desc or len(desc) > 1024:
        fail(f"description is {len(desc)} characters (1-1,024)")
    https("homepage", manifest.get("homepage"), 2048)

    ext = manifest["extensions"]["com.openai"]
    face = ext["interface"]
    for key, limit in (("displayName", 30), ("shortDescription", 30),
                       ("longDescription", 4000), ("developerName", 80)):
        value = face.get(key, "")
        if not value or len(value) > limit:
            fail(f"{key} is {len(value)} characters (1-{limit})")
    if "\n" in face.get("shortDescription", ""):
        fail("shortDescription must be one line")
    if face.get("category") not in CATEGORIES:
        fail(f"category {face.get('category')!r} is not one of {list(CATEGORIES)}")
    caps = face.get("capabilities", [])
    if len(caps) > 20 or any(not c or len(c) > 120 or "\n" in c for c in caps):
        fail("capabilities: at most 20, each one line of 1-120 characters")
    prompts = face.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if len(prompts) > 3:
        fail(f"defaultPrompt has {len(prompts)} entries (at most three)")
    if len({" ".join(p.lower().split()) for p in prompts}) != len(prompts):
        fail("defaultPrompt entries must be unique")
    for p in prompts:
        if not p or len(p) > 128 or "\n" in p or "@" in p:
            fail(f"defaultPrompt {p!r}: one line of 1-128 characters, no @mention")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        https(key, face.get(key))
    for key, against in (("brandColor", "#FFFFFF"), ("brandColorDark", "#212121")):
        colour = face.get(key, "")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", colour):
            fail(f"{key} must be #RRGGBB")
        elif contrast(colour, against) < 2:
            fail(f"{key} {colour} has under 2:1 contrast against {against}")
    for key in ("composerIcon", "composerIconDark", "logo", "logoDark"):
        rel = face.get(key)
        if key in ("composerIcon", "logo") and not rel:
            fail(f"{key} is required")
        if not rel:
            continue
        path = ROOT / rel
        if not rel.startswith("./") or ".." in rel or not path.is_file():
            fail(f"{key} {rel!r} must be a ./ path to a file in the package")
            continue
        size = path.stat().st_size
        try:
            w, h = png_size(path)
        except ValueError:
            fail(f"{key} {rel} is not a PNG this check can read")
            continue
        if w != h or not 48 <= w <= 4096 or size > 5 * 1024 * 1024:
            fail(f"{key} {rel} is {w}x{h}, {size} bytes (square, 48-4096 px, at most 5 MiB)")

    onboarding = ext.get("onboardingSkill")
    if onboarding and not (ROOT / onboarding).is_file():
        fail(f"onboardingSkill {onboarding!r} is not in the package")

    review = ext.get("review", {})
    for banned in ("test_credentials", "reviewer_instructions"):
        if banned in review:
            fail(f"review.{banned} is rejected in the ZIP; it goes in the dashboard")
    cases = review.get("test_cases", {})
    pos, neg = cases.get("positive", []), cases.get("negative", [])
    if len(pos) != 5 or len(neg) != 3:
        fail(f"test cases: {len(pos)} positive and {len(neg)} negative (exactly 5 and 3)")
    for case in pos:
        for key in ("description", "prompt", "tools_triggered", "expected_behavior"):
            if not case.get(key):
                fail(f"positive case {case.get('description')!r} has no {key}")
        named = [t.strip() for t in str(case.get("tools_triggered", "")).split(",") if t.strip()]
        for tool in named:
            if tool not in tools:
                fail(f"positive case {case.get('description')!r} names `{tool}`, "
                     "which is not on /mcp")
    for case in neg:
        if not case.get("description") or not case.get("prompt"):
            fail("a negative case needs a description and a prompt")
    demo = review.get("demo_recording_url", "")
    https("review.demo_recording_url", demo)
    if "TO-RECORD" in demo:
        warn("review.demo_recording_url is still the placeholder: record the walkthrough")
    if not isinstance(review.get("commerce"), bool):
        fail("review.commerce must be true or false")
    pub = ext.get("publication", {})
    if not pub.get("release_notes"):
        fail("publication.release_notes is empty")
    for code in pub.get("countries", []):
        if not re.fullmatch(r"[A-Z]{2}", code):
            fail(f"publication country {code!r} must be an uppercase code")

    listing = " ".join([desc, face.get("shortDescription", ""), face.get("longDescription", ""),
                        pub.get("release_notes", ""), *prompts])
    if PRICE.search(listing):
        fail("the listing text states a price; prices come from the tools")
    return manifest


def check_skills(plugin: str, tools: set[str], show_tools: bool) -> None:
    banned, soft = names("scripts/other-tools.txt")
    seen: dict[str, str] = {}
    folders = sorted(p for p in (ROOT / "skills").iterdir())
    for folder in folders:
        if not folder.is_dir() or folder.name.startswith("."):
            warn(f"skills/{folder.name} is not a skill folder; it is not imported")
            continue
        path = folder / "SKILL.md"
        if not path.is_file():
            fail(f"skills/{folder.name} has no SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            fail(f"{folder.name}: no front matter between --- lines")
            continue
        end = lines.index("---", 1)
        front = {}
        for line in lines[1:end]:
            key, sep, value = line.partition(":")
            if not sep or not key.strip():
                fail(f"{folder.name}: front matter line {line!r} is not `key: value`")
            front[key.strip()] = value.strip()
        name, description = front.get("name", ""), front.get("description", "")
        if name != folder.name:
            fail(f"{folder.name}: name is {name!r}; it must match its folder")
        if name in seen:
            fail(f"{folder.name}: the name {name!r} is also used by {seen[name]}")
        seen[name] = folder.name
        if len(f"{plugin}:{name}") > IDENTITY:
            fail(f"{folder.name}: `{plugin}:{name}` is over {IDENTITY} characters")
        if not description or len(description) > SKILL_DESCRIPTION:
            fail(f"{folder.name}: description is {len(description)} characters "
                 f"(1-{SKILL_DESCRIPTION})")
        if "Use " not in description or "NOT for" not in description:
            warn(f"{folder.name}: description has no 'Use ...' or no 'NOT for' clause")
        if not "\n".join(lines[end + 1:]).strip():
            fail(f"{folder.name}: nothing below the front matter")
        if len(lines) > SKILL_LINES:
            fail(f"{folder.name}: {len(lines)} lines (at most {SKILL_LINES})")
        named = set()
        for n, line in enumerate(lines, 1):
            for token in re.findall(r"`([a-z][a-z0-9_]*)`", line):
                if token in tools:
                    named.add(token)
                elif token in banned:
                    fail(f"{folder.name}:{n} names `{token}`, which is not a tool on /mcp")
                elif token in soft:
                    warn(f"{folder.name}:{n} `{token}` is not a tool on /mcp; fine as a "
                         f"field or a value: {line.strip()[:90]}")
            if n > end and PRICE.search(line):
                fail(f"{folder.name}:{n} types a price; the tools give prices: "
                     f"{line.strip()[:90]}")
        for other in re.findall(r"\(([a-z][a-z0-9-]+)\)", description):
            if other not in {f.name for f in folders} and "-" in other:
                fail(f"{folder.name}: its description points at ({other}), "
                     "which is not a skill here")
        if show_tools:
            print(f"  {folder.name}: {', '.join(sorted(named)) or '(no tool named)'}")
    print(f"{len(seen)} skills")


def main() -> int:
    tools = set(names("scripts/mcp-tools.txt")[0])
    print(f"{len(tools)} tools on /mcp (scripts/mcp-tools.txt)")
    manifest = check_manifest(tools)
    face = manifest["extensions"]["com.openai"]["interface"]
    print(f"displayName {len(face['displayName'])}/30, shortDescription "
          f"{len(face['shortDescription'])}/30, longDescription "
          f"{len(face['longDescription'])}/4000, {len(face['defaultPrompt'])} prompts "
          f"(longest {max(map(len, face['defaultPrompt']))}/128), category {face['category']}")
    check_skills(manifest["name"], tools, "--tools" in sys.argv)
    for line in warns:
        print("warning:", line)
    for line in fails:
        print("FAIL:", line)
    print("ok" if not fails else f"{len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
