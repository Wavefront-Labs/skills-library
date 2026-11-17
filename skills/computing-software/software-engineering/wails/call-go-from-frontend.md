---
id: computing-software.software-engineering.wails.call-go-from-frontend
name: call-go-from-frontend
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, bindings, typescript, javascript]
level: practitioner
status: docs-checked
description: "Call bound Go methods from JavaScript using generated wailsjs bindings, handle Promise resolve/reject, and use generated TypeScript models."
sources: [https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Go from the frontend

Goal: use the generated bindings and models in the frontend.

## Method

`wails dev` (or `wails generate module`) generates bindings in `wailsjs/go`, mirroring Go package names. Binding `App` in package `main` gives `wailsjs/go/main/App.js` and `App.d.ts`.

```javascript
import { Greet } from "../wailsjs/go/main/App";
Greet(name).then((result) => { /* use result */ });
```

Declaration: `export function Greet(arg1: string): Promise<string>;`

Promise behaviour: success resolves with the first Go return value. If the method has an `error` as its second return value and returns a non-nil error, the Promise rejects. A method returning only a value never rejects (barring invalid data).

Structs: returned structs arrive as JavaScript classes; JS maps or classes passed where Go expects a struct are converted. Structs used in bound method signatures get TypeScript versions in `wailsjs/go/models.ts`, in a namespace named after the Go package:

```js
import { Greet } from "../wailsjs/go/main/App";
import { main } from "../wailsjs/go/models";
let person = new main.Person();
person.name = "Peter"; person.age = 27;
Greet(person).then(console.log);
```

Runtime methods live on `window.runtime`, e.g. `window.runtime.EventsEmit("my-event", 1);`.

## Gotchas
- Struct fields must have a valid `json` tag to appear in the generated TypeScript.
- Anonymous nested structs are not supported.
- Using the models requires TypeScript in your frontend build.

## Related skills
- computing-software.software-engineering.wails.bind-go-methods

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "How does it work" (howdoesitwork).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
