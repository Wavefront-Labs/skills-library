---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-extension-model
name: junit5-extension-model
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [junit-extensions, junit5, extendwith, parameter-resolver, test-lifecycle-callbacks]
level: practitioner
status: docs-checked
description: "Write and use JUnit 5 extensions: ExtendWith and RegisterExtension, lifecycle callbacks, ParameterResolver, TestWatcher, ExtensionContext.Store, and auto-registration."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/extensions/registering-extensions.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/extensions/keeping-state-in-extensions.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/extensions/test-lifecycle-callbacks.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/extensions/test-result-processing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension model in JUnit 5

**Goal:** reusable cross-cutting test behaviour (resources, injection, reporting) without base-class inheritance.

## Using extensions
```java
@ExtendWith({MockitoExtension.class, SpringExtension.class})
class OrderServiceTest { ... }

class ApiTest {
  @RegisterExtension
  static WireMockExtension wm = WireMockExtension.newInstance().options(wireMockConfig().dynamicPort()).build();
}
```
`@RegisterExtension` (static or instance field) allows configuration in code.

## Writing one: timing + parameter injection
```java
public class TempDatabaseExtension implements BeforeAllCallback, AfterAllCallback, ParameterResolver {
  private static final ExtensionContext.Namespace NS = ExtensionContext.Namespace.create(TempDatabaseExtension.class);

  @Override public void beforeAll(ExtensionContext ctx) {
    ctx.getStore(NS).put("db", TempDatabase.start());
  }
  @Override public void afterAll(ExtensionContext ctx) {
    ctx.getStore(NS).get("db", TempDatabase.class).stop();
  }
  @Override public boolean supportsParameter(ParameterContext p, ExtensionContext e) {
    return p.getParameter().getType() == TempDatabase.class;
  }
  @Override public Object resolveParameter(ParameterContext p, ExtensionContext e) {
    return e.getStore(NS).get("db", TempDatabase.class);
  }
}

@ExtendWith(TempDatabaseExtension.class)
class RepoTest {
  @Test void saves(TempDatabase db) { ... }
}
```
Stored values implementing `AutoCloseable` (since 5.13) are closed automatically when the context ends; `ExtensionContext.Store.CloseableResource` is the deprecated pre-5.13 mechanism. Automatic closing can be switched off with `junit.jupiter.extensions.store.close.autocloseable.enabled=false`.

## Extension points
`BeforeAllCallback`, `BeforeEachCallback`, `BeforeTestExecutionCallback`, `AfterTestExecutionCallback`, `AfterEachCallback`, `AfterAllCallback`, `ParameterResolver`, `TestInstancePostProcessor`, `ExecutionCondition` (conditional disable), `TestExecutionExceptionHandler`, `TestWatcher` (testSuccessful/testFailed: screenshots on failure), `InvocationInterceptor`, `TestTemplateInvocationContextProvider`.

## Composed annotations
```java
@Target(TYPE) @Retention(RUNTIME)
@ExtendWith(TempDatabaseExtension.class) @Tag("integration")
public @interface DatabaseTest {}
```

## Auto-registration
`META-INF/services/org.junit.jupiter.api.extension.Extension` + `junit.jupiter.extensions.autodetection.enabled=true` (off by default; `.include` / `.exclude` patterns narrow it).

## Gotchas
- State in extension fields is shared across tests and threads; use the Store.
- Fields registered with `@ExtendWith` and `@RegisterExtension` are ordered by an intentionally non-obvious algorithm unless you add `@Order`. After-callbacks wrap before-callbacks (see "Wrapping Behavior of Callbacks" in the user guide).

## Verify
The extension works when applied to two unrelated test classes, cleans up resources, and parallel execution does not share state.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: `@RegisterExtension` and `@ExtendWith` registration and ordering notes; AutoCloseable store values since 5.13 and the CloseableResource deprecation; the auto-detection property; extension point interfaces (callbacks, `TestWatcher`, `ParameterResolver`).

Method: documentation only; no commands were run.
