---
id: computing-software.web-development.htmx.htmx-pattern-async-auth-token
name: htmx-pattern-async-auth-token
category: computing-software
field: web-development
product: htmx
tags: [htmx, authentication, htmx-confirm, configrequest, promise, headers]
level: advanced
status: docs-checked
description: "Hold htmx requests until an async auth token resolves: cancel in htmx:confirm, re-issue with issueRequest() after the promise, and add the token header in htmx:configRequest."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/async-auth.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: no htmx request leaves the page until an authentication promise has produced a token, and every request then carries it.

Markup needs nothing special:

```html
<button hx-post="/example" hx-target="next output">An htmx-Powered button</button>
<output>--</output>
```

Script (here `auth` is a promise returned by your authentication library):

```html
<script>
  let authToken = null;
  auth.then((token) => { authToken = token })

  // gate htmx requests on the auth token
  htmx.on("htmx:confirm", (e) => {
    if (authToken == null) {
      e.preventDefault()                        // stop the regular request
      auth.then(() => e.detail.issueRequest())  // issue it once auth resolves
    }
  })

  // add the auth token to the request as a header
  htmx.on("htmx:configRequest", (e) => {
    e.detail.headers["AUTH"] = authToken
  })
</script>
```

How it works
- `htmx:confirm` fires on every trigger for a request (not just elements with `hx-confirm`); calling `preventDefault()` stops the request and `e.detail.issueRequest()` issues it later.
- `htmx:configRequest` fires after htmx has collected parameters, and `e.detail.headers` holds the request headers. The header name `AUTH` is the example's choice; use whatever your server expects.
- The token is kept in a global variable in the example; the source notes `localStorage` or any other mechanism works as long as the `configRequest` handler can read it.
- Once the promise has resolved, `authToken` is set and the `confirm` handler lets requests straight through.

Compare with htmx-pattern-custom-confirm-dialog, which uses the same event with `issueRequest(true)` to skip the native confirm.

## Checked

2026-11-07. Confirmed on examples/async-auth.md (markup, script, `localStorage` note, closing statement) and events.md (`htmx:confirm` firing on every trigger, `preventDefault()`, `issueRequest(skipConfirmation=false)`; `htmx:configRequest` details).
Fixed: wording of the two event notes now follows events.md. Removed the invented Verify step.
Method: documentation only; no commands were run.
