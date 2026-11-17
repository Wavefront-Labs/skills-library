---
id: computing-software.web-development.frontend-development.progressive-enhancement-without-javascript
name: progressive-enhancement-without-javascript
category: computing-software
field: web-development
product: frontend-development
tags: [cross-browser, no-javascript-fallback, graceful-degradation, progressive-enhancement, html-forms, resilience]
level: practitioner
status: docs-checked
description: "Making pages work when JavaScript fails or is slow: HTML first, then CSS, then JavaScript that enhances real links and forms."
sources:
  - https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement
  - https://www.gov.uk/service-manual/technology/using-progressive-enhancement
  - https://remix.run/docs/en/main/discussion/progressive-enhancement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working without JavaScript

Progressive enhancement provides a baseline of essential content and functionality to as many users as possible, then delivers the best experience to browsers that can run all the required code. Feature detection decides whether a browser can handle newer functionality; polyfills add missing features. Graceful degradation is related but not the same, and the two can complement each other (MDN).

## 1. Layers (GOV.UK)
- **HTML first.** Make the page work with HTML alone: correct semantic markup, logical source order and outline, navigable using only the HTML. The HTML layer is fault-tolerant: browsers ignore markup they do not understand.
- **CSS.** Reasonably fault-tolerant: unknown declarations are ignored, but an unknown selector makes the browser ignore the whole ruleset. GOV.UK advises avoiding CSS-in-JS so the page looks right if JavaScript fails to load.
- **JavaScript.** Not fault-tolerant: unsupported syntax or APIs error and the rest of the script does not run. Improve odds with feature detection, polyfills, transpiling, automated tests or linters and manual testing on older or lower-powered devices (weighing the extra size of polyfills and transpilation). Where possible, JavaScript should enhance HTML and CSS that already give the same core function, for example an autocomplete enhancing a select element.
- Build each JavaScript-dependent part as a separate component so a failure only affects that component.

## 2. Why CSS or JavaScript fails
Network errors, ad-blocker extensions, CDN or third-party downtime, DNS failures, browser-update bugs, third-party script bugs, corporate or personal firewalls and antivirus, mobile networks rewriting content, and ISPs injecting code on insecure connections. Some users switch features off on purpose; respect that.

## 3. Pattern: links and forms that work first (Remix docs)
- A link renders a real `<a href>`; when JavaScript loads, the router intercepts clicks for client-side navigation.
- An action is a real form with `method="post"` and an `action` URL and a submit button; it works whether or not JavaScript has loaded, and when JavaScript loads the submission is intercepted to add pending UI. Build it in iterations (simplest version first) rather than twice.
- Make search a GET form to a URL (`<input type="search" name="query">`); with the URL as source of truth you need little client-side state.
- "Everybody has JavaScript disabled until it's loaded": account for users interacting before hydration in server-rendered UI.

## 4. Features that need JavaScript
For an interactive graph, GOV.UK suggests a data table, a data export, or pre-rendered images. If the core function cannot work without JavaScript, consider other channels such as phone or in person. Avoid single-page applications for such services: assistive technology users may miss context changes, focus is not handled, back/forward buttons break and users cannot recover from network errors.

## Verify
- [ ] Main journeys complete with JavaScript blocked or failing, and forms work when submitted before the bundle loads.

## Checked

2026-11-09. Read in full the MDN glossary entry, the GOV.UK progressive enhancement guidance and the Remix discussion page. Confirmed the layer model, failure causes, form/link/GET-search patterns and the single-page-app caution. Removed claims these pages do not state: Post/Redirect/Get, the Accept-header JSON endpoint and fetch snippet, the framework list (Next.js Server Actions, SvelteKit, Rails Turbo, htmx), the `js` class and module-script gating, `<noscript>` limits, details/dialog advice, try/catch and error boundary advice, and the DevTools disable-JavaScript and Slow 3G tests.

Method: documentation only; no commands were run.
