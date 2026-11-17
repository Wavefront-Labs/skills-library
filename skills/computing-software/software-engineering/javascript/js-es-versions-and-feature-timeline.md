---
id: computing-software.software-engineering.javascript.js-es-versions-and-feature-timeline
name: js-es-versions-and-feature-timeline
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-ecmascript-versions, es2015, tc39-process, stage-proposals]
level: intro
status: draft
description: "Map ECMAScript editions and the TC39 stage process to decide which features are safe to use."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECMAScript editions and TC39

- Editions are annual since ES2015 (ES6): ES2015 (let/const, classes, modules, promises, arrow functions, destructuring, generators), ES2017 (async/await), ES2018 (object spread, async iteration), ES2020 (optional chaining, nullish coalescing, BigInt, `import()`), ES2022 (class fields, private methods, top-level await, `at()`, `Object.hasOwn`), ES2023 (`toSorted` family, `findLast`), ES2024 (`Object.groupBy`, `Promise.withResolvers`, `Array.fromAsync`, well-formed strings, resizable ArrayBuffer). Verify later editions on tc39.es and MDN.
- TC39 stages: 0 strawperson, 1 proposal, 2 draft, 2.7 reviewed, 3 candidate (implementations feedback), 4 finished (ships in next edition). Do not depend on stage 3 or lower without a transpiler or polyfill and a plan to remove it.
- The specification at tc39.es/ecma262 is the authority; MDN documents behaviour and browser support; Node versions follow V8, see node.green.
- Check support before adoption: the MDN "Browser compatibility" table or the Baseline status.
- Prefer features that are Baseline widely available; transpile syntax, polyfill APIs.
