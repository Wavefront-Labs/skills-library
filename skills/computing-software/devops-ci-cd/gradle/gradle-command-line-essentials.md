---
id: computing-software.devops-ci-cd.gradle.gradle-command-line-essentials
name: gradle-command-line-essentials
category: computing-software
field: devops-ci-cd
product: gradle
tags: [command-line, task-selection, exclude-task, continue, dependency-insight, console, warning-mode]
level: intro
status: docs-checked
description: "Select, exclude, preview and diagnose Gradle tasks from the command line with the common flags and reporting commands."
sources: ["https://docs.gradle.org/current/userguide/command_line_interface.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle command line essentials

Task selection: `gradle :task` runs a task in the root project; `gradle sub:task` or `gradle :sub:task` targets a subproject; `gradle task` from the root runs matching tasks in all subprojects. Tasks run in the order listed, subject to dependencies (`gradle clean build`). Task options follow the task name (`--exampleOption=value`); use `--` before a task name that clashes with a built-in option. `--tests` is a filter added by Java test filtering.

Abbreviations: unique prefixes (`gradle che`) and camel-case patterns (`gradle mAL:cT` matches `:my-awesome-library:compileTest`) work, also with `-x`. Use `--info` or `--debug` to see how they expanded.

Control flags:
- `-x <task>` / `--exclude-task` skips a task and its otherwise-unneeded dependencies.
- `--rerun-tasks` ignores up-to-date checks for all tasks; `--rerun` reruns one task.
- `--continue` runs every task whose dependencies succeeded and reports all failures at the end.
- `--offline`; `-U` / `--refresh-dependencies`.
- `-m` / `--dry-run` shows what would run; `--task-graph` (since 9.1.0) prints the graph; `-t` / `--continuous` reruns on input changes.
- `-q`, `-w`, `-i`, `-d` set log level; `-s` / `-S` print stacktraces; `--scan` creates a Build Scan.
- `--console=(auto,plain,colored,rich,verbose)`; `--warning-mode=(all,fail,none,summary)` (default summary); `--non-interactive` for CI.
- `-Pname=value` sets a project property, `-Dname=value` a JVM system property.

Reporting: `gradle tasks [--all] [--group=...]`, `gradle help --task <name>`, `gradle dependencies`, `gradle dependencyInsight --dependency <spec> --configuration compileClasspath`, `gradle buildEnvironment`, `gradle projects`, `gradle properties --property <name>`.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
