---
id: computing-software.messaging-and-integration.strimzi.oauth-custom-authentication
name: oauth-custom-authentication
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [oauth2, custom-authentication, token-validation]
level: sme
status: docs-checked
description: "Configure OAuth 2.0 on listeners with the custom authentication type."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OAuth 2.0 with the custom type

**Goal:** secure Kafka with tokens issued by an authorization server.

Strimzi supports OAuth 2.0 authentication and authorization for Kafka and for Kafka Connect, MirrorMaker 2 and the HTTP Bridge as clients. Brokers validate tokens using the OAuth configuration on the listener, and Keycloak Authorization Services can add fine-grained policy-based authorization.

The `oauth` and `keycloak` authentication types are **deprecated** and will be removed in a future release. Listeners and clients must now configure OAuth 2.0 with the **`custom`** authentication type. OAuth support is the same; only the configuration model changes, on both server-side listeners and client-side authentication for Strimzi components.

Outline:

1. Prepare an OAuth 2.0 authorization server: it needs a token endpoint, TLS, and either a JWKS endpoint (local JWT validation) or an introspection endpoint (remote validation of opaque tokens). Only one validation method is required.
2. Define `authentication.type: custom` with the `OAUTHBEARER` SASL mechanism on the listeners used by clients. The JAAS config string holds all validation settings.
3. Configure clients (Connect, MirrorMaker 2, Bridge) to authenticate with access tokens.
4. Optionally enable authorization on brokers, using token claims or Keycloak.

Minimal JWT validation listener (JWKS endpoint):

```yaml
listeners:
  - name: tls
    port: 9093
    type: internal
    tls: true
    authentication:
      type: custom
      sasl: true
      listenerConfig:
        sasl.enabled.mechanisms: OAUTHBEARER
        oauthbearer.sasl.server.callback.handler.class: io.strimzi.kafka.oauth.server.JaasServerOauthValidatorCallbackHandler
        oauthbearer.sasl.jaas.config: |
          org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required
          oauth.valid.issuer.uri="https://${SSO_HOST}/realms/kafka-authz"
          oauth.jwks.endpoint.uri="https://${SSO_HOST}/realms/kafka-authz/protocol/openid-connect/certs"
          oauth.username.claim="preferred_username";
        connections.max.reauth.ms: 3600
config:
  principal.builder.class: io.strimzi.kafka.oauth.server.OAuthKafkaPrincipalBuilder
```

`connections.max.reauth.ms` makes brokers prompt clients to re-authenticate so expiring tokens refresh without closing the connection. `principal.builder.class` maps validated tokens to Kafka principals. If you set `oauth.check.issuer="false"`, do not configure `oauth.valid.issuer.uri`.

**Checklist**

1. Migrate any `oauth` or `keycloak` listener types.
2. Check both server and client sides.
3. Do not put sensitive values directly in the `config` section of `custom` authentication; load them with Kafka configuration providers.
4. Advanced options (timeouts, JWKS refresh, introspection, TLS) are in the Strimzi OAuth project documentation.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (single page, section 17 on OAuth 2.0 read in full, plus the Keycloak examples note); listener example corrected to the documented OAUTHBEARER form and the unconfirmed bearer-credential claim dropped.
