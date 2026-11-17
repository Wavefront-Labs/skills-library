---
id: computing-software.web-development.wordpress.http-api-wp-remote-get
name: http-api-wp-remote-get
category: computing-software
field: web-development
product: wordpress
tags: [wp-remote-get, wordpress-http-api, wp-remote-post, external-apis, wordpress]
level: practitioner
status: docs-checked
description: "Calling external services with the WordPress HTTP API: wp_remote_get/post, timeouts and errors, wp_safe_remote_* for user URLs, caching and mocking."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/http.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-http.php
  - https://developer.wordpress.org/plugins/http-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP API (wp_remote_get / wp_remote_post)

Use the HTTP API instead of curl or `file_get_contents`: it goes through WordPress's filters, SSL settings and outbound-request restrictions.

## 1. GET with error handling
```php
function acme_get_rates() {
    $cached = get_transient( 'acme_rates' );
    if ( false !== $cached ) return $cached;

    $response = wp_remote_get( 'https://api.example.com/v1/rates', [
        'timeout' => 5,                                   // default is 5 seconds (filter http_request_timeout)
        'headers' => [ 'Authorization' => 'Bearer ' . ACME_API_KEY, 'Accept' => 'application/json' ],
        'user-agent' => 'AcmePlugin/1.2; ' . home_url(),
    ] );
    if ( is_wp_error( $response ) ) {                     // network/DNS/timeout errors
        error_log( 'acme rates: ' . $response->get_error_message() );
        return [];
    }
    $code = wp_remote_retrieve_response_code( $response );
    if ( 200 !== $code ) { error_log( "acme rates: HTTP $code" ); return []; }
    $data = json_decode( wp_remote_retrieve_body( $response ), true );
    if ( ! is_array( $data ) ) return [];
    set_transient( 'acme_rates', $data, 15 * MINUTE_IN_SECONDS );
    return $data;
}
```
- Non-2xx responses are **not** WP_Errors - check the status code.
- Cache results (transients, object cache) so a slow API does not slow every page render.

## 2. POST JSON
```php
$response = wp_remote_post( $url, [
    'timeout' => 10,
    'headers' => [ 'Content-Type' => 'application/json' ],
    'body'    => wp_json_encode( $payload ),
] );
```
`wp_remote_request( $url, [ 'method' => 'PATCH', ... ] )` for other verbs; `wp_remote_head` for HEAD. For non-GET/HEAD requests the request arguments are sent in the request body.

## 3. User-supplied URLs
Use `wp_safe_remote_get()` / `wp_safe_remote_post()` for any URL influenced by users (link previews, webhooks, imports): they set `reject_unsafe_urls`, so URLs go through `wp_http_validate_url()`, which rejects hosts resolving to loopback and private ranges (for example 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) and ports other than 80, 443 and 8080 (filter `http_allowed_safe_ports`), reducing SSRF risk. Still validate scheme and host against an allowlist where possible, and disable redirects (`'redirection' => 0`) if you validate the URL.

## 4. Configuration and filters
- `sslverify` defaults to true; keep it that way in production.
- `http_request_args` filter to adjust requests globally; `pre_http_request` to short-circuit (mocking in tests, blocking).
- `WP_HTTP_BLOCK_EXTERNAL` set to true in wp-config blocks external requests; `WP_ACCESSIBLE_HOSTS` is a comma-separated list of hosts (wildcards allowed) that may still be called.

## 5. Testing
```php
add_filter( 'pre_http_request', fn( $pre, $args, $url ) => str_contains( $url, 'api.example.com' )
    ? [ 'headers' => [], 'body' => '{"usd":1}', 'response' => [ 'code' => 200, 'message' => 'OK' ], 'cookies' => [], 'filename' => null ]
    : $pre, 10, 3 );
```

## Verify
- [ ] Timeouts set; WP_Error and non-200 handled; results cached; user URLs go through wp_safe_remote_*; tests mock HTTP via pre_http_request.

## Checked

2026-10-25: against wordpress-develop trunk source (`http.php`, `class-wp-http.php`; last commit 2026-10-25). Confirmed: default args (`timeout` 5, `redirection` 5, `sslverify` true, `user-agent`), `reject_unsafe_urls` handling in `wp_safe_remote_*` and the `wp_http_validate_url()` IP ranges and allowed ports 80/443/8080, `http_request_args` and `pre_http_request` filters, `WP_HTTP_BLOCK_EXTERNAL`/`WP_ACCESSIBLE_HOSTS`, `wp_remote_head`/`wp_remote_request`, body format for non-GET requests. Removed the redundant `data_format` argument and unconfirmed claims about proxies and cron.

Method: documentation only; no commands were run.
