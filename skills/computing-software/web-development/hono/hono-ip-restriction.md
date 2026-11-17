---
id: computing-software.web-development.hono.hono-ip-restriction
name: hono-ip-restriction
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, ip, access-control, security]
level: practitioner
status: docs-checked
description: "Restrict Hono access by IP with ipRestriction, allowList and denyList, IPv4/IPv6 CIDR rules, getConnInfo per runtime and a custom 403."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/ip-restriction.md
  - https://github.com/honojs/website/blob/main/docs/helpers/conninfo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IP restriction

Import: `import { ipRestriction } from 'hono/ip-restriction'`. The first argument is the `getConnInfo` function from the ConnInfo helper for your runtime (`@hono/bun`, `@hono/deno`, `@hono/cloudflare-workers`, and so on).

```ts
import { getConnInfo } from '@hono/bun'
app.use(
  '*',
  ipRestriction(getConnInfo, {
    denyList: [],
    allowList: ['127.0.0.1', '::1'],
  })
)
```

## Rule syntax
- IPv4: `192.168.2.0` static, `192.168.2.0/24` CIDR, `*` all.
- IPv6: `::1` static, `::1/10` CIDR, `*` all.

## Custom error
Return a `Response` from the third argument:

```ts
ipRestriction(getConnInfo, { denyList: ['192.168.2.0/24'] },
  async (remote, c) => c.text('Blocking access', 403))
```

## Gotcha
Pass the `getConnInfo` function itself, taken from the ConnInfo helper package for your platform: `@hono/cloudflare-workers`, `@hono/deno`, `@hono/bun`, `@hono/vercel`, `@hono/aws-lambda`, `@hono/netlify`, `@hono/lambda-edge`, or `@hono/node-server/conninfo` for Node.js. Inside a handler, `getConnInfo(c).remote.address` gives the client address; `remote` has optional `address`, `addressType` (`IPv4` or `IPv6`), `port` and `transport` (`tcp` or `udp`).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/ip-restriction.md, docs/helpers/conninfo.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the `remote.addr` field in the custom-error example (the page example uses it but the ConnInfo type page names the field `address`, so the example no longer reads it), plus duplicated gotcha text.

Method: documentation only; no commands were run.
