---
id: computing-software.software-engineering.quarkus.quarkus-test-profiles
name: quarkus-test-profiles
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, testing, test-profile, quarkus-test-resource, junit, mocking]
level: advanced
status: docs-checked
description: "Write QuarkusTestProfile classes, filter by profile tags, and manage test resources with QuarkusTestResource and WithTestResource scopes."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/getting-started-testing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus test profiles and test resources

By default Quarkus boots once for all `@QuarkusTest` classes. A test profile lets a class run with different configuration; if the profile differs from the previous test's, Quarkus is shut down and restarted (slower). To reduce restarts, `io.quarkus.test.junit.util.QuarkusTestProfileAwareClassOrderer` is registered as a global `ClassOrderer`; set a secondary orderer FQCN with `quarkus.test.class-orderer`.

## Writing a profile
Implement `io.quarkus.test.junit.QuarkusTestProfile` (all methods have defaults; override what you need) and apply it with `@TestProfile(MockGreetingProfile.class)` on the test class. Overridable methods: `getConfigOverrides()` (merged over `application.properties`), `getEnabledAlternatives()` (like `quarkus.arc.selected-alternatives`), `getConfigProfile()` (sets `quarkus.test.profile`), `testResources()` (list of `TestResourceEntry`), `disableGlobalTestResources()`, `tags()`, `commandLineParameters()`, `runMainMethod()`, `disableApplicationLifecycleObservers()`. A CDI bean declared in a profile (producer method/field or nested static class) only applies when that profile is used.

## Filtering by tags
Return tags from `tags()`, then set the system property `quarkus.test.profile.tags` (comma-separated). Only tests whose `@TestProfile` has at least one matching tag run; the rest are skipped, including tests with no `@TestProfile`. Unset means all tests run. Example: with tags `test1` and `test1,test2` on two profiles, `quarkus.test.profile.tags=test2,test3` runs only the second.

## Test resources
Start dependencies (Testcontainers, WireMock) before the app by implementing `QuarkusTestResourceLifecycleManager` (`start()` returns a config map, `stop()`, optional `inject(TestInjector)`) and annotating any test with `@QuarkusTestResource`. Resources are global even when declared on a class or profile; use `@QuarkusTestResource(restrictToAnnotatedClass = true)` to limit them and `parallel = true` to start several concurrently. The manager is not a CDI bean, so no `@Inject`; read config via `Config.get().getValue(...)`. For annotation-driven resources, put `@QuarkusTestResource` on your own annotation and implement `QuarkusTestResourceConfigurableLifecycleManager<A>` with `init(A)`; make it repeatable with `@QuarkusTestResourceRepeatable`.

## `@WithTestResource` scopes
`TestResourceScope.MATCHING_RESOURCES` (default; groups tests with identical resources and stops them after each group), `RESTRICTED_TO_CLASS`, `GLOBAL`. Quarkus restarts if a current or next test has class-restricted resources, or different `MATCHING_RESOURCES` sets are used.

## Gotchas
`@Nested` tests cannot take different profiles or resources than their parent. Mixing `@QuarkusTest` with `@QuarkusDevModeTest`, `@QuarkusProdModeTest` or `@QuarkusExtensionTest` in one run is not allowed; isolate via the JUnit tag `io.quarkus.test.junit.QuarkusTest` (Surefire `groups` / `excludedGroups`).

## Checked

2026-11-07. Matched against the text (with includes) of: getting-started-testing.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
