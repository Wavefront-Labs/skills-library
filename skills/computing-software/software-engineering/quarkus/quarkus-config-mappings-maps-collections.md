---
id: computing-software.software-engineering.quarkus.quarkus-config-mappings-maps-collections
name: quarkus-config-mappings-maps-collections
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, config-mapping, smallrye-config, maps, collections, withunnamedkey, withkeys]
level: advanced
status: docs-checked
description: "Map Quarkus properties to @ConfigMapping List, Set and Map members: indexed keys, quoting rules, @WithParentName, @WithUnnamedKey, @WithKeys, @WithDefaults."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-mappings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collections and Maps in Quarkus @ConfigMapping

A `@io.smallrye.config.ConfigMapping(prefix = "server")` interface maps `server.host` to `host()`. Missing non-Optional values throw `NoSuchElementException`; wrap in `Optional` to avoid that.

## List and Set
`List`/`Set` members can use indexed properties; simple element types take a comma-separated value:

```properties
server.environments[0].name=dev
server.environments[0].apps[0].name=rest
server.environments[0].apps[0].services=bookstore,registration
```

`List` is backed by `ArrayList`, `Set` by `HashSet`; only `List` keeps order.

## Map
`Map<String, String> form()` needs an extra segment as the key: `server.form.login.page=login.html` gives key `login.page`. Quotes around a key are required only when it contains a dot: `server.aliases."io.quarkus"[0].name=quarkus`.
Do not mix `server.aliases.localhost.name` and `server.aliases."localhost".name` for the same key: the quoted form wins, a warning is logged, and unquoted names are left unmapped (validation may fail). Pick one form everywhere.

## Maps of groups with `@WithParentName`
```java
@ConfigMapping(prefix = "server")
public interface Servers {
    @WithParentName
    Map<String, Server> allServers();
}
```
`server."my-server".host=localhost` yields key `my-server`.

## `@WithUnnamedKey`
`@WithUnnamedKey("localhost") Map<String, Alias> aliases()` lets `server.aliases.name=localhost` fill key `localhost`, alongside `server.aliases.prod.name=prod`. An explicit `server.aliases.localhost.name` takes precedence. Attribute `eager` (default `true`); with `eager = false` the unnamed entry is omitted unless a value is set explicitly in a source.

## `@WithKeys`
`@WithKeys(KeysProvider.class)`, where the class implements `Supplier<Iterable<String>>`, declares the keys to load instead of discovering them via `Config#getPropertyNames`; useful when a ConfigSource does not enumerate properties. Every key must exist in the final configuration or a `ConfigValidationException` is thrown.

## `@WithDefaults`
On a Map, any key lookup returns an instance built from `@WithDefault` values (e.g. `@WithDefault("localhost") String name()`), while the Map only iterates/sizes explicitly defined keys.

## Checked

2026-11-07. Read in full: config-mappings.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
