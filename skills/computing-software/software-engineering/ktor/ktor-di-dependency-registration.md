---
id: computing-software.software-engineering.ktor.ktor-di-dependency-registration
name: ktor-di-dependency-registration
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, dependency-injection, di, registration, provide, kotlin]
level: practitioner
status: docs-checked
description: "Register Ktor DI dependencies in a dependencies block with provide: lambdas, constructor, class and function references, named providers, and config-file registration."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-di-dependency-registration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Register dependencies in Ktor DI

Requires `io.ktor:ktor-server-di`. Registration tells the container how to create the objects your application depends on. It is done in code, typically in an `Application` module, inside the `dependencies {}` block.

## Forms of provide()

```kotlin
dependencies {
    provide<GreetingService> { GreetingServiceImpl() }       // lambda: full control
    provide<GreetingService>(::GreetingServiceImpl)           // constructor reference
    provide(BankServiceImpl::class)                           // class reference
    provide(::createBankTeller)                               // function reference
    provide<() -> GreetingService> { { GreetingServiceImpl() } } // factory lambda
}
```

- Lambda: executed each time `GreetingService` is requested.
- Constructor reference: all constructor parameters must already be registered; DI resolves them.
- Class reference: registers a concrete class without an interface; it is resolved by that type.
- Function reference: DI resolves the function parameters and uses the return value as the instance.
- Factory lambda: registers a function that can be injected and called manually to create new instances.

## Named registration

To register several providers of one type, pass a name as the first argument:

```kotlin
dependencies {
    provide("default") { GreetingServiceImpl() }
    provide("alternative") { AlternativeGreetingServiceImpl() }
}
```

Named dependencies must be resolved explicitly with the `@Named` annotation (see ktor-di-dependency-resolution).

## Configuration-based registration

List classpath references under the `ktor.application.dependencies` group in the configuration file (for example `application.yaml`). Each entry can be a function that returns an object, or a class with a resolvable constructor. Ktor resolves function and constructor parameters automatically through the DI container.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-di-dependency-registration.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
