---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-typescript-scripts
name: k6-typescript-scripts
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-typescript, typescript-load-tests, k6-types, compatibility-mode]
level: practitioner
status: verified
description: "Write k6 tests in TypeScript: native TS support (k6 0.57+), @types/k6 for editor types, tsconfig, compatibility modes and bundling for older versions."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/javascript-typescript-compatibility-mode/
  - https://www.npmjs.com/package/@types/k6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing k6 scripts in TypeScript

## Native support
Recent k6 (0.57+, and 1.x) runs `.ts` files directly by stripping types with esbuild:
```bash
k6 run script.ts
```
Older 0.52-0.56: `k6 run --compatibility-mode=experimental_enhanced script.ts` (k6 2.3.0 still accepts it but warns it is deprecated: types are stripped by default for `.ts`; use `base`). Type checking is **not** performed at run time; run `tsc --noEmit` in CI. Run on k6 2.3.0: the example below, including a local `.ts` import and an `enum`, executed with all 102 checks passing.

## Types
```bash
npm i -D @types/k6 typescript
```
```json
// tsconfig.json
{ "compilerOptions": { "target": "ES2020", "module": "ES2020", "moduleResolution": "bundler", "strict": true, "noEmit": true, "allowImportingTsExtensions": true, "types": ["k6"] } }
```

## Example
```ts
import http from 'k6/http';
import { check } from 'k6';
import type { Options } from 'k6/options';

export const options: Options = {
  scenarios: { api: { executor: 'constant-arrival-rate', rate: 50, timeUnit: '1s', duration: '5m', preAllocatedVUs: 50 } },
  thresholds: { http_req_duration: ['p(95)<300'] },
};

interface Order { id: string; total: number }

export default function (): void {
  const res = http.get(`${__ENV.BASE_URL}/orders/1`);
  const order = res.json() as unknown as Order;
  check(res, { 'ok': (r) => r.status === 200, 'total>0': () => order.total > 0 });
}
```

## Limits
- Type stripping only: no `enum` emit quirks beyond esbuild's support, no decorators metadata, no path aliases unless bundled.
- Imports of local `.ts` modules must include the extension (`./lib/auth.ts`; without it k6 fails with `The moduleSpecifier "./lib/auth" couldn't be found`), and `tsc` then needs `"allowImportingTsExtensions": true` (without it: `TS5097: An import path can only end with a '.ts' extension`; checked with TypeScript 7.0.2 and `@types/k6`).
- npm dependencies still need bundling (esbuild/webpack templates).

## Gotchas
- `res.json()` returns a JSON value type; cast via `unknown` or validate.
- Editor errors on `__ENV`/`open` vanish once `@types/k6` is in `types`.

## Verify
`npx tsc --noEmit && k6 run --vus 1 --iterations 1 script.ts` passes in CI.
