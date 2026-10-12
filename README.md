# Zero Page Studio for ChatGPT

The plugin package submitted to OpenAI's plugin directory (`https://platform.openai.com/plugins`):
the Zero Page Studio render door as an MCP server, the studio's skills ported to it, and the icons.

- `plugin.json`: identity, the listing (`extensions.com.openai.interface`), the onboarding skill,
  the review cases (five positive, three negative), `commerce: false`, publication.
- `mcp.json`: the render door, `https://api.zeropage.studio/mcp` (35 tools), OAuth with dynamic
  client registration. On this door a still is drawn and a scene rendered from the chat, each after
  a quote in credits and the person's explicit yes.
- `skills/`: the studio's skills for this door, plus `setup`, which OpenAI runs after install.
- `assets/`: the four icons.

Build the ZIP from this folder, so the manifest sits at the ZIP's root:

    zip -r ../zeropage-studio-chatgpt-1.0.0.zip plugin.json mcp.json assets skills README.md LICENSE

The Claude plugin is a different package for a different directory, in
[zeropage-studio-plugin](https://github.com/zeropage-onryo/zeropage-studio-plugin); it points at the
other door, `/mcp/claude`, which never renders.
