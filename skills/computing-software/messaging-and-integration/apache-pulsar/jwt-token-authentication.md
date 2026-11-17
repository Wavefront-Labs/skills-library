---
id: computing-software.messaging-and-integration.apache-pulsar.jwt-token-authentication
name: jwt-token-authentication
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [jwt, token-authentication, tokens-create, secret-key, key-pair, authentication-provider-token]
level: practitioner
status: docs-checked
description: "Enable JWT authentication in Pulsar: generate secret or key-pair keys, mint tokens with bin/pulsar tokens, configure brokers, proxies, CLI tools and clients."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-jwt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate Pulsar clients with signed JWTs whose subject is the role.

Always use TLS with tokens, since sending a token equals sending a password.

Keys (symmetric secret, or asymmetric private key to sign and public key to validate):
```shell
bin/pulsar tokens create-secret-key --output my-secret.key            # add --base64 for base64 output
bin/pulsar tokens create-key-pair --output-private-key my-private.key --output-public-key my-public.key
```
Keep the private key with administrators; the public key goes to every broker.

Mint tokens (prints to stdout):
```shell
bin/pulsar tokens create --secret-key file:///path/to/my-secret.key --subject test-user
bin/pulsar tokens create --private-key file:///path/to/my-private.key --subject test-user
bin/pulsar tokens create --secret-key file:///path/to/my-secret.key --subject test-user --expiry-time 1y
```
A token carries no permissions itself: enable authorization and grant roles separately.

Broker and proxy config (`broker.conf`, `proxy.conf`, or `standalone.conf`):
```properties
authenticationEnabled=true
authenticationProviders=org.apache.pulsar.broker.authentication.AuthenticationProviderToken
brokerClientAuthenticationPlugin=org.apache.pulsar.client.impl.auth.AuthenticationToken
brokerClientAuthenticationParameters={"token":"<token>"}
tokenSecretKey=file:///path/to/secret.key
# or tokenPublicKey=file:///path/to/public.key
```
Parameters may also be `token:<string>` or `file:///path/to/token`. Key files must be DER-encoded; `tokenSecretKey=data:;base64,<value>` passes it inline. `tokenAuthClaim` picks the principal claim (default `sub`); audience checking uses `tokenAudienceClaim` with `tokenAudience`. Through a proxy set `forwardAuthorizationCredentials=true` on the proxy and keep `authenticateOriginalAuthData=true` on brokers.

CLI tools (`conf/client.conf`): `authPlugin=org.apache.pulsar.client.impl.auth.AuthenticationToken` and `authParams=token:<token>` or `file:///path/to/token/file`.

Java client: `PulsarClient.builder().serviceUrl(...).authentication(AuthenticationFactory.token("<token>")).build()`, or pass a Supplier to re-read tokens.

## Checked

2026-11-03. Confirmed against the pulsar-site page security-jwt: TLS note, key and token commands, expiry flag, broker, proxy and CLI settings, token and key formats, validation settings, proxy forwarding and the Java client calls. Removed the invented Verify step.

Method: documentation only; no commands were run.
