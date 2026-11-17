---
id: computing-software.web-development.frontend-development.navigation-api-interception
name: navigation-api-interception
category: computing-software
field: web-development
product: frontend-development
tags: [history-api, navigation-api, spa-routing, navigate-event, javascript]
level: practitioner
status: docs-checked
description: "Routing with the Navigation API: intercepting navigate events, async handlers with scroll and focus handling, traversal, entries and when to fall back to History."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigation_API
  - https://developer.mozilla.org/en-US/docs/Web/API/NavigateEvent/intercept
  - https://developer.chrome.com/docs/web-platform/navigation-api
  - https://html.spec.whatwg.org/multipage/nav-history-apis.html#navigation-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigation API interception

A single `navigate` event fires for link clicks, form submissions, back/forward and programmatic navigations - replacing click hijacking plus `popstate`.

## 1. Router
```js
navigation.addEventListener("navigate", e => {
  if (!e.canIntercept || e.hashChange || e.downloadRequest || e.formData) return;   // let the browser do it
  const url = new URL(e.destination.url);
  if (url.origin !== location.origin) return;
  e.intercept({
    async handler() {
      const view = await loadView(url, { signal: e.signal });   // signal aborts if the user navigates again
      render(view);
    },
    focusReset: "after-transition",   // default: after the handler resolves, focus the first autofocus element or the body
    scroll: "after-transition",       // default: the browser handles scrolling (fragment target, restoring position on history traversal)
  });
});
```
- The URL updates immediately, so show placeholder content while data loads; `navigation.transition.finished` resolves when the handler promises fulfil, and a rejected handler makes the navigation fail (`navigateerror`).
- In Chrome the native loading indicator and stop button reflect the handler's promise (not yet for back/forward button navigations when the Chrome article was written).
- Programmatic: `navigation.navigate(url, { state, history: "replace" })`, `navigation.back()`, `navigation.traverseTo(key)`; `navigation.entries()` lists same-origin history; `navigation.currentEntry.getState()`.

## 2. Support and fallback
Chrome 102, Firefox 147, Safari 26.2 (browser-compat-data). Feature-detect `"navigation" in window`; keep a History API path (or a router library) for older browsers.

## 3. Pitfalls
- Do not intercept cross-document cases like `download` links or when `canIntercept` is false (cross-origin).
- By default scrolling happens once the handler promise resolves; call `e.scroll()` earlier if it makes sense, or set `scroll: "manual"` to handle it yourself.
- Update `document.title` and make sure the route change is announced to screen readers; the default focus reset only moves focus to the `autofocus` element or the body.
- Pass `e.signal` into every fetch so superseded navigations cancel.

## Verify
Back/forward restores scroll; rapid clicks abort earlier loads (Network panel shows cancelled); browser stop button aborts the handler.

## Checked

Checked 2026-10-26 against mdn/content (main) Navigation API, NavigateEvent and `intercept()` pages, the Chrome developer documentation for the Navigation API (GoogleChrome/developer.chrome.com) and mdn/browser-compat-data.

- Fixed: the support sentence ("late 2025 / early 2026, Baseline 2026") is replaced by the compatibility data (Chrome 102, Firefox 147, Safari 26.2); the `focusReset` and `scroll` option comments now state the documented defaults (focus the first `autofocus` element or the body; the browser handles scrolling).
- Confirmed: `canIntercept`, `hashChange`, `downloadRequest`, `formData` and `signal` on `NavigateEvent`; `navigation.transition.finished`; `traverseTo()`, `entries()`, `currentEntry.getState()`; passing `e.signal` to `fetch()` cancels superseded loads; the URL changes immediately.

Method: documentation only; no commands were run.
