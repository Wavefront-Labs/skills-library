---
id: creative-arts.design-for-form-and-experience.prototyping.coded-prototypes
name: coded-prototypes
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [coded-prototype, html-prototype, code-prototype, react-prototype, prototyping-with-code, framework-prototype, vibe-coded-prototype]
level: practitioner
status: draft
description: "Build coded prototypes: when code beats Figma, how to scaffold quickly with HTML, CSS and a framework, fake data, test with real devices and avoid prototype-to-production traps."
sources:
  - "GOV.UK Prototype Kit documentation (prototype-kit.service.gov.uk/docs)"
  - "Nielsen Norman Group - Prototyping: coded vs tool-based (nngroup.com/articles/prototyping)"
  - "Vite documentation - Getting Started (vite.dev/guide)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coded prototypes

**Goal:** a believable, testable prototype where real behaviour, data or performance matter and tools like Figma cannot show it.

## When to code
- **Real interaction:** complex state, form validation, sorting and filtering of live data, drag and drop, charts, animations with physics, speech or camera/sensor input, offline behaviour.
- **Real performance** or device features (WebGL, haptics via Vibration API, `getUserMedia`).
- A team that already ships in a framework and can reuse its design system (`creative-arts.design-for-form-and-experience.design-systems.documenting-components-in-storybook-and-a-docs-site`).

## Fast start options
- Plain **HTML/CSS/JS** with a tiny dev server (`npx serve`, Vite); copy the design-system CSS.
- **GOV.UK Prototype Kit** or **Prototyping kits** with page templates, routing and session data.
- **React/Next.js + component library** (Storybook components, shadcn/ui, Chakra), **Observable/Streamlit** for data-driven explorations, **Framer** or **Webflow** for design-led.
- **AI-assisted generation** to scaffold screens quickly; review everything for fakery and accessibility.

## Practice
1. Prototype **one flow**: stub backend with JSON files, `localStorage`, or a mock service (MSW, JSON Server); use realistic content (`creative-arts.design-for-form-and-experience.prototyping.building-realistic-high-fidelity-mockups`).
2. Keep it **throwaway**: no auth, tests, or architecture work beyond what the test requires; label "PROTOTYPE" in the repo and UI.
3. Host on Netlify/Vercel/GitHub Pages with a password for stakeholders; test on **real devices** by URL or QR code.
4. Instrument if needed (page timings, event logs) for the test.
5. After learning, **write requirements and discard** the code, or deliberately refactor; do not let prototype shortcuts slip into production by default.

## Verify
- [ ] Coded because behaviour or data demanded it; one flow only.
- [ ] Realistic content; tested on real devices.
- [ ] Throwaway policy documented.
