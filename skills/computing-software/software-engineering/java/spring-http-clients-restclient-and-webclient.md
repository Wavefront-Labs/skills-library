---
id: computing-software.software-engineering.java.spring-http-clients-restclient-and-webclient
name: spring-http-clients-restclient-and-webclient
category: computing-software
field: software-engineering
product: java
tags: [java, restclient, webclient, http-interface, http-timeouts, spring-boot, resttemplate]
level: practitioner
status: docs-checked
description: "Call HTTP APIs from Spring: RestClient (sync) and WebClient (reactive), declarative @HttpExchange interfaces, timeouts on the underlying client, error handling and observability."
sources: ["https://docs.spring.io/spring-framework/reference/integration/rest-clients.html", "https://docs.spring.io/spring-boot/reference/io/rest-client.html", "https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring HTTP clients: RestClient and WebClient

**Goal:** outbound HTTP calls with explicit timeouts, typed errors and tracing, using
the client that fits the app's programming model.

## Which client
| Client | Use |
|---|---|
| `RestClient` (6.1+) | blocking apps (Spring MVC, virtual threads); fluent replacement for RestTemplate |
| `WebClient` | reactive stacks (WebFlux) or many concurrent non-blocking calls |
| `RestTemplate` | deprecated since Spring Framework 7.0 in favour of `RestClient`, to be removed in a future version |
| `@HttpExchange` interfaces | declarative clients backed by either |

## RestClient with timeouts
```java
@Bean
RestClient billingClient(RestClient.Builder builder) {          // Boot-provided builder: observability + converters
    var settings = HttpClientSettings.defaults()                    // org.springframework.boot.http.client
        .withConnectTimeout(Duration.ofSeconds(2))
        .withReadTimeout(Duration.ofSeconds(5));
    return builder
        .baseUrl("https://billing.internal")
        .requestFactory(ClientHttpRequestFactoryBuilder.detect().build(settings))
        .defaultHeader("User-Agent", "orders-service")
        .build();
}

Invoice inv = billingClient.get().uri("/invoices/{id}", id)
    .retrieve()
    .onStatus(s -> s.value() == 404, (req, res) -> { throw new InvoiceNotFound(id); })
    .body(Invoice.class);
```
Boot also supports global `spring.http.clients.connect-timeout` / `read-timeout` properties for all auto-configured clients, and `spring.http.serviceclient.<group>.*` (`base-url`, timeouts) for HTTP Service clients.

## Declarative interfaces
```java
@HttpExchange("/invoices")
interface BillingApi {
    @GetExchange("/{id}") Invoice get(@PathVariable String id);
    @PostExchange Invoice create(@RequestBody NewInvoice body);
}
@Bean BillingApi billingApi(RestClient billingClient) {
    return HttpServiceProxyFactory.builderFor(RestClientAdapter.create(billingClient)).build()
        .createClient(BillingApi.class);
}
```

## WebClient
```java
Mono<Invoice> inv = webClient.get().uri("/invoices/{id}", id)
    .retrieve().bodyToMono(Invoice.class)
    .timeout(Duration.ofSeconds(5))
    .retryWhen(Retry.backoff(3, Duration.ofMillis(200)).filter(this::isTransient));
```
Avoid `.block()` on reactive threads; in MVC apps prefer RestClient.

## Errors and resilience
- `retrieve()` throws `HttpClientErrorException` (4xx) / `HttpServerErrorException` (5xx);
  map to domain exceptions with `onStatus`.
- Retry only idempotent calls; add circuit breaking with a resilience library around the client.
- Declare one client bean per downstream service and reuse it.

## Observability
Boot reports HTTP client metrics under the name `http.client.requests` (rename with `management.observations.http.client.requests.name`). Building with `RestClient.create()` bypasses Boot's auto-configuration and `RestClientCustomizer` beans.

## Verify
- [ ] Every client bean has connect and read timeouts.
- [ ] Tests stub the downstream (WireMock / MockRestServiceServer) including 404/500/timeout cases.

## Checked

Date: 2026-10-25. Documentation release: Spring Boot 4.1.2 and Spring Framework 7.0.10 (GitHub main documentation sources; releases of 2026-10-22).

Confirmed: RestClient since 6.1 and RestTemplate deprecation in 7.0; `RestClient.Builder` methods (`baseUrl`, `requestFactory`, `defaultHeader`), `onStatus`; `HttpClientSettings.defaults()`, `withConnectTimeout`, `withReadTimeout` and `ClientHttpRequestFactoryBuilder.detect().build(settings)`; `spring.http.clients.*` and `spring.http.serviceclient.*` properties; `@HttpExchange` / `@GetExchange` with `HttpServiceProxyFactory.builderFor(RestClientAdapter.create(...))`; `http.client.requests` metric name; `RestClient.create()` bypasses auto-configuration; Reactor `Retry.backoff`, `Mono.timeout` and `retryWhen` signatures in source.

Removed as unconfirmed: the `ClientHttpRequestFactorySettings` class and the `spring.http.client.*` property names (Boot 3.x), the claim that some clients wait indefinitely without timeouts, the Resilience4j name, the connection pooling remark, trace propagation header claim and the ".block() is an error" statement.

Method: documentation only; no commands were run.
