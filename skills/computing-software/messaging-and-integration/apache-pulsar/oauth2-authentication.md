---
id: computing-software.messaging-and-integration.apache-pulsar.oauth2-authentication
name: oauth2-authentication
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [oauth2, client-credentials, issuer-url, audience, token-refresh, tls-client-auth]
level: practitioner
status: docs-checked
description: "Authenticate Pulsar clients with OAuth 2.0 access tokens: broker/proxy settings, Java client-credentials builder, mTLS at the token endpoint and earlyTokenRefreshPercent."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-oauth2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let clients obtain an access token from an OAuth 2.0 issuer and present it to Pulsar for authentication.

Flow: the client gets an access token from the authorization server and passes it to the broker. By default brokers validate it with `AuthenticationProviderToken`.

Broker and proxy config (`broker.conf`, `proxy.conf`, or `standalone.conf`):
```properties
authenticationEnabled=true
authenticationProviders=org.apache.pulsar.broker.authentication.AuthenticationProviderToken
brokerClientAuthenticationPlugin=org.apache.pulsar.client.impl.auth.oauth2.AuthenticationOAuth2
brokerClientAuthenticationParameters={"privateKey":"file:///path/to/privateKey","audience":"https://broker.example.com","issuerUrl":"https://issuer.example.com"}
tokenSecretKey=file:///path/to/secret.key
# or tokenPublicKey=file:///path/to/public.key
```
The privateKey value can also be inline as `data:application/json;base64,<body>`. Token key files must be DER-encoded.

Java client with the client-credentials builder:
```java
PulsarClient client = PulsarClient.builder()
  .serviceUrl("pulsar://broker.example.com:6650/")
  .authentication(AuthenticationFactoryOAuth2.clientCredentialsBuilder()
    .issuerUrl(new URL("https://issuer.example.com"))
    .credentialsUrl(new URL("file:///path/to/KeyFile.json"))
    .audience("https://broker.example.com").build())
  .build();
```
Encoded alternative: `AuthenticationFactory.create(AuthenticationOAuth2.class.getName(), "{\"type\":\"client_credentials\",\"privateKey\":\"file:///path/to/KeyFile.json\",\"issuerUrl\":\"https://issuer.example.com\",\"audience\":\"pulsar\"}")`.

Mutual TLS at the token endpoint (Java client): `.tokenEndpointAuthMethod(TokenEndpointAuthMethod.TLS_CLIENT_AUTH)` with `.clientId(...)`, `.tlsCertFile(...)`, `.tlsKeyFile(...)` and `.trustCertsFilePath(...)`. This certificate authenticates the client to the OAuth2 server only; the Pulsar connection uses the resulting access token, and TLS for that connection is configured separately. For encoded parameters or CLI tools set `tokenEndpointAuthMethod` to `tls_client_auth`.

Token refresh: `.earlyTokenRefreshPercent(0.8)` (or `"earlyTokenRefreshPercent":"0.8"` in encoded parameters) starts refreshing after 80% of the token lifetime. The default is `1`, which disables early refresh; values must be greater than zero and values of 1 or more disable it.

Verify: connect, wait past the refresh point, and confirm the client keeps working.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/security-oauth2.md (read in full)
