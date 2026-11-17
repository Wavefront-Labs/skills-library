---
id: computing-software.software-engineering.quarkus.quarkus-rest-csrf-prevention
name: quarkus-rest-csrf-prevention
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, csrf, rest, qute, security, double-submit-cookie]
level: practitioner
status: docs-checked
description: "Add CSRF protection to Quarkus REST with quarkus-rest-csrf: Qute hidden field or header token, cookie and signature options, restricting verification paths, manual checks."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-csrf-prevention.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus REST CSRF prevention

The `quarkus-rest-csrf` extension implements Double Submit Cookie and a request-header variant. A Quarkus REST filter creates and verifies tokens for `application/x-www-form-urlencoded` and `multipart/form-data` forms; it applies to `POST`, `PUT`, `PATCH`, `DELETE` and other state-changing methods. Add it with `rest-csrf` (artifact `io.quarkus:quarkus-rest-csrf`).

## Form token via Qute

```html
<form action="/service/csrfTokenForm" method="post">
  <input type="hidden" name="{inject:csrf.parameterName}" value="{inject:csrf.token}" />
  <input type="text" name="name" />
</form>
```

The resource returns the template for `GET` and handles `POST` with `@Consumes(MediaType.APPLICATION_FORM_URLENCODED)`; the method runs only if the filter verified the token. Failure (missing field, missing cookie, or mismatch) gives HTTP `400`. Defaults need no configuration; the field and cookie name default to `csrf-token`:

```properties
quarkus.rest-csrf.form-field-name=csrftoken
quarkus.rest-csrf.cookie-name=csrftoken
```

## Signed tokens

Store HMAC signatures as the cookie token with a secret of at least 32 characters:

```properties
quarkus.rest-csrf.token-signature-key=<secret of 32+ characters>
```

## Header token (HTMX, JavaScript)

When not using forms, inject the header name and token, for example `<body hx-headers='{"{inject:csrf.headerName}":"{inject:csrf.token}"}'>`. Default header is `X-CSRF-TOKEN`; change with `quarkus.rest-csrf.token-header-name`. To read the cookie from JavaScript use `{inject:csrf.cookieName}` and set `quarkus.rest-csrf.cookie-http-only=false`.

## Limit verification

If the same path also accepts other media types (JSON) that carry no token:

```properties
quarkus.rest-csrf.create-token-path=/service/user
quarkus.rest-csrf.require-form-url-encoded=false
```

The first restricts verification to that path; the second is unnecessary when the token is sent as a header.

## Manual verification

Compare `@CookieParam` and `@FormParam("csrf-token")` values yourself (throw `BadRequestException` on mismatch) and turn off the filter check with `quarkus.rest-csrf.verify-token=false`.

## Programmatic config

With `quarkus-security`, observe `HttpSecurity` and call `httpSecurity.csrf(CSRF.builder().formFieldName("my-csrf-token").tokenSize(32).build())`. `CSRF.builder()` fails if `quarkus-rest-csrf` is missing.

## Cross-origin

Do not allow all origins when enforcing CSRF cross-origin; restrict to trusted origins (see the CORS filter). The CORS filter alone is a stateless alternative via Origin checking.

## Checked

2026-11-07. Matched against the text (with includes) of: security-csrf-prevention.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
