---
id: languages-linguistics.braille-and-tactile-literacy.refreshable-braille.pairing-and-navigating-a-refreshable-braille-display
name: pairing-and-navigating-a-refreshable-braille-display
category: languages-linguistics
field: braille-and-tactile-literacy
product: refreshable-braille
tags: [refreshable-braille, braille-display, braille-notetaker, screen-reader, nvda, jaws, voiceover, talkback, narrator, brltty, bluetooth-pairing, usb-hid, cursor-routing, panning-keys, perkins-input, braille-input, braille-tables, computer-braille, 8-dot-braille, contracted-input, assistive-technology]
level: practitioner
status: draft
description: "Connect a refreshable braille display to NVDA, JAWS, VoiceOver or TalkBack, choose input and output tables, navigate with panning and routing keys, and type in braille."
sources: ["NV Access NVDA User Guide (Braille section)", "Apple VoiceOver braille support documentation", "Google TalkBack braille display help", "Display manufacturers' manuals (paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pairing and navigating a refreshable braille display

**Goal:** get a braille display working with a screen reader reliably, set the braille
tables correctly, and move around documents and apps faster by touch than by speech alone.

## 1. Know your hardware
- **Displays** have a row of cells (commonly 14–40 for portable, up to 80 for desktop) whose
  pins rise and fall; each cell usually has **8 dots** (6-dot braille + dots 7 and 8 for the
  cursor and computer braille).
- Above each cell sits a **cursor-routing key**: press it to move the caret (or click) there.
- **Panning keys** at the ends or front move the window along a line longer than the display.
- **Perkins-style keys** (dots 1–8 plus space) let you type in braille. Some devices are
  **notetakers** with their own apps and OS; they can also act as a display for a phone/PC.

## 2. Connecting (by screen reader)
- **NVDA (Windows):** connect by USB or pair in Windows Bluetooth settings, then NVDA menu ›
  Preferences › Settings › Braille › Display: *Automatic* usually finds it; pick the model
  manually if not. Set output and input tables in the same panel.
- **JAWS (Windows):** Settings Center › Braille, choose the display; many models need the
  manufacturer's driver installed first.
- **Windows Narrator:** supports displays via BRLTTY; braille support is an optional
  download in Narrator settings.
- **VoiceOver (iPhone/iPad):** pair in Settings › Accessibility › VoiceOver › Braille —
  **not** in the general Bluetooth screen. Pairing from the general screen is the most
  common failure.
- **VoiceOver (Mac):** System Settings › Accessibility › VoiceOver › VoiceOver Utility › Braille.
- **TalkBack (Android):** recent TalkBack versions include braille-display support in
  TalkBack settings; older devices needed the separate BrailleBack app (check your version).

## 3. Tables: the setting most people get wrong
- **Output table** = how screen text appears. Choose **UEB grade 2** for reading prose; choose
  **computer braille (8-dot)** or grade 1 for code, spreadsheets, URLs and anything exact.
- **Input table** = how your typing is interpreted. Typing in contracted braille is fast but
  can mis-translate names and passwords; use **computer braille input for passwords** and
  code, then switch back. Many screen readers have a hotkey to toggle.
- Language mismatch (e.g. a US table on a UK setup) shows wrong symbols for punctuation and
  numbers; set the table explicitly instead of trusting auto.

## 4. Navigating efficiently
- Read with the display and **turn speech off or down** — it trains braille fluency and is
  silent in meetings.
- **Pan** with the panning keys; set the screen reader to *word wrap* so words aren't split
  across display windows.
- **Route** to edit: pan to the error, press the routing key above it, correct it — far faster
  than arrowing letter by letter.
- Learn the **display-key commands** for: top/bottom of document, next/previous line, toggle
  cursor tracking (follow focus vs review), and show text attributes.
- Cursor shown as dots 7-8 underline; if it vanishes, the display is following the review
  cursor, not the system caret.

## Gotchas
- Bluetooth sleep: displays drop the connection to save power. Re-pair only after trying to
  reconnect from the screen reader's own menu; repeated pairing creates duplicate entries.
- Two screen readers grabbing the same display (e.g. JAWS and NVDA both running) blocks it.
- Some apps don't expose text properly; the display then shows nothing useful. That's the
  app's accessibility, not your setup — confirm with speech.
- Firmware updates fix many disconnect bugs; check the manufacturer's site.

## Verify
- [ ] Display connects after a reboot without re-pairing.
- [ ] Output table shows contracted prose; you can switch to computer braille on demand.
- [ ] A password typed with computer-braille input succeeds first time.
- [ ] You can route the caret to a mid-line error and fix it without arrow keys.
- [ ] You can read a full email with speech muted.
