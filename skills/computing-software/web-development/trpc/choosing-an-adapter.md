---
id: computing-software.web-development.trpc.choosing-an-adapter
name: choosing-an-adapter
category: computing-software
field: web-development
product: trpc
tags: [trpc, adapter, standalone, fetch, hosting]
level: intro
status: docs-checked
description: "Pick the tRPC adapter for your host: Standalone, Express, Fastify, AWS Lambda, Fetch for edge, or Next.js; all share createContext and onError."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
tRPC is not a server by itself; adapters are the glue between your host and the router. All adapters follow common conventions: `createContext` for per-request context and `onError` for global error handling.

Choose by hosting mode:

- Serverful: the Standalone adapter (a wrapper around the Node.js HTTP server), or Express / Fastify adapters to hook into an existing API.
- Serverless: AWS Lambda, or Fetch for edge runtimes (Cloudflare Workers, Deno Deploy, Vercel Edge).
- Full-stack frameworks: Next.js (pages router adapter), or the Fetch adapter with Next.js App Router, Astro, Remix or SolidStart.

The docs tip: for local development or serverful infrastructure the Standalone adapter is the simplest and is recommended when you must start quickly and have no HTTP server to integrate with; swapping later is trivial. It is also not uncommon to have two entry points: Standalone locally and another adapter when deployed.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters.md, server/adapters/standalone.md, server/adapters/fetch.md (runtime list). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the unsupported claim that AppRouter, procedures and client code never change between adapters.

Method: documentation only; no commands were run.
