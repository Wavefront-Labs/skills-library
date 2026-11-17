---
id: computing-software.qa-testing-engineering.jest-pytest.coverage-exclusions-and-pragmas
name: coverage-exclusions-and-pragmas
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [coverage-exclusions, pragma-no-cover, istanbul-ignore, jacoco-exclude, coverage-config]
level: practitioner
status: verified
description: "Exclude code from coverage deliberately: coverage.py exclude_also and pragma no cover, istanbul ignore hints, Jest coveragePathIgnorePatterns, JaCoCo excludes, and review rules."
sources:
  - https://coverage.readthedocs.io/en/latest/excluding.html
  - https://github.com/istanbuljs/nyc#parsing-hints-ignoring-lines
  - https://www.jacoco.org/jacoco/trunk/doc/maven.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage exclusions and pragmas

## coverage.py
```toml
[tool.coverage.report]
exclude_also = [
  "if TYPE_CHECKING:",
  "raise NotImplementedError",
  "if __name__ == .__main__.:",
  "@(abc\\.)?abstractmethod",
  "\\.\\.\\.$",                     # protocol stubs
]
omit = ["src/*/migrations/*", "src/*/_version.py"]
```
Line/block: `# pragma: no cover` (excludes the line, or the whole block if on a `def`/`if` line). Branch only: `# pragma: no branch` for intentionally one-sided conditions (`while True:`).
`exclude_also` adds to defaults; `exclude_lines` replaces them (and drops the default pragma unless re-added).

## Istanbul (Jest, nyc, Vitest with istanbul provider)
```js
/* istanbul ignore next */          // next statement/function
/* istanbul ignore if */            // the if branch
/* istanbul ignore else */
/* istanbul ignore file */
```
V8 provider: `/* v8 ignore next */`, `/* v8 ignore start */ ... /* v8 ignore stop */`. Comment pragmas only work if the instrumenter still sees the comments: check the instrumented output if you pre-transform code (run: V8 `next 3` / `start`+`stop` and Istanbul `else`/`next` honoured by their own provider only, so pick one syntax per provider).
Config: `coveragePathIgnorePatterns: ['/node_modules/', '/generated/']`, or prefer `collectCoverageFrom` negations.

## JaCoCo
```xml
<configuration><excludes><exclude>**/generated/**</exclude><exclude>**/*Config.class</exclude></excludes></configuration>
```
JaCoCo automatically filters Lombok-generated code if `lombok.addLombokGeneratedAnnotation = true`; any annotation whose simple name contains `Generated` with class/runtime retention is excluded (JaCoCo 0.8.3+ changelog; 0.8.2 required the exact name `Generated`).

## Policy
Exclude only code that can't or shouldn't be tested in unit tests (type-checking blocks, platform guards, generated code, debug-only paths). Require a comment explaining why, and review pragmas in PRs: they are the cheapest way to fake a coverage gate.

## Gotchas
- Excluding a whole module because it is "hard to test" hides the riskiest code.
- Coverage % rises when excluding; communicate config changes so trend lines aren't misread.

## Verify
`grep -rn "pragma: no cover\|istanbul ignore" src | wc -l` tracked over time; each occurrence has a reason.
