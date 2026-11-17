---
id: computing-software.data-engineering.apache-nifi.custom-properties-files
name: custom-properties-files
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, custom-properties, variable-registry, expression-language, nifi-properties]
level: practitioner
status: docs-checked
description: "Supply external property files to Expression Language via nifi.variable.registry.properties, with restart and cluster consistency rules."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom property files

`nifi.variable.registry.properties` takes a comma-separated list of property file paths. Rules from the admin and user guides:
- Restart NiFi after changing the list; updates are not picked up otherwise.
- Each custom property should have a distinct name so it is not overridden by existing environment properties, system properties or FlowFile attributes.
- Every node in a cluster should be configured with the same custom properties.

The Expression Language guide lists the lookup hierarchy for a name, returning the first match (null if none): FlowFile attribute, process group variables, the custom property files, NiFi JVM properties, then system environment variables.

The user guide says custom properties and variables remain supported for compatibility but will be removed in a future release, and recommends Parameters (`#{name}`), which support sensitive values.

Verify: a processor property of `${your.key}` resolves to the file value after restart.

## Checked

Confirmed against the NiFi administration guide (Custom Properties), the user guide (Custom Properties; Variables deprecation note) and the Expression Language guide (Expression Language Hierarchy).

Method: docs-only read of cited pages, 2026-11-08
