# Phantra AI for ChatGPT

The plugin package submitted to OpenAI's plugin directory (`https://platform.openai.com/plugins`):
Phantra's AI image and video generator as an MCP server, the skills that drive it, and
the icons. What it does and how to connect it: <https://phantra.ai/mcp>.

- `plugin.json`: identity, the listing (`extensions.com.openai.interface`), the onboarding skill,
  the review cases (five positive, three negative), `commerce: false`, publication.
- `mcp.json`: the server, `https://api.phantra.ai/mcp` (37 tools), OAuth with dynamic client
  registration. A still is drawn and a scene rendered from the chat, each after a quote in
  credits and the person's explicit yes.
- `skills/`: thirty-one skills for this server (listed below), one of them `setup`, which OpenAI
  runs after install.
- `assets/`: the four icons.
- `scripts/`: the package check and the tool list it reads. Not part of the ZIP.

## Check, then build

    python3 scripts/check.py

checks the manifest against OpenAI's final submission limits (30-character name and short
description, three starter prompts of 128 characters, the category list, https links, square
icons, five and three test cases) and every skill against the tools the server has
(`scripts/mcp-tools.txt`). It needs nothing but Python 3. Add `--tools` to list the tools each
skill names.

Build the ZIP from this folder, so the manifest sits at the ZIP's root:

    zip -r ../phantra-ai-chatgpt-1.3.0.zip plugin.json mcp.json assets skills README.md LICENSE

## The skills

Thirty-one, each a `SKILL.md` of at most a hundred lines that names only tools the server has.

| for | skills |
|---|---|
| getting started | `setup`, `phantra-ai-use`, `start-a-project`, `ideas-and-projects` |
| ads | `product-ad-set`, `ad-formats`, `ad-variations`, `product-shots`, `explainer` |
| creator-style video | `ugc-ad`, `ugc-review`, `ugc-unboxing`, `ugc-tutorial`, `ugc-try-on` |
| covers and scripts | `thumbnails`, `youtube-script` |
| changing what is made | `effects` |
| writing a scene | `write-scene`, `storyboard`, `hooks-and-first-seconds`, `camera-moves`, `look-matching`, `sound-plan`, `model-prompting`, `series-and-continuity` |
| pricing, finishing, delivering | `price-and-render`, `credits-and-limits`, `edit-and-deliver`, `platform-delivery` |
| a person's own style and clients | `brand-kit-from-my-work`, `client-treatment` |

Not here, because the server has no tool for them yet: narration or a voice, subtitles on the
video, and a website builder.

## Before submitting

- TODO(Mike): record the demo walkthrough by hand and put its https address in
  `review.demo_recording_url` (`plugin.json`). The value there now is a placeholder, and the
  check warns until it is replaced.
- The reviewer's sign-in goes in the dashboard's Review details, never in this package.

## Help

Questions and problems: support@phantra.ai, or an issue on this repository.

The Claude plugin is a different package for a different directory, in
[phantra-claude-plugin](https://github.com/zeropage-onryo/phantra-claude-plugin); it points at
the server's other address, `/mcp/claude`, which never renders.
