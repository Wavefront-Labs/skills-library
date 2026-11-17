---
id: computing-software.web-development.micronaut.micronaut-client-filters
name: micronaut-client-filters
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, client-filter, request-filter, filter-matcher, basic-auth]
level: practitioner
status: docs-checked
description: "Write Micronaut @ClientFilter classes that add auth to matching requests, inject another client via BeanProvider, and match filters by custom annotation."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientFilter.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: apply the same headers or parameters to a set of client requests without touching each call.

## Path-matched filter

```java
@ClientFilter("/repos/**")
class BintrayFilter {
    final String username;
    final String token;

    BintrayFilter(@Value("${bintray.username}") String username,
                  @Value("${bintray.token}") String token) {
        this.username = username;
        this.token = token;
    }

    @RequestFilter
    public void filter(MutableHttpRequest<?> request) {
        request.basicAuth(username, token);
    }
}
```

The path pattern restricts the filter to a subset of paths. Filter mechanics are the same as server filters.

## Injecting another client into a filter

Building a `ReactorHttpClient` resolves all `ClientFilter` beans, so injecting a client (or any `@Client` bean) into a filter is a circular dependency. Inject a `BeanProvider` instead and call `get()` when needed:

```java
@Requires(env = Environment.GOOGLE_COMPUTE)
@ClientFilter(patterns = "/google-auth/api/**")
public class GoogleAuthFilter {
    private final BeanProvider<HttpClient> authClientProvider;

    public GoogleAuthFilter(BeanProvider<HttpClient> httpClientProvider) {
        this.authClientProvider = httpClientProvider;
    }

    @RequestFilter
    @ExecuteOn(TaskExecutors.BLOCKING)
    public void filter(MutableHttpRequest<?> request) throws Exception {
        String t = authClientProvider.get().toBlocking().retrieve(HttpRequest.GET(uri)
            .header("Metadata-Flavor", "Google"));
        request.bearerAuth(t);
    }
}
```

(`uri` is built by a helper in the guide's full example.)

## Match by annotation instead of URL

Create an annotation carrying `@FilterMatcher`, put it on both the client and the filter:

```java
@FilterMatcher
@Documented
@Retention(RUNTIME)
@Target({TYPE, PARAMETER})
public @interface BasicAuth { }

@BasicAuth
@Client("/message")
public interface BasicAuthClient { @Get String getMessage(); }

@BasicAuth
@Singleton
@ClientFilter
public class BasicAuthClientFilter {
    @RequestFilter
    public void filter(MutableHttpRequest<?> request) { request.basicAuth("user", "pass"); }
}
```

Gotcha: `@Filter` normally makes a filter a singleton; since it is not used here, apply the scope (`@Singleton`) yourself.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
