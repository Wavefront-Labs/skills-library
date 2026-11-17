---
id: computing-software.software-engineering.java.spring-security-filter-chain-and-jwt
name: spring-security-filter-chain-and-jwt
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, spring-security, jwt, oauth2-resource-server, securityfilterchain, method-security, spring-tx-security]
level: practitioner
status: docs-checked
description: "Configure Spring Security 6: SecurityFilterChain beans, JWT resource server validation and claims mapping, method security, CSRF/CORS choices and security tests."
sources:
  - https://docs.spring.io/spring-security/reference/servlet/architecture.html
  - https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
  - https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Spring Security filter chain and JWT resource server

**Goal:** an API that validates bearer tokens from your identity provider and authorises by scopes/roles, with tests proving it.

## 1. Filter chain bean (Spring Security 6 style)
```java
@Configuration
@EnableMethodSecurity
class SecurityConfig {
    @Bean
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        return http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers(HttpMethod.GET, "/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(jwtConverter())))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(c -> c.disable())          // stateless bearer-token API only
            .build();
    }
}
```
An application can define multiple `SecurityFilterChain` beans (see the Architecture page); `securityMatcher` selects which requests a chain handles. Rules are evaluated top-down: put specific matchers first.

## 2. JWT validation
```yaml
spring.security.oauth2.resourceserver.jwt:
  issuer-uri: https://login.example.com/realms/acme     # discovers JWKS, validates iss
  audiences: orders-api                                 # validates the aud claim
```
`issuer-uri` validates the `iss` claim and needs a provider configuration endpoint (otherwise supply `jwk-set-uri`, which avoids contacting the authorization server at startup); `audiences` validates `aud`. Scopes are mapped to authorities prefixed `SCOPE_` by default.

## 3. Mapping roles from claims
Supply your own converter through `jwtAuthenticationConverter(...)` in the chain (as in section 1) to map claims other than `scope` to authorities; see the JWT resource-server page for the converter API.

## 4. Method security
```java
@PreAuthorize("hasAuthority('SCOPE_orders:write')")
public Order create(...) { }
@PreAuthorize("@orderAuth.canView(authentication, #id)")
public Order get(long id) { }
```
Object-level checks (is this the caller's order?) belong here or in the service, not in URL patterns.

## Gotchas
- `hasRole("ADMIN")` checks authority `ROLE_ADMIN`; `hasAuthority` checks the literal string.
- Disable CSRF only for stateless bearer-token APIs; browser apps with session cookies need it.
- 401 = unauthenticated, 403 = authenticated but not allowed.

## Checked
2026-11-01. Confirmed against Spring Security reference pages (Architecture, OAuth 2.0 Resource Server JWT,
Method Security): multiple SecurityFilterChain beans, issuer-uri and jwk-set-uri behaviour, audiences property
validating aud, SCOPE_ prefix, jwtAuthenticationConverter, @EnableMethodSecurity, @PreAuthorize with SpEL.
Removed: 60 s skew figure, Boot 3.2 version note, WebSecurityConfigurerAdapter and @Order statements, converter
setter code, test examples, CORS 401 and TRACE logging notes (not on these pages).
Method: documentation only; no commands were run.

## Verify
- Tests cover: no token 401, wrong audience 401, missing scope 403, correct scope 200.
