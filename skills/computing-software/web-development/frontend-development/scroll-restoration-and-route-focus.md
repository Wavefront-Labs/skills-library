---
id: computing-software.web-development.frontend-development.scroll-restoration-and-route-focus
name: scroll-restoration-and-route-focus
category: computing-software
field: web-development
product: frontend-development
tags: [history-api, scroll-restoration, focus-management, spa-routing, accessibility]
level: practitioner
status: docs-checked
description: "Restoring scroll position and moving focus on SPA route changes: history.scrollRestoration, saving positions per entry, focusing headings, and announcing new pages."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration
  - https://www.gatsbyjs.com/blog/2019-07-11-user-testing-accessible-client-routing/
  - https://reactrouter.com/en/main/components/scroll-restoration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scroll restoration and focus on route change

## 1. Expected behaviour (match the browser)
- New navigation (push): scroll to top (or to `#hash` target).
- Back/forward: restore the previous scroll position after content renders.
- Same-page filter changes (replace): keep position.

## 2. Manual restoration
Browsers auto-restore too early for async content. Take control:
```js
history.scrollRestoration = "manual";
addEventListener("pagehide", saveScroll);
function saveScroll() { history.replaceState({ ...history.state, scrollY: scrollY }, ""); }
// before pushState: saveScroll();
// on popstate, after render + data:
addEventListener("popstate", async e => { await render(location); requestAnimationFrame(() => scrollTo(0, e.state?.scrollY ?? 0)); });
```
Inner scroll containers need their own saved positions. Routing libraries usually offer this; check your router's scroll-restoration option before hand-rolling.

## 3. Focus
After a client-side route change, focus stays on the clicked link (now removed or off-screen); screen-reader users hear nothing. Fix:
```js
function afterRoute() {
  document.title = `${pageTitle} – Acme`;
  const h1 = document.querySelector("main h1");
  h1.setAttribute("tabindex", "-1");
  h1.focus({ preventScroll: true });
}
```
- Focusing the `<h1>` (or a skip-link target/main wrapper) is the pattern examined in the Gatsby user-testing write-up cited in sources. An alternative is a visually hidden live region announcing "Navigated to <title>".
- Do not move focus for in-page filter/sort changes - announce result counts via a polite live region instead.
- Remove the focus outline on the heading only for mouse users (`:focus:not(:focus-visible)`).

## 4. Pitfalls
- Sticky headers hide the scrolled-to target - `scroll-padding-top` on `html`.
- `scroll-behavior: smooth` on `html` makes restoration animate visibly - disable during restoration or for reduced motion.

## Verify
Scroll halfway, open a detail page, press Back: same position. With NVDA/VoiceOver, follow a link: the new page heading is announced.

## Checked
2026-10-28. Confirmed: MDN `history.scrollRestoration` (auto and manual values). The rest of the skill is behaviour guidance with no further figures. Removed: named router APIs and the Navigation API option, and the mislabelled study attribution (not confirmed on the fetched pages).
Method: documentation only; no commands were run.
