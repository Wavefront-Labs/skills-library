---
id: computing-software.software-engineering.java.annotation-processors-and-compile-time-codegen
name: annotation-processors-and-compile-time-codegen
category: computing-software
field: software-engineering
product: java
tags: [java, java-reflection, annotation-processor, javax-annotation-processing, compile-time-codegen, gradle-incremental]
level: advanced
status: docs-checked
description: "Write annotation processors against the Processor contract (rounds, claiming, robustness) and make them Gradle-incremental; wire annotationProcessor and Maven compilerArgs."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.compiler/javax/annotation/processing/Processor.html", "https://docs.gradle.org/current/userguide/java_plugin.html#sec:java_compile_avoidance", "https://maven.apache.org/plugins/maven-compiler-plugin/examples/pass-compiler-arguments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotation processors

## The Processor contract (JDK 21 Javadoc)
- Processing runs in a sequence of rounds. A processor asked to process in one round is asked again in later rounds, including the last, even with no annotations to process. Files generated in a round feed the next one.
- A processor needs a public no-argument constructor. The tool calls `init(ProcessingEnvironment)`, then `getSupportedAnnotationTypes`, `getSupportedOptions` and `getSupportedSourceVersion` (once per run, not per round), then `process` as needed. No new processor object is created per round.
- `process(annotations, roundEnv)` returns whether it claims the annotation interfaces. Which processors run depends on the annotations present on the root elements, what each processor supports and whether earlier ones claimed them.
- A processor supporting `"*"` that returns `true` claims every annotation; a universal processor doing validity checks should return `false` so other checkers still run.
- Annotations wrapped in a container annotation are not "present". For repeatable annotations, list both the repeatable and the container annotation interface as supported.
- Raising an error lets the current round finish and the next round report the error. Throw an uncaught exception only when no error recovery or reporting is feasible.
- Robust processors are orthogonal (output not dependent on other inputs), consistent, commutative (A then B equals B then A) and independent of other processors' output.
- Multi-threaded access to environmental resources is not required to be supported.
- Extending `AbstractProcessor` is the convenient way to implement the interface. Writing files is governed by the `Filer` interface.

## Wiring the build
- Maven: extra javac arguments go in the compiler plugin's `compilerArgs`, one `<arg>` per argument (the cited page's example is `-verbose` and `-Xlint:all,-options,-path`).
- Gradle: the `annotationProcessor` configuration holds processors used when compiling the main source; the java plugin also defines a per-source-set equivalent for test sources.
- For javac processor flags (`-proc:none|only|full`, `-Xlint:processing`), see `javac-lint-flags-and-release-option`.

## Gradle incremental annotation processing
- Since Gradle 4.7. Processors must opt in or they trigger a full recompilation. `--info` shows which processors cause full recompiles.
- Register in `META-INF/gradle/incremental.annotation.processors`, one line per processor: `fully.qualified.Name,isolating` (category is case-insensitive; `aggregating` and `dynamic` also exist). `dynamic` processors report their real type at runtime via `getSupportedOptions()` (for example `org.gradle.annotation.processing.aggregating`).
- Isolating processors decide per annotated element from information reachable from its AST and must give exactly one originating element per generated file, otherwise Gradle recompiles everything. If decisions combine unrelated elements, mark the processor aggregating.
- Both categories: only CLASS or RUNTIME retention annotations are readable; parameter names only with `-parameters`; generate files through the Filer API only; no compiler-specific APIs such as `com.sun.source.util.Trees`; `Filer#createResource` locations must be `CLASS_OUTPUT`, `SOURCE_OUTPUT` or `NATIVE_HEADER_OUTPUT`.
- Incremental processing is off when a custom executable or javaHome is set on the compile task.

## Self-check
- [ ] A processor registered as `isolating` that reads an unrelated element fails the "decisions from the annotated type only" rule above.

## Checked

Confirmed on the JDK 21 Processor Javadoc, the Gradle Java plugin page and the Maven pass-compiler-arguments page. Removed because the pages do not state them: the sample processor code and Filer usage details, `META-INF/services` registration and `@AutoService`, Maven `annotationProcessorPaths` and the JDK 23 default change, Lombok and MapStruct ordering, IDE settings, and the `-XprintRounds` check.

Method: docs-only read of cited pages, 2026-11-08
