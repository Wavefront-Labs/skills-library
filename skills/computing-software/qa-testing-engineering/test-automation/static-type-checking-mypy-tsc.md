---
id: computing-software.qa-testing-engineering.test-automation.static-type-checking-mypy-tsc
name: static-type-checking-mypy-tsc
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [static-type-checking, mypy, static-analysis, typescript-strict, pyright]
level: practitioner
status: verified
description: "Use static type checking as defect detection: mypy or pyright strict mode for Python, tsc strict for TypeScript, gradual adoption and CI enforcement."
sources:
  - https://mypy.readthedocs.io/en/stable/config_file.html
  - https://www.typescriptlang.org/tsconfig/#strict
  - https://microsoft.github.io/pyright/#/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static type checking as defect detection

**Goal:** catch None/undefined errors, wrong argument types and broken refactors before any test runs.

## Python (mypy)
```toml
[tool.mypy]
python_version = "3.12"
strict = true                 # disallow_untyped_defs, warn_return_any, warn_unused_ignores, strict_equality...
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "legacy.*"
ignore_errors = true          # gradual adoption: tighten module by module

[[tool.mypy.overrides]]
module = ["boto3.*"]
ignore_missing_imports = true
```
Run `mypy src tests`. mypy 2.4.0 `--strict` enables: disallow_any_generics, disallow_subclassing_any, disallow_untyped_calls, disallow_untyped_defs, disallow_incomplete_defs, check_untyped_defs, disallow_untyped_decorators, warn_redundant_casts, warn_unused_ignores, warn_return_any, no_implicit_reexport, strict_equality, extra_checks (`no_implicit_optional` is not in the list because it is already the default: `def h(x: int = None)` is an error without strict). On a sample file strict reported the unguarded `re.match(...).group` (`union-attr`), untyped defs (`no-untyped-def`), `Returning Any` (`no-any-return`), a missing `Literal` case caught by `assert_never` (`arg-type`) and an unneeded `# type: ignore[...]` (`unused-ignore`). Pyright (`pyright`, or basedpyright) is an alternative checker; pick one per repo.

Override gotcha: `module = "legacy.*"` matches the module name mypy derives, which depends on `__init__.py` files. With `legacy/old.py` and no `legacy/__init__.py` the module is `old`, and with `src/__init__.py` it is `src.legacy.old`; in both cases the `ignore_errors` override silently did nothing until the pattern matched (`"src.legacy.*"`) or `legacy/__init__.py` was added. Check with one deliberate error in the legacy folder.

## TypeScript
```json
{ "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true, "noImplicitOverride": true } }
```
With TypeScript 6.0.3 each of the four options produced its own error on a sample (`noUncheckedIndexedAccess`: `number | undefined` from `arr[0]`; `exactOptionalPropertyTypes`: `{ a: undefined }` rejected; `noImplicitOverride`: TS4114; strict: possibly undefined), and `@typescript-eslint/no-floating-promises` flagged a bare `f();` on an async function (typescript-eslint with ESLint 10.13, `projectService: true`).
CI: `tsc --noEmit` (bundlers like esbuild/Vite strip types without checking).

## Adoption plan for an untyped codebase
1. Enable checking with lenient settings in CI so it never gets worse.
2. Turn on strict for new modules; add overrides list for legacy, shrink it each sprint.
3. Type the boundaries first: API models (pydantic/zod), DB models, public functions.
4. Ban bare `# type: ignore` / `any`: require an error code (`# type: ignore[attr-defined]`; mypy enforces it with `enable_error_code = ["ignore-without-code"]`, which flagged a bare ignore) and lint `@typescript-eslint/no-explicit-any`.

## Defects it finds
Optional values used without checks, misspelled attributes, wrong argument order, missing awaits (`no-floating-promises` in typescript-eslint), unhandled union cases (`assert_never`, exhaustive `switch` with `never`).

## Gotchas
- `cast()` and `as` silence the checker; review them like `ignore`s.
- Runtime data (JSON, env vars) is untyped until validated; parse at the boundary.
- Stub packages (`types-requests`) must match library versions.

## Verify
CI fails on a deliberately introduced `None` misuse, and the count of ignores/overrides trends down.
