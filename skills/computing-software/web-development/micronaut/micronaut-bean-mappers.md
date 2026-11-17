---
id: computing-software.web-development.micronaut.micronaut-bean-mappers
name: micronaut-bean-mappers
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, bean-mappers, mapper, mapping, dto, introspection, merge]
level: practitioner
status: docs-checked
description: "Generate compile-time type-to-type mappings and bean merges with @Mapper and @Mapping, using expressions for transformed properties."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beanMappers.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beanMappers/beanMappersMerging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: map one type onto another (or merge several) without hand-written code or reflection. `@Mapper` is available since 4.1.x; merging since 4.8.x. It builds on bean introspection and expressions, so both source and target types must be `@Introspected`.

## Simple mapping

```java
@Introspected
public record ContactForm(String firstName, String lastName) {}

@Introspected
public record ContactEntity(Long id, String firstName, String lastName) {}

public interface ContactMappers {
    @Mapper
    ContactEntity toEntity(ContactForm contactForm);
}
```

The compiler generates the implementation; inject `ContactMappers` and call `toEntity(new ContactForm("John", "Snow"))`.

## Customizing with @Mapping

Put one `@Mapper`, or one or more `@Mapping` annotations, on an abstract method. `@Mapping` is needed only for properties that require a transformation; the rest map and convert automatically. `from` is a source property name or an expression over the method arguments (it can call methods of the mapper instance, via `this`); `to` is the target property; `format` formats values.

```java
@Singleton
public interface ProductMappers {
    @Mapping(
        to = "price",
        from = "#{product.price * 2}",
        format = "$#.00"
    )
    @Mapping(
        to = "distributor",
        from = "#{this.getDistributor()}"
    )
    ProductDTO toProductDTO(Product product);

    default String getDistributor() {
        return "Great Product Company";
    }
}
```

With `Product("MacBook", 910.50, "Apple")` the DTO has price `"$1821.00"` and distributor `"Great Product Company"`.

## Merging

A method with two or more arguments merges them into the return type; refer to arguments by parameter name in `from`:

```java
public interface ChristmasMappers {
    @Mapping(from = "packaging.color", to = "packagingColor")
    @Mapping(from = "#{packaging.weight + present.weight}", to = "weight")
    @Mapping(from = "#{'Merry christmas'}", to = "greetingCard")
    ChristmasPresent merge(PresentPackaging packaging, Present present);
}
```

`merge(new PresentPackaging(1f, "red"), new Present(10f, "teddy bear"))` yields weight 11, colour `red`, type `teddy bear`, greeting `Merry christmas`. All involved records are `@Introspected`.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
