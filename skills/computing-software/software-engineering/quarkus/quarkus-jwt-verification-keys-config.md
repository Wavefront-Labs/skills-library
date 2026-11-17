---
id: computing-software.software-engineering.quarkus.quarkus-jwt-verification-keys-config
name: quarkus-jwt-verification-keys-config
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, smallrye-jwt, jwt-verification, jwks, jwtparser, decryption, mp-jwt]
level: advanced
status: docs-checked
description: "Configure SmallRye JWT in Quarkus for key formats, EC and HMAC keys, decryption, JWTParser, blocking calls, custom factories and the dev-mode default key."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-jwt.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus SmallRye JWT: verification keys, decryption and parsing

## Key formats (in order of precedence)

PKCS#8 PEM, JWK, JWKS, JWK Base64 URL encoded, JWKS Base64 URL encoded.

## Asymmetric keys

- `mp.jwt.verify.publickey.location`: relative path or URL of the verification key. For an HTTPS-based JWK set in native mode, `quarkus.ssl.native` must also be `true`.
- `mp.jwt.verify.publickey`: key text as a string.
- `mp.jwt.verify.publickey.algorithm`: default `RS256`; use `ES256` for EC keys.
- `mp.jwt.verify.issuer`, `mp.jwt.verify.audiences` (comma-separated), `mp.jwt.verify.clock.skew` (default `60` seconds), `mp.jwt.verify.token.age`.

## Symmetric (HMAC) keys

The secret must be a JWK or JWK Set, for example `{"keys":[{"kty":"oct","kid":"secretKey","k":"..."}]}`. Refer to it with `smallrye.jwt.verify.key.location` and set `smallrye.jwt.verify.algorithm` to `HS256`, `HS384` or `HS512`. If `smallrye.jwt.verify.key.location` is set, `mp.jwt.verify.publickey.location` is ignored.

## Decryption

Set `smallrye.jwt.decrypt.key.location` (the page lists `mp.jwt.decrypt.key.location` as the non-deprecated name). If only the decryption key is set, tokens are expected to contain encrypted claims only. If a verification key property is also set, tokens must be inner-signed then encrypted.

## Tokens from other places

`mp.jwt.token.header` defaults to `Authorization`; set it to `Cookie` and name the cookie with `mp.jwt.token.cookie`. For tokens not injectable (for example in a request payload), inject `io.smallrye.jwt.auth.principal.JWTParser` and call `parser.parse(token)`, or `parser.verify(token, secret)` / `parser.decrypt(token, secret)` with a local secret. All `mp.jwt` and `smallrye.jwt` properties still apply; only the key is customised.

## Custom principal factory

`DefaultJWTCallerPrincipalFactory` is the default. Replace it with a `META-INF/services/io.smallrye.jwt.auth.principal.JWTCallerPrincipalFactory` entry, or an `@ApplicationScoped @Alternative @Priority(1)` bean extending `JWTCallerPrincipalFactory`.

## Blocking calls

SmallRye JWT is not reactive. Remote JWKS refresh or custom key resolvers such as AWS ALB can block an IO thread, notably when the key endpoint takes over 3 seconds. Set `quarkus.smallrye-jwt.blocking-authentication=true` to avoid it.

## Using smallrye-jwt directly

For extensions without HTTP support (such as gRPC) add `io.smallrye:smallrye-jwt` and set `quarkus.index-dependency.smallrye-jwt.group-id=io.smallrye` and `quarkus.index-dependency.smallrye-jwt.artifact-id=smallrye-jwt`.

## Debugging

Set `quarkus.log.category."io.quarkus.smallrye.jwt.runtime.auth.MpJwtValidator".level=TRACE` and the same with `.min-level=TRACE`.

## Gotcha

In dev and test modes a 2048-bit RSA key pair is auto-generated if none of `mp.jwt.verify.publickey.location`, `mp.jwt.verify.publickey`, `mp.jwt.decrypt.key.location`, `smallrye.jwt.encrypt.key.location`, `smallrye.jwt.sign.key.location` or `smallrye.jwt.sign.key` is set. In dev mode the default issuer is `https://quarkus.io/issuer` unless `mp.jwt.verify.issuer` is set (use `NONE` to suppress it).

## Checked

2026-11-07. Read in full: security-jwt.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
