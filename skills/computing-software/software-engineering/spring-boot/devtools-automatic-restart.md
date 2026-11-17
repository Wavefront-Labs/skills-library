---
id: computing-software.software-engineering.spring-boot.devtools-automatic-restart
name: devtools-automatic-restart
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, devtools, restart, classloader, trigger-file, spring-devtools-properties, hot-reload]
level: practitioner
status: docs-checked
description: "Add spring-boot-devtools and tune automatic restart: triggering, exclusions, extra paths, trigger file, disabling, restart classloader customization and known limits."
sources:
  - https://docs.spring.io/spring-boot/reference/using/devtools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dependency: Maven `org.springframework.boot:spring-boot-devtools` with `<optional>true</optional>`; Gradle `developmentOnly("org.springframework.boot:spring-boot-devtools")`. Optional/`developmentOnly` stops devtools applying transitively to other modules. Repackaged archives do not contain devtools by default.

Devtools is disabled automatically for a fully packaged application (`java -jar` or a special classloader). Force with `-Dspring.devtools.restart.enabled=true` (never in production, a security risk); disable by excluding the dependency or `-Dspring.devtools.restart.enabled=false`.

Restart: applications restart whenever classpath files change; any classpath directory entry is monitored. The only trigger is updating the classpath, so files must be recompiled: Eclipse saving a file; IntelliJ IDEA `Build -> Build Project`; with build plugins `mvn compile` or `gradle build`. With the Maven/Gradle plugins leave `forking` enabled, otherwise the isolated classloader is not created. With JRebel, restarts are disabled in favour of class reloading. It needs the shutdown hook (not `setRegisterShutdownHook(false)`), wraps any custom `ResourceLoader`, and is unsupported with AspectJ weaving.

How it works: unchanging classes (third-party jars) sit in a base classloader; your project classes in a restart classloader that is discarded and recreated on restart, so restarts are faster than cold starts.

Settings:
- Condition delta report is logged each restart; disable with `spring.devtools.restart.log-condition-evaluation-delta: false`.
- Changes in `/META-INF/maven`, `/META-INF/resources`, `/resources`, `/static`, `/public`, `/templates` do not restart (they live reload). Replace with `spring.devtools.restart.exclude: "static/**,public/**"`, or keep defaults and add via `spring.devtools.restart.additional-exclude`.
- `spring.devtools.restart.additional-paths` watches non-classpath paths.
- `spring.devtools.restart.enabled=false` in properties still creates the restart classloader; to fully disable set the System property before `SpringApplication.run(...)`.
- Trigger file: `spring.devtools.restart.trigger-file: ".reloadtrigger"` (name only, must be on the classpath, for example `src/main/resources/.reloadtrigger`); a restart occurs only if devtools detected something to do.
- File watcher: `spring.devtools.restart.poll-interval: "2s"` and `quiet-period: "1s"` if changes are missed.

Classloading problems (notably multi-module): disable restart to diagnose, then customize with `META-INF/spring-devtools.properties` keys prefixed `restart.include.` (pull into restart classloader) or `restart.exclude.` (push to base), each a regex on the classpath, unique keys:
```properties
restart.exclude.companycommonlibs="/mycorp-common-[\\w\\d-\\.]/(build|bin|out|target)/"
restart.include.projectcommon="/mycorp-myproj-[\\w\\d-\\.]+\\.jar"
```
By default open IDE projects use the restart classloader and regular `.jar` files the base. Limitation: standard `ObjectInputStream` deserialization misbehaves; use `ConfigurableObjectInputStream` with `Thread.currentThread().getContextClassLoader()`.

## Checked

2026-11-07

Read devtools.adoc (docs-repo source of the cited Developer Tools page) in full (448 lines), using the intro, Diagnosing Classloading Issues and Automatic Restart sections with all subsections (condition delta, excluding resources, additional paths, disabling, trigger file, restart classloader, known limitations). The MyApplication include example for disabling restart was not opened; the claim rests on the page prose.
Confirmed: Maven optional / Gradle developmentOnly dependency and the transitive-application TIP; devtools disabled for java -jar or special classloaders and the spring.devtools.restart.enabled true/false system property with the production-security warning; repackaged archives exclude devtools; classpath-directory monitoring and the Eclipse, IntelliJ Build Project, mvn compile and gradle build triggers; forking must stay enabled; JRebel disables automatic restart; shutdown-hook, ResourceLoader wrapping and AspectJ weaving notes; the two-classloader Restart vs Reload explanation; log-condition-evaluation-delta; the default no-restart resource paths (live reload instead), exclude replacing and additional-exclude adding; additional-paths; restart.enabled in properties still creating the classloader versus the System property before run(...); trigger-file (name only, on classpath, .reloadtrigger example, restart only if something to do); poll-interval 2s and quiet-period 1s example; spring-devtools.properties restart.include / restart.exclude regex entries, unique keys, the two example lines; default classloader assignment; ObjectInputStream limitation with ConfigurableObjectInputStream.
Nothing trimmed.

Method: documentation only; no commands were run.
