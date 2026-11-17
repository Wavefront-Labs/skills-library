---
id: computing-software.software-engineering.quarkus.quarkus-startup-shutdown-lifecycle
name: quarkus-startup-shutdown-lifecycle
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, lifecycle, startup, shutdown, startup-event, quarkus-main, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Run code at Quarkus startup and shutdown with StartupEvent, @Startup, @Shutdown, QuarkusApplication main classes, and configure graceful shutdown delay."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/lifecycle.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus application startup and shutdown hooks

## Observers

```java
@ApplicationScoped
public class AppLifecycleBean {
    void onStart(@Observes StartupEvent ev) { /* starting */ }
    void onStop(@Observes ShutdownEvent ev) { /* stopping */ }
}
```

Types: `io.quarkus.runtime.StartupEvent` / `ShutdownEvent`. They also fire in dev mode between redeployments, and the methods can use injected beans.

Versus `@Initialized(ApplicationScoped.class)` / `@Destroyed(ApplicationScoped.class)`: in JVM mode `StartupEvent` fires after `@Initialized`, `ShutdownEvent` before `@Destroyed`. In a native build `@Initialized` fires during the native build, `StartupEvent` when the image runs, so prefer `StartupEvent`.

## @Startup

`io.quarkus.runtime.Startup` on a class, producer method or field initializes the bean at startup (a synthetic `StartupEvent` observer with default priority). A class with `@Startup` but no scope gets `@ApplicationScoped`. `@Dependent` beans are destroyed right afterwards.

On a non-static, non-producer, no-args method it invokes that method on the contextual instance at startup. A method returning `Uni<Void>` runs on a non-blocking thread and needs the Vert.x extension (error otherwise).

## @Shutdown and shutdown delay

`io.quarkus.runtime.Shutdown` marks a non-private, non-static, no-arg business method; equivalent to observing `ShutdownEvent`.

`@ShutdownDelayInitiated` (same method rules) is equivalent to observing `ShutdownDelayInitiatedEvent`; requires `quarkus.shutdown.delay-enabled=true`. These methods always run and can block shutdown.

## Graceful shutdown

- `quarkus.shutdown.timeout`: wait for running requests up to this timeout; disabled by default. Only the HTTP extension supports it so far.
- `quarkus.shutdown.delay-enabled=true` (build-time) plus `quarkus.shutdown.delay` (runtime): the app keeps serving but the readiness probe fails, giving infrastructure time to stop routing traffic.

## Custom main

`@io.quarkus.runtime.annotations.QuarkusMain` on a class with `main` calling `Quarkus.run(args)`. Avoid business logic in `main` (Quarkus not set up, may be a different ClassLoader). Instead pass a `QuarkusApplication` to `Quarkus.run(MyApp.class, args)`; its `int run(String... args)` is invoked after startup and the app exits when it returns, so for startup logic that keeps the app alive call `Quarkus.waitForExit()`, which waits until a shutdown is requested. Inject args with `@Inject @CommandLineArguments String[] args`; pass them via `-Dquarkus.args=...`.

`LaunchMode` (`NORMAL`, `DEVELOPMENT`, `TEST`) is injectable or via `LaunchMode.current()`.

## Checked

2026-11-07. Matched against the text (with includes) of: lifecycle.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that `quarkus.shutdown.delay` is unset by default (the page gives no default) and the loose claim that `Quarkus.waitForExit()` keeps the app serving; it now says it waits until a shutdown is requested.

Method: documentation only; no commands were run.
