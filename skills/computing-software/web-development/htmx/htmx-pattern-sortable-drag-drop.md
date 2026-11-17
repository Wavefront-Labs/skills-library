---
id: computing-software.web-development.htmx.htmx-pattern-sortable-drag-drop
name: htmx-pattern-sortable-drag-drop
category: computing-software
field: web-development
product: htmx
tags: [htmx, sortable, sortablejs, drag-and-drop, onload, hx-trigger]
level: practitioner
status: docs-checked
description: "Persist drag-and-drop reordering with Sortable.js and htmx: init in htmx.onLoad, post hidden item ids on Sortable's end event, and disable sorting until htmx:afterSwap."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/sortable.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let users reorder a list by dragging and POST the new order to the server.

Step 1: initialise Sortable on every `.sortable` element, including ones swapped in later, by using `htmx.onLoad`, whose callback receives the loaded `content` element:

```js
htmx.onLoad(function(content) {
    var sortables = content.querySelectorAll(".sortable");
    for (var i = 0; i < sortables.length; i++) {
      var sortable = sortables[i];
      var sortableInstance = new Sortable(sortable, {
          animation: 150,
          ghostClass: 'blue-background-class',
          // Make the `.htmx-indicator` unsortable
          filter: ".htmx-indicator",
          onMove: function (evt) {
            return evt.related.className.indexOf('htmx-indicator') === -1;
          },
          // Disable sorting on the `end` event
          onEnd: function (evt) {
            this.option("disabled", true);
          }
      });
      // Re-enable sorting on the `htmx:afterSwap` event
      sortable.addEventListener("htmx:afterSwap", function() {
        sortableInstance.option("disabled", false);
      });
    }
})
```

Step 2: a form whose request fires on Sortable's `end` event. Each row carries a hidden input holding its id, so the POST body lists ids in the new order:

```html
<form class="sortable" hx-post="/items" hx-trigger="end">
  <div class="htmx-indicator">Updating...</div>
  <div><input type='hidden' name='item' value='1'/>Item 1</div>
  <div><input type='hidden' name='item' value='2'/>Item 2</div>
  <div><input type='hidden' name='item' value='3'/>Item 3</div>
</form>
```

Notes
- `filter` and `onMove` make the `.htmx-indicator` div unsortable, per the example's comment.
- Sorting is disabled in `onEnd` and re-enabled on `htmx:afterSwap`.
- Load the library separately; the example uses `https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js`.

## Checked

2026-11-07. Confirmed against the htmx Sortable example page (`htmx.onLoad` code, Sortable options, `end` trigger, hidden inputs, CDN script URL). Trimmed two inferred explanations and removed the invented Verify step.
Method: documentation only; no commands were run.
