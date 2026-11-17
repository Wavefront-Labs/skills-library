---
id: computing-software.software-engineering.java.archunit-architecture-rules
name: archunit-architecture-rules
category: computing-software
field: software-engineering
product: java
tags: [java, java-test-libraries, archunit, architecture-tests, layered-architecture, package-dependencies, freezingarchrule, java-testing]
level: practitioner
status: docs-checked
description: "Enforce Java architecture rules as unit tests with ArchUnit: layer access, no cycles, package rules, and freezing existing violations."
sources: ["https://www.archunit.org/userguide/html/000_Index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ArchUnit architecture rules

Rules run as ordinary JUnit tests over imported classes. The user guide lists the JUnit 5 artifacts as `archunit-junit5-api`, `archunit-junit5-engine` and `archunit-junit5-engine-api`.

## Rules in JUnit
```java
@AnalyzeClasses(packages = "com.mycompany.myapp", importOptions = DoNotIncludeTests.class)
public class MyArchitectureTest {

    @ArchTest
    public static final ArchRule serviceAccess = classes()
        .that().resideInAPackage("..service..")
        .should().onlyBeAccessed().byAnyPackage("..controller..", "..service..");

    @ArchTest
    public static final ArchRule layers = layeredArchitecture()
        .consideringAllDependencies()
        .layer("Controller").definedBy("..controller..")
        .layer("Service").definedBy("..service..")
        .layer("Persistence").definedBy("..persistence..")
        .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
        .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service");

    @ArchTest
    public static final ArchRule noCycles =
        slices().matching("com.myapp.(*)..").should().beFreeOfCycles();
}
```
- Package patterns: `*` is one package segment, `..` is any number of segments including zero, `(*)` captures a segment (used for slice identifiers).
- `ImportOption`s such as `DoNotIncludeTests` and `DoNotIncludeJars` narrow what is imported; `@AnalyzeClasses(wholeClasspath = true)` imports the whole classpath instead of just the test class's package. `@AnalyzeClasses` can be used as a meta-annotation to avoid repeating configuration.
- `ArchRuleDefinition` offers `members()`, `fields()`, `codeUnits()`, `constructors()` and the negations `noMembers()`, `noFields()`, `noMethods()`.
- `onionArchitecture()` defines domain models, domain services, application services and adapters by package.

## Adopting on an existing codebase
`FreezingArchRule.freeze(rule)` records all existing violations to a `ViolationStore`; later runs report only new violations. When violations are fixed, the store shrinks automatically to prevent regression. By default the store is plain text files you can commit to version control, and line numbers are ignored. The location is configured in `archunit.properties` (`freeze.store.default.path`), and creating a new store must be allowed explicitly (`freeze.store.default.allowStoreCreation=true`, default false).

## Verify
Add a deliberate violation (a controller depending on a persistence class) and check the build fails; revert.

## Checked

Method: docs-checked 2026-11-09 against the ArchUnit user guide (000_Index.html). Dropped unconfirmed claims (consideringOnlyDependenciesInLayers, GeneralCodingRules constants, failOnEmptyShould and the 0.23 default, archunit_store folder name, generated-class and Kotlin or Scala notes, performance remarks). The GitHub repository source was not read.
