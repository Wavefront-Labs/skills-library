---
id: computing-software.web-development.trpc.express-adapter
name: express-adapter
category: computing-software
field: web-development
product: trpc
tags: [trpc, express, createexpressmiddleware, adapter, body-parser]
level: practitioner
status: docs-checked
description: "Mount tRPC in Express with createExpressMiddleware and avoid body-parser conflicts for FormData and binary inputs on Express 4 versus 5."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/express.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Express adapter turns a router into Express middleware.

```ts
import * as trpcExpress from '@trpc/server/adapters/express';

const createContext = ({ req, res }: trpcExpress.CreateExpressContextOptions) => ({});
const app = express();
app.use('/trpc', trpcExpress.createExpressMiddleware({ router: appRouter, createContext }));
app.listen(4000);
```

Endpoints are then plain HTTP: `GET /trpc/getUser?input=INPUT` (a URI-encoded JSON string) for queries and `POST /trpc/createUser` with the JSON body for mutations. `createContext` receives Express `req` and `res`, so you can read `req.headers.authorization`. The middleware accepts the common adapter options plus `middleware` and `maxBodySize`.

Body parsers: tRPC parses request bodies itself, so tRPC routes need no `express.json()`. If a parser runs first, tRPC uses `req.body`, which is fine for JSON. For FormData and binary inputs: on Express 5 `express.json()` and `urlencoded()` leave other content types unread; on Express 4 the parsers set `req.body` to `{}` for content types they skip, so tRPC receives `{}`; and in both versions a parser that consumes the upload (for example `express.raw()` for `application/octet-stream`) breaks binary inputs.

Safest: register body parsers only on routes that need them (`app.use('/api', express.json())`) and mount tRPC on a separate path.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters/express.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
