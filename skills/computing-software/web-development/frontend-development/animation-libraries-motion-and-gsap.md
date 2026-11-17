---
id: computing-software.web-development.frontend-development.animation-libraries-motion-and-gsap
name: animation-libraries-motion-and-gsap
category: computing-software
field: web-development
product: frontend-development
tags: [gsap, framer-motion, motion-library, javascript-animation, css-animation]
level: practitioner
status: docs-checked
description: "Choosing and using Motion (formerly Framer Motion) and GSAP: when CSS or WAAPI suffice, layout and exit animations, timelines and ScrollTrigger, bundle cost and reduced motion."
sources:
  - https://motion.dev/docs
  - https://gsap.com/docs/v3/
  - https://gsap.com/docs/v3/Plugins/ScrollTrigger/
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Animation libraries: Motion and GSAP

## 1. Do you need one
CSS transitions, `@starting-style`, view transitions and the Web Animations API cover hovers, enter/exit, and simple sequences with no bundle cost. Reach for a library for: layout (FLIP) animations, gesture/spring physics, exit animations in React, complex timelines, scroll choreography.

## 2. Motion (motion.dev)
```jsx
import { motion, AnimatePresence, MotionConfig } from "motion/react";

<MotionConfig reducedMotion="user">
  <AnimatePresence>
    {open && (
      <motion.div key="panel" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }} transition={{ type: "spring", bounce: 0.2 }} />
    )}
  </AnimatePresence>
</MotionConfig>
```
- Check the Motion docs for the current package and import names; the examples here may lag.

## 3. GSAP
```js
import { gsap } from "gsap";
// import ScrollTrigger as shown on the GSAP ScrollTrigger docs page
gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.timeline({ scrollTrigger: { trigger: ".hero", start: "top top", end: "+=600", scrub: true, pin: true } })
      .to(".hero h1", { y: -80, opacity: 0 })
      .from(".hero img", { scale: 1.2 }, "<");
});
```
- Check GSAP's licensing page for current terms before commercial use.
- In React use `useGSAP()` (see the GSAP React page).
- `gsap.matchMedia()` cleans up on breakpoint/preference change.

## 4. Performance rules (either library)
Kill/revert animations on unmount. Check the Performance panel for long frames on mid-range Android.

## 5. Reduced motion
Always provide a path: Motion `reducedMotion="user"`, GSAP `matchMedia`, or swap movement for opacity.

## Verify
- [ ] Animations stop and clean up on route change; reduced-motion setting respected; bundle analyser shows only the imported features.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the Motion docs (react-motion-config, react-accessibility, react-animation), GSAP docs (matchMedia, ScrollTrigger, React) and MDN pages: MotionConfig with reducedMotion, useReducedMotion, gsap.matchMedia() with add(), ScrollTrigger start/end/scrub/pin and relative "+=" end values, useGSAP, CSS @starting-style and the Web Animations API.

Removed: the layout prop example, AnimatePresence key and bundle-mode bullets, the ScrollTrigger import path, the @gsap/react behavioural claims, the layout-property performance rule and the former-name remark (not on the pages read). Code samples are illustrative.

Method: documentation only; no commands were run.
