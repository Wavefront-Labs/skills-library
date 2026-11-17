---
id: computing-software.software-engineering.quarkus.quarkus-first-application
name: quarkus-first-application
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, getting-started, live-coding, dev-mode, rest, cdi]
level: intro
status: docs-checked
description: "Create a Quarkus REST app, run it in dev mode with live reload, add a CDI bean, write a @QuarkusTest, and package it as a fast-jar."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/getting-started.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create, run, test and package a first Quarkus application

## Bootstrap
Create the project with the page's create-app command using artifact id `getting-started` and the `rest` extension. It generates the Maven structure, `org.acme.GreetingResource` exposed on `/hello`, a unit test, a landing page at `http://localhost:8080`, example `Dockerfile` files for `native` and `jvm` in `src/main/docker`, and the application configuration file. The `pom.xml` imports `quarkus-bom` (so dependency versions can be omitted) and uses `quarkus-maven-plugin` for packaging and dev mode. Run `mvn --version` to confirm Maven uses the JDK you expect.

## Run in dev mode and live-code
Start dev mode (`quarkus:dev` runs Quarkus in development mode). Check it with `curl -w "\n" http://localhost:8080/hello`. Edit and save Java or resource files, refresh the browser, and the change applies with no restart; compile or deployment errors show on an error page. The Dev UI is at `http://localhost:8080/q/dev-ui/`. A debugger listens on port `5005`; pass `-Dsuspend` to wait for it to attach, or `-Ddebug=false` to disable it. Stop with `CTRL+C`.

## Add injection
Dependency injection is ArC (CDI-based), already a dependency of `quarkus-rest`. Create `GreetingService` annotated `@ApplicationScoped` with `greeting(String name)`, then in `GreetingResource` add `@Inject GreetingService service;` and a `@GET @Path("/greeting/{name}")` method returning `service.greeting(name)`. Check `curl -w "\n" http://localhost:8080/hello/greeting/quarkus` returns `hello quarkus`.

## Test
The generated build file has test dependencies `io.quarkus:quarkus-junit` and `io.rest-assured:rest-assured`. For Maven, set the Surefire plugin version (the default does not support JUnit) and its `systemPropertyVariables` `java.util.logging.manager=org.jboss.logmanager.LogManager` and `maven.home`. Annotate the test class with `@QuarkusTest` so the app starts before tests; use RestAssured `given().when().get("/hello").then().statusCode(200)`. Run `./mvnw test`, or run from the IDE after stopping the dev-mode app. Tests use port `8081` by default (RestAssured is auto-configured); change it with `quarkus.http.test-port`. To use another HTTP client, inject the URL with `@TestHTTPResource("/hello") URL testUrl;` (`String`, `URL` or `URI`). In dev mode, press `r` to run tests continuously.

## Package
Build with the build command; it produces `target/quarkus-app/quarkus-run.jar`, a fast-jar (dependencies in `quarkus-app/lib/`), run with `java -jar target/quarkus-app/quarkus-run.jar`. Deploy the whole `quarkus-app` directory. Stop dev mode first or you get a port conflict.

Verify: `curl -w "\n" http://localhost:8080/hello` prints `Hello from Quarkus REST`.

## Checked

2026-11-07. Read in full: getting-started.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the explicit `quarkus dev` / CLI create-app forms (shown only through includes not in the checked text).

Method: documentation only; no commands were run.
