---
id: computing-software.software-engineering.spring-boot.configtree-secrets
name: configtree-secrets
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, configtree, kubernetes, secrets, configmap, docker-secrets, volume-mount]
level: practitioner
status: docs-checked
description: "Import volume-mounted files such as Kubernetes ConfigMaps, Secrets and Docker secrets as properties using the configtree: prefix in spring.config.import."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment variables have drawbacks for secrets. Cloud platforms can mount config into volumes, in two patterns: one file with a full property set (import it directly with `spring.config.import`), or a directory tree where each file name is the key and its contents the value (use the `configtree:` prefix).

Given a mounted tree:
```
etc/
  config/
    myapp/
      username
      password
```
```yaml
spring:
  config:
    import: "optional:configtree:/etc/config/"
```
This exposes `myapp.username` and `myapp.password`. Folder and file names form the property name. To get plain `username` and `password`, import `optional:configtree:/etc/config/myapp`. A file named `myapp.username` in `/etc/config` also maps correctly.

Wildcard: a `configtree:` location ending in `/*/` imports every immediate child as a config tree. With `dbconfig/db/{username,password}` and `mqconfig/mq/{username,password}` under `/etc/config`, importing `optional:configtree:/etc/config/*/` adds `db.username`, `db.password`, `mq.username`, `mq.password`. Wildcard directories load alphabetically; list each location separately for a different order.

Docker swarm secrets: a secret named `db.password` mounted at `/run/secrets/` is made available with
`spring.config.import: "optional:configtree:/run/secrets/"`.

Values can be bound to `String` or `byte[]`.

## Checked

2026-11-07

Read the Importing Configuration Trees / Configuration Trees section of external-config.adoc (docs-repo source of the cited Externalized Configuration page) (volume-mount patterns, myapp example, wildcard and Docker secrets parts); the import section was read for the configtree: prefix. The page has no include-code snippets here.
Confirmed: the two volume-mount patterns and which one uses the configtree: prefix; etc/config/myapp tree and import "optional:configtree:/etc/config/" giving myapp.username and myapp.password; importing /etc/config/myapp for plain names; dotted filename mapping; String and byte[] binding TIP; the /*/ wildcard with the dbconfig/mqconfig example giving db.* and mq.*; alphabetical wildcard order and the list-separately advice; Docker swarm secret db.password at /run/secrets/.
Trimmed: "poor fit" softened to the page's "has drawbacks, especially if the value is supposed to be kept secret".

Method: documentation only; no commands were run.
