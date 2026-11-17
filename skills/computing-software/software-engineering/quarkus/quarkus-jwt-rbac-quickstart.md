---
id: computing-software.software-engineering.quarkus.quarkus-jwt-rbac-quickstart
name: quarkus-jwt-rbac-quickstart
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, smallrye-jwt, jwt, rbac, rolesallowed, bearer-token, microprofile-jwt]
level: practitioner
status: docs-checked
description: "Secure Quarkus REST endpoints with SmallRye JWT: dependencies, verify config, key pair, token generation, RolesAllowed and claim injection."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-jwt.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus JWT RBAC quickstart with SmallRye JWT

## 1. Add the extensions

Create with extensions `rest-jackson,smallrye-jwt,smallrye-jwt-build`, or add `smallrye-jwt,smallrye-jwt-build` to an existing project. They add `io.quarkus:quarkus-smallrye-jwt` and `io.quarkus:quarkus-smallrye-jwt-build`.

## 2. Verify configuration (`application.properties`)

```properties
mp.jwt.verify.publickey.location=publicKey.pem
mp.jwt.verify.issuer=https://example.com/issuer
quarkus.native.resources.includes=publicKey.pem
```

The last line ensures the key file is bundled in a native executable. Put the RSA public key at `src/main/resources/publicKey.pem`. The MicroProfile JWT spec requires RSA-256 signed tokens.

## 3. Secure the endpoint

Inject `org.eclipse.microprofile.jwt.JsonWebToken` (it extends `java.security.Principal`), use `@RolesAllowed({ "User", "Admin" })` on a method, and `@PermitAll` for public ones. Without a token a `@RolesAllowed` endpoint returns HTTP 401 Unauthorized.

## 4. Generate a key pair and token

```shell
quarkus jwt generate-key
quarkus jwt generate-key --algo EC
quarkus jwt generate-key --algo RSA --size 4096
```

The CLI writes `src/main/resources/privateKey.pem` and `publicKey.pem` (PKCS#8) and adds the needed properties to `application.properties`; default is RSA 2048. With OpenSSL, generate with `openssl genrsa` and `openssl rsa -pubout`, then convert the private key with `openssl pkcs8 -topk8 -nocrypt -inform pem ... -outform pem`.

Build a token with `io.smallrye.jwt.build.Jwt`:

```java
String token = Jwt.issuer("https://example.com/issuer")
        .upn("jdoe@quarkus.io")
        .groups(new HashSet<>(Arrays.asList("User", "Admin")))
        .claim(Claims.birthdate.name(), "2001-07-13")
        .sign();
```

The `iss` must equal `mp.jwt.verify.issuer`; `upn` is the preferred principal claim; `groups` carries the roles. Sign with `-Dsmallrye.jwt.sign.key.location=privateKey.pem`.

## 5. Call it

```shell
curl -H "Authorization: Bearer eyJraWQ..." http://127.0.0.1:8080/secured/roles-allowed
```

Verify: the page's sample response is `hello jdoe@quarkus.io, isHttps: false, authScheme: Bearer, hasJWT: true, birthdate: 2001-07-13`.

## Claim injection

Inject a claim with `@Inject @Claim(standard = Claims.birthdate) String birthdate;`. This requires `@RequestScoped` on the bean when claims are injected as simple types such as `String`. `@ApplicationScoped`, `@Singleton` and `@RequestScoped` all work for injecting `JsonWebToken` itself.

## Checked

2026-11-07. Read in full: security-jwt.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
