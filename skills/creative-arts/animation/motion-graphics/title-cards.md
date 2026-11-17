---
id: creative-arts.animation.motion-graphics.title-cards
name: title-cards
category: creative-arts
field: animation
product: motion-graphics
tags: [motion-graphics, title-card, text, overlay, ffmpeg, drawtext, compositor, captions, lower-third, typography]
level: advanced
status: verified
description: "Title cards, lower-thirds and credits via ffmpeg drawtext: Windows fontfile escaping, shadow, alpha fades, scanline/grain/vignette texture, palette discipline."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# title-cards — real text frames, not black slates

**Goal:** the `TITLE`/`FX`-text shots a shot-renderer would otherwise slate black —
the show title card, act breaks, end card, diegetic on-screen text, lower-thirds,
credits — built into real frames that match the show's retro-TV look. Reusable
title/lower-third/credits craft, grounded in a card that actually shipped.

## In this pipeline

Grounded in `series/production/build_fx.py` → `title_card(out, d=4.0)`, the verified
builder that rendered the **HOLLOW CREEK / R E R U N S** opening card (1920x1080 @
24fps, ffmpeg only, no gen-AI). Palette constants from that script: gold
`#e0a93b`, cream `#f2e7cf`, mint `#5fe39b`, dark-warm bg `#140f0a`. The card is a
single `-vf` filter chain over an `lavfi color` source; the final assembly splices
these FX clips over the black slates at the same `dur_s`, so timing is unchanged.

## The chain (what the shipped card does, in order)

Source: `-f lavfi -i color=c=0x140f0a:s=1920x1080:r=24:d=4`. Then the `-vf`:

1. **Fill the background** — `drawbox=...:color=0x140f0a:t=fill`. A dark warm base,
   not pure black, so the glow/vignette have something to sit on.
2. **Title** — `drawtext` with the brand face and a drop shadow:
   ```
   drawtext=fontfile='C\:/Windows/Fonts/georgiab.ttf':text='HOLLOW CREEK':
   fontcolor=0xe0a93b:fontsize=168:x=(w-text_w)/2:y=360:
   shadowcolor=0x000000AA:shadowx=4:shadowy=5:
   alpha='if(lt(t,0.6),t/0.6,1)'
   ```
   - **Windows fontfile colon escape**: `C\:/Windows/Fonts/georgiab.ttf`. The colon
     after the drive letter is the libavfilter option separator; escape it with a
     backslash or the chain dies with a parse/"No such filter" error. Forward slashes
     (not backslashes) for the rest of the path.
   - Gold `#e0a93b`, `fontsize=168`, horizontally centred (`x=(w-text_w)/2`), fixed
     `y=360` so the mint underline and subtitle sit in known positions below it.
   - **Drop shadow** `shadowcolor=0x000000AA` (semi-transparent black) offset
     `+4,+5` — lifts the text off the textured background so scanlines don't eat it.
   - **Fade in via alpha expression**: `alpha='if(lt(t,0.6),t/0.6,1)'` ramps 0→1 over
     the first 0.6s. Driving `alpha` with `t` is the per-element fade; prefer it over
     a global `fade` filter when different elements come up at different times.
3. **Mint underline accent** — `drawbox=x=(iw-520)/2:y=560:w=520:h=4:color=0x5fe39b:
   t=fill:enable='gt(t,0.5)'`. A 520x4 mint rule, centred, that appears after 0.5s
   (`enable='gt(t,0.5)'`). A single accent bar is the cheapest way to make flat text
   look designed; the brand mint ties it to the show's HUD/seam colour.
