---
id: computing-software.web-development.laravel.trusted-proxies-and-hosts
name: trusted-proxies-and-hosts
category: computing-software
field: web-development
product: laravel
tags: [laravel, requests, trusted-proxies, trusted-hosts, load-balancer, https]
level: practitioner
status: docs-checked
description: "Configure Laravel trustProxies and trustHosts in bootstrap/app.php so HTTPS URLs work behind a load balancer and the Host header is restricted."
sources:
  - https://laravel.com/docs/requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Behind a load balancer that terminates TLS, the `url` helper may not generate HTTPS links because traffic is forwarded on port 80. Enable the `TrustProxies` middleware via `trustProxies` in `bootstrap/app.php`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: ['192.168.1.1', '10.0.0.0/8']);
})
```

Trust the proxy headers you need:

```php
$middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB
);
```

AWS Elastic Load Balancing: use `Request::HEADER_X_FORWARDED_AWS_ELB`. A load balancer using the RFC 7239 `Forwarded` header: use `Request::HEADER_FORWARDED`.

If you do not know the balancer IPs (AWS or another cloud provider), trust all: `$middleware->trustProxies(at: '*');`

Trusted hosts: by default Laravel responds regardless of the `Host` header, and that value is used when generating absolute URLs. Prefer configuring Nginx or Apache to restrict hostnames; otherwise enable `TrustHosts`. Hostname strings are regular expressions and other hosts are rejected:

```php
$middleware->trustHosts(at: ['^laravel\.test$']);
$middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
$middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
```

Subdomains of the application URL are trusted by default; `subdomains: false` disables that.

## Checked

2026-11-07

Method: read the whole requests page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed trustProxies(at:), the header constants, the `*` value for load balancers, trustHosts behaviour including the default subdomain trust and subdomains: false, and the closure form. The linked proxy and Symfony pages were not opened.
