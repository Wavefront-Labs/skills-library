---
id: computing-software.software-engineering.clojure.containerising-clojure-uberjars-and-jvm-flags
name: containerising-clojure-uberjars-and-jvm-flags
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, docker, container, uberjar, tools-build, dockerfile, multi-stage, deployment, deploy-docker-jvm, clojure-deployment]
level: practitioner
status: docs-checked
description: "Build a Clojure uberjar with tools.build (clj -T:build uber) and package it with a multi-stage, non-root Dockerfile following Docker's best-practice guidance."
sources: ["https://clojure.org/guides/tools_build", "https://docs.docker.com/build/building/best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uberjar and Docker image

**Goal:** a reproducible, small container built from a tools.build uberjar.

## Build the uberjar (tools.build)
- A build is a program written in Clojure and run as a tool: `clj -T:build uber`. The `:build` alias in
  deps.edn depends on `io.github.clojure/tools.build` (git tag and sha) with `:ns-default build`; the guide
  assumes Clojure CLI 1.10.3.933 or higher.
- build.clj requires `clojure.tools.build.api` as `b`, defines `class-dir` (`target/classes`) and a `basis`
  as a `delay` around `(b/create-basis {:project "deps.edn"})`.
- `uber` cleans, runs `b/copy-dir` for `src` and `resources` into `class-dir`, runs `b/compile-clj` on the main
  namespace, then `b/uber` with `:main`. The main namespace needs `(:gen-class)` and `-main`.
- `compile-clj` compiles transitively; dynamically or optionally loaded namespaces may need listing explicitly.
- Output such as `target/lib1-0.1.0-standalone.jar` runs with `java -jar`.

## Dockerfile (illustrative template, not taken from the guides)
```dockerfile
FROM clojure:temurin-21-tools-deps AS build        # pick a current tag
WORKDIR /app
COPY deps.edn build.clj ./
COPY src ./src
COPY resources ./resources
RUN clojure -T:build uber

FROM eclipse-temurin:21-jre
RUN useradd -r app
USER app
COPY --from=build /app/target/app.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```
From Docker's best practices:
- Multi-stage builds reduce the final image size; use one image for build/test and a typically slimmer one
  for production, built from a trusted, minimal base.
- If a service can run without privileges, use `USER` to switch to a non-root user (consider an explicit
  UID/GID).
- Use a `.dockerignore` (gitignore-like patterns) to exclude irrelevant files.
- Tags are mutable; pin an image to a digest for supply-chain integrity (Dependabot with
  `package-ecosystem: "docker"` can update pins).
- Use the exec/JSON-array form for CMD and ENTRYPOINT; `exec` in a helper script makes the application PID 1.

## Self-check
Run `clj -T:build uber`, then `java -jar` the output, then build the image and confirm it runs as non-root.

## Checked
Method: 2026-11-08 read clojure.org/guides/tools_build and docs.docker.com/build/building/best-practices. Removed unsupported claims from v1: MaxRAMPercentage/ExitOnOutOfMemoryError guidance, SIGTERM shutdown hooks, health endpoints, AppCDS/CRaC/jlink, the dependency-layer caching trick (`clojure -P`), JAVA_TOOL_OPTIONS and the --memory self-check. The Dockerfile was not built; its image tags are examples only. The jar file name in the Dockerfile must match your build.clj output.
