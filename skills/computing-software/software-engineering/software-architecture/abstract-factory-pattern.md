---
id: computing-software.software-engineering.software-architecture.abstract-factory-pattern
name: abstract-factory-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, abstract-factory, gof, product-families, dependency-injection, platform-abstraction]
level: practitioner
status: draft
description: "Use the GoF Abstract Factory to create families of related objects that must be used together (UI themes, cloud providers, DB dialects) behind one interface."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Abstract Factory", "https://refactoring.guru/design-patterns/abstract-factory"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abstract Factory

**Intent (GoF):** provide an interface for creating families of related or dependent
objects without specifying their concrete classes.

## When it fits
The key word is FAMILY: several products that must be consistent with each other.
- UI toolkits: `Button`, `Checkbox`, `Dialog` for macOS vs Windows themes.
- Storage backends: `BlobStore`, `Queue`, `SecretStore` for AWS vs GCP vs local dev.
- Database dialects: `QueryBuilder`, `TypeMapper`, `MigrationRunner` per engine.

## Shape
```kotlin
interface CloudFactory {
    fun blobStore(): BlobStore
    fun queue(name: String): Queue
}
class AwsFactory(private val cfg: AwsConfig) : CloudFactory {
    override fun blobStore() = S3BlobStore(cfg)
    override fun queue(name: String) = SqsQueue(cfg, name)
}
class LocalFactory : CloudFactory {
    override fun blobStore() = FileBlobStore(Path.of("/tmp/blobs"))
    override fun queue(name: String) = InMemoryQueue(name)
}
// composition root picks ONE factory based on config:
val cloud: CloudFactory = if (env == "local") LocalFactory() else AwsFactory(cfg)
```
Client code receives `CloudFactory` and can never mix an S3 store with a local queue.

## Consequences
+ Swapping the whole family is one line at the composition root.
+ Consistency between products enforced by construction.
- Adding a NEW KIND of product (e.g. `cache()`) changes the interface and every
  factory: costly when families are many.

## Relationship to DI containers
A DI container configured per environment (Spring profiles, .NET environment-specific
registrations) often replaces hand-written abstract factories. Keep an explicit factory
when objects must be created at runtime with parameters (`queue(name)`), which
containers handle awkwardly.

## Pitfalls
- Using it with a single family "for future flexibility": YAGNI.
- Factories that leak concrete types in return values (`fun blobStore(): S3BlobStore`).

## Verify
- [ ] At least two real families exist (production and a test/local one counts).
- [ ] Only the composition root references concrete factories.
