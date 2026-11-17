---
id: computing-software.devops-ci-cd.gradle.gradle-daemon-lifecycle-and-jvm-args
name: gradle-daemon-lifecycle-and-jvm-args
category: computing-software
field: devops-ci-cd
product: gradle
tags: [gradle-daemon, jvmargs, idle-timeout, gradle-stop, daemon-logs]
level: practitioner
status: docs-checked
description: "Understand when the Gradle Daemon is reused, how JVM args affect it, and how to inspect, stop and configure it."
sources: ["https://docs.gradle.org/current/userguide/gradle_daemon.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle daemon lifecycle and jvm args

Each Gradle invocation starts a client JVM that connects to a compatible Daemon, or starts one. The client sends the build request and the Daemon runs the build, returning output over a local socket. It stays alive between builds, caching project data and benefiting from JVM optimisation. The docs recommend the Daemon for both developer machines and CI.

Reuse requires an exact match of Java home or version, JVM attributes and properties (`org.gradle.jvmargs`, `GRADLE_OPTS`) and Gradle version; otherwise a new Daemon (or a single-use one) starts. `-Xmx`, `-Xms`, `-Xbootclasspath` and `-ea` are fixed at JVM startup, and some system properties are immutable afterwards (`file.encoding`, `java.io.tmpdir`, `javax.net.ssl.*`). Without a stated maximum the Daemon uses up to 512MB of heap.

Lifecycle: a Daemon stops after 3 hours idle or when system memory is low. `gradle --stop` terminates all Daemons of the same Gradle version; others can be killed with PIDs from `jps`. `gradle --status` lists PIDs and IDLE or BUSY state for the current version.

Configuration:
- `org.gradle.daemon=true|false` in `gradle.properties` (project root or `GRADLE_USER_HOME`); `--daemon` / `--no-daemon` override per build; `-Dorg.gradle.daemon=false` in `GRADLE_OPTS` disables globally.
- `org.gradle.java.home` sets the Daemon JVM.
- `org.gradle.daemon.performance.enable-monitoring=false` turns off memory-leak monitoring (on by default).

Logs live in `~/.gradle/daemon/<gradle-version>/` as `daemon-<pid>.out.log`; logs older than 14 days are removed during cache cleanup, and an init script can change retention.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
