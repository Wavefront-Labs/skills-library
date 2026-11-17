---
id: computing-software.software-engineering.quarkus.quarkus-config-profiles
name: quarkus-config-profiles
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, configuration, profiles, application-properties, parent-profile, smallrye-config]
level: practitioner
status: docs-checked
description: "Quarkus configuration profiles: %profile prefixes, dev/test/prod, custom and multiple profiles, profile-aware files, parent profiles and their pitfalls."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus configuration profiles

Profiles let one application hold different configuration per environment.

## Syntax
Prefix the property with `%` and the profile name:

```properties
quarkus.http.port=9090
%dev.quarkus.http.port=8181
```

Port is 9090, or 8181 under `dev`. In `.env` use `_DEV_QUARKUS_HTTP_PORT=8181`. A profile that does not define a property falls back to the unprefixed value.

Built-in profiles: `dev` (dev mode), `test` (running tests), `prod` (default otherwise). Custom profile: set `quarkus.profile=staging` and define `%staging.` properties.

## Profile-aware files
Put `quarkus.http.port=9190` in `application-staging.properties`; names there need no `%staging.` prefix and win over profile properties in the main file. Rules:
- An `application.properties` must exist (even empty) in the same location as the `application-[profile].properties` file, to keep load order consistent.
- Never set `quarkus.profile` or `quarkus.test.profile` in a profile-aware file; the profile is needed before those files load.

## Multiple profiles
`quarkus.profile=common,dev` activates both. If both define a property the last listed wins (lookup checks `dev` first, then `common`). A property key can also list profiles, e.g. `%prod,dev.my.prop=1234`; when it clashes with `%dev.my.prop=5678`, the most specific profile wins (5678).

## Parent profile
`quarkus.config.profile.parent=common` (comma-separated list) makes lookup fall back from the active profile to the parent. With `quarkus.profile=dev`, `%common.quarkus.http.port=9090` beats plain `quarkus.http.port=8080`, while `%dev.quarkus.http.ssl-port=9443` beats the parent. Multi-level chains work:

```properties
quarkus.profile=child
%child.quarkus.config.profile.parent=parent
%parent.quarkus.config.profile.parent=grandparent
```

`child` overrides `parent`, which overrides `grandparent`. Do not set the parent profile in a profile-aware file.

## Build vs runtime
Quarkus builds with `prod` by default, and the runtime default profile is the one used to build (e.g. `./mvnw package -Dnative -Dquarkus.profile=prod-aws` runs as `prod-aws` unless `quarkus.profile` overrides it). Running with a different profile than the build used can give unexpected results. Read active profiles in code with `io.quarkus.runtime.configuration.ConfigUtils.getProfiles`.

## Checked

2026-11-07. Read in full: config-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
