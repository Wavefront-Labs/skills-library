---
id: computing-software.software-engineering.quarkus.quarkus-integration-test
name: quarkus-integration-test
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, integration-test, failsafe, native-image, testing, containers]
level: advanced
status: docs-checked
description: "Test the built jar, native executable or container with @QuarkusIntegrationTest: failsafe setup, profile, debugging, container networks, and remote targets."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/getting-started-testing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing the built artifact with @QuarkusIntegrationTest

`@QuarkusIntegrationTest` launches the artifact produced by the Quarkus build and runs black-box tests against it: a jar is run as `java -jar ...`, a native image as `./application ...`, and a container image (built with `quarkus-container-image-jib`, `quarkus-container-image-docker` or `container-image-podman` plus `quarkus.container-image.build=true`) is run as a container, needing `docker` or `podman`. It supports the guide's features except injecting into tests.

## Setup
Run it in the integration test phase, not with `@QuarkusTest`: Maven needs `-DskipITs=false` and the `maven-failsafe-plugin` (goals `integration-test` and `verify`, system properties `native.image.path`, `java.util.logging.manager`, `maven.home`). Gradle uses the `quarkusIntTest` task with tests in `src/integrationTest/java` (or `kotlin`). Typical test: `@QuarkusIntegrationTest public class GreetingResourceIT extends GreetingResourceTest {}`. `@QuarkusTest` stays under Surefire / the `test` source set.

## Configuration
The app runs with the `prod` profile; change with `quarkus.test.integration-test-profile`. `src/test/resources/application.properties` test-specific settings do not work for integration tests. Callbacks for these tests need `quarkus.test.enable-callbacks-for-integration-tests=true`.

## Debugging
The app is a separate process, so pass JVM flags via `quarkus.test.arg-line`, for example `-Dquarkus.test.arg-line="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005"`; it waits for a debugger on port `5005`. Debug the test code itself normally (for Maven add `-Dmaven.failsafe.debug`).

## Containers and Dev Services
When the app runs as a container it joins a predictable container network, so Dev Services work out of the box. A custom `QuarkusTestResourceLifecycleManager` that starts extra containers should also implement `io.quarkus.test.common.DevServicesContext.ContextAware`, store `context.containerNetworkId()` in `setIntegrationTestContext`, and call `container.withNetworkMode(...)` if present. Testcontainers connection strings ignore that network, so rewrite the JDBC URL to use the container's network host and the unmapped port.

## Running against a live app
Set `quarkus.http.test-host` and `quarkus.http.test-port`, for example `./mvnw verify -Dquarkus.http.test-host=1.2.3.4 -Dquarkus.http.test-port=4321` or `./gradlew quarkusIntTest ...`. For TLS-only targets set `quarkus.http.test-ssl-enabled=true` and `quarkus.http.test-ssl-port`.

## AOT cache (JDK 25+)
Adding `-Dquarkus.package.jar.aot.enabled=true` produces `app.aot` next to the jar (for example `target/quarkus-app/app.aot`); run with `java -XX:AOTCache=app.aot -jar quarkus-run.jar`. Cache quality depends on how representative the tests are.

## Checked

2026-11-07. Read in full: getting-started-testing.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
