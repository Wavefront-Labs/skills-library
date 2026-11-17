---
id: computing-software.qa-testing-engineering.jest-pytest.jest-with-esm-and-typescript
name: jest-with-esm-and-typescript
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [ts-jest, jest-esm, typescript, babel-jest, jest-config]
level: practitioner
status: verified
description: "Configure Jest for TypeScript and ES modules: ts-jest vs babel-jest vs SWC, path aliases via moduleNameMapper, native ESM with experimental-vm-modules, and transformIgnorePatterns."
sources:
  - https://jestjs.io/docs/getting-started#using-typescript
  - https://kulshekhar.github.io/ts-jest/
  - https://jestjs.io/docs/ecmascript-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jest with ESM and TypeScript

## Choose a transformer
| | Type-checks | Speed | Notes |
|---|---|---|---|
| ts-jest | yes (unless `isolatedModules` is on) | slower | closest to tsc behaviour; ts-jest 29.4 declares `typescript >=4.3 <7`, so it does not accept TypeScript 7 |
| babel-jest + @babel/preset-typescript | no | faster | run `tsc --noEmit` separately |
| @swc/jest | no | faster | speed ranking not measured here; the swc transformer was not run |

## ts-jest config
```js
// jest.config.js
/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',                 // 'jsdom' for DOM tests (install jest-environment-jsdom)
  moduleNameMapper: { '^@/(.*)$': '<rootDir>/src/$1' },          // mirror tsconfig "paths"
  transform: { '^.+\\.tsx?$': ['ts-jest', { tsconfig: 'tsconfig.test.json' }] },
};
```
Set `"isolatedModules": true` in `tsconfig.test.json` to skip per-file type checking. The ts-jest transformer option `isolatedModules` still works in 29.4 but prints a deprecation warning telling you to use the tsconfig setting (ran: with it on, a file with `const x: number = 's'` passed; with it off ts-jest failed the suite with TS2322).
`pathsToModuleNameMapper(compilerOptions.paths, { prefix: '<rootDir>/' })` from ts-jest generates the mapper from tsconfig.

## Native ESM
```json
// package.json
{ "type": "module", "scripts": { "test": "node --experimental-vm-modules node_modules/jest/bin/jest.js" } }
```
```js
// jest.config.js (ESM)
export default {
  preset: 'ts-jest/presets/default-esm',
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapper: { '^(\\.{1,2}/.*)\\.js$': '$1' },     // allow .js extensions in TS imports
  transform: { '^.+\\.ts$': ['ts-jest', { useESM: true }] },
};
```
In ESM mode `jest` must be imported (`import { jest } from '@jest/globals'`; the global is undefined) and module mocks use `jest.unstable_mockModule` followed by a dynamic `await import()` (ran with ts-jest `default-esm`, `useESM`, and `node --experimental-vm-modules node_modules/jest/bin/jest.js`).

## ESM-only dependencies (CJS mode)
From node_modules these show as an error such as `Must use import to load ES Module` (Jest 30, ran with nanoid 5) or `SyntaxError: Cannot use import statement outside a module`: transform them.
```js
transformIgnorePatterns: ['/node_modules/(?!(nanoid)/)'],
```
(with babel-jest, or ts-jest with `"allowJs": true` in the tsconfig and a `'^.+\\.[tj]sx?$'` transform; ran). Jest 30's error text also notes that Node 24.9+ lets Jest `require()` ESM natively.

## Gotchas
- Type errors are silently ignored with babel/SWC (not run here); add `tsc --noEmit` to CI.
- `isolatedModules` speeds ts-jest but disables type-check per file (ran).
- Vitest is often simpler for ESM/Vite projects; same API surface.

## Verify
`npx jest` runs TS tests with aliases resolving, ESM-only deps load, and CI also runs a type-check.
