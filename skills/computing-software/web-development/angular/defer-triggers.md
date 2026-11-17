---
id: computing-software.web-development.angular.defer-triggers
name: defer-triggers
category: computing-software
field: web-development
product: angular
tags: [angular, defer, triggers, viewport, interaction, hover, idle, timer, prefetch]
level: practitioner
status: docs-checked
description: "@defer triggers (idle, viewport, interaction, hover, immediate, timer, when), custom IdleService and prefetch triggers, with exact syntax."
sources:
  - https://angular.dev/guide/templates/defer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Triggers control when deferred content loads and replaces the placeholder. Separate several triggers with `;`; they are OR conditions. There are `on` triggers and `when`.

- `idle` (default): browser idle via requestIdleCallback. Optional timeout in ms: `@defer (on idle(500)) { <large-cmp /> }`. Customize by providing your own `IdleService` (`requestOnIdle`, `cancelOnIdle`) with `provideIdleServiceWith(CustomIdleService)` in the application providers.
- `viewport`: content enters the viewport using Intersection Observer. By default the `@placeholder` is watched (it must have a single root element), or pass a template reference variable: `<div #greeting>Hello!</div> @defer (on viewport(greeting)) { <greetings-cmp /> }`. Options object supports all `IntersectionObserver` second-parameter properties except `root`; with an object you pass the trigger via `trigger`: `on viewport({trigger: greeting, rootMargin: '100px', scrollMargin: '50px', threshold: 0.5})`, or omit `trigger` to imply the placeholder.
- `interaction`: user `click` or `keydown` on the element. Placeholder by default (single root element) or `on interaction(greeting)`.
- `hover`: `mouseover` and `focusin` events. Placeholder by default or `on hover(greeting)`.
- `immediate`: as soon as all non-deferred content has rendered.
- `timer(500ms)`: after a duration in `ms` or `s`.
- `when condition`: loads when the expression becomes truthy. One-time: the block does not revert to the placeholder if the condition later turns falsy.

Prefetch loads the JavaScript earlier than showing it. Prefix a trigger with `prefetch`, separated by `;`:

```html
@defer (on interaction; prefetch on idle) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}

<!-- Prefetching with a 500ms idle timeout -->
@defer (on interaction; prefetch on idle(500)) {
  <large-cmp />
}
```

Here prefetching starts when the browser is idle and the contents render only once the user interacts with the placeholder. See `computing-software.web-development.angular.defer-blocks` for sub-blocks and `computing-software.web-development.angular.defer-practices-testing` for caveats.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/defer (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
