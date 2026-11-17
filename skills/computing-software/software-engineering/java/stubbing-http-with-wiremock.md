---
id: computing-software.software-engineering.java.stubbing-http-with-wiremock
name: stubbing-http-with-wiremock
category: computing-software
field: software-engineering
product: java
tags: [java, wiremock, http-stubbing, fault-injection, integration-tests, contract-stubs, java-testing]
level: practitioner
status: docs-checked
description: "Test HTTP integrations with WireMock: JUnit 5 extension, request matching, response templating, faults and delays for timeout tests, request verification and recording."
sources: ["https://wiremock.org/docs/junit-jupiter/", "https://wiremock.org/docs/stubbing/", "https://wiremock.org/docs/simulating-faults/", "https://wiremock.org/docs/verifying/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stubbing HTTP with WireMock

**Goal:** fast, deterministic tests of code that calls HTTP APIs, including the
failure modes real dependencies produce.

## JUnit 5 setup
```java
@WireMockTest                                      // random port, HTTP only, by default
class BillingClientTest {
    @Test
    void fetchesInvoice(WireMockRuntimeInfo wm) {
        stubFor(get(urlPathEqualTo("/invoices/42"))
            .withHeader("Authorization", matching("Bearer .+"))
            .willReturn(okJson("""{"id": "42", "total": 1999}""")));

        var client = new BillingClient("http://localhost:" + wm.getHttpPort(), Duration.ofSeconds(1));
        assertThat(client.invoice("42").total()).isEqualTo(1999);

        verify(getRequestedFor(urlPathEqualTo("/invoices/42")));
    }
}
```
With Spring Boot, point the client's base URL property at WireMock via
`@DynamicPropertySource` (a static method that adds properties to the Spring Environment) or a `@RegisterExtension WireMockExtension` field.

## Matching
`urlEqualTo` (exact incl. query) vs `urlPathEqualTo` + `withQueryParam`; `withRequestBody(equalToJson(..., true, true))`
(ignore array order, extra fields); `matchingJsonPath(...)` with a JSONPath expression. Priorities
(`atPriority(1)`) resolve overlapping stubs; unmatched requests return 404 and WireMock logs a
"near miss" diff - read it first when a test fails.

## Failure modes (where the value is)
```java
stubFor(get("/slow").willReturn(ok().withFixedDelay(3_000)));              // client timeout path
stubFor(get("/reset").willReturn(aResponse().withFault(Fault.CONNECTION_RESET_BY_PEER)));  // reliable on Unix-like OSs; may behave differently on Windows
stubFor(get("/garbage").willReturn(aResponse().withFault(Fault.MALFORMED_RESPONSE_CHUNK)));
stubFor(get("/busy").willReturn(aResponse().withStatus(429)));
```
Stateful scenarios test retries:
```java
stubFor(get("/flaky").inScenario("retry").whenScenarioStateIs(STARTED)
    .willReturn(aResponse().withStatus(500)).willSetStateTo("recovered"));
stubFor(get("/flaky").inScenario("retry").whenScenarioStateIs("recovered").willReturn(ok()));
```

## Templating and recording
`.withTransformers("response-template")` (or global templating via a startup option) to echo request data,
e.g. `{{request.path.[0]}}`. Record real traffic once with `startRecording(url)`
to bootstrap stubs, then review and trim them.

## Standalone / Docker
`docker run -it --rm -p 8080:8080 wiremock/wiremock` (official image since WireMock 2.31.0; it accepts the same command line arguments as the standalone JAR, and mappings are listed at `/__admin/mappings`) for local dev or non-JVM tests.

## Gotchas
- Stubs prove your client matches your assumptions, not the real API; pair with contract tests.
- Reset between tests (the extension does per test); static stubs leak across tests otherwise.

## Verify
- [ ] Tests cover success, 4xx, 5xx, timeout and connection reset for each external call.
- [ ] Verification asserts the request your code sends (headers, body), not just the response handling.

## Checked

Date: 2026-10-25. Documentation release: WireMock documentation site sources (GitHub main, last commit 2026-10-21; WireMock 3.13.2 is the latest GitHub release).

Confirmed: `@WireMockTest` runs one server on a random HTTP-only port by default and stubs are reset before each test; `WireMockRuntimeInfo.getHttpPort()`; `Fault` values `CONNECTION_RESET_BY_PEER` (documented as reliable only on Unix-like systems), `MALFORMED_RESPONSE_CHUNK`, `EMPTY_RESPONSE`, `RANDOM_DATA_THEN_CLOSE`; `withFixedDelay`; scenarios (`inScenario`, `whenScenarioStateIs`, `willSetStateTo`, `Scenario.STARTED`); `atPriority`; 404 for unmatched requests; `response-template` transformer and `{{request.path.[0]}}`; `startRecording`; official Docker image since 2.31.0; `equalToJson` ignore flags.

Removed as unconfirmed: `httpPort = 0`, `getHttpBaseUrl()`, the `serverError()` helper, the Retry-After header, the Testcontainers module name, the JSONPath filter expression and the "recorded stubs over-match headers" remark.

Method: documentation only; no commands were run.
