---
id: computing-software.web-development.nextjs.self-hosting-standalone-docker
name: self-hosting-standalone-docker
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-standalone, nextjs-self-hosting, docker, output-standalone, cache-handler, web-development]
level: practitioner
status: docs-checked
description: "Self-hosting Next.js with output standalone and Docker: copying static assets, image optimisation, shared cache handlers, version skew and reverse proxy settings."
sources:
  - https://nextjs.org/docs/app/guides/self-hosting
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/output
  - https://github.com/vercel/next.js/tree/canary/examples/with-docker
  - https://nextjs.org/docs/app/guides/deploying-to-platforms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-hosting Next.js with standalone output and Docker

**Goal:** a small production image that runs `node server.js`, scales horizontally and doesn't break caches or server actions across instances.

## 1. Standalone output
```ts
// next.config.ts
export default { output: "standalone" };
```
`next build` writes `.next/standalone/` with a minimal `server.js` and only the traced `node_modules`. It does **not** copy `public/` or `.next/static/` - you must.

## 2. Dockerfile (multi-stage)
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS run
WORKDIR /app
ENV NODE_ENV=production PORT=3000 HOSTNAME=0.0.0.0
RUN addgroup -S app && adduser -S app -G app
COPY --from=build /app/public ./public
COPY --from=build --chown=app:app /app/.next/standalone ./
COPY --from=build --chown=app:app /app/.next/static ./.next/static
USER app
EXPOSE 3000
CMD ["node", "server.js"]
```
`HOSTNAME=0.0.0.0` is needed or the server binds only inside the container's localhost.

## 3. Multi-instance concerns
- **Cache**: ISR/data cache defaults to the local filesystem/memory per instance. Configure a shared `cacheHandler` (the Next.js repo has a Redis `cache-handler-redis` example) with `cacheMaxMemorySize: 0`; backends for `'use cache'` are configured separately with `cacheHandlers`.
- **Server actions**: set the same `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` (base64, AES key length of 16, 24 or 32 bytes) on all instances at build time, or actions fail across instances.
- **Version skew**: set `deploymentId` (or a stable `generateBuildId`) so clients on old builds hard-reload instead of requesting missing chunks; keep old static assets on the CDN.

## 4. Images
`next/image` optimisation runs in the Next.js server; on glibc-based Linux it may need extra configuration to limit memory use (see the sharp install notes linked from the self-hosting guide). You can set `unoptimized` or use a custom `loader` if you optimise images separately.

## 5. Reverse proxy
- Disable response buffering for streaming: the self-hosting guide sets the `X-Accel-Buffering: no` header from `next.config` for nginx.
- Serve `/_next/static/*` with `Cache-Control: public, max-age=31536000, immutable` (Next sets this; ensure the proxy doesn't override).
- Forward `Host`/`X-Forwarded-Host`: Server Actions compare the request `Origin` with the host taken from `x-forwarded-host` or `host`.

## 6. Env vars
Server env is read at runtime; `NEXT_PUBLIC_*` is baked at build - see per-environment builds or runtime config.

## Verify
- [ ] `docker run -p 3000:3000 img` serves pages, `/_next/static` files and `public/` assets.
- [ ] Two replicas behind a load balancer: revalidating on one is visible on the other.
- [ ] A server action works after a rolling deploy.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/self-hosting, config output, deploymentId, serverActions, images) and the `examples/with-docker/Dockerfile` in the same repository.
Confirmed: `output: "standalone"` and `node server.js`, `public` and `.next/static` not copied by default, `HOSTNAME="0.0.0.0"` and the `COPY` layout in the official Dockerfile, `cacheHandler` with `cacheMaxMemorySize: 0`, `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` rules, `deploymentId` for version skew, immutable asset `Cache-Control` that cannot be overridden, `X-Accel-Buffering: no`.
Corrected or removed: `@neshca/cache-handler`, the "sharp bundled in 15+" claim and CPU-heavy claim, the `proxy_buffering` directive and the `X-Forwarded-For/Proto` forwarding list.
Method: documentation only; no commands were run.
