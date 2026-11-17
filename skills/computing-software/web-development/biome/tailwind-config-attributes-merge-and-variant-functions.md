---
id: computing-software.web-development.biome.tailwind-config-attributes-merge-and-variant-functions
name: tailwind-config-attributes-merge-and-variant-functions
category: computing-software
field: web-development
product: biome
tags: [biome, tailwind, tailwind-stylesheet, mergefunctions, variantfunctions, cva, clsx, tailwind-rules, custom-theme]
level: advanced
status: docs-checked
description: "Configure the tailwind section so Biome's Tailwind rules find classes in attributes, clsx/cn calls and cva variants, and read a custom stylesheet."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`tailwind` tells Biome's Tailwind rules where to find Tailwind CSS classes in JavaScript and HTML files and which stylesheet defines your Tailwind configuration. Setting any of the three lists **replaces** that list's defaults, so repeat the default names if you want to keep them.

- `attributes` (default `["class", "className"]`): attributes whose values hold classes. HTML attribute names match case-insensitively.
- `mergeFunctions` (default `["clsx", "tw", "twMerge", "twJoin", "cn", "cc", "cnb", "ctl"]`): functions that combine classes. Biome checks every string argument (both in `cn("px-2", "py-2")`, and the text in tw`px-2`), and for objects it checks the keys (in `cn({ "px-2": isActive })` it checks `"px-2"`). Properties of these functions are covered, so `tw` also covers `tw.div` calls and templates.
- `variantFunctions` (default `["cva", "tv"]`): functions describing component styles with an object. Biome checks strings passed directly and, in the object, the classes under `base`, `class`, `className`, `variants` and `slots`, and only `class`/`className` of each `compoundVariants` and `compoundSlots` entry. Other properties such as `defaultVariants` hold names, not classes, so they are skipped: in `cva("rounded", { variants: { size: { small: "px-2", large: "px-4" } }, defaultVariants: { size: "small" } })` it checks `"rounded"`, `"px-2"`, `"px-4"` but not `"small"`.
- `stylesheet` (string): the CSS file defining the Tailwind setup, e.g. `"./src/app.css"`, resolved relative to the config file. Biome reads `@theme`, `@utility` and `@custom-variant` in it and in local files it `@import`s, so rules recognise custom theme values, utilities and variants. Setting it also enables `css.parser.tailwindDirectives` unless that is set explicitly. Without it, rules know only Tailwind's defaults.

Example config:

```json
{ "tailwind": { "attributes": ["class", "className", "tw"], "mergeFunctions": ["clsx", "cn", "tw"], "variantFunctions": ["cva"], "stylesheet": "./src/app.css" } }
```

Verify: a class from `@theme` in your stylesheet is accepted by the Tailwind rules.

## Checked

2026-11-08. Read the tailwind section of the Biome configuration reference in full; the rest of that page was not read for this skill. Confirmed attributes, mergeFunctions and variantFunctions defaults and checking rules, stylesheet behaviour, and that lists replace defaults. Nothing removed.

Method: documentation only; no commands were run.
