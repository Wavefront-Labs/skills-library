---
id: computing-software.web-development.laravel.request-inspection
name: request-inspection
category: computing-software
field: web-development
product: laravel
tags: [laravel, requests, headers, content-negotiation, url, ip]
level: practitioner
status: docs-checked
description: "Inspect the Laravel request: path, URL, host, method, headers, bearer token, IP, content negotiation with accepts, prefers and expectsJson."
sources:
  - https://laravel.com/docs/requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type-hint `Illuminate\Http\Request` on a route closure or controller method (route parameters go after it). It extends Symfony's request.

Path and route:

```php
$request->path();                  // foo/bar for http://example.com/foo/bar
$request->is('admin/*');           // wildcard path match
$request->routeIs('admin.*');      // named route match
$request->url();                   // no query string
$request->fullUrl();               // with query string
$request->fullUrlWithQuery(['type' => 'phone']);
$request->fullUrlWithoutQuery(['type']);
$request->host();                  // localhost
$request->httpHost();              // localhost:8000
$request->schemeAndHttpHost();     // http://localhost:8000
$request->method();
$request->isMethod('post');
```

Headers:

```php
$request->header('X-Header-Name', 'default'); // null if absent and no default
$request->hasHeader('X-Header-Name');
$request->bearerToken();                      // empty string if absent
```

IP: `$request->ip()`; `$request->ips()` includes forwarded client IPs, with the original client at the end. IP addresses are untrusted, user-controlled input and should be used for information only.

Content negotiation:

```php
$request->getAcceptableContentTypes();
$request->accepts(['text/html', 'application/json']);
$request->prefers(['text/html', 'application/json']); // null if none accepted
$request->expectsJson();
$request->wantsMarkdown();   // most preferred is text/markdown
$request->acceptsMarkdown();
```

PSR-7: install `symfony/psr-http-message-bridge` and `nyholm/psr7`, then type-hint `Psr\Http\Message\ServerRequestInterface`. A returned PSR-7 response converts back automatically.

## Checked

2026-11-07

Method: read the whole requests page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed Request type-hinting and parameter ordering, the path/url/host/method helpers, header and bearerToken behaviour, ip/ips, content negotiation methods and the PSR-7 bridge packages. The linked Symfony Request and proxy pages were not opened.
