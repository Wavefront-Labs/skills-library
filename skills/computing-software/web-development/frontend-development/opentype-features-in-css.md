---
id: computing-software.web-development.frontend-development.opentype-features-in-css
name: opentype-features-in-css
category: computing-software
field: web-development
product: frontend-development
tags: [font-feature-settings, font-variant-numeric, tabular-nums, ligatures, small-caps, typography]
level: practitioner
status: docs-checked
description: "Using OpenType features from CSS: tabular and oldstyle figures, fractions, slashed zero, ligatures, real small caps, stylistic sets, and keeping features when subsetting fonts."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-feature-settings
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-alternates
  - https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py
  - https://fonttools.readthedocs.io/en/latest/subset/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenType features in CSS

## 1. High-level properties first
```css
table, .price, .timer { font-variant-numeric: tabular-nums; }      /* digits align in columns, no jitter */
.prose { font-variant-numeric: oldstyle-nums proportional-nums; }  /* figures blend into text */
.code-id { font-variant-numeric: slashed-zero; }
.recipe { font-variant-numeric: diagonal-fractions; }              /* 1/2 rendered as a fraction */
code, pre { font-variant-ligatures: none; }                         /* or keep for coding fonts with ligatures */
.label { font-variant-caps: all-small-caps; letter-spacing: .04em; }
```
These inherit and combine predictably; the font must contain the feature, otherwise nothing happens.

## 2. Low-level escape hatch
```css
.brand { font-feature-settings: "ss01" 1, "cv11" 1; }    /* stylistic set 1, character variant 11 (e.g. single-storey a) */
```
`font-feature-settings` is all-or-nothing: a later rule setting `"liga" 0` replaces the whole list, dropping `ss01`. Prefer `font-variant-*` where one exists; define stylistic sets in `@font-feature-values` for named access (`font-variant-alternates: styleset(alt-a)`).
Variable fonts expose axes via `font-variation-settings`, but use `font-weight`, `font-stretch`, `font-style`, `font-optical-sizing` for registered axes.

## 3. Subsetting keeps or loses features
```bash
pyftsubset Inter.ttf --unicodes="U+0000-00FF,U+2000-206F" --layout-features="*" --flavor=woff2 --output-file=inter-latin.woff2
```
By default `pyftsubset` keeps a fixed list of layout features (calt, ccmp, clig, curs, dnom, frac, kern, liga, locl, mark, mkmk, numr, rclt, rlig, rvrn and the features needed for script shaping), so `tnum` or `ss01` are dropped unless you add them (`--layout-features+=tnum,ss01`) or keep all with `*`.

## Verify
- [ ] Numbers in tables and countdowns do not shift width as values change; DevTools Fonts/Computed shows the expected features applied.

## Checked

Checked 2026-10-26 against current documentation. MDN `font-variant-numeric`, `font-feature-settings` and `font-variant-alternates` (`styleset`), and the fontTools subsetter source: default preserved layout features (calt, ccmp, clig, curs, dnom, frac, kern, liga, locl, mark, mkmk, numr, rclt, rlig, rvrn plus script shaping), `--layout-features`, `--flavor`, `--unicodes`, `--output-file`. Removed the Wakamai Fondue and Google Fonts claims.

Method: documentation only; no commands were run.
