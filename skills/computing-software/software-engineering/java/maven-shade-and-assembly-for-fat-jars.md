---
id: computing-software.software-engineering.java.maven-shade-and-assembly-for-fat-jars
name: maven-shade-and-assembly-for-fat-jars
category: computing-software
field: software-engineering
product: java
tags: [java, java-maven, maven-shade-plugin, maven-assembly-plugin, fat-jar, uber-jar, relocation, service-files-transformer]
level: practitioner
status: docs-checked
description: "Build executable uber-jars with maven-shade-plugin: Main-Class manifest, relocate conflicting packages, merge META-INF/services, exclude signatures."
sources: ["https://maven.apache.org/plugins/maven-shade-plugin/", "https://maven.apache.org/plugins/maven-assembly-plugin/", "https://docs.spring.io/spring-boot/maven-plugin/packaging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shade and assembly for fat JARs

Use for CLI tools, agents, Lambda/function packages. Spring Boot apps should use `spring-boot-maven-plugin` `repackage` goal (nested jars), not shade.

## maven-shade-plugin
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-shade-plugin</artifactId>
  <version>3.6.2</version>
  <executions><execution>
    <phase>package</phase><goals><goal>shade</goal></goals>
    <configuration>
      <createDependencyReducedPom>false</createDependencyReducedPom>
      <transformers>
        <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
          <mainClass>com.acme.Main</mainClass>
        </transformer>
        <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
      </transformers>
      <filters><filter>
        <artifact>*:*</artifact>
        <excludes><exclude>META-INF/*.SF</exclude><exclude>META-INF/*.DSA</exclude><exclude>META-INF/*.RSA</exclude></excludes>
      </filter></filters>
      <relocations><relocation>
        <pattern>com.google.common</pattern><shadedPattern>com.acme.shaded.guava</shadedPattern>
      </relocation></relocations>
    </configuration>
  </execution></executions>
</plugin>
```
- `ServicesResourceTransformer` merges multiple implementations of the same interface in `META-INF/services/` into one service entry (and relocates the implementation class names).
- Relocation creates a private copy of dependency bytecode, avoiding class-loading conflicts when the uber jar is reused as a dependency of another project.
- Signature files (`META-INF/*.SF`, `*.DSA`, `*.RSA`) from signed dependencies are excluded with a `*:*` filter, as in the plugin's include/exclude example.

## maven-assembly-plugin
The Assembly Plugin combines project output into a single distributable archive that also contains dependencies, modules, site documentation and other files; use a custom descriptor for distribution zips or tarballs (`bin/`, `lib/`, `conf/`).

## Gotchas
- `ApacheLicenseResourceTransformer` prevents duplicate licence files and `ApacheNoticeResourceTransformer` assembles an appropriate `NOTICE`, since licences such as Apache 2 require notices to be preserved.
- `minimizeJar` respects classes explicitly included in a filter (since 1.6); an include filter for an artifact implicitly excludes all non-specified classes unless `excludeDefaults` is false. Classes reached only by reflection may need explicit includes.

## Verify
`java -jar target/app.jar` on a clean machine; `jar tf` lists the jar contents so you can confirm merged `META-INF/services` entries and no `*.SF` files.

## Checked

Method: docs-checked 2026-11-09 against the maven-shade-plugin index, resource-transformers, class-relocation, includes-excludes, executable-jar and shade-mojo pages, the maven-assembly-plugin index, and the Spring Boot Maven plugin packaging page. Dropped unconfirmed claims (jar-with-dependencies limits, Multi-Release manifest entry, module-info, Docker layering).
