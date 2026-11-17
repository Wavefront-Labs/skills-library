---
id: computing-software.messaging-and-integration.apache-camel.circuit-breaker
name: circuit-breaker
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, circuit-breaker, resilience4j, fallback, fault-tolerance]
level: practitioner
status: docs-checked
description: "Camel Circuit Breaker EIP: Resilience4j or Fault Tolerance, states, onFallback, inheritErrorHandler and response exchange properties."
sources:
  - https://camel.apache.org/components/next/eips/circuitBreaker-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Circuit Breaker

Implementations: Resilience4j via `resilience4jConfiguration`, or MicroProfile Fault Tolerance via `faultToleranceConfiguration`.

Options: `configuration` (named config), `inheritErrorHandler` (default `false`, so Camel error handling is off inside the breaker), `onFallback`, `outputs` (required steps), `disabled` (default false).

States: Closed (normal), Open (fail fast), Half-Open (after a short period in Open, an operation is attempted and the outcome moves it to Open or Closed).

`onFallback` runs when the call fails, times out, or is rejected because the breaker is open or the bulkhead is full. Its output becomes the EIP output; otherwise the output is whatever the steps produce. Steps receive the body unchanged.

Properties: `CamelResponseSuccessfulExecution`, `CamelResponseFromFallback`, `CamelResponseShortCircuited`, `CamelResponseTimedOut`, `CamelResponseRejected`, `CamelResponseIgnored`, `CamelResponseState`. The page also uses the `CamelCircuitBreakerResponse...` prefix, so check which your version uses. In the fallback, `Rejected` means the call was never attempted. `CamelCircuitBreakerState` is read after the call is recorded, so the call that opens the breaker shows `OPEN`.

Example: `to("http://fooservice.com/slow")` with a fallback setting the body to "Fallback message".

Stopping and starting the route resets the breaker to Closed and clears metrics.

Verify: with the target down, calls return the fallback body and, once open, are not attempted.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Circuit Breaker EIP page source (circuitBreaker-eip.adoc) and the model definition (circuitBreaker.json) from the apache/camel repository, which generate the cited page. Confirmed the two implementations and their configuration elements, the three states, the options (configuration, inheritErrorHandler default false, onFallback, outputs, disabled), the rejected, timed-out and short-circuited property semantics, CamelCircuitBreakerState reporting OPEN for the opening call, the fallback example, and the route stop and start reset. The model lists the response properties as CamelResponse*, the page text as CamelCircuitBreakerResponse*, as the skill already notes. No commands were run.
