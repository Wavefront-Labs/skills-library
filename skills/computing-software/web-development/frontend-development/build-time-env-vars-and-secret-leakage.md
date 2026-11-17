---
id: computing-software.web-development.frontend-development.build-time-env-vars-and-secret-leakage
name: build-time-env-vars-and-secret-leakage
category: computing-software
field: web-development
product: frontend-development
tags: [build-tooling, build-env-vars, import-meta-env, secrets, vite, nextjs-env]
level: practitioner
status: docs-checked
description: "Handling build-time environment variables in frontend bundles: VITE_/NEXT_PUBLIC_ prefixes, why everything inlined is public, runtime config, and scanning bundles for leaks."
sources:
  - https://vite.dev/guide/env-and-mode
  - https://nextjs.org/docs/app/guides/environment-variables
  - https://create-react-app.dev/docs/adding-custom-environment-variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build-time env vars and secrets leakage

## 1. The rule
Any value referenced in client code is **string-replaced into the JavaScript at build time** and shipped to every visitor. There is no such thing as a secret frontend env var.

| Tool | Exposed to client | Access |
|---|---|---|
| Vite | `VITE_*` only (`envPrefix` configurable) | `import.meta.env.VITE_API_URL` |
| Next.js | `NEXT_PUBLIC_*` (others server-only) | `process.env.NEXT_PUBLIC_X` |
| CRA (legacy) | `REACT_APP_*` | `process.env.REACT_APP_X` |
| webpack DefinePlugin | whatever you define | literal replacement |

## 2. Leak patterns seen in audits
- Widening Vite's `envPrefix` (or defining all of `process.env` into the bundle) exposes variables you meant to keep server-side.
- Naming a secret `VITE_STRIPE_SECRET_KEY` "so it works".
- Server-only modules imported into client components (Next.js) - use `import "server-only"` to make that a build error.
- Source maps uploaded publicly revealing server code paths and comments.

## 3. What belongs in the client
Public identifiers only (API base URL, publishable keys, restricted browser keys). Everything else goes through your backend or serverless functions.

## 4. Build once, deploy many
Inlined values force a rebuild per environment. For one artifact across staging/prod, load runtime config: serve a `/config.json` (or inject the values into `index.html` when the container starts) and read it before boot. CRA's docs describe replacing placeholders in the HTML on the server for the same reason.

## 5. Modes and files
Vite: `.env`, `.env.local`, `.env.[mode]`, `.env.[mode].local` (`.local` git-ignored); `vite build --mode staging`. Values are strings - `"false"` is truthy. Variables already in the shell override files. Type them in `vite-env.d.ts` (`interface ImportMetaEnv`).

## Checked

2026-11-01. Confirmed from docs sources: Vite `VITE_` prefix, `envPrefix`, build-time static replacement, no sensitive data in `VITE_*`, `.env` / `.env.local` / `.env.[mode]` / `.env.[mode].local` loading and precedence, shell variables win, string values, `--mode staging`, `vite-env.d.ts` with `ImportMetaEnv` (Vite env guide); Next.js `NEXT_PUBLIC_` inlined at build time and other variables server-only, `server-only` package (Next.js environment-variables and server-and-client-boundary guides); CRA `REACT_APP_` prefix and build-time embedding. Removed: gitleaks flags, grep patterns, named key types, envsubst detail.

Method: documentation only; no commands were run.

## Verify
- After build: search `dist/` for your secret prefixes (nothing found) and run a secret scanner over the output.
- Review `import.meta.env` / `process.env` usage in client code during PR review.
