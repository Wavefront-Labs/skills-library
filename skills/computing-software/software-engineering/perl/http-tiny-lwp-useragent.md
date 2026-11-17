---
id: computing-software.software-engineering.perl.http-tiny-lwp-useragent
name: http-tiny-lwp-useragent
category: computing-software
field: software-engineering
product: perl
tags: [perl, http-tiny, lwp-useragent, ssl-certificates, http-timeouts, http-requests, http-tiny-lwp-useragent, perl-http-clients]
level: practitioner
status: docs-checked
description: "Make HTTP requests with core HTTP::Tiny: timeouts, TLS verification, redirects, error responses (status 599); points to LWP::UserAgent for larger needs."
sources: ["https://perldoc.perl.org/HTTP::Tiny"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP::Tiny (and when to reach for LWP::UserAgent)

**Goal:** reliable outbound HTTP.

```perl
use HTTP::Tiny;
my $http = HTTP::Tiny->new(timeout => 10, agent => 'my-tool/1.0', verify_SSL => 1);
my $res = $http->get($url, { headers => { Accept => 'application/json' } });
die "GET $url failed: $res->{status} $res->{reason}\n" unless $res->{success};
my $body = $res->{content};                         # raw bytes
my $r2 = $http->post_form($url, { a => 1 });
my $r3 = $http->request('PUT', $url, { content => $json, headers => { 'Content-Type' => 'application/json' } });
```

## Facts from the HTTP::Tiny documentation (version 0.096)
- It is a small HTTP/1.1 client "without the overhead of a large framework like LWP::UserAgent"; it supports proxies and redirection, and cookies need `HTTP::CookieJar` or an equivalent class.
- `timeout` is in seconds, default 60; a socket open, read or write that takes longer gives status 599.
- Any error during execution gives pseudo status **599** with reason "Internal Exception", and `content` holds the error text. `success` is true only for 2XX.
- `verify_SSL` defaults to true (changed from false in 0.083). Setting environment variable `PERL_HTTP_TINY_SSL_INSECURE_BY_DEFAULT=1` flips the default to no verification when `verify_SSL` is not set; avoid.
- HTTPS needs `IO::Socket::SSL` 1.56+ and `Net::SSLeay` 1.49+; `HTTP::Tiny->can_ssl` reports whether they are present.
- CA certificates come from `IO::Socket::SSL::default_ca()` (honours `SSL_CERT_FILE` and `SSL_CERT_DIR`, falls back to `Mozilla::CA`). To use your own CA file: `SSL_options => { SSL_ca_file => $path }`.
- `max_redirect` default 5. Caller-supplied `Authorization`, `Cookie` and `Proxy-Authorization` headers are stripped on cross-origin redirects, and https-to-http redirects are refused, unless you set `allow_credentialed_redirects` or `allow_downgrade`.
- `max_size` makes oversized responses return 599. `keep_alive` defaults to 1 (one destination only).
- Proxies default from `http_proxy`, `https_proxy` and `all_proxy` environment variables; `no_proxy` lists exclusions.
- Request and response content are raw bytes; encoding and decoding is the caller's job. URLs must already be escaped, and method names are case-sensitive (`GET`, not `get`).
- `post_form` sends `application/x-www-form-urlencoded`; `mirror` saves to a file using `If-Modified-Since` and treats 304 as success.

## Rules
- Always set a timeout and check `success`; handle 599 separately from HTTP error statuses.
- Do not disable certificate verification to "fix" errors; fix the CA setup instead.
- Retry only idempotent requests, with backoff.
- Need cookies, rich response objects or decoded text? Use LWP::UserAgent (CPAN); this skill does not cover its API because its documentation page could not be read here.

## Self-check
- [ ] A request to a closed port returns failure (status 599) within the timeout, not a hang.

## Checked
Confirmed on the perldoc HTTP::Tiny page (version 0.096): constructor attributes and defaults, 599 behaviour, TLS requirements and CA discovery, redirect rules, raw-bytes handling, post_form and mirror.
Removed: all LWP::UserAgent claims (metacpan page blocked), the URI query_form and JSON decoding advice, and the scraping remark.
Method: docs-only read of cited pages, 2026-11-08
