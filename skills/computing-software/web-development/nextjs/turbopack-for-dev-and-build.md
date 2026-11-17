---
id: computing-software.web-development.nextjs.turbopack-for-dev-and-build
name: turbopack-for-dev-and-build
category: computing-software
field: web-development
product: nextjs
tags: [turbopack, nextjs-bundler, webpack-migration, build-performance, nextjs]
level: practitioner
status: verified
description: "Using Turbopack in Next.js for dev and production builds: enabling it, webpack config migration, loaders and aliases, unsupported features, filesystem caching, and debugging."
sources:
  - https://nextjs.org/docs/app/api-reference/turbopack
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack
  - https://nextjs.org/blog/next-16
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turbopack for dev and build

Turbopack is Next.js's Rust bundler. Per the docs version history: `next dev` stable in v15.0.0, `next build` experimental in v15.3.0, beta in v15.5.0, stable and the default bundler in v16.0.0.

## 1. Enabling / opting out
```json
{ "scripts": { "dev": "next dev", "build": "next build" } }
```
- Next.js 16: Turbopack is the default for dev and build; opt out with `next dev --webpack` / `next build --webpack`.
- Next.js 15: opt in with `next dev --turbopack` and `next build --turbopack`.

## 2. Migrating webpack customisations
```js
// next.config.ts
export default {
  turbopack: {
    rules: { "*.svg": { loaders: ["@svgr/webpack"], as: "*.js" } },   // webpack loaders that return JS
    resolveAlias: { underscore: "lodash" },
    resolveExtensions: [".mdx", ".tsx", ".ts", ".jsx", ".js", ".json"],
  },
};
```
- A custom `webpack()` function in next.config is **ignored** by Turbopack, and Next.js 16 fails the build if you have one and no explicit choice (ran on 16.4.2: `This build is using Turbopack, with a `webpack` config and no `turbopack` config`; silence it with `--turbopack`, `--webpack`, or an empty `turbopack: {}`). The `rules`/`resolveAlias`/`resolveExtensions` config above was accepted by a 16.4.2 build without warnings. Translate each piece: loaders -> `turbopack.rules`, aliases -> `resolveAlias`, plugins -> often unnecessary or unsupported.
- Supported out of the box: CSS, CSS Modules, PostCSS (`postcss.config`), Sass, TypeScript paths, `.env`, `next/font`, `next/image`, MDX via `@next/mdx`.
- Babel: SWC is always used; since 16.0.0 Turbopack also runs Babel automatically when it finds a Babel config file (docs), which can slow builds - remove the config if you can.

## 3. Not supported (check before migrating)
webpack plugins (docs: not supported), `webpack()` config, `experimental.urlImports`, `experimental.esmExternals`, Yarn PnP, `sassOptions.functions`, legacy CSS Modules features (standalone `:local`/`:global`, `@value`, ICSS `:import`/`:export`). Check the "Unsupported and unplanned features" list in the Turbopack docs for your version.

## 4. Performance
- Filesystem caching persists compiler artifacts between runs and is enabled by default for both `next dev` and `next build` in Next 16 (`experimental.turbopackFileSystemCacheForDev` / `...ForBuild`, per the 16 upgrade guide); set them to `false` to disable.
- Compare `next build --webpack` against the default on your own CI to measure the difference for your app.
- Trace slow compiles: `next dev --internal-trace` (listed in `next dev --help`; the docs write the trace to `.next-profiles/trace-turbopack.bin`), then open it with `npx next internal trace .next-profiles/trace-turbopack.bin`. The `NEXT_TURBOPACK_TRACING` variable from older guides is not in the 16.4.2 docs.

## 5. Bundle analysis
`@next/bundle-analyzer` is webpack-based and prints `not compatible with Turbopack builds, no report will be generated` under the default build (ran). With Turbopack use `npx next analyze` (Next 16.1+, `next build --analyze` is also listed in `next build --help`), or run `ANALYZE=true next build --webpack`.

## Verify
- [ ] Dev and build pass with Turbopack; no leftover webpack() config silently ignored; output size and behaviour match the webpack build (spot-check routes, SVG imports, env vars).
