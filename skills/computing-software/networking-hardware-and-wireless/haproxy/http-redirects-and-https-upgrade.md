---
id: computing-software.networking-hardware-and-wireless.haproxy.http-redirects-and-https-upgrade
name: http-redirects-and-https-upgrade
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, redirect-scheme, redirect-location, http-to-https, redirect-prefix]
level: practitioner
status: docs-checked
description: "Redirect HTTP to HTTPS and canonicalise hosts or paths in HAProxy with redirect scheme, prefix and location, codes and drop-query."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http redirects and https upgrade
`redirect location|prefix|scheme <value> [code <code>] [options] [if|unless <condition>]` returns a redirect; the same forms exist as `http-request redirect` rules, where the value is a log-format expression and so can include dynamic values. With no condition the redirect is unconditional; with no code it is a 302.

```
frontend fe_http
    bind :80
    redirect scheme https code 301 unless { ssl_fc }

frontend fe_www
    bind :80
    http-request redirect code 301 location http://www.%[hdr(host)]%[capture.req.uri] unless { hdr_beg(host) -i www }
```
Forms: `scheme` builds `<scheme>://<first Host header><path and query>` (mostly used for HTTP to HTTPS; an empty host if no Host header); `prefix` concatenates the prefix with the full URI path and query (a prefix of exactly `/` inserts nothing); `location` places the value in `Location` as is. Codes supported are 301 (permanent, may be cached), 302 (temporary), 303 (browser fetches with GET), 307 (same method reused) and 308 (301 with same method).

Options: `drop-query` (prefix redirects only) removes the query string; `append-slash` with `drop-query` redirects URLs lacking a trailing `/` (a 301 is preferred); `ignore-empty` skips the rule when a log-format location is empty, for mass redirects through a map such as `http-request redirect code 301 location %[path,map_str(old-blog-articles.map)] ignore-empty`; `set-cookie NAME[=value]` and `clear-cookie NAME[=]` add a `Set-Cookie` header (a bare name differs from `NAME=` for clearing).

Verify: `haproxy -c -f <config>`, then fetch an HTTP URL and check the response status and `Location` header.

## Checked
2026-11-03. Confirmed against configuration.html `redirect` keyword (arguments, codes, options and examples) and the `http-request redirect` examples that use `map_str` and `ignore-empty`. Removed: the ACME-challenge example, the `X-Forwarded-Proto` loop gotcha (not in the docs), the `regsub` redirect example, the claim that the `redirect` keyword is "older" and the claim that it runs "in rule order", and the `curl -sI` verify output.
Method: documentation only; no commands were run.
