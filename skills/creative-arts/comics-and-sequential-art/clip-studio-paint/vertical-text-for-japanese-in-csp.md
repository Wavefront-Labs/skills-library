---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.vertical-text-for-japanese-in-csp
name: vertical-text-for-japanese-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-text-tool, csp-balloons, csp-vertical-text, tategaki, ruby, tate-chu-yoko]
level: practitioner
status: draft
description: "Letter vertical Japanese text (tategaki) in Clip Studio Paint: vertical direction, tate-chu-yoko for numbers, ruby furigana, punctuation, balloon fitting and fonts."
sources:
  - https://www.w3.org/TR/jlreq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vertical text for Japanese

Japanese manga dialogue is set vertically (*tategaki*), columns read top to bottom, right to left.

## Setup
- Text tool > Tool property > **Direction: Vertical**. Use a Japanese font with vertical glyph forms
  (e.g. the anti-gothic/mincho mix typical of manga: kana in mincho, kanji in gothic; many publishers
  use specific fonts).
- Alignment: top for each column; balloon text block centred in the balloon.

## Details
- **Tate-chu-yoko** (horizontal within vertical): two-digit numbers and short abbreviations ("12", "!?")
  set horizontally inside one vertical cell. Select the characters and apply the horizontal-in-vertical
  option in the text settings.
- **Ruby / furigana**: small kana above kanji (to the right in vertical text). Select the base text and add
  ruby in the text tool settings.
- Punctuation: vertical forms of brackets, long vowel mark (ー rotates), small kana positions follow the
  font's vertical glyphs; check they are not rotated incorrectly.
- Ellipsis "…" and dash "――" should run vertically; use full-width forms.

## Balloon fitting
- Narrow tall balloons; columns 3-8 characters long; break lines at natural phrase boundaries.

## Gotchas
- A font without vertical alternates rotates or misplaces punctuation.
- Latin text in vertical setting rotates sideways by default; use tate-chu-yoko for short terms or keep
  long Latin words horizontal.

## Verify
- [ ] Read each balloon top-to-bottom, right-to-left with correct punctuation forms.
