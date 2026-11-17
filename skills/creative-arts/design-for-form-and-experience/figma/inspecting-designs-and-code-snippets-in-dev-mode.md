---
id: creative-arts.design-for-form-and-experience.figma.inspecting-designs-and-code-snippets-in-dev-mode
name: inspecting-designs-and-code-snippets-in-dev-mode
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [dev-mode-inspect, figma-dev-mode, inspect-panel, code-snippets, design-to-code, developer-handoff]
level: practitioner
status: draft
description: "Inspect designs in Figma Dev Mode: read measurements, tokens and styles, copy CSS, iOS and Android snippets, download assets, and know the limits of generated code."
sources:
  - "Figma Help Center (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Inspecting and code snippets in Dev Mode

Dev Mode is a view of a Figma file built for developers. Access depends on seat type and plan, so check the Help Center for current requirements.

## Use
1. Switch the toggle to **Dev Mode** (or open the file link in Dev Mode).
2. **Select a layer:** the Inspect panel shows layout (size, position, auto layout padding and gap), typography, fills and strokes, effects, and the **variables and styles** applied, ideally with code syntax names (see `...figma.scoping-variables-and-setting-code-syntax`).
3. **Code snippets:** choose a language such as CSS, iOS (SwiftUI or UIKit), or Android (Compose or XML) in the panel; copy the snippet. Snippets reflect the design's values; **treat them as a starting point**, not production code.
4. **Measurements:** select one layer and hover another to see the spacing between them.
5. **Assets:** export from the Assets section with the export settings defined in the file (see `...figma.figma-export-settings`).
6. **Components:** see the component name, description, a link to documentation, and mapped code if Code Connect is set up (see `...design-systems.connecting-figma-to-code-with-code-connect`).
7. **Plugins** in Dev Mode can add integrations and extra code generators.

## Gotchas
- Raw values (hex) in snippets mean the design used no variable; ask the designer to bind variables.
- Auto layout in Figma maps to flexbox in CSS, but behaviour at other widths is not shown; read the annotations and responsive notes.

## Verify
- [ ] The token name shows in the panel rather than a raw value.
- [ ] Spacing values come from the scale.
- [ ] The built UI matches the measurements.
