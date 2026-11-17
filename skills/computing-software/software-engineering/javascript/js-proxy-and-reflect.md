---
id: computing-software.software-engineering.javascript.js-proxy-and-reflect
name: js-proxy-and-reflect
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-proxy, reflect-api, metaprogramming, observable-objects]
level: advanced
status: docs-checked
description: "Intercept object operations with Proxy and forward them correctly with Reflect."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy and Reflect

- `new Proxy(target, handler)` intercepts operations with handler traps such as `get(target, prop, receiver)`.
- Proxy invariants are enforced for non-extensible objects and non-configurable properties: a trap cannot report values that contradict them.
- Proxies do not forward private fields or internal slots: wrapping a `Map` and calling `proxy.size` throws a TypeError about an incompatible receiver; bind methods to the target.
- `Proxy.revocable()` gives a proxy that can be revoked.
- Use cases: validation, observable state, API wrappers. Forward operations with the matching `Reflect` method and pass the receiver.

## Checked

Date: 2026-11-02. Confirmed on MDN (Global_Objects/Proxy): get trap signature with receiver, invariants, private fields and internal slots incompatible-receiver error, Proxy.revocable. Removed as not stated there: the full trap list, set-trap return value rule, and the performance remark (not read).

Method: documentation only; no commands were run.
