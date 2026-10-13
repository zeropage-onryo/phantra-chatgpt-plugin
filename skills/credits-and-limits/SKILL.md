---
name: credits-and-limits
description: Explain what is free and what costs credits in Phantra, read the balance and where credits went, walk the quote -> yes -> approve flow every spend takes, set up draft-first rendering, and explain a refusal or the connector's rate limit (a 429). Use when someone asks how much something costs, what credits are, what their balance is, where their credits went, how to render cheaper, what a quote token is, why a call was refused, why they got "rate limited", or whether an action will charge them. NOT for pricing a particular scene and approving its render (price-and-hand-off) and NOT for choosing ideas (ideas-and-projects).
---

# Credits and limits

## What is free

**Every read and every write spends nothing.** Reads: `projects`, `project`, `elements`,
`scene`, `quote`, `image_models`, `video_models`, `library`, `balance`, `credit_history`,
`recommend_model`, `what_works`, `job`...; writes: `create_project`, `add_element`,
`upload_link`, `write_scene`, `duplicate_scene`, `set_preferences`, `save_recipe`. The
free edits -- `reformat`, `trim_clip`, `assemble_clips` -- run on the studio's own server
and spend nothing: each starts a job you follow with `job` (`wait` holds up to 15 seconds)
and makes a NEW item in the library, the source untouched. Writing the prompt happens in
this chat. Only `generate_image`, `apply_effect` and `approve` spend, each quoted first.

## What costs credits

- **A still**: `generate_image` WITHOUT `quote_token` draws nothing and answers the quote:
  the credits (`image_models` lists each model's at 1:1), the balance after
  it and a `quote_token`. The SAME call WITH that token starts the job.
- **An effect** (`effects` lists them): `apply_effect` WITHOUT `quote_token` runs nothing
  and answers the quote; the SAME call WITH its token starts the job (effects).
- **Keyframes**: one still per shot. `quote` says how many are still to draw and the
  credits for `each`; `approve` with `what="keyframes"` and its `tokens` draws them.
- **The clip**: one render per shot still without a clip, priced by model, length and
  frame. `quote` lists `clip.renders` (part, seconds, credits, `token`) and the
  total. `approve` with `what="clip"`, those `tokens` and
  the same `provider`, `model`, `frame` and `duration` renders at exactly that price.

A token is good for one hour, for exactly that request, and once. Credit is held when the
job starts and released if the render fails; `job` follows it and `scene` shows what
landed. Credits are added in the studio, never here. Prices are in credits in every tool reply; repeat them as returned and never convert to money.

## The balance, and where credits went

- `balance`: what is available, what is held by renders in flight, the plan, and each
  credit lot with what is left and when it expires. Call it when the person asks what they
  have; never guess from an old quote.
- `credit_history`: every hold, charge, return, grant and expiry, newest first, each with
  what it was for and the balance it left. Pass the reply's `next` as `before` to page
  back. This answers "what did that cost me".
- `quote` also returns `balance`, `credits_needed` and `affordable` for one scene; report
  those three plainly beside the price (price-and-hand-off).

## Draft first: a cheaper frame to check a take

Wan 3.0 and Seedance 2.5 have a cheaper 480p **draft frame**; `video_models` shows it
where a model has one. Drafting pays when not every take is kept:

1. `recommend_model` with `draft` true ranks models with a draft frame first (the rest
   still appear), each with its reason and its credits at the model's default frame -- not
   the draft price; `quote` prices the draft exactly.
2. `set_preferences` with `video_model` set to one of those models and `draft_first` true
   makes `quote` (called with no renderer choice) price the draft frame and say so in
   `preference`; a value the catalogue lacks is refused.
3. Show the draft price, get the yes, then `approve` with the quote's `tokens` and
   renderer choice. A take they like is **finished (upscaled) in the studio**, not here.

## Say the cost, then wait for the yes

Before any call that spends, say what it would cost from the quote, in credits beside the
balance, and WAIT for an explicit yes in this chat. Never approve on the person's behalf,
never spend twice, never pass a token or call `approve` on a guess. If `affordable` is
false, say so first and that credits are added in the studio, and make no call.

## Refusals you will see (repeat them in their own words; never retry the same call)

- `insufficient_credits` (`needs`, `available`): stop; nothing was charged. Say `needs`
  against `available` and that credits are added in the studio; pass on no link.
- `already_used` on a token: the first call started the job; poll `job` for it. Nothing
  new was charged; a new render needs a new quote and a new yes. A stale, expired or
  changed quote is refused the same way: quote again, show the new price, get a new yes.
- `needs_reference` on a saved scene: it has no photos, so it waits as a draft scene. Add
  one (`add_element`, `upload_link`, or a ref from `elements`) and save it again with its
  `scene_id`. It cannot be priced.
- A photo ref that is refused: it was not one `elements` listed for this person. Read
  `elements` again and use a ref exactly as listed.
- `add_element` refused: the address was not https, neither an image file nor a product
  page, or too large. Say which; ask for the picture itself (or give an `upload_link`).
- `set_preferences` or a free edit refused: the value is not in the live catalogue
  (`preferences` lists the choices), the range lay outside the clip, the clips' shapes
  differ (`letterbox` on `assemble_clips`), or the id was not one `library` listed.
- "no scene N" / "no project N": the id is not one this person can see. Re-read `projects`
  or the project rather than retrying the id.
- "no workspace yet": the person has not signed in at https://phantra.ai. One web
  sign-in creates the workspace; then reconnect.
- `rate_limited` (HTTP 429): too many calls in one minute from this account. The response
  carries `Retry-After` in seconds. Wait that long, then continue; do not loop on it. The
  limit is generous (over a hundred calls a minute) and only a tight loop reaches it: read
  `scene` or `job` on request.

## What is never charged or changed through this connector

Nothing is posted or removed, no payment method is touched, and nothing is rendered or
drawn without a quote shown and a yes in this chat. Every edit makes a new item; rewriting
a scene with `write_scene` replaces the text it had, so show the new version and get a yes
first. Buying credits and changing a plan happen in the studio, never here.
