---
name: effects
description: Changes something already in the person's Phantra library with `apply_effect`: an image edit, a background removal, a camera move or animated template on a still, an upscale or added sound on a clip, a cut-out. Picks the effect from `effects`, quotes it in credits and runs it only on the person's yes. Use when someone asks to edit, animate, upscale or add sound to something already made. NOT for a new still (thumbnails), the free edits (edit-and-deliver) or a scene's sound line (sound-plan).
---

# Effects

An effect takes something that already exists in the person's library and
makes a NEW item from it; the source is never changed. Every effect spends
credits, so every one is quoted first and runs only on their yes. Looking
at the menu costs nothing.

## 1. Is there a free way first?

A new shape by padding or cropping is `reformat`; a shorter clip or clips
joined is `trim_clip` or `assemble_clips`. None costs credits. Use an effect
when the picture itself has to change, and say so when a free edit would do.

## 2. Read the menu, never recite it

`effects` lists what `apply_effect` can run. `category` narrows it:

| `category` | what is in it |
|---|---|
| `image_edit` | change an image by instruction; remove its background |
| `video_effect` | one-click animated templates on a still |
| `camera` | a named camera move on a still |
| `finish` | a clip upscaled or smoothed, given sound, extended to a new shape, or cut out from its background |

Each row says what it `takes` (an image or a clip) and how many `sources`,
whether a `prompt` is required, optional or refused, its `options` with
their legal values, and a `note` with its limits (a longest clip, a number
of images). Long option lists are sampled: call `effects` with `effect` set
to one row's id for every value. Never name an effect, a template or a
camera move from memory; one the menu does not list is refused.

## 3. What it acts on

`sources` are ids from `library`, and nothing else:

- `gen:<id>`: something made in their studio (a still, a rendered clip, an
  earlier effect's result);
- `asset:<id>`: a file they uploaded.

A web address, a photo that is only an element, or anything else is
refused, and only their own ids work. A picture not in the library yet comes
in through `upload_link`; `library` then lists it with its id. An image
effect takes images; a clip effect takes ONE clip, measured before pricing.

## 4. Quote, yes, run

1. `apply_effect` with `effect`, `sources`, the `options` and `prompt` that
   row needs, and NO `quote_token`. Nothing runs. The answer is the quote:
   the effect and options exactly as they will run, the sources, the
   credits, the balance and the balance after, a `quote_token`, and for a
   clip its measured length and size.
2. Say what will be made and from what, with the quote's own credits, and
   WAIT for an explicit yes in this chat.
3. Call `apply_effect` again with the SAME arguments plus that
   `quote_token`. It answers a `job_id`; `job` with `wait` 15 until `done`
   gives the result's address and its `ref`, a new `gen:<id>` in `library`.

The menu's `credits` is the price at an effect's default options, and null
when the price depends on the clip it is given; the quote is the price of
the real request, so read that one out. A token works once, for one hour
and for exactly that request: a different effect, option, source or prompt
needs a new quote and a new yes. A repeat with a used token answers
`already_used` and charges nothing.

## 5. What to ask before quoting

- **An edit by instruction**: the change in one sentence, and what must
  stay the same ("the label stays readable, only the background changes").
- **A template or a camera move**: which one, from the menu's own names;
  read a few out rather than guessing what a name does.
- **Sound**: what it should sound like, as the prompt.
- **A new shape by extension**: the shape, and what belongs in the new
  area. Say that the added area is generated, not filmed.
- **A cut-out**: a person or an object, and a see-through background or a
  flat colour. The row's `note` says which file type each gives.

## 6. Chains

A result is an ordinary library item, so it can be the next source: a still
given a camera move, that clip given sound, that clip upscaled. Each link
is its own quote and its own yes. Say the whole chain and how many quotes
it is before starting, and stop after any step they do not like.

## The spending rules

- Never run an effect on the person's behalf, never twice on one yes, and
  never one they did not name.
- `refused: insufficient_credits` (with `needs` and `available`): stop, say
  both numbers and that credits are added in the studio.
- A refusal comes in plain words (a clip too long, an option not on the
  list, a source not theirs). Repeat it and change something.
- Never state a price yourself, and never promise how a result will look.
- A person's face is edited only at their own request, on their own
  photo. Never use an edit to put someone where they were not, to change
  what a product is, or to remove a mark that is not theirs.
