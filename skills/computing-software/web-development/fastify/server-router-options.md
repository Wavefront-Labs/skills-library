---
id: computing-software.web-development.fastify.server-router-options
name: server-router-options
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, router, find-my-way, routing]
level: advanced
status: docs-checked
description: "Tune routing with the routerOptions object: case sensitivity, trailing slashes, maxParamLength, query parser, constraints."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`routerOptions` configures find-my-way:

- `allowUnsafeRegex`: default `false`; routes only allow safe regular expressions unless set to `true`.
- `buildPrettyMeta`: function that sanitizes a route's store object for the pretty-print output; takes one object and returns an object.
- `caseSensitive`: default `true`. When `false` paths match as lowercase, but route parameters and wildcards keep their casing; query strings are unaffected.
- `compile`: default `false`. When `true`, find-my-way `compile()` runs once all routes are registered, right before `onReady` hooks, for faster lookups.
- `constraints`: custom constraint strategies (find-my-way's built-ins constrain by `version` or `host`).
- `defaultRoute`, `onBadUrl`, `onMaxParamLength`: handlers whose `req`/`res` are the raw Node.js objects, without Fastify helpers such as `res.send`. `onBadUrl(path, req, res)` handles badly formatted URLs such as `/hello/%world`.
- `ignoreDuplicateSlashes`, `ignoreTrailingSlash`: both default `false`; with both `true`, `//a//b//c//` becomes `/a/b/c`.
- `maxParamLength`: default 100 characters; if exceeded the not found route is invoked, or `onMaxParamLength` if set.
- `querystringParser`: default is fast-querystring; replace with `qs` for a custom parser.
- `useSemicolonDelimiter`: default `false`; when `true`, `/dev;foo=bar` splits path and query at `;`.

```js
const qs = require('qs')
const fastify = require('fastify')({
  routerOptions: {
    ignoreTrailingSlash: true,
    caseSensitive: false,
    maxParamLength: 200,
    querystringParser: str => qs.parse(str)
  }
})
```

Gotcha: `maxParamLength` does not limit the input a route regex processes and does not protect against ReDoS; keep `allowUnsafeRegex` disabled so catastrophic regexes are rejected at route registration. Setting `caseSensitive: false` goes against RFC3986.

`rewriteUrl` is a separate top-level option (a sync function receiving the raw request and returning a string); it runs before routing, is not encapsulated and applies instance-wide.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
