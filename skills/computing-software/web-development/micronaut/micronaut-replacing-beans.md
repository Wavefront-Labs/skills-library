---
id: computing-software.web-development.micronaut.micronaut-replacing-beans
name: micronaut-replacing-beans
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, bean-replacement, replaces, defaultimplementation, factory-replacement, testing, mock]
level: practitioner
status: docs-checked
description: "Replace a Micronaut bean with @Replaces, swap whole factories or single factory methods, and let an interface declare a replaceable @DefaultImplementation."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/replaces.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: override an existing bean (for a test or customisation) without bean names or load order.

Micronaut beans have a type and a qualifier, no names and no load order, so you cannot override a bean with one of a completely different type. Overriding is explicit through `@Replaces`, which combines with conditional beans.

## Replace a bean

```java
@Replaces(JdbcBookService.class)
@Singleton
public class MockBookService implements BookService { ... }
```

Place it, for example, under `src/test/java` to replace the real bean in tests only.

## Replace a factory or one of its methods

Given:

```java
@Factory
public class BookFactory {
    @Singleton Book novel() { return new Book("A Great Novel"); }
    @Singleton TextBook textBook() { return new TextBook("Learning 101"); }
}
```

Replace the whole factory with `@Replaces(factory = BookFactory.class)` on a factory class:

```java
@Factory
@Replaces(factory = BookFactory.class)
public class CustomBookFactory {
    @Singleton Book otherNovel() { return new Book("An OK Novel"); }
}
```

Warning: to replace a factory entirely, your factory methods must match the return types of all methods in the replaced factory. Here `textBook()` is not replaced because the new factory has no method returning `TextBook`.

To replace only some methods, annotate the method with the type and the factory:

```java
@Factory
public class TextBookFactory {
    @Singleton
    @Replaces(value = TextBook.class, factory = BookFactory.class)
    TextBook textBook() { return new TextBook("Learning 305"); }
}
```

`BookFactory#novel()` stays, since only `TextBook` is named.

## Default implementation for API authors

If the default implementation is package private, users cannot reference it to replace it. Point the interface at it with `@DefaultImplementation`:

```java
@DefaultImplementation(DefaultResponseStrategy.class)
public interface ResponseStrategy {}

@Singleton
class DefaultResponseStrategy implements ResponseStrategy {}

@Singleton
@Replaces(ResponseStrategy.class)
public class CustomResponseStrategy implements ResponseStrategy {}
```

A bean declaring `@Replaces(ResponseStrategy.class)` therefore replaces `DefaultResponseStrategy`.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state. Dropped the unconfirmed claim that `@Infrastructure` beans cannot be replaced.

Method: documentation only; no commands were run.
