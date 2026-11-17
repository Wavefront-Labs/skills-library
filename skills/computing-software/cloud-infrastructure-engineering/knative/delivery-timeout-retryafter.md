---
id: computing-software.cloud-infrastructure-engineering.knative.delivery-timeout-retryafter
name: delivery-timeout-retryafter
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [delivery-timeout, retryaftermax, retry-after, delivery-spec, feature-flag]
level: advanced
status: docs-checked
description: "Cap each delivery request with timeout and honor HTTP Retry-After on 429 and 503 with retryAfterMax."
sources:
  - https://knative.dev/docs/eventing/features/delivery-timeout/
  - https://knative.dev/docs/eventing/features/delivery-retryafter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound how long each event delivery request may run and how Retry-After is applied.

Timeout: the `delivery-timeout` feature is Beta and enabled by default. In a `delivery` spec, `timeout` sets the timeout for each sent HTTP request, as an ISO 8601 duration. The page example is a Subscription that retries 3 times with each request limited to 5 seconds:

```yaml
spec:
  delivery:
    backoffDelay: PT2S
    backoffPolicy: linear
    retry: 3
    timeout: PT5S
```

Retry-After: the `delivery-retryafter` feature is Alpha and disabled by default. When enabled, the `retryAfterMax` field controls how HTTP Retry-After headers affect backoff when retrying 429 and 503 responses. Details:
- It applies to any resource spec that accepts `delivery`, including Channels, Subscriptions, Brokers and Triggers.
- It only takes effect when the `delivery` spec performs retries.
- It is an override that stops large Retry-After values hurting throughput, written in ISO 8601.
- The larger of the normal backoff and the Retry-After value is used for the next retry.
- `PT0S` effectively disables Retry-After support.
- With the flag disabled, a spec that sets `retryAfterMax` is rejected by webhook validation.
- Webhook validation does not guarantee an implementation honours the field: extensions that do not use the shared retry library (the page names RabbitMQ and Google Pub/Sub) need extra work to respect it.

## Checked

2026-11-04. Confirmed against the DeliverySpec.Timeout and DeliverySpec.RetryAfterMax pages (knative/docs source): `delivery-timeout` Beta and enabled by default, ISO 8601 `timeout`, the Subscription example (retry 3, `PT5S`), `delivery-retryafter` Alpha and disabled by default, 429 and 503 handling, applicability to resources accepting `delivery`, effect only with retries, the larger-of-backoff-and-header rule, `PT0S` disabling support, and rejection by webhook validation when the flag is off. Added the retryafter page to sources and its note that not every implementation honours the field.

Method: documentation only; no commands were run.
