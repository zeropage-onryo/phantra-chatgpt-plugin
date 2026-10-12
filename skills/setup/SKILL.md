---
name: setup
description: The first minutes with Zero Page Studio in ChatGPT: sign in once, see what the workspace holds, and learn the one rule about spending. Use right after the plugin is installed, when the person asks how to start, or when a call answers that the sign-in has no workspace yet. NOT for the work itself: writing a scene (write-scene), pricing and rendering (price-and-hand-off), choosing ideas (ideas-and-projects), or explaining credits (credits-and-limits).
---

# Setting up Zero Page Studio

Zero Page Studio is the person's own AI production studio: projects, their
reference photos (elements), scenes written as timed shots, and the renders
those scenes become. This plugin works in their existing studio account.

## 1. The sign-in

The person signs in once at https://zeropage.studio to create their workspace,
then connects this plugin, which opens the studio's sign-in and a consent
page. If a call answers that the sign-in has no workspace yet, say exactly
that: sign in once on the site, then reconnect.

## 2. Look before you make

Call `whoami` (the workspace and who is signed in), then `recent` (the latest
projects, scenes and renders) and `elements` (the photos every scene is held
to). Say in two sentences what is there. A new workspace has no elements yet:
offer `upload_link` (a one-time page for a photo from their phone) or
`add_element` (a picture or product page by address) before any scene.

## 3. The one rule about spending

Reading, writing scenes, the free edits (`reformat`, `trim_clip`,
`assemble_clips`, `share_link`) and everything else cost nothing. Only a
still (`generate_image`) and a render (`approve`, after `quote`) spend the
account's credits, and each one is quoted first: show the person the price
in credits and the balance, wait for their yes in this chat, and only then
make the call that spends. Never say yes for them, and never spend twice. If
a quote says the credits are short, say so and that credits are added in the
studio; start nothing.

## 4. Where to go next

- "Start a project" → start-a-project. "Write the scene" → write-scene.
- "What would it cost, render it" → price-and-hand-off.
- "What is free, where did my credits go" → credits-and-limits.
