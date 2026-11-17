---
id: computing-software.data-engineering.apache-kafka.sasl-authentication
name: sasl-authentication
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, kafka-sasl, sasl-scram, oauthbearer, gssapi, kerberos, sasl-ssl, jaas, kafka-authentication]
level: advanced
status: docs-checked
description: "Authenticate Kafka clients with SASL over TLS: SCRAM-SHA-512 users, OAUTHBEARER/OIDC, GSSAPI (Kerberos) notes, listener and JAAS config, and the never-use-PLAIN-without-TLS rule."
sources:
  - https://kafka.apache.org/documentation/#security_sasl
  - https://kafka.apache.org/documentation/#security_sasl_scram
  - https://kafka.apache.org/documentation/#security_sasl_oauthbearer
  - https://github.com/apache/kafka/blob/trunk/docs/security/authentication-using-sasl.md
  - https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/config/internals/BrokerSecurityConfigs.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SASL authentication for Kafka

**Goal:** every client proves its identity with a credential you can rotate and revoke, over an encrypted connection.

## Mechanisms
| Mechanism | Use |
|---|---|
| SCRAM-SHA-512 | Username/password stored salted in Kafka metadata; simple, self-contained |
| OAUTHBEARER (OIDC) | Tokens from your IdP (Okta, Entra ID, Keycloak); short-lived, central control |
| GSSAPI | Kerberos estates (Hadoop) |
| PLAIN | Only over SSL as the transport; the default implementation keeps credentials in the JAAS file, so use it for development or with a custom callback handler |
Always use the `SASL_SSL` security protocol (SASL over TLS).

## SCRAM
```bash
kafka-configs.sh --bootstrap-server $B --command-config admin.properties --alter \
  --add-config 'SCRAM-SHA-512=[iterations=8192,password=<generated>]' --entity-type users --entity-name billing-svc
```
Broker:
```properties
listeners=SASL_SSL://:9094
listener.security.protocol.map=SASL_SSL:SASL_SSL,...
sasl.enabled.mechanisms=SCRAM-SHA-512
listener.name.sasl_ssl.scram-sha-512.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required;
```
Client:
```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="billing-svc" password="${env:KAFKA_PASSWORD}";
```
(`${env:...}` needs the `EnvVarConfigProvider` registered through `config.providers`; otherwise inject the whole property from a secret. SCRAM iterations default to 4096 if omitted.)

## OAUTHBEARER with OIDC
Broker validates JWTs against the IdP JWKS:
```properties
sasl.enabled.mechanisms=OAUTHBEARER
listener.name.sasl_ssl.oauthbearer.sasl.server.callback.handler.class=org.apache.kafka.common.security.oauthbearer.OAuthBearerValidatorCallbackHandler
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.jwks.endpoint.url=https://<IDP>/oauth2/v1/keys
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.expected.audience=<audience>
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.expected.issuer=https://<IDP>
```
The JWKS and token endpoint URLs must also be listed in the JVM system property `org.apache.kafka.sasl.oauthbearer.allowed.urls` (default: empty list), for example `-Dorg.apache.kafka.sasl.oauthbearer.allowed.urls=https://<IDP>/oauth2/v1/keys,https://<IDP>/oauth2/v1/token`, on every JVM that fetches them. Clients use the `client_credentials` grant: `sasl.login.callback.handler.class=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginCallbackHandler`, `sasl.oauthbearer.token.endpoint.url`, `sasl.oauthbearer.scope` and the client id and secret as documented for the OAUTHBEARER client configuration. The principal is the token's `sub` claim unless `sasl.oauthbearer.sub.claim.name` names another.

## Re-authentication
`connections.max.reauth.ms` (broker, default 0 = off; can be prefixed per listener and mechanism, e.g. `listener.name.sasl_ssl.oauthbearer.connections.max.reauth.ms`) sets a session lifetime for clients on version 2.2.0 or later; the broker disconnects connections that are not re-authenticated within it.

## Debugging
- Authentication failures with SCRAM: wrong password or user missing (`kafka-configs.sh --describe --entity-type users`).
- A client speaking plaintext or SSL to a SASL listener fails during the SASL handshake: match `security.protocol` to the listener.

## Verify
- [ ] Anonymous/plaintext connections are refused.
- [ ] Deleting a SCRAM user (or disabling the OIDC client) blocks that client within `connections.max.reauth.ms`.
- [ ] Credentials come from a secret store, not committed config.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: SASL_SSL transport rule and PLAIN-only-over-SSL guidance, SCRAM `kafka-configs.sh` syntax and default 4096 iterations, SCRAM credentials stored in the metadata log, OAUTHBEARER validator class and listener-prefixed property names (`jwks.endpoint.url`, `expected.audience`, `expected.issuer`), the `org.apache.kafka.sasl.oauthbearer.allowed.urls` requirement (new, absent from the earlier text), `client_credentials` retriever, `sub` claim default, `connections.max.reauth.ms` default and prefixing (BrokerSecurityConfigs source). Removed: the KIP-768 and 3.1 version gate, unprefixed JWKS properties, `clientId`/`clientSecret` JAAS option names, the Kafka 3.5 gate for env provider, the exact exception strings and Okta/Entra/Keycloak names.

Method: documentation only; no commands were run.
