---
id: computing-software.software-engineering.spring-boot.config-file-locations
name: config-file-locations
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, application-properties, application-yaml, spring-config-location, spring-config-name, wildcard, optional]
level: practitioner
status: docs-checked
description: "Where Spring Boot looks for application.properties and application.yaml, and how spring.config.name, location, additional-location, optional: and wildcards change that."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spring Boot loads `application.properties` and `application.yaml` from these locations, later ones overriding earlier:
1. classpath root
2. classpath `/config` package
3. current directory
4. `config/` subdirectory of the current directory
5. immediate child directories of `config/`

Change the base name: `java -jar myproject.jar --spring.config.name=myproject`.

Replace the locations with a comma-separated list:
`java -jar myproject.jar --spring.config.location=optional:classpath:/default.properties,optional:classpath:/override.properties`

`spring.config.name`, `spring.config.location` and `spring.config.additional-location` are read very early, so set them as an OS environment variable, system property or command-line argument.

Rules:
- Directories in `spring.config.location` should end in `/`; the `spring.config.name` names are appended at runtime. Files listed are imported directly.
- Profile-specific variants of each location are also checked.
- `spring.config.location` replaces the defaults; `spring.config.additional-location` adds locations that can override the defaults.
- A missing location throws `ConfigDataLocationNotFoundException` and the app fails to start, unless you use the `optional:` prefix (also valid on `spring.config.import`). Set `spring.config.on-not-found` to `ignore` to ignore all such errors.
- Wildcard: `*` only in the last path segment (`config/*/` for directories, `*/<filename>` for files), external directories only (not `classpath:`), sorted alphabetically by absolute path. `config/*/` is already a default location, useful for Kubernetes mounts.
- Location groups separated by `;` are treated at the same level for profile-specific override order.

## Checked

2026-11-07

Read the External Application Properties, Optional Locations and Wildcard Locations sections of external-config.adoc (docs-repo source of the cited Externalized Configuration page); the profile-specific and import sections were read for contradictions and none found.
Confirmed: the five default locations and their override order; spring.config.name=myproject example; spring.config.location with optional:classpath: example; the WARNING that name, location and additional-location must be environment properties; trailing-slash rule, name appended at runtime, files imported directly; profile-specific expansion; location replacement versus spring.config.additional-location; ConfigDataLocationNotFoundException and the optional: prefix (also valid on spring.config.import); spring.config.on-not-found=ignore; wildcard rules (one asterisk, last segment, */<filename> for files, alphabetical by absolute path, external directories only, config/*/ in the defaults); location groups separated by ;.
Trimmed: "must end in /" reworded to "should end in /" to match the page wording.

Method: documentation only; no commands were run.
