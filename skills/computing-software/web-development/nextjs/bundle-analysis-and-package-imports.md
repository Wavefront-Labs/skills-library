---
id: computing-software.web-development.nextjs.bundle-analysis-and-package-imports
name: bundle-analysis-and-package-imports
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-optimization, nextjs-metadata, nextjs-bundle-analyzer, optimizepackageimports, client-bundle-size, use-client-boundary-cost, barrel-imports, server-only-code]
level: practitioner
status: verified
description: "Shrinking Next.js client bundles: @next/bundle-analyzer, optimizePackageImports for barrel-heavy libraries, keeping heavy code server-side and dynamic() imports."
sources:
  - https://nextjs.org/docs/app/guides/package-bundling
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports
  - https://nextjs.org/docs/app/guides/lazy-loading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle analysis and package imports

**Goal:** know what ends up in the client JS and cut it - first-load JS directly affects hydration time and INP.

## 1. Analyse
Next 16 builds with Turbopack by default, and the `@next/bundle-analyzer` plugin does not work with it. Ran on 16.4.2: `ANALYZE=true next build` prints `The Next Bundle Analyzer is not compatible with Turbopack builds, no report will be generated` and writes nothing. Two options:
- Turbopack analyzer (Next 16.1+, per the package-bundling guide): `npx next analyze` (interactive web UI, does not produce an app build; `next build --analyze` is also listed in `next build --help`).
- Webpack plugin: `ANALYZE=true next build --webpack` with
```js
// next.config.mjs
import ba from '@next/bundle-analyzer';
const withBundleAnalyzer = ba({ enabled: process.env.ANALYZE === 'true', openAnalyzer: false });
export default withBundleAnalyzer({});
```
which wrote `.next/analyze/client.html`, `nodejs.html` and `edge.html` (ran).
Also read the build output's route table.

## 2. Biggest wins, in order
1. **Move work to Server Components.** Anything not interactive (markdown rendering, date formatting libs, syntax highlighting, data transforms) stays server-side and ships zero JS. Push `'use client'` down to the smallest interactive leaf - everything a client component imports becomes client JS.
2. **Barrel-heavy libraries**: icon sets and UI kits that re-export thousands of modules. `experimental.optimizePackageImports: ['my-ui-kit', …]` rewrites barrel imports to direct imports. The docs list these as optimised by default: `lucide-react`, `date-fns`, `lodash-es`, `ramda`, `antd`, `react-bootstrap`, `@headlessui/react`, `@heroicons/react/*`, `rxjs`, `@mui/material`, `@mui/icons-material`, `recharts`, `react-use`, `@tabler/icons-react` and others (see the optimizePackageImports page for the current list). Or import paths directly.
3. **Lazy-load heavy client widgets**:
```tsx
const Chart = dynamic(() => import('./Chart'), { ssr: false, loading: () => <ChartSkeleton /> });
```
`ssr: false` only in Client Components. Load on interaction/visibility for editors, maps, charts.
4. **Replace heavy deps**: moment -> date-fns/Temporal/Intl, lodash -> native/lodash-es per-method, big validation libs on client -> validate on server.

## 3. Guard against regressions
- `import 'server-only'` in modules that must never reach the client (DB, secrets) - build fails if a client component imports them.
- Size budget in CI: compare the build route table and chunk sizes between commits.

## Verify
- [ ] Analyzer shows no duplicated libraries and no server-only libs in client chunks.
- [ ] First Load JS per key route decreased and within budget.
- [ ] Lighthouse TBT/INP improved on mid-range mobile throttling.
