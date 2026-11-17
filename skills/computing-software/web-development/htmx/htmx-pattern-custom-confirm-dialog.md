---
id: computing-software.web-development.htmx.htmx-pattern-custom-confirm-dialog
name: htmx-pattern-custom-confirm-dialog
category: computing-software
field: web-development
product: htmx
tags: [htmx, confirm, sweetalert2, htmx-confirm, issuerequest, dialogs]
level: practitioner
status: docs-checked
description: "Replace window.confirm with a custom dialog (SweetAlert2) in htmx by intercepting htmx:confirm, calling preventDefault, then e.detail.issueRequest(true) on accept."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/confirm.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep `hx-confirm` semantics but show your own dialog instead of the browser's `confirm()`.

Option 1: click plus custom event. The request is bound to a custom `confirmed` trigger; JavaScript raises it after the dialog resolves:

```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<button hx-get="/confirmed" hx-trigger='confirmed'
        onClick="Swal.fire({title: 'Confirm', text:'Do you want to continue?'}).then((result)=>{
            if(result.isConfirmed){ htmx.trigger(this, 'confirmed'); }
        })">Click Me</button>
```

Option 2: keep `hx-confirm` and intercept the `htmx:confirm` event, which fires for every triggered request:

```html
<script>
  document.addEventListener("htmx:confirm", function(e) {
    // fires for every request; ignore elements with no hx-confirm question
    if (!e.detail.question) return
    // stop the request so we can issue it manually later
    e.preventDefault()
    Swal.fire({ title: "Proceed?", text: `I ask you... ${e.detail.question}` })
      .then(function(result) {
        if (result.isConfirmed) {
          e.detail.issueRequest(true); // true = skip the built-in window.confirm()
        }
      })
  })
</script>
<button hx-get="/confirmed" hx-confirm="Some confirm text here">Click Me</button>
```

Key points
- `e.detail.question` holds the `hx-confirm` text; returning early when it is empty lets all other requests through untouched.
- `e.detail.issueRequest(skipConfirmation)` sends the request; passing `true` avoids a second native `window.confirm`.
- Because the question comes from the attribute, it can be templated per element, e.g. a server loop rendering `hx-confirm="Delete {{client.name}}??"` on each delete button.
- The same `htmx:confirm` event is the hook for delaying requests (see htmx-pattern-async-auth-token).

## Checked

2026-11-07. Confirmed on examples/confirm.md (both options and their code, the every-trigger comment, `issueRequest(true)` skipping `window.confirm`, the per-element question and Django loop example).
Removed: the unsupported "preferred" label on option 2 and the invented Verify step.
Method: documentation only; no commands were run.
