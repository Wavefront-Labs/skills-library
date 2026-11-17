---
id: computing-software.web-development.micronaut.micronaut-cli-create-projects-and-code
name: micronaut-cli-create-projects-and-code
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, cli, mn, create-app, features, micronaut-cli-yml, code-generation]
level: intro
status: docs-checked
description: "Use the mn CLI to create Micronaut apps with language, test, build and feature flags, run them, and generate beans, controllers and clients that honor micronaut-cli.yml."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cli/createProject.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cli/commands.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cli/features.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cli/proxy.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/quickStart/creatingServer.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut CLI (`mn`): create projects and generate code

## Create a project

Commands: `create-app` (HTTP server), `create-cli-app`, `create-function-app` (AWS by default; add `--features azure-function` or `google-cloud-function` for others), `create-messaging-app` (Kafka by default; `--features rabbitmq` to switch), `create-grpc-app`.

| Flag | Meaning |
|---|---|
| `-l`, `--lang` | `java` (default), `groovy`, `kotlin` |
| `-t`, `--test` | `junit` (default), `spock` |
| `-b`, `--build` | `gradle`, `gradle_kotlin`, `maven` (default `gradle` for java/groovy, `gradle_kotlin` for kotlin) |
| `-f`, `--features` | comma-separated, or repeat `-f` |
| `-i`, `--inplace` | generate in the current directory (name optional) |

```bash
mn create-app my-project --features mongo-reactive,security-jwt --build maven
mn create-app --list-features        # features differ per create command
```

Without the CLI, use https://launch.micronaut.io or `curl https://launch.micronaut.io/hello-world.zip -o hello-world.zip` (add `?build=maven` for Maven). Generated projects include Gradle/Maven wrappers.

Run: `./gradlew run` (Gradle) or `./mvnw mn:run` (Maven).

## micronaut-cli.yml

Generated files record choices:

```yaml
applicationType: default
defaultPackage: com.example
testFramework: junit
sourceLanguage: java
buildTool: gradle
features: [annotation-api, app-name, application, gradle, http-client, java, junit, logback, netty-server, shade, yaml]
```

All code-generation commands honor it, and some commands appear only when a feature is listed (e.g. `create-kafka-listener` needs `kafka`). You may edit values (e.g. `testFramework: spock`), but you must add the matching dependencies yourself.

## Generate code (inside a project)

Each accepts `-l/--lang` and `-f/--force`:

```bash
mn create-bean EmailService          # singleton, no test
mn create-job UpdateFeeds --lang groovy   # *Job, @Scheduled, no test
mn create-controller Book            # *Controller plus a test using an HTTP client
mn create-client Book                # *Client interface, no test
mn create-websocket-server MyChat    # *Server
mn create-websocket-client MyChat    # *Client
mn create-command print              # picocli *Command plus test (CLI projects)
```

`mn -h` lists context-dependent commands; `feature-diff` and `create-test` also exist.

## Behind a proxy

Pass JVM options in `MN_OPTS`; profile dependencies resolve over HTTPS so host/port use `https.`, user/password use `http.`:

```bash
export MN_OPTS="-Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=3128 -Dhttp.proxyUser=test -Dhttp.proxyPassword=test"
```

## Hello World check

A controller from the quick start: `@Controller("/hello")` with `@Get(produces = MediaType.TEXT_PLAIN)` returning `"Hello World"`; `curl http://localhost:8080/hello` returns `Hello World`.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
