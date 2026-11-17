---
id: computing-software.web-development.prisma.client-driver-adapter
name: client-driver-adapter
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-driver-adapter, prisma, adapter-pg, prismapg, esm-type-module, accelerate-retirement]
level: practitioner
status: docs-checked
description: "Construct PrismaClient with a mandatory driver adapter such as PrismaPg, enable ESM in package.json, and know hosted Accelerate connections retire on 2026-12-01."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/index.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/generators.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Driver adapter (required in Prisma 7)

Since Prisma 7 a driver adapter is mandatory for direct database connections, which standardises Node.js, serverless and edge. Install the one for your database (`@prisma/adapter-pg`, `@prisma/adapter-mariadb`, and so on) and hand it to the client:

```ts
import { PrismaClient } from "./generated/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });
```

The import path is whatever your generator `output` produced. Initialise the adapter by its driver's own requirements.

Also required: `"type": "module"` in `package.json` (ESM).

Because the generated client does not load `.env`, make sure `DATABASE_URL` is set in the process (for example via `dotenv`).

Hosted Prisma Accelerate connections retire on December 1, 2026. A Prisma Postgres app still using a `prisma+postgres://` URL should switch to pooled TCP or the Prisma Postgres serverless driver.

If the project has no connection string, the docs' agent prompt says to stop and ask rather than invent one.

## Checked

2026-11-03. Read in the Prisma docs repository (index and prisma-schema/overview/generators pages, orm/v7): mandatory adapter in Prisma 7, adapter packages, PrismaPg example, type module requirement, no .env loading, Accelerate retirement date, stop-and-ask prompt. Removed a hedge about an unread page.

Method: documentation only; no commands were run.
