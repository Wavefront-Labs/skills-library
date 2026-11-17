---
id: computing-software.software-engineering.quarkus.quarkus-cdi-scopes-client-proxies
name: quarkus-cdi-scopes-client-proxies
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cdi, arc, bean-scope, client-proxy, application-scoped, singleton]
level: intro
status: docs-checked
description: "Choose between @ApplicationScoped, @Singleton, @RequestScoped and @Dependent in Quarkus CDI and avoid field access on client-proxied beans."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/cdi.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Quarkus CDI bean scope

Every bean has exactly one scope, which decides when and where its instances are created and destroyed. Quarkus supports all built-in CDI scopes except `jakarta.enterprise.context.ConversationScoped`.

## Scopes available

| Annotation | Behaviour |
|---|---|
| `@jakarta.enterprise.context.ApplicationScoped` | One instance shared by all injection points; created lazily when a method is first invoked on the client proxy. |
| `@jakarta.inject.Singleton` | Like `@ApplicationScoped` but no client proxy; instance created when an injection point resolving to it is injected. |
| `@jakarta.enterprise.context.RequestScoped` | Bound to the current request (usually HTTP). |
| `@jakarta.enterprise.context.Dependent` | Pseudo-scope: every injection point gets a new instance, created and destroyed with the injecting bean. |
| `@jakarta.enterprise.context.SessionScoped` | Backed by `HttpSession`; only available with the `quarkus-undertow` extension. |

Extensions can add scopes, e.g. `quarkus-narayana-jta` provides `jakarta.transaction.TransactionScoped`.

## ApplicationScoped vs Singleton

- `@Singleton` has no proxy: created eagerly at injection, slightly faster, and its fields can be read/written safely. But it cannot be mocked with QuarkusMock.
- `@ApplicationScoped` is created lazily, can be destroyed and recreated at runtime (injected proxies keep working).
- The guide recommends defaulting to `@ApplicationScoped` unless there is a good reason for `@Singleton`.

## Client proxies

A client proxy is a generated class (implements `io.quarkus.arc.ClientProxy`, extends the bean class, e.g. `Translator_ClientProxy`) that looks up the current contextual instance and delegates each method call. It enables lazy instantiation, injecting narrower-scoped beans (e.g. `@RequestScoped`) into wider ones (`@ApplicationScoped`), circular dependencies, and manual bean destruction without stale references.

Gotcha: proxies only delegate methods. Never read or write a field of a normal-scoped bean directly, or you work with non-contextual or stale data.

## Resolution rule

Exactly one bean must be assignable to an injection point, else the build fails: `UnsatisfiedResolutionException` (none) or `AmbiguousResolutionException` (several). To pick at runtime, inject `jakarta.enterprise.inject.Instance<T>` (it is `Iterable`).

## Checked

2026-11-07. Read in full: cdi.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
