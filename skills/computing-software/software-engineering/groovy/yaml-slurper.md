---
id: computing-software.software-engineering.groovy.yaml-slurper
name: yaml-slurper
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, yaml-slurper, groovy-yaml-toml]
level: practitioner
status: docs-checked
description: "Parse and emit YAML with the optional groovy-yaml module: YamlSlurper, YamlBuilder, null handling, anchors and aliases, and SnakeYAML differences."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-yaml/src/spec/doc/yaml-userguide.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YamlSlurper and YamlBuilder
- `groovy-yaml` is an optional module for converting between Groovy objects and YAML; its classes are in `groovy.yaml`. Because it is optional, add it to your build first.
- `YamlSlurper` parses YAML text or reader content into plain Groovy maps, lists and primitives; results conform to GPath expressions. A YAML `null` becomes Groovy `null`.
- It is built on the Jackson YAML backend. `parseText(...) as ServerConfig` and the Jackson-databinding methods (`parseTextAs`) read YAML into typed objects; standard Jackson annotations such as `@JsonProperty` and `@JsonFormat` are supported there.
- `YamlSlurper` does NOT resolve YAML anchors and aliases: an alias arrives as a plain string holding the anchor's name, and a merge key (`<<`) is left as a literal entry instead of merging anything. This is a long-standing limitation of the Jackson YAML backend.
- `YamlBuilder` creates YAML in builder style; `YamlBuilder.toYaml(object)` serializes a typed object using Jackson databinding.
- The guide also shows SnakeYAML used directly (declare `org.yaml:snakeyaml` as your own dependency if you do). With `SafeConstructor` it produces only maps, lists and scalars; it follows YAML 1.1 typing, so an untagged timestamp becomes a `java.util.Date` where `YamlSlurper` returns a `String`; input is capped at 3MB of code points by default and at most 50 aliases of non-scalar nodes, both changeable through `LoaderOptions`; a self-referential anchor builds a cyclic object graph that `toString()` and `JsonOutput.toJson` will not survive.

## Checked

2026-11-03. Confirmed against the YAML user guide (YamlSlurper, anchors and aliases, SnakeYAML comparison, YamlBuilder). Removed: the code snippet and self-check, the "3.0.?" version claim, the claim about `yes`/`no`/`1e3` coercions, and the generic advice about constructing arbitrary classes.

Method: documentation only; no commands were run.
