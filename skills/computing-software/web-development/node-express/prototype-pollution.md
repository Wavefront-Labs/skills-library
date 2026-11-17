---
id: computing-software.web-development.node-express.prototype-pollution
name: prototype-pollution
category: computing-software
field: web-development
product: node-express
tags: [prototype-pollution, javascript-security, deep-merge, object-create-null, node-security, security]
level: advanced
status: verified
description: "Understanding and preventing prototype pollution in Node and browser JS: unsafe merges and path setters, __proto__/constructor keys, gadgets to RCE/XSS, and hardening options."
sources:
  - https://portswigger.net/web-security/prototype-pollution
  - https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html
  - https://nodejs.org/api/cli.html#--disable-protomode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype pollution

## 1. How it happens
```js
function merge(t, s) { for (const k in s) typeof s[k] === "object" ? merge(t[k] ??= {}, s[k]) : (t[k] = s[k]); return t; }
merge({}, JSON.parse('{"__proto__": {"isAdmin": true}}'));
({}).isAdmin;   // true for every object in the process
```
Sources: recursive merge/clone/defaults, path setters (`set(obj, req.query.path, value)`), query-string parsers producing nested objects (`?a[__proto__][x]=1`), YAML/JSON config merging. Keys to watch: `__proto__`, `constructor.prototype`, `prototype`.

## 2. Why it is serious (gadgets)
Polluted defaults are read by code that never expected them: `options.shell` in `child_process.spawn` -> command execution on older runtimes (a polluted `shell` was ignored on Node 20 and 24 in a test, but other option-reading libraries remain exposed); template engine options -> RCE; `isAdmin` checks -> privilege escalation; in browsers, script loaders reading `config.src` -> DOM XSS.

## 3. Prevent
- Reject dangerous keys in any merge/set utility:
```js
const BAD = new Set(["__proto__", "constructor", "prototype"]);
if (BAD.has(key)) continue;
```
- Use `Object.create(null)` or `Map` for dictionaries from user keys; check with `Object.hasOwn(obj, k)` not `obj[k]`.
- Validate input shape with a schema that strips unknown keys (zod `.strict()`, Ajv `additionalProperties: false`) before merging.
- Keep libraries patched (historic CVEs in lodash `merge/defaultsDeep/set`, `minimist`, `qs`, `jquery.extend(true, ...)`); `npm audit` flags many.
- Hardening: `node --disable-proto=delete` removes `Object.prototype.__proto__` accessor; `Object.freeze(Object.prototype)` at startup blocks pollution but can break libraries that patch prototypes, so test thoroughly.
- Prefer `structuredClone` or `{...a, ...b}` (shallow, own props) over custom deep merges.

## 4. Detect
Unit test every merge/set helper with `__proto__` and `constructor.prototype` payloads and assert `({}).polluted === undefined`. Server-side probes: send `{"__proto__":{"json spaces":10}}` to Express apps; changed JSON indentation reveals pollution (PortSwigger technique) - only on systems you own.

## Verify
- [ ] Payload tests pass for all merge/set utilities; schema validation strips unknown keys on every endpoint.

## Checked
- Node 24.22.0 (and 20.20.2 for the gadget): the recursive `merge` with `JSON.parse('{"__proto__": ...}')` made `({}).isAdmin` true for every object, the `constructor.prototype` path polluted too, the key-blocklist merge blocked both; `{...a}` and `structuredClone` keep `__proto__` as an own key without touching the prototype, while `Object.assign` sets the prototype of the target object only (not global); `Object.create(null)` dictionaries and `Object.hasOwn` behave as described; `--disable-proto=delete` removes the `__proto__` accessor; `Object.freeze(Object.prototype)` makes strict-mode pollution throw `TypeError` and sloppy writes silently do nothing. A polluted `Object.prototype.shell` was ignored by `spawnSync`/`execFileSync` on Node 20 and 24 (the options are copied), so that gadget is not reproducible on current Node. Query-string parser, lodash and minimist CVEs were not re-run.
