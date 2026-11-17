---
id: computing-software.web-development.htmx.htmx-pattern-tabs
name: htmx-pattern-tabs
category: computing-software
field: web-development
product: htmx
tags: [htmx, tabs, hateoas, aria, hx-target, hx-on]
level: practitioner
status: docs-checked
description: "Build tabs with htmx two ways: server re-renders the whole tab list with the selected tab marked (HATEOAS), or load only panes and switch aria-selected in an hx-on handler."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/tabs-hateoas.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/tabs-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tabs whose content loads from the server and whose selected state stays correct.

Approach 1: HATEOAS (the selected tab is application state, so the server renders it). The main page holds only a loader:

```html
<div id="tabs" hx-get="/tab1" hx-trigger="load delay:100ms" hx-target="#tabs" hx-swap="innerHTML"></div>
```

Every tab response returns the full tab list plus the panel, marking the current tab:

```html
<div class="tab-list" role="tablist">
  <button hx-get="/tab1" class="selected" role="tab" aria-selected="true"  aria-controls="tab-content">Tab 1</button>
  <button hx-get="/tab2"                  role="tab" aria-selected="false" aria-controls="tab-content">Tab 2</button>
  <button hx-get="/tab3"                  role="tab" aria-selected="false" aria-controls="tab-content">Tab 3</button>
</div>
<div id="tab-content" role="tabpanel" class="tab-content">...</div>
```

The demo puts `hx-target="this" hx-swap="innerHTML"` on the `#tabs` container, so each button click replaces everything inside it. The demo responses also add `autofocus` to the selected button (an addition seen in the demo markup, not the sample above).

Approach 2: JavaScript selects the tab; the server returns only the pane. Less duplicated rendering on the server:

```html
<div id="tabs" hx-target="#tab-contents" role="tablist"
     hx-on:htmx-after-on-load="let currentTab = document.querySelector('[aria-selected=true]');
                               currentTab.setAttribute('aria-selected', 'false')
                               currentTab.classList.remove('selected')
                               let newTab = event.target
                               newTab.setAttribute('aria-selected', 'true')
                               newTab.classList.add('selected')">
  <button role="tab" aria-controls="tab-contents" aria-selected="true" hx-get="/tab1" class="selected">Tab 1</button>
  <button role="tab" aria-controls="tab-contents" aria-selected="false" hx-get="/tab2">Tab 2</button>
  <button role="tab" aria-controls="tab-contents" aria-selected="false" hx-get="/tab3">Tab 3</button>
</div>
<div id="tab-contents" role="tabpanel" hx-get="/tab1" hx-trigger="load"></div>
```

The handler is written `hx-on:htmx-after-on-load` and takes `event.target` as the new tab.

Choose: the page calls Approach 1 the more idiomatic one; Approach 2 offloads re-rendering the tab HTML from the server to the browser, reducing duplication.

## Checked

2026-11-07. Confirmed against the htmx Tabs (Using HATEOAS) and Tabs (Using JavaScript) example pages (both code samples, loader with `delay:100ms`, `hx-target="this"` in the demo, `autofocus` in demo responses, rationale for each approach). Removed an unsourced event-bubbling explanation and the invented Verify step.
Method: documentation only; no commands were run.
