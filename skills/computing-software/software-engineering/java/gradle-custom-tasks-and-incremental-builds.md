---
id: computing-software.software-engineering.java.gradle-custom-tasks-and-incremental-builds
name: gradle-custom-tasks-and-incremental-builds
category: computing-software
field: software-engineering
product: java
tags: [java, java-gradle, gradle-custom-tasks, task-inputs-outputs, incremental-build, build-cache, cacheabletask]
level: advanced
status: docs-checked
description: "Write Gradle custom tasks with declared inputs and outputs so they are up-to-date and cacheable: typed task classes, @CacheableTask and @PathSensitive."
sources: ["https://docs.gradle.org/current/userguide/incremental_build.html", "https://docs.gradle.org/current/userguide/build_cache.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle custom tasks

A typed task class with annotated properties (shape follows the Gradle incremental build example):
```java
@CacheableTask
public abstract class ProcessTemplates extends DefaultTask {
    @Input  public abstract Property<TemplateEngineType> getTemplateEngine();
    @InputFiles @PathSensitive(PathSensitivity.RELATIVE) public abstract ConfigurableFileCollection getSourceFiles();
    @Nested public abstract TemplateData getTemplateData();      // not Serializable: annotate its own properties
    @OutputDirectory public abstract DirectoryProperty getOutputDir();
    @Inject public abstract FileSystemOperations getFs();

    @TaskAction public void processTemplates() { /* ... */ }
}
```

## Rules
1. Tell Gradle which properties are inputs and which are outputs. If a property affects the output, register it as an input or the task is wrongly considered up to date; do not register properties that do not affect the output (for example a compiler's `memoryMaximumSize`), or the task runs needlessly.
2. Incremental build does not work unless a task has at least one output; tasks usually have at least one input too. Unchanged inputs and outputs mark the task `UP-TO-DATE` and its actions are skipped.
3. Simple serializable values (String, an enum) take `@Input`; a collection of files takes `@InputFiles`; a single output directory takes `@OutputDirectory`; a value with nested input properties takes `@Nested`.
4. Non-deterministic tasks (different output for identical inputs) should not be set up for incremental build, as up-to-date checks will not work.
5. Custom task types are not cacheable by default. Opt in with `@CacheableTask`, which is not inherited by subclasses. Use `@DisableCachingByDefault` (with an optional reason) for tasks that gain nothing from caching, such as ones that only move files.
6. Cache keys include the task type and its classpath, output property names, annotated property values, and the classpath of the Gradle distribution, buildSrc and plugins.
7. Make inputs relocatable with `@PathSensitive` so a cached result can load into a different build directory, and cover this with integration tests (for example TestKit). For volatile inputs, configure input normalization.

## Verify
Run the task twice: the second run reports `UP-TO-DATE`. With `./gradlew --build-cache` after a clean, a cacheable task reports `FROM-CACHE`.

## Checked

Method: docs-checked 2026-11-09 against the Gradle user guide pages Incremental Build and Build Cache. The Writing Tasks page was only a navigation shell. Dropped unconfirmed claims (Kotlin DSL snippet, tasks.register laziness and provider wiring, configuration-cache advice, ExecOperations, afterEvaluate, environment-variable inputs, overlapping outputs, convention-plugin advice).
