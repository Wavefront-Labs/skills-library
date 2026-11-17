---
id: computing-software.software-engineering.java.type-tokens-for-runtime-generics
name: type-tokens-for-runtime-generics
category: computing-software
field: software-engineering
product: java
tags: [java, java-generics, type-tokens, typereference, parameterizedtypereference, super-type-token, jackson-typereference, type-erasure]
level: advanced
status: draft
description: "Recover generic types at runtime past erasure using Class tokens and super type tokens (TypeReference, ParameterizedTypeReference) for JSON and HTTP deserialization."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/ParameterizedType.html", "https://docs.spring.io/spring-framework/reference/integration/rest-clients.html", "https://github.com/FasterXML/jackson-docs/wiki/JacksonDataBinding"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type tokens for runtime generics

**Problem:** `List<User>` and `List<String>` are both `List` at runtime, so `mapper.readValue(json, List.class)` yields a list of maps.

## Class token (non-generic types)
```java
<T> T read(String json, Class<T> type)       // works for User.class
```

## Super type token (generic types)
Generic information survives in the signature of a *subclass*. An anonymous subclass captures it:
```java
List<User> users = mapper.readValue(json, new TypeReference<List<User>>() {});   // Jackson
List<User> body = restClient.get().uri("/users").retrieve()
    .body(new ParameterizedTypeReference<List<User>>() {});                       // Spring 6.1
```
Note the `{}`: it creates the subclass. Without it the information is erased.

## Writing your own
```java
abstract class TypeToken<T> {
    final Type type;
    protected TypeToken() {
        Type s = getClass().getGenericSuperclass();
        if (!(s instanceof ParameterizedType p)) throw new IllegalStateException("use new TypeToken<...>() {}");
        this.type = p.getActualTypeArguments()[0];
    }
}
```
Prefer Guava `TypeToken`, Jackson `TypeReference`, or Spring `ResolvableType` over a hand-rolled version.

## Gotchas
- Raw `new TypeReference<>() {}` with diamond infers nothing useful on older compilers; spell the type.
- A type variable (`TypeReference<List<T>>` inside a generic method) cannot be resolved: the token holds `T`, not the caller's type. Pass the token from the caller.
- Arrays: `User[].class` works without a token.
- Cache the token in a `static final`; creating an anonymous class on every call adds loading overhead.

## Verify
Assert the result's first element `instanceof User` (not `LinkedHashMap`) in a test; a `ClassCastException` appears only when the element is used, so check an element rather than the list type.
