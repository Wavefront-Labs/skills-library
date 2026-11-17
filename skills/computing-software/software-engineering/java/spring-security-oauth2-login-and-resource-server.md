---
id: computing-software.software-engineering.java.spring-security-oauth2-login-and-resource-server
name: spring-security-oauth2-login-and-resource-server
category: computing-software
field: software-engineering
product: java
tags: [java, spring-tx-security, oauth2-login, oidc, oauth2-client, resource-server, pkce]
level: advanced
status: draft
description: "Configure Spring Security OAuth2/OIDC login with a provider, call APIs with an OAuth2AuthorizedClient, and map claims to authorities; redirect URIs, PKCE and logout."
sources: ["https://docs.spring.io/spring-security/reference/servlet/oauth2/login/core.html", "https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html", "https://datatracker.ietf.org/doc/html/rfc7636"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OAuth2/OIDC login in Spring Security

```yaml
spring.security.oauth2.client:
  registration.keycloak:
    client-id: web
    client-secret: ${OIDC_SECRET}
    scope: openid,profile,email
    authorization-grant-type: authorization_code
  provider.keycloak:
    issuer-uri: https://id.example.com/realms/acme      # discovery fills in endpoints and JWKS
```
```java
@Bean SecurityFilterChain chain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.requestMatchers("/", "/public/**").permitAll().anyRequest().authenticated())
        .oauth2Login(o -> o.userInfoEndpoint(u -> u.oidcUserService(oidcService())))
        .logout(l -> l.logoutSuccessHandler(new OidcClientInitiatedLogoutSuccessHandler(repo)))
        .build();
}
```
Register the redirect URI `{baseUrl}/login/oauth2/code/{registrationId}` exactly at the provider. Spring uses PKCE for public clients and, since Security 6.x, defaults it for confidential authorization-code flows where supported. Map roles from claims with a `GrantedAuthoritiesMapper` (e.g. `realm_access.roles`).

## Calling APIs as the user
Inject `@RegisteredOAuth2AuthorizedClient("keycloak") OAuth2AuthorizedClient c` or configure `WebClient`/`RestClient` with the OAuth2 interceptor; tokens refresh automatically when a refresh token exists. For machine-to-machine use `client_credentials`.

## Gotchas
- Behind a proxy set `server.forward-headers-strategy=framework` or redirect URIs will be `http://`.
- Never log tokens; keep secrets in env or a vault.
- Resource server APIs use `oauth2ResourceServer(jwt())` instead; a BFF with login in the server and cookies for the SPA avoids tokens in the browser.
- Validate `iss` and `aud`; clock skew defaults to 60 s.
- Sessions: scale-out needs Spring Session or sticky sessions.

## Verify
Local Keycloak via Testcontainers or `oauth2Login()` with `SecurityMockMvcRequestPostProcessors.oidcLogin()` in tests; confirm an unauthenticated request redirects to the provider.
