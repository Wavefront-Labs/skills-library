---
id: computing-software.general-digital-literacy.web-browsers.accessibility-and-browser-customization
name: accessibility-and-browser-customization
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, accessibility, zoom, page-zoom, reader-mode, reading-mode, dark-mode, high-contrast, captions, text-to-speech, screen-reader, font-size, low-vision, cognitive-accessibility, browser-font-size, browser-dark-mode, browser-accessibility]
level: intro
status: draft
description: "Make any browser easier to read and use: page zoom vs text-only zoom, reader mode, dark mode, forced captions, and built-in text-to-speech."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessibility and browser customization — make the browser work for your eyes and attention

**Goal:** use the accessibility features already built into every major browser —
zoom, reader mode, dark mode, captions, read-aloud — so the web is comfortable to use
without installing anything extra, whatever the reason (low vision, screen glare,
reading difficulty, or just a cluttered page).

## 1. Zoom — two different kinds
- **Page zoom** (`Ctrl++`/`Ctrl+-`/`Ctrl+0` on Windows, `Cmd` equivalents on Mac) scales
  the *entire* page — text, images, layout — proportionally. This is what most people
  mean by "zoom" and works everywhere, in every browser.
- **Text-only zoom** (Firefox: View menu › Zoom › Zoom Text Only; other browsers mostly
  don't offer this separately) increases just the font size while images/layout stay
  the same size — useful on sites where page zoom alone makes images huge and pushes
  text off-screen awkwardly.
- A **permanent minimum font size**, not just per-visit zoom: Chrome/Edge Settings ›
  Appearance › Font size (and the "Customize fonts" page for finer control); Firefox
  Settings › General › Language and Appearance › Fonts; this persists across every
  site without re-zooming each time.

## 2. Reader mode — strip the clutter
- Safari: the **lines icon** in the address bar (Reader icon) strips ads, navigation
  and sidebars down to just the article text, with its own adjustable font/size/theme.
- Firefox: the **book/reading-view icon** at the right of the address bar on article-
  type pages, same function.
- Chrome/Edge: no single built-in button on desktop by that name, but Edge has
  **Immersive Reader** (right-click the page, or the icon in the address bar on
  supported pages) with the same effect plus read-aloud (section 4) and a word/line
  focus mode.
- Reader mode only appears/works on pages the browser recognises as **article-style
  content** — it won't activate on a dashboard, search results page, or app-like site;
  that's expected, not a bug.

## 3. Dark mode and high contrast
- **System-level dark mode** (Windows Settings › Personalisation › Colors; macOS
  System Settings › Appearance) is usually followed automatically by Chrome, Edge,
  Firefox and Safari without a separate in-browser toggle — set it at the OS level.
- Some sites ignore dark mode and render white regardless; Edge has a **"Force dark
  mode for web content"** option (Settings › Appearance) that attempts to invert/adjust
  colours even on sites that don't support it natively — works well on some pages,
  poorly on others (images can look washed out), so treat it as a per-site toggle to
  try, not a universal fix.
- **High contrast mode** is an OS-level feature (Windows Settings › Accessibility ›
  Contrast themes; macOS System Settings › Accessibility › Display › Increase contrast)
  that the browser inherits automatically, same principle as dark mode.

## 4. Captions and text-to-speech
- Browser-played video (YouTube embeds, many news sites): most video players have
  their own **CC/captions toggle** directly in the player controls — this is a per-site
  player feature, not a browser setting.
- **Read-aloud / text-to-speech**: Edge's Immersive Reader (section 2) includes a
  play button that reads the page aloud with adjustable voice and speed. Safari has
  **Spoken Content** under macOS System Settings › Accessibility, which can read a
  selected passage or the whole page via a keyboard shortcut you assign. These are
  genuinely built-in — no extension or paid app required for basic use.

## 5. When built-in isn't enough
For a full **screen reader** (navigating, not just having text read aloud — needed for
significant vision loss), use the OS-level tool, not a browser feature: Windows
**Narrator** (`Win+Ctrl+Enter` to toggle) or **NVDA** (free, third-party, widely used);
macOS **VoiceOver** (`Cmd+F5`). These operate across the whole OS, not just the
browser, and are a meaningfully different tool from reader mode/zoom — say clearly to
anyone being supported that reader mode is a readability aid, not a substitute for a
screen reader if that's the actual need.

## Verify
- [ ] You know the difference between page zoom and text-only zoom, and which your
      main browser offers.
- [ ] A permanent minimum font size is set at the browser level, not re-applied each visit.
- [ ] Dark mode follows the OS setting automatically in your main browser.
- [ ] For a genuine screen-reader need, the OS-level tool (Narrator/NVDA/VoiceOver) was
      suggested, not just reader mode.
