---
id: computing-software.software-engineering.spring-boot.actuator-info-and-sbom-endpoints
name: actuator-info-and-sbom-endpoints
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, info, infocontributor, git-properties, build-info, sbom, cyclonedx]
level: practitioner
status: docs-checked
description: "Populate the Actuator info endpoint with build, git, env, java, os, process and ssl contributors, write InfoContributors, and expose SBOMs through the sbom endpoint."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `info` endpoint merges all `InfoContributor` beans. Each is toggled by `management.info.<id>.enabled`; `management.info.defaults.enabled=false` disables every one that is on by default.
- `build` (on by default): needs `META-INF/build-info.properties`, giving a `BuildProperties` bean; Maven and Gradle plugins can generate it.
- `git` (on by default): needs a `git.properties` at the classpath root (auto-configures `GitProperties`). Default exposes `git.branch`, `git.commit.id`, `git.commit.time` if present; `management.info.git.mode: "full"` shows all; `management.info.git.enabled: false` removes it.
- `env` (off by default): exposes `Environment` properties starting with `info.`.
- `java`, `os`, `process` (off by default): runtime, OS and process information.
- `ssl` (off by default; needs an SSL bundle): certificate information.
Enable the off-by-default ones with `management.info.<id>.enabled=true`.

Custom data with `env`:
```yaml
info:
  app:
    encoding: "UTF-8"
    java:
      source: "17"
      target: "17"
```
Values can be build-time expanded, for Maven `"@project.build.sourceEncoding@"`, `"@java.version@"`.

Custom contributor: register a bean implementing `InfoContributor`. A contribution of key `example` with `key: value` appears as `{"example": {"key": "value"}}`.

SBOM: the `sbom` endpoint exposes an SBOM named "application"; CycloneDX is auto-detected. Other formats: `management.endpoint.sbom.application.location` (for example `classpath:sbom.json`); media type of CycloneDX, SPDX and Syft is detected, override with `management.endpoint.sbom.application.media-type`. More SBOMs:
```yaml
management:
  endpoint:
    sbom:
      additional:
        system:
          location: "optional:file:/system.spdx.json"
          media-type: "application/spdx+json"
```
`optional:` prevents startup failure if the file is missing.

## Checked

2026-11-07

Read endpoints.adoc in full (cited Actuator endpoints page); used Application Information (auto-configured contributors table, custom info, git, build, java/os/process/ssl, custom InfoContributor) and Software Bill of Materials sections. The MyInfoContributor include example was not opened.
Confirmed: contributor IDs build, env, git, java, os, process, ssl with prerequisites; management.info.<id>.enabled; env/java/os/process/ssl disabled by default and build/git enabled by default; management.info.defaults.enabled; git.properties auto-configuring GitProperties, default git.branch / git.commit.id / git.commit.time, git.mode full, git.enabled false; build-info.properties and Maven/Gradle plugin generation; info.* env example and the @...@ build-time expansion for Maven; example entry JSON; sbom endpoint "application" SBOM, CycloneDX auto-detection, application.location classpath:sbom.json, media-type override and auto-detection for CycloneDX/SPDX/Syft, the `additional` example and the optional: prefix.
Nothing trimmed.

Method: documentation only; no commands were run.
