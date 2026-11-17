---
id: computing-software.web-development.micronaut.micronaut-run-server-and-port
name: micronaut-run-server-and-port
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, running-server, specific-port, embedded-server, micronaut-test]
level: intro
status: docs-checked
description: "Start a Micronaut HTTP server from a main class, test it with EmbeddedServer, and set a fixed or random listening port."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/runningServer.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/runningSpecificPort.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run a Micronaut server and choose its port

Goal: boot the HTTP server, exercise it from a test, and control the port.

## Start the application

Create an `Application` class with a `main` method that calls `Micronaut.run`:

```java
public class Application {
    public static void main(String[] args) {
        Micronaut.run(Application.class);
    }
}
```

## Test it with EmbeddedServer

Annotate the test with `@MicronautTest`, inject the `EmbeddedServer` and an HTTP client, and call the controller:

```java
@MicronautTest
public class HelloControllerSpec {

    @Inject
    EmbeddedServer server; // provides the URL of the server under test, on a random port

    @Inject
    @Client("/")
    HttpClient client;

    @Test
    void testHelloWorldResponse() {
        String response = client.toBlocking()
                .retrieve(HttpRequest.GET("/hello"));
        assertEquals("Hello World", response);
    }
}
```

`retrieve` returns the controller response as a `String`. In the Spock variant the `@AutoCleanup` annotation stops the `EmbeddedServer` when the specification completes.

## Port rules

- With no explicit port the server uses 8080, unless the app runs under the `test` environment, where the port is random. A test class's context adds the `test` environment automatically.
- Fixed port in configuration:

```yaml
micronaut:
  server:
    port: 8086
```

- The same setting can come from an environment variable, e.g. `MICRONAUT_SERVER_PORT=8086`.
- Random port: set `micronaut.server.port` to `-1`.

## Gotcha

An explicit port can make tests fail when several servers start at the same time on that port. Put a random port (`-1`) in the test environment configuration to avoid this.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
