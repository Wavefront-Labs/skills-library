---
id: computing-software.general-digital-literacy.basic-troubleshooting.keyboard-layout-language-and-region
name: keyboard-layout-language-and-region
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-os-settings, keyboard-layout, input-language, region-settings]
level: intro
status: draft
description: "Fix wrong characters such as @ and quote swapped or a Y and Z swap by setting the right keyboard layout, remove extra input languages, and set region formats for dates."
sources:
  - https://support.microsoft.com/en-us/windows/manage-the-input-and-display-language-settings-in-windows-12a10cb4-8626-9b77-0ccb-5013e0c7c7a2
  - https://support.apple.com/guide/mac-help/use-input-sources-to-type-in-other-languages-mchlp1406/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Language, keyboard layout and region

## Symptom: keys type the wrong symbols
- `@` and `"` swapped, `#` gives `£`, `\` missing → **UK vs US layout** mismatch. Y and Z swapped → German layout. Letters with accents appearing → *International* or *Canadian Multilingual* layout.
- Usually caused by an accidental shortcut: Windows `Win+Space` or `Alt+Shift` cycles layouts; Mac `Ctrl+Space`.

## Windows
- Settings › Time & language › **Language & region** › your language › ⋯ › Language options › **Keyboards** › add the right one (e.g. *United Kingdom*) and remove the wrong one.
- Taskbar shows `ENG UK` / `ENG US` near the clock; click to switch.
- Stop accidental switching: Settings › Time & language › Typing › Advanced keyboard settings › **Input language hot keys** › change/remove.
- **Regional format** (dates DD/MM vs MM/DD, decimal comma, first day of week) is separate: Language & region › Regional format.

## Mac
- System Settings › Keyboard › Text Input › **Input Sources › Edit** › add/remove (*British*, *U.S.*, *British – PC* for PC keyboards on a Mac).
- Show the menu-bar input menu to see the current layout.
- Region: System Settings › General › Language & Region (date, number, temperature formats).

## Phones
- iPhone: Settings › General › Keyboard › Keyboards. Android (Gboard): Settings › System › Languages & input › On-screen keyboard › Gboard › Languages.

## Gotchas
- The sign-in screen uses its own layout: a password with symbols may fail there; check the layout indicator on the lock screen.
- Excel dates and CSV separators follow the regional format.

## Verify
- [ ] `@`, `"`, `£`/`#` and `\` type what is printed on the keys.