4. **Subtitle** — the `"R E R U N S"` line in cream `#f2e7cf`, `fontsize=58`, centred
   at `y=600`, fading in *later and slower*:
   `alpha='if(lt(t,1.0),max(0\,(t-0.6)/0.4),1)'` — note `max(0\,...)` clamps the
   expression non-negative before t=0.6 (the comma inside the expression is escaped
   `\,` so it isn't read as a filter-arg separator). Letter-spacing the word by hand
   (`R E R U N S`) gives a broadcast-ident feel without a kerning feature.
5. **TV texture pass**, applied over the finished text so it unifies the frame:
   - **Scanlines** via `geq`:
     `geq=lum='lum(X,Y)*(0.82+0.18*sin(Y*3.14159))':cb='cb(X,Y)':cr='cr(X,Y)'` —
     modulates luma by a sine of the Y coordinate (bright/dark horizontal lines),
     leaving chroma untouched. `0.82+0.18*sin(...)` keeps lines subtle (82–100%
     brightness), not a harsh CRT grille.
   - **Grain** `noise=alls=8:allf=t` — light temporal noise (`allf=t` = re-randomised
     each frame so it shimmers like film/sensor grain, not a frozen dither).
   - **Vignette** `vignette=PI/5` — gentle corner darkening to gather the eye.

Output: `-c:v libx264 -pix_fmt yuv420p -r 24` (delivery-safe; see
`creative-arts.animation.encode-delivery.youtube-master`).

## Generalising — lower-thirds, act breaks, credits

The same primitives cover the whole title kit:

- **Lower-third**: a `drawbox` bar pinned to the lower title-safe area + two stacked
  `drawtext` (name large, role small), alpha-fading in from screen-left via an
  `x` expression (`x='-tw+min(t*600\,tw+60)'` slides in then holds). Keep it in the
  bottom ~15% and inside a 5% safe margin.
- **Act break**: the same card held shorter (~2s) with just the act title; match the
  animatic timing.
- **Credits roll**: one tall `drawtext` with `y='h-t*SPEED'` scrolling up; pick SPEED
  so the block clears in the music's length. `fontfile` escaping applies the same way.
- **End card**: see `end_card()` in the same script — cream text on black with a
  symmetric in/out alpha ramp (`if(lt(t,0.8),fade-in, if(gt(t,2.2),fade-out,1))`).

## Gotchas that bite on real cards

- **Long / dynamic text**: pass it with `textfile='notes.txt'` (and `reload=1` for
  text that changes per frame) instead of a giant `text=` — safer with punctuation
  and line breaks. Escape `%`, `:` and `\` inside `text=`; a stray colon is read as
  an option separator.
- **A plate behind the text**: `drawtext` has `box=1:boxcolor=0x000000AA:boxborderw=20`
  to lay a translucent pad under the type for legibility over busy footage — cheaper
  than a separate `drawbox`, and it tracks the text's own box.
- **Positioning by expression**: `x`/`y` take the same expression grammar as `alpha`
  (`w`,`h`,`text_w`,`text_h`,`t`,`line_h`). Centre with `(w-text_w)/2`; **commas
  inside any expression must be escaped** `\,`.
- **Fontconfig vs fontfile**: on systems with fontconfig you can use `font='Georgia
  Bold'`; on Windows prefer the explicit escaped `fontfile` path — it's deterministic
  and doesn't depend on a font cache.

## Style discipline (match the show)

- **One type family** across every card. Brand face here is Georgia Bold
  (`georgiab.ttf`) for titles; a mono (`consola.ttf`) suits technical/end text.
- **Palette only**: title gold `#e0a93b`, subtitle/body cream `#f2e7cf`, accent mint
  `#5fe39b`, base `#140f0a`. No off-palette colours on a card.
- **Hold timings**: title card ~3–4s, act break ~2s, matched to the animatic.
- **Always inside title-safe** (≥5% margin): overscan still exists on TVs/some players.

## Text that must track footage

`drawtext` is **screen-space only** — fine for full-frame cards and fixed overlays.
For text that must follow a moving element (a sign, a screen, a character's HUD), do
it in the Blender compositor with a Text node / a 3D-parented Text object instead
(see `creative-arts.animation.motion-graphics.hud-engagement-counter`), so it tracks
and takes the beauty comp/grade.

## Verify

- [ ] Windows `fontfile` drive colon escaped (`C\:/...`), forward slashes; chain runs
      with no "No such filter"/parse error.
- [ ] Commas *inside* alpha/position expressions escaped `\,` (not read as arg
      separators).
- [ ] Text centred and inside title-safe (≥5%), legible at 1080p *and* scaled down.
- [ ] Palette only (gold/cream/mint/base); one type family.
- [ ] Elements fade on their own `alpha(t)` ramps at the intended moments.
- [ ] Scanline/grain/vignette present but subtle; shadow keeps text off the texture.
- [ ] Card `dur_s` matches the shotlist so the splice leaves timing unchanged.
- [ ] Output `yuv420p` (delivery-safe).

status draft: `title_card()` is verified (built a production opening card in
`build_fx.py`); the lower-third/credits generalisations are standard drawtext and
correct, not yet all cut into an episode. See
`creative-arts.animation.motion-graphics.glitch-scanline`,
`creative-arts.animation.motion-graphics.hud-engagement-counter`,
`creative-arts.animation.encode-delivery.probe`.
