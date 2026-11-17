---
id: creative-arts.design-for-form-and-experience.prototyping.framer-prototypes
name: framer-prototypes
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [framer, framer-prototype, framer-motion, code-components, interactive-prototype, framer-sites, design-to-web]
level: practitioner
status: draft
description: "Make Framer prototypes and sites: frames, stacks, variants, scroll and page effects, components with code overrides, CMS and publishing to a real URL."
sources:
  - "Framer Academy and documentation (framer.com/learn)"
  - "Motion (Framer Motion) documentation (motion.dev)"
  - "Framer Developers - Code components and plugins (framer.com/developers)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framer prototypes

**Goal:** design-led, realistic, responsive prototypes (and shippable sites) with the interactivity of code.

## Building blocks
- **Frames and Stacks** (auto layout with direction, gap, padding, distribute, **responsive breakpoints** for desktop, tablet, phone): design once and let content reflow.
- **Components with Variants:** states (default, hover, pressed) and **transitions between variants** (spring, tween, duration); **interactions** (tap, hover, press, scroll, appear) change variants.
- **Page and scroll effects:** scroll-linked animations (parallax, sticky, progress bars), **appear effects**, **page transitions** (fade, slide, magic motion with shared element), **cursor** effects.
- **Variables and CMS:** collections with fields for dynamic pages (blog, products); **Locales** for localisation.
- **Code components and overrides:** React components with property controls (`addPropertyControls`) and **overrides** that wrap a layer in logic:
```tsx
import type { ComponentType } from "react"
export function withCounter(Component): ComponentType {
  return (props) => { const [n, set] = useState(0); return <Component {...props} onTap={() => set(n+1)} text={`Clicks ${n}`} /> }
}
```
- Plugins and **Framer Motion** (Motion library) for gestures, springs and layout animation.

## Workflow
1. Import from Figma (copy-paste with the Framer plugin), set breakpoints and stacks.
2. Build components with variants and wire interactions; add scroll effects for hero and storytelling sections.
3. Preview in browser on real devices (Preview, or share link); test performance (Lighthouse).
4. **Publish** to a framer.website domain or custom domain with SEO settings, OG images, and analytics; or export prototypes for testing.

## Gotchas
- Heavy effects hurt performance on mid-range phones; test and reduce.
- Keep component props consistent with the design system (`creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants`) to ease handoff.

## Verify
- [ ] Breakpoints and stacks reflow correctly.
- [ ] Variant interactions cover states; effects respect reduced motion where relevant.
- [ ] Tested on devices and published settings checked.
