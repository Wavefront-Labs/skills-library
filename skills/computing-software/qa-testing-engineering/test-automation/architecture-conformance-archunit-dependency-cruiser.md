---
id: computing-software.qa-testing-engineering.test-automation.architecture-conformance-archunit-dependency-cruiser
name: architecture-conformance-archunit-dependency-cruiser
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [archunit, architecture-conformance, dependency-cruiser, static-analysis, import-linter]
level: practitioner
status: gated
description: "Enforce architecture rules as tests: ArchUnit for JVM layers and cycles, dependency-cruiser for JS/TS, import-linter for Python, with baselines for legacy."
sources:
  - https://www.archunit.org/userguide/html/000_Index.html
  - https://github.com/sverweij/dependency-cruiser
  - https://import-linter.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Architecture conformance checks

**Goal:** stop layer violations and dependency cycles from creeping in, by failing the build.

## ArchUnit (Java/Kotlin, JUnit 5)
```java
@AnalyzeClasses(packages = "com.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {
  @ArchTest
  static final ArchRule layers = layeredArchitecture().consideringAllDependencies()
      .layer("Web").definedBy("..web..")
      .layer("Service").definedBy("..service..")
      .layer("Persistence").definedBy("..persistence..")
      .whereLayer("Web").mayNotBeAccessedByAnyLayer()
      .whereLayer("Service").mayOnlyBeAccessedByLayers("Web")
      .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service");

  @ArchTest
  static final ArchRule noCycles = slices().matching("com.shop.(*)..").should().beFreeOfCycles();

  @ArchTest
  static final ArchRule domainPure = noClasses().that().resideInAPackage("..domain..")
      .should().dependOnClassesThat().resideInAnyPackage("org.springframework..", "..persistence..");
}
```
Legacy code: wrap with `FreezingArchRule.freeze(rule)`; existing violations are stored and only new ones fail. The method names above (`layeredArchitecture`, `consideringAllDependencies`, `mayNotBeAccessedByAnyLayer`, `mayOnlyBeAccessedByLayers`, `beFreeOfCycles`, `ImportOption.DoNotIncludeTests`, `FreezingArchRule.freeze`, `.because`) appear in the ArchUnit user guide, but the Java was not compiled or run here (gated: unconfirmed, source is paywalled or blocked). Reason: no Java 11+ or Maven in this environment.

## dependency-cruiser (JS/TS)
```js
// .dependency-cruiser.cjs
module.exports = { forbidden: [
  { name: "no-circular", severity: "error", from: {}, to: { circular: true } },
  { name: "ui-not-to-db", severity: "error", from: { path: "^src/ui" }, to: { path: "^src/db" } },
]};
```
`npx depcruise src --config .dependency-cruiser.cjs`; `--output-type dot` for a graph. Run on dependency-cruiser 18.7.0 with a UI file importing a DB file and a two-file cycle: it printed `error ui-not-to-db: src/ui/ui.js -> src/db/db.js` and the `no-circular` chain, and exited with code 2. Baseline legacy with `npx depcruise-baseline src --config .dependency-cruiser.cjs` (writes `.dependency-cruiser-known-violations.json`; `depcruise --baseline src` treated `src` as the baseline file name and wrote nothing), then run `depcruise src --config ... --ignore-known`: the 2 known violations were ignored (exit 0) and a new offending file failed with `1 dependency violations`.

## import-linter (Python)
```ini
[importlinter]
root_package = shop
[importlinter:contract:layers]
name = Layered
type = layers
layers =
    shop.api
    shop.services
    shop.repositories
```
List layers one per line, highest first. A `|` separates independent sibling layers: with `layers = shop.api | shop.services | shop.repositories` (import-linter run in a scratch project) a valid chain api -> services -> repositories was reported as two broken imports. With the multi-line form the chain is KEPT and a `repositories -> api` import is reported as `shop.repositories is not allowed to import shop.api`. Run `lint-imports` in CI.

## Gotchas
- Rules without a short rationale get deleted the first time they block someone; add `.because("...")` in ArchUnit or comments.
- Package naming must be consistent for patterns to work; fix naming first.
- Check tests separately if tests are allowed to cross layers.

## Verify
A deliberate import from UI to DB layer fails CI with the rule name and reason.
