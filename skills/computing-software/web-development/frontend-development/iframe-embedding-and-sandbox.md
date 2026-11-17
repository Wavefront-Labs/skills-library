---
id: computing-software.web-development.frontend-development.iframe-embedding-and-sandbox
name: iframe-embedding-and-sandbox
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, iframe-sandbox, html-iframes, iframe, permissions-policy, lazy-loading, security]
level: practitioner
status: docs-checked
description: "Embedding third-party content with iframe safely and fast: sandbox tokens, allow permissions, loading=lazy, title, referrerpolicy, and facades for heavy embeds."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding with iframe

## 1. Template
```html
<iframe src="https://www.youtube-nocookie.com/embed/ID"
        title="Product demo video"
        width="560" height="315"
        loading="lazy"
        allow="encrypted-media; picture-in-picture; fullscreen"
        referrerpolicy="strict-origin-when-cross-origin"
        sandbox="allow-scripts allow-same-origin allow-presentation"></iframe>
```
- Give every iframe a `title` that describes its content (not "iframe") so assistive technology can name the frame.
- `width`/`height` or CSS `aspect-ratio: 16/9` prevents layout shift.
- `loading="lazy"` defers loading until the frame is near the viewport (and only when JavaScript is enabled, per MDN); leave it off for an above-the-fold embed.

## 2. sandbox
Empty `sandbox` = maximum restriction: unique origin, no scripts, no forms, no popups, no top navigation. Add back only what is needed:
- `allow-scripts`, `allow-forms`, `allow-popups`, `allow-popups-to-escape-sandbox`, `allow-modals`, `allow-downloads`, `allow-presentation`, `allow-same-origin`, `allow-top-navigation-by-user-activation`.
- **Never combine `allow-scripts` + `allow-same-origin` when the embedded document has the same origin as the embedding page** - MDN: the embedded document can then remove the `sandbox` attribute, making it no more secure than no sandbox. For cross-origin content the combination only keeps the frame's real origin.
- Rendering untrusted user HTML: `sandbox` with the fewest tokens, and MDN advises serving such content from a separate origin because sandboxing is useless if the attacker can display the content outside the frame (for example in a new tab).

## 3. allow (Permissions Policy)
Powerful features in a cross-origin frame must be delegated with the `allow` attribute: `allow="camera 'src'; fullscreen"` (a bare feature name defaults to `'src'`, and origins in `allow` are not quoted). Chromium honours the `Permissions-Policy` header; see that skill for support limits.

## 4. Protecting yourself from being framed
That is the embedded side's job: `Content-Security-Policy: frame-ancestors 'self' https://partner.example`.

## 5. Performance: facades
Third-party embeds (video, maps, chat) load their own scripts. Render a static thumbnail button and inject the iframe on click.

## 6. Messaging
Use `postMessage` with an explicit target origin and check `event.origin` on receipt; never `"*"` for sensitive data.

## Verify
- DevTools > Application > Frames shows sandbox flags and the effective permissions policy.
- The third-party embed loads only after the user clicks the facade.

## Checked
Checked 2026-10-26 against the MDN iframe reference (sandbox tokens and the same-origin allow-scripts plus allow-same-origin warning, separate-origin advice, lazy loading only with JavaScript, allow attribute) and MDN Permissions-Policy and postMessage pages. Removed unconfirmed items: the WCAG 4.1.2 citation, 'hundreds of KB', lite-youtube-embed, the YouTube autoplay parameter, the Lighthouse audit name and the claim that the header can only restrict.

Method: documentation only; no commands were run.
