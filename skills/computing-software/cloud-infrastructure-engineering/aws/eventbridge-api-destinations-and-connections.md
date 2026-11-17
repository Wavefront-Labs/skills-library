---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-api-destinations-and-connections
name: eventbridge-api-destinations-and-connections
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, api-destinations, eb-connection, http-target, webhook, oauth-client-credentials, api-key-auth, basic-auth, invocation-rate-limit, http-parameters, saas-integration, secrets-manager, event-driven]
level: practitioner
status: docs-checked
description: "Call external HTTP APIs from EventBridge rules via API destinations: connections (basic, API key, OAuth), rate limits, parameters, retries, DLQ, private endpoints."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-destinations.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-quota.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-monitoring.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EventBridge API destinations and connections

**Goal:** events become HTTPS calls to Slack, PagerDuty, Stripe, a partner webhook or your
own API — authenticated, rate-limited and retried — with no Lambda whose only code is
`requests.post`.

## 1. Connection (credentials)
```bash
aws events create-connection --name pagerduty --authorization-type API_KEY \
  --auth-parameters '{"ApiKeyAuthParameters":{"ApiKeyName":"Authorization","ApiKeyValue":"Token token=<KEY>"},
                      "InvocationHttpParameters":{"HeaderParameters":[{"Key":"Content-Type","Value":"application/json","IsValueSecret":false}]}}'
# OAuth client credentials — EventBridge fetches and caches the token itself
aws events create-connection --name partner-oauth --authorization-type OAUTH_CLIENT_CREDENTIALS \
  --auth-parameters '{"OAuthParameters":{"AuthorizationEndpoint":"https://auth.partner.com/oauth/token","HttpMethod":"POST",
     "ClientParameters":{"ClientID":"<ID>","ClientSecret":"<SECRET>"},
     "OAuthHttpParameters":{"BodyParameters":[{"Key":"scope","Value":"events:write","IsValueSecret":false}]}}}'
```
Authorization types (API model): `BASIC`, `API_KEY`, `OAUTH_CLIENT_CREDENTIALS`. Creating a connection adds the service-linked role `AmazonEventBridgeApiDestinationsServiceRolePolicy` to the account; EventBridge uses it to create and store the connection secret in Secrets Manager. Connection states in the API model include `AUTHORIZED`, `DEAUTHORIZED` and `FAILED_CONNECTIVITY`; use `describe-connection` to check state. Private APIs use `InvocationConnectivityParameters` on the connection.

## 2. API destination
```bash
aws events create-api-destination --name pagerduty-events --connection-arn "$CONN_ARN" \
  --invocation-endpoint "https://events.pagerduty.com/v2/enqueue" --http-method POST --invocation-rate-limit-per-second 10
```
- `invocation-rate-limit-per-second`: the account quota "Rate of invocations per API destination" is 300 per second by default (adjustable; quotas page read 2026-10-27). Invocations above the limit are throttled, that is delayed, and are retried within the retry window (24 hours by default). If the rate is set far below the incoming volume the backlog can exceed 24 hours and events are lost, so configure a DLQ and set the rate from the partner's documented limit.
- Any HTTP method except CONNECT and TRACE is allowed; the API model lists POST, GET, HEAD, OPTIONS, PUT, PATCH, DELETE.
- The endpoint may contain path parameters: `https://api.example.com/orders/*/status`; fill
  `*` with `HttpParameters.PathParameterValues` on the target.

## 3. Rule target
```json
{"Id":"pd","Arn":"arn:aws:events:<REGION>:<ACCOUNT_ID>:api-destination/pagerduty-events/<id>",
 "RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/eb-invoke-api-dest",
 "InputTransformer":{"InputPathsMap":{"msg":"$.detail.message","sev":"$.detail.severity"},
   "InputTemplate":"{\"routing_key\":\"<ROUTING_KEY>\",\"event_action\":\"trigger\",\"payload\":{\"summary\":<msg>,\"severity\":<sev>,\"source\":\"eventbridge\"}}"},
 "HttpParameters":{"HeaderParameters":{"X-Request-Source":"eventbridge"},"QueryStringParameters":{"env":"prod"},"PathParameterValues":["$.detail.orderId"]},
 "DeadLetterConfig":{"Arn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:eb-api-dlq"},
 "RetryPolicy":{"MaximumRetryAttempts":8,"MaximumEventAgeInSeconds":3600}}
```
The role needs `events:InvokeApiDestination` on the destination ARN. Body = transformed input
(or the whole event). `HttpParameters` values may be literals or `$.path` references into
the **original** event.

## 4. Failure semantics
- EventBridge retries events that get 401, 407, 409, 429 or 5xx responses. Other 1xx, 2xx, 3xx and 4xx responses are not retried. It reads the standard `Retry-After` header and, on event buses, uses the more conservative of that value and the retry policy; a negative value stops retries.
- Default event bus retry policy: up to 24 hours and 185 attempts, with exponential backoff and jitter. After retries are exhausted the event goes to the DLQ if one is configured, otherwise it is dropped. DLQ messages carry the custom attributes `RULE_ARN`, `TARGET_ARN` and `ERROR_CODE`, plus an `ERROR_MESSAGE` that includes the exhausted retry condition.
- Requests must complete within 5 seconds or EventBridge times out and retries them, so make the endpoint idempotent.
- Requests always include `User-Agent: Amazon/EventBridge/ApiDestinations` (cannot be overridden); if you set no `Content-Type`, `application/json; charset=utf-8` is sent.
- CloudWatch metrics documented for rules: `Invocations`, `FailedInvocations`, `RetryInvocationAttempts`, `InvocationsSentToDlq`, `InvocationsFailedToBeSentToDlq`, `ThrottledRules`.

## 5. Private endpoints
API destinations support private APIs through the connection's connectivity parameters, but the documentation states that API destinations support only public domain names with publicly trusted certificates for HTTPS endpoints, and do not support mutual TLS. The Custom Event Bus - Classic quotas page lists a default of 20 private connections per account per Region. Read the current connection documentation before designing private connectivity.

## Gotchas
- Headers set on the connection apply to every destination that uses it.
- Choose the OAuth and secret-rotation procedure from the connection documentation; use `update-connection` rather than editing the managed secret.
- API destinations to public HTTPS endpoints are available only in the Regions listed on the API destinations page.

## Verify
- [ ] `describe-connection` → `ConnectionState: AUTHORIZED`; `describe-api-destination` → `ApiDestinationState: ACTIVE`.
- [ ] A test event produces a 2xx at the partner (their log) and `Invocations` = 1, `FailedInvocations` = 0.
- [ ] A destination that returns 503 shows `RetryInvocationAttempts` climbing; after retries are exhausted the event reaches the DLQ with `ERROR_CODE`.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide (API destinations as targets, dead-letter queues, quotas, monitoring metrics), read this date. Confirmed: retryable status codes 401/407/409/429/5xx (the draft said only 429/5xx), Retry-After handling, 24 h / 185 default retry policy, 5 s timeout, DLQ attributes, 300 per second default invocation rate quota, headers, HTTP methods, public-certificate and no-mTLS limits, private connection quota. Confirmed from the EventBridge API model (botocore events 2015-10-07): connection authorization types are only BASIC, API_KEY and OAUTH_CLIENT_CREDENTIALS (the draft listed a fourth type), connection and destination state enums. Removed unconfirmed secret naming, billing, OAuth caching, rotation, binary-body and partner-template claims and the InvocationsFailedToBeSent metric.
Method: documentation only; no commands were run.
