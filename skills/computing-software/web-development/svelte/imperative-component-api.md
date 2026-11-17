---
id: computing-software.web-development.svelte.imperative-component-api
name: imperative-component-api
category: computing-software
field: web-development
product: svelte
tags: [mount-function, unmount-function, hydrate-function, server-render, flush-sync]
level: practitioner
status: docs-checked
description: "Create root components imperatively: mount, unmount with outro, hydrate, and svelte/server render, plus why effects do not run during mount and need flushSync."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/04-imperative-component-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Svelte application starts by imperatively creating a root component: mounted to an element on the client, or rendered to an HTML string on the server.

`mount(Component, { target, props })` instantiates and mounts. Multiple components per page are fine, and you can mount from inside your app (e.g. attaching a tooltip to the hovered element).

```js
import { mount } from 'svelte';
import App from './App.svelte';

const app = mount(App, {
  target: document.querySelector('#app'),
  props: { some: 'property' }
});
```

Unlike `new App(...)` in Svelte 4, effects (including `onMount` callbacks and action functions) do not run during `mount`. Force pending effects, for example in tests, with `flushSync()`.

`unmount(app, { outro: true })`: removes a component from `mount` or `hydrate`. With `outro: true`, transitions play first and a Promise resolves after they finish; otherwise it resolves immediately.

`render(Component, { props })` from `svelte/server`: server only, when compiling with the `server` option. Returns `body` and `head` HTML:

```js
import { render } from 'svelte/server';
const result = render(App, { props: { some: 'property' } });
result.body; result.head;
```

`hydrate(Component, { target, props })`: like `mount` but reuses HTML produced by SSR `render` inside the target and makes it interactive. As with `mount`, effects do not run; call `flushSync()` right after if needed.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the imperative component API page: mount, unmount with outro, render from svelte/server, hydrate, and effects not running until flushSync. Nothing removed.
