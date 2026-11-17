---
id: computing-software.web-development.rails.stimulus-controllers
name: stimulus-controllers
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, stimulus, stimulus-controllers, data-controller, stimulus-targets, stimulus-values, outlets, stimulus-rails]
level: practitioner
status: docs-checked
description: "Writing Stimulus controllers: targets, values, actions, classes and outlets, lifecycle callbacks, cleaning up, and keeping behaviour declarative in HTML."
sources:
  - https://stimulus.hotwired.dev/reference/controllers
  - https://stimulus.hotwired.dev/reference/lifecycle-callbacks
  - https://stimulus.hotwired.dev/reference/values
  - https://stimulus.hotwired.dev/reference/actions
  - https://stimulus.hotwired.dev/reference/outlets
  - https://stimulus.hotwired.dev/reference/css-classes
  - https://github.com/hotwired/stimulus-rails
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stimulus controllers

**Goal:** add behaviour to server-rendered HTML through `data-` attributes.

## 1. A controller
```js
// app/javascript/controllers/clipboard_controller.js
import { Controller } from "@hotwired/stimulus"
export default class extends Controller {
  static targets = ["source", "button"]
  static values = { successText: { type: String, default: "Copied!" }, resetAfter: { type: Number, default: 2000 } }
  static classes = ["success"]
  copy(event) {
    event.preventDefault()
    navigator.clipboard.writeText(this.sourceTarget.value)
    this.buttonTarget.textContent = this.successTextValue
    this.element.classList.add(...this.successClasses)
    this.timer = setTimeout(() => this.reset(), this.resetAfterValue)
  }
  reset() { this.buttonTarget.textContent = "Copy"; this.element.classList.remove(...this.successClasses) }
  disconnect() { clearTimeout(this.timer) }
}
```
```erb
<div data-controller="clipboard" data-clipboard-success-class="is-copied" data-clipboard-reset-after-value="1500">
  <input data-clipboard-target="source" value="<%= @invite.url %>" readonly>
  <button data-clipboard-target="button" data-action="clipboard#copy">Copy</button>
</div>
```

## 2. Concepts
- **Lifecycle**: `initialize()` once when first instantiated; `connect()` any time the controller is connected to the DOM; `disconnect()` any time it is disconnected. A controller re-attached to the document reuses its instance, so `connect()` can run several times, each pair separated by a `disconnect()`. Clean up timers and listeners in `disconnect()`.
- **Values**: typed `data-[identifier]-[name]-value` attributes, declared on the same element as `data-controller`. Define `[name]ValueChanged(value, previousValue)` to react to changes.
- **Actions**: `event->controller#method`. Defaults per element include `form` submit, `input` input, `textarea` input, `input type=submit` click. Keyboard filters such as `keydown.esc->modal#close`; append `@window` or `@document` to listen on those objects. Action params: `data-[identifier]-[param-name]-param`, read from `event.params`, on the same element as the action.
- **Classes**: `static classes` logical names map to `data-[identifier]-[name]-class`, available as `this.[name]Classes` (array), on the controller element.
- **Outlets**: reference other controllers; the attribute pattern is `data-chat-user-status-outlet=".online-user"` (controller, outlet name, CSS selector).
- `this.dispatch("copy", { detail })` emits a custom event prefixed with the controller identifier and a colon (`clipboard:copy`); another controller outside the emitter's ancestry listens with `@window`, e.g. `clipboard:copy@window->effects#flash`.

## 3. Rails setup
`stimulus-rails` works with importmap-rails or a JavaScript bundler. With importmap, controllers in `app/javascript/controllers` are pinned and registered from the file structure; swap `eagerLoadControllersFrom` for `lazyLoadControllersFrom` in `controllers/index.js` to load a controller only when its identifier appears in the DOM. Generator: `./bin/rails generate stimulus controllerName`.

## Verify
- [ ] `disconnect` cleans up (no duplicate listeners after the element is detached and re-attached).
- [ ] Value, class and outlet attributes sit on the `data-controller` element.

## Checked
2026-11-01. Confirmed on the Stimulus reference pages (controllers, lifecycle callbacks, values, actions, outlets, CSS classes) and the stimulus-rails README: lifecycle semantics, ValueChanged signature, default events, keydown filters, @window, params format, classes mapping, dispatch prefixing, outlet attribute form, eager/lazy loading, generator command. Removed: claims about Turbo navigation, Turbo Streams, snapshots and morphing, and the inline-script rule, which these pages do not state.
Method: documentation only; no commands were run.
