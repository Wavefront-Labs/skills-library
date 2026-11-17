---
id: computing-software.web-development.htmx.htmx-hypermedia-friendly-scripting
name: htmx-hypermedia-friendly-scripting
category: computing-software
field: web-development
product: htmx
tags: [htmx, scripting, hateoas, javascript, events, islands, inline-scripts, hyperscript]
level: advanced
status: docs-checked
description: "Rules for adding JavaScript to an htmx app without breaking hypermedia: respect HATEOAS, keep only ephemeral state client-side, use events, isolate islands, script inline."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/essays/hypermedia-friendly-scripting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide how to script a Hypermedia-Driven Application (HDA) so scripting augments the hypermedia rather than replacing it. Five rules.

1. Respect HATEOAS. Scripting should avoid non-hypermedia network exchanges: avoid `fetch()` and `XMLHttpRequest` unless the server replies with hypermedia (HTML), not plain JSON data. Avoid complicated state held in JavaScript rather than the DOM. Exception: state that directly supports a richer widget than HTML allows. A rich-text editor may keep a large internal model, but should expose its content to the DOM through standard features, for example a hidden input, rather than requiring a JavaScript API call.

2. Client-side-only state is fine. Test: does the state need to synchronise with the server? If yes, use a hypermedia exchange; if no, keep it client-side. A visibility toggle that adds a class to another element is ephemeral front-end state and needs no request. If showing or hiding changes data stored on the server, use a hypermedia exchange.

3. Communicate with events. A component that fires custom events lets htmx listen and trigger exchanges, turning any library into a hypermedia control. Example: Sortable.js fires `end` after a drag-and-drop and htmx posts the new order:

```html
<form class="sortable" hx-post="/items" hx-trigger="end">
  <div class="htmx-indicator">Updating...</div>
  <div><input type='hidden' name='item' value='1'/>Item 1</div>
  ...
</form>
```

4. Isolate non-hypermedia components as islands. When you need richer scripting or non-hypermedia server communication, wrap it in a small island inside a server-rendered page and connect it to the rest via events. Quoted observation (Deniz Akşimşek): embedding non-hypermedia islands inside an HDA is easier than the reverse.

5. Optionally script inline. Writing scripts in the markup (Alpine.js, hyperscript) keeps the hypermedia emphasised and satisfies Locality of Behavior. Keep it to a soft limit so the shape of the document stays readable; pull implementations out via library functions or hyperscript behaviors.

```html
<button _="on click toggle .visible on the next <section/>">Show Next Section</button>
<section>....</section>
```

Pragmatism. Many useful libraries ignore HATEOAS and fire no events. If it is easy, alter or wrap the library so it is hypermedia-friendly (or send the maintainer a pull request). Otherwise use it as designed, isolate it from the rest of the app, and do not spend your complexity budget on conceptual purity.

## Checked

2026-11-07. Confirmed on essays/hypermedia-friendly-scripting.md (the five rules, `fetch()` and `XMLHttpRequest` guidance, rich-text editor and hidden input, visibility toggle and the synchronise-with-server test, Sortable.js `end` example, islands and the Akşimşek observation, inline scripting with Alpine.js and hyperscript, soft limit, Locality of Behavior, pragmatism).
Fixed: spelling of the quoted author's name. Removed the invented Verify step.
Method: documentation only; no commands were run.
