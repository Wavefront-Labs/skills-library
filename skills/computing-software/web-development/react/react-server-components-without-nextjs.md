---
id: computing-software.web-development.react.react-server-components-without-nextjs
name: react-server-components-without-nextjs
category: computing-software
field: web-development
product: react
tags: [rsc-payload, rsc-bundler-integration, react-server-components, server-functions, react]
level: sme
status: docs-checked
description: "Using React Server Components outside Next.js: how RSC payloads and client references work, bundler integrations in React Router, Waku, Parcel and Vite, and security."
sources:
  - https://react.dev/reference/rsc/server-components
  - https://react.dev/reference/rsc/use-client
  - https://react.dev/reference/rsc/use-server
  - https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components
  - https://parceljs.org/recipes/rsc/
  - https://reactrouter.com/how-to/react-server-components
  - https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-rsc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Server Components outside Next.js

RSC is a React feature that needs a framework or bundler integration. Next.js App Router is the most mature, but others now support it.

## 1. How it works
- Server Components run only on the server (at build or request time). Their output is serialised into the **RSC payload**: a streamed description of the tree with props, plus **client references** (module id + export name) for `"use client"` components.
- The client runtime (`react-server-dom-*` packages) reads the stream, loads referenced client chunks, and renders. Server Component code and its dependencies never ship to the browser.
- `"use server"` marks Server Functions callable from the client via generated references (each call is a network request).

## 2. Why a bundler integration is needed
The bundler must build separate server and client module graphs (the server graph loads modules with the `react-server` condition), replace `"use client"` modules with client references, and handle `"use server"` references. The bundler-facing packages (`react-server-dom-webpack`, `-parcel`, `-turbopack`) do not follow semver and may break between React 19.x minors.

## 3. Options
| Option | Notes |
|---|---|
| React Router (RSC support is marked experimental) | Framework mode and data mode, using `@vitejs/plugin-rsc`; routes can render server components |
| Parcel 2.14.0+ | built-in RSC support; `"use server-entry"` marks a page entry |
| `@vitejs/plugin-rsc` | RSC support for Vite (in the vite-plugin-react repository); framework-agnostic, built on the Vite environment API |

Pin React versions exactly (or use Canary): RSC is stable for apps, but the APIs bundlers and frameworks use do not follow semver.

## 4. Serialisable boundary
Props passed from server to client components must be serialisable: primitives, plain objects/arrays, Date, Map/Set, typed arrays, Promises, JSX, and server function references. Not functions, class instances, or Symbols (except global ones).

## 5. Security
- Server Functions are exposed server endpoints and their arguments are fully client-controlled: authenticate and authorise inside every one and validate arguments (for example with zod).
- Use `import "server-only"` in modules with secrets; Next.js and `@vitejs/plugin-rsc` validate it at build time. React's taint APIs (`experimental_taintObjectReference`, `experimental_taintUniqueValue`) are experimental and only an extra layer.
- Keep React and the RSC integration patched: CVE-2025-55182 (disclosed 2025-12-03, CVSS 10.0) was an unauthenticated remote code execution flaw in payload decoding in `react-server-dom-webpack`, `-parcel` and `-turbopack` 19.0 to 19.2.0, fixed in 19.0.1, 19.1.2 and 19.2.1.

## Verify
- [ ] Server-only modules absent from client bundles (inspect build output); RSC payload responses stream; every server function checks auth and validates input.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the React Router RSC guide, the Parcel RSC recipe, the @vitejs/plugin-rsc README (last commit 2026-10-20) and Next.js data security docs. Confirmed: server and client component model; serialisable prop types (primitives, Date, Map, Set, typed arrays, plain objects, Promises, JSX; not functions, class instances or unregistered symbols); bundler-facing APIs are not semver; Parcel 2.14.0+ supports RSC with `"use server-entry"`; React Router RSC is marked experimental and builds on `@vitejs/plugin-rsc` for Vite; the plugin loads the server environment with the `react-server` condition; Server Function arguments are client-controlled and need validation and authorisation; the taint APIs are experimental; CVE-2025-55182 details and fixed versions. Removed the Flight, `-esm`, Waku, RedwoodSDK and Expo Router claims and the claim that React Router RSC works with Parcel, which the docs do not support.

Method: documentation only; no commands were run.
