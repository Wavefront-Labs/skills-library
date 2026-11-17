---
id: computing-software.game-programming.godot.richtextlabel-bbcode-and-effects
name: richtextlabel-bbcode-and-effects
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-ui, richtextlabel, bbcode, custom-richtext-effect, game-programming]
level: practitioner
status: docs-checked
description: "Format Godot UI text with RichTextLabel BBCode: tags, meta links, images, typewriter reveal via visible_ratio, custom RichTextEffect and performance with large logs."
sources: ["https://docs.godotengine.org/en/stable/tutorials/ui/bbcode_in_richtextlabel.html", "https://docs.godotengine.org/en/stable/classes/class_richtextlabel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RichTextLabel BBCode and effects

**Goal:** dialogue, tooltips and logs with colours, icons, clickable keywords and animated text.

## Basics
Enable `bbcode_enabled`, then set `text`:
```
[b]Bold[/b] [i]italic[/i] [color=#ff5555]red[/color] [font_size=24]big[/font_size]
[img=24x24]res://ui/icons/coin.png[/img] x 50
[url=item:sword]Iron Sword[/url]  [hint="Deals slashing damage"]tooltip[/hint]
[center]...[/center] [table=2][cell]A[/cell][cell]B[/cell][/table]
[wave amp=20 freq=5]wavy[/wave] [shake rate=20 level=5]shaky[/shake] [rainbow]...[/rainbow]
```
`fit_content = true` sizes the label to its text (useful in containers); `scroll_following` for logs.

## Links
```gdscript
rich.meta_clicked.connect(func(meta): if str(meta).begins_with("item:"): show_item(str(meta).substr(5)))
```
`[url]` tags do nothing until you handle `meta_clicked`; `meta_hover_started/ended` for hover cards;
`meta_underlined` controls whether links are underlined.

## Typewriter reveal
```gdscript
rich.visible_characters_behavior = TextServer.VC_CHARS_AFTER_SHAPING
var tw = create_tween()
rich.visible_ratio = 0.0
tw.tween_property(rich, "visible_ratio", 1.0, rich.get_total_character_count() / 40.0)
```
`visible_characters` counts Unicode codepoints (an emoji can be several) and setting it updates
`visible_ratio`. Skip on input: `tw.kill(); rich.visible_ratio = 1`.

## Custom effects
```gdscript
@tool
extends RichTextEffect
class_name RichTextGhost
var bbcode := "ghost"
func _process_custom_fx(c: CharFXTransform) -> bool:
    c.color.a = 0.5 + 0.5 * sin(c.elapsed_time * 4.0 + c.relative_index)
    return true
```
Add instances to the label's `custom_effects` array; use `[ghost]...[/ghost]`.

## Escaping user text
Player-supplied text can inject tags (for example `[url]` links to phishing sites). Replace `[` with `[lb]`
(only opening brackets need escaping) before embedding, or add it with `add_text()`, which adds raw
non-BBCode text.

## Performance
- For logs use `append_text()` (it avoids rebuilding the whole BBCode; a tag opened in one call cannot be
  closed in a later one) and cap lines with `remove_paragraph(0)`.
- `threaded = true` does text processing in a background thread (see the `finished` signal).

## Gotchas
- `get_parsed_text()` returns the text without BBCode mark-up (for length or search).

## Verify
- [ ] Player named `[color=red]x` renders literally.
- [ ] 5,000-line combat log stays responsive (capped, append-based).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: tags `[center]`, `[url]`, `[hint="..."]` (quoted), `[img=WxH]`, `[font_size]`, `[table=N]` with `[cell]`, `[wave amp freq]`, `[shake rate level]`, `[rainbow]`; `[lb]` and `[rb]` escapes and that replacing `[` with `[lb]` is enough; `[url]` does nothing until `meta_clicked` is handled; RichTextEffect needs a `bbcode` member and `_process_custom_fx(CharFXTransform)` (`color`, `elapsed_time`, `relative_index`); `custom_effects`, `fit_content`, `scroll_following`, `visible_ratio`, `visible_characters_behavior` (TextServer `VC_CHARS_AFTER_SHAPING`), `get_total_character_count`, `append_text`, `add_text`, `remove_paragraph`, `get_parsed_text`, `threaded` and `finished`. The earlier unquoted `[hint=...]` form was corrected. Removed the unconfirmed cursor-shape, redraw and tag-exclusion claims.

Method: documentation only; no commands were run.
