---
id: computing-software.software-engineering.java.spring-security-csrf-and-cors-configuration
name: spring-security-csrf-and-cors-configuration
category: computing-software
field: software-engineering
product: java
tags: [java, spring-tx-security, spring-csrf-cors, csrf, cors, corsconfigurationsource]
level: practitioner
status: docs-checked
description: "Configure CSRF protection and CORS in Spring Security 6: when CSRF can be disabled, cookie token repository for SPAs, CorsConfigurationSource and preflight ordering."
sources: ["https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html", "https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSRF and CORS in Spring Security

## CSRF
CSRF protection is enabled by default and affects both backend integration and testing. A backend that does not serve browser traffic (for example a mobile or JSON API backend) may disable it; a backend that also serves browser traffic still needs it. Consider ignoring only certain endpoints before disabling globally.
```java
http.csrf(c -> c.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))   // JavaScript can read the XSRF-TOKEN cookie
    // backend with no browser traffic only:
    // .csrf(AbstractHttpConfigurer::disable)
```
With the cookie repository the token is sent back in the `X-XSRF-TOKEN` request header (the session repository uses `X-CSRF-TOKEN`). The framework's reference has a dedicated section on SPA/JavaScript integration and the deferred-token request handler; follow it for Angular-style clients. Server-rendered forms carry the token in a hidden `_csrf` field.

## CORS
CORS must be processed before Spring Security, because the preflight request carries no cookies; if Security runs first it sees an unauthenticated request and rejects it. The simplest way is the `CorsFilter` integrated through a `CorsConfigurationSource`; Spring Security configures CORS automatically only if a `UrlBasedCorsConfigurationSource` is present.
```java
@Bean CorsConfigurationSource cors() {
    var c = new CorsConfiguration();
    c.setAllowedOrigins(List.of("https://app.example.com"));
    var s = new UrlBasedCorsConfigurationSource(); s.registerCorsConfiguration("/api/**", c); return s;
}
// http.cors(Customizer.withDefaults());   // uses the bean above
```
For per-chain configuration, `http.securityMatcher("/api/**").cors(c -> c.configurationSource(...))` on a filter chain with its own `@Order`.

## Verify
Use Spring Security's MockMvc support and `CsrfRequestPostProcessor` (`csrf()`) to test CSRF protection: a POST without a token is rejected, a POST with `.with(csrf())` passes.

## Checked

Method: docs-checked 2026-11-09 against the Spring Security CSRF reference page (default-enabled note, cookie repository, mobile and JavaScript integration, testing, disabling) and the CORS integration page (preflight ordering, UrlBasedCorsConfigurationSource, per-chain configuration). Dropped unconfirmed claims (SameSite advice, allowCredentials and wildcard rules, SpaCsrfTokenRequestHandler by name, 403 and 401 test outcomes) and the MDN source, which was not read.
