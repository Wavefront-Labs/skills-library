---
id: computing-software.qa-testing-engineering.vitest.in-source-testing
name: in-source-testing
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [in-source-testing, import-meta-vitest, include-source, define-dead-code]
level: practitioner
status: docs-checked
description: "Write Vitest tests inside source files under if (import.meta.vitest), enable them with includeSource, strip them from production builds, and add the TypeScript types."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/in-source.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Put a block at the end of the source file, so tests share the closure and can reach private state.

```ts
export function add(...args: number[]) {
  return args.reduce((a, b) => a + b, 0)
}

if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest
  it('add', () => {
    expect(add()).toBe(0)
    expect(add(1, 2, 3)).toBe(6)
  })
}
```

Tell Vitest which files to scan:

```ts
export default defineConfig({
  test: { includeSource: ['src/**/*.{js,ts}'] },
})
```

For production builds define the flag away so the bundler removes the dead code:

```ts
export default defineConfig({
  define: { 'import.meta.vitest': 'undefined' },
})
```

Other bundlers use their own replace/define plugin (Rollup replace, webpack DefinePlugin, unbuild `replace`, Rolldown `transform.define`).

TypeScript: add `"types": ["vitest/importMeta"]` to `compilerOptions` in tsconfig.

Assertion functions such as `assert` have a typing limitation in in-source tests. Use separate test files for more complex tests such as components or E2E.

## Checked

2026-11-04. Confirmed against guide/in-source.md: the `import.meta.vitest` block, `includeSource`, the `define` setting, the Rolldown, Rollup, unbuild and webpack examples, the `vitest/importMeta` types entry, the assertion-function warning and the separate-files recommendation.

Method: documentation only; no commands were run.
