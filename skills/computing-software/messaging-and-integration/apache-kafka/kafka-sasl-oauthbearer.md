---
id: computing-software.messaging-and-integration.apache-kafka.kafka-sasl-oauthbearer
name: kafka-sasl-oauthbearer
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, oauthbearer, sasl-oauthbearer-jwks-endpoint-url, client-credentials-jwt-retriever, token-endpoint-url]
level: advanced
status: docs-checked
description: "Use production SASL/OAUTHBEARER with an OAuth 2.0 identity provider: validator handler, JWKS URL and client credentials retriever."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate with OAuth 2.0 tokens. The default implementation creates and validates unsecured JWTs and is for non-production only; always use TLS in production.

Broker (production): JAAS `org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required ;` plus
```
listeners=SASL_SSL://host.name:port
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=OAUTHBEARER
sasl.enabled.mechanisms=OAUTHBEARER
listener.name.<listener name>.oauthbearer.sasl.server.callback.handler.class=org.apache.kafka.common.security.oauthbearer.OAuthBearerValidatorCallbackHandler
listener.name.<listener name>.oauthbearer.sasl.oauthbearer.jwks.endpoint.url=https://example.com/oauth2/v1/keys
```
Related broker settings include `sasl.oauthbearer.expected.audience`, `sasl.oauthbearer.expected.issuer`, `sasl.oauthbearer.clock.skew.seconds`, `sasl.oauthbearer.jwks.endpoint.refresh.ms`, `sasl.oauthbearer.scope.claim.name` and `sasl.oauthbearer.sub.claim.name`.

Client with the client_credentials grant:
```
security.protocol=SASL_SSL
sasl.mechanism=OAUTHBEARER
sasl.oauthbearer.jwt.retriever.class=org.apache.kafka.common.security.oauthbearer.ClientCredentialsJwtRetriever
sasl.oauthbearer.client.credentials.client.id=jdoe
sasl.oauthbearer.client.credentials.client.secret=...
sasl.oauthbearer.scope=my-application-scope
sasl.oauthbearer.token.endpoint.url=https://example.com/oauth2/v1/token
```
For the jwt-bearer grant use `JwtBearerJwtRetriever` with `sasl.oauthbearer.assertion.private.key.file`, `.algorithm=RS256`, `.claim.exp.seconds` and `.template.file`.

The default implementation depends on the optional jackson-databind library; add it with your build tool. Tokens refresh via `sasl.login.refresh.window.factor`, `.window.jitter`, `.min.period.seconds` and `.min.buffer.seconds`.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Authentication using SASL page (OAUTHBEARER). Removed: closing summary paragraph (mechanism summary and advice not on the page).

Method: documentation only; no commands were run.
