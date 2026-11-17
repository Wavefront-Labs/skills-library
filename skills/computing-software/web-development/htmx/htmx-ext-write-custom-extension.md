---
id: computing-software.web-development.htmx.htmx-ext-write-custom-extension
name: htmx-ext-write-custom-extension
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, defineextension, onevent, handleswap, transformresponse]
level: advanced
status: docs-checked
description: "Write an htmx extension with htmx.defineExtension(name, {...}) and know the seven overridable extension points and their default return values."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/building.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add or change htmx behaviour by registering a named extension.

Define one by calling `htmx.defineExtension(name, definition)`:

```html
<script>
  htmx.defineExtension('my-ext', {
    onEvent : function(name, evt) {
        console.log("Fired event: " + name, evt);
    }
  })
</script>
```

Conventions
- Normally put this in a stand-alone JavaScript file rather than an inline script tag.
- Give the extension a short, descriptive, dash-separated name.

Extension points. An extension may override any of these; the defaults are:

```javascript
{
    init: function(api) {return null;},
    getSelectors: function() {return null;},
    onEvent : function(name, evt) {return true;},
    transformResponse : function(text, xhr, elt) {return text;},
    isInlineSwap : function(swapStyle) {return false;},
    handleSwap : function(swapStyle, target, fragment, settleInfo) {return false;},
    encodeParameters : function(xhr, parameters, elt) {return null;}
}
```

Reading the signatures
- `onEvent(name, evt)` is called with the event name and event object; the example logs both.
- `transformResponse(text, xhr, elt)` defaults to returning `text` unchanged, so an override returns the (possibly modified) text.
- `isInlineSwap` and `handleSwap` default to `false`, and `init`, `getSelectors` and `encodeParameters` default to `null`.

The page documents only the signatures and default returns above; it does not describe when each point is called, so read the htmx source or api.md (`htmx.defineExtension(name, ext)`, `htmx.removeExtension(name)`) for more. Enable a defined extension with `hx-ext` (comma-separated list; `hx-ext="ignore:name"` opts a subtree out).

## Checked

2026-11-07. Confirmed on extensions/building.md (the `defineExtension` example, stand-alone file and dash-separated naming advice, the seven extension points with their default returns), api.md (`htmx.defineExtension`, `removeExtension`) and attributes/hx-ext.md (comma list, `ignore:`).
Thin skill: the source page is about 20 lines, so the skill cannot say more without unconfirmed claims. Removed the invented Verify step.
Method: documentation only; no commands were run.
