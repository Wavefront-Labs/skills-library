---
id: computing-software.web-development.laravel.response-headers-and-cookies
name: response-headers-and-cookies
category: computing-software
field: web-development
product: laravel
tags: [laravel, responses, headers, cookies, cache-control, macros]
level: practitioner
status: docs-checked
description: "Build Laravel responses with headers, cache.headers middleware, cookies (queue, expire, encryption exceptions) and Response::macro."
sources:
  - https://laravel.com/docs/responses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Routes can return strings (full HTTP response), arrays (JSON), Eloquent models and collections (JSON, respecting hidden attributes), or `Illuminate\Http\Response` objects:

```php
return response('Hello World', 200)->header('Content-Type', 'text/plain');
return response($content)->withHeaders(['X-Header-One' => 'Header Value']);
return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

Cache-Control via the `cache.headers` middleware: snake_case directives separated by semicolons; `etag` sets an xxh128 hash of the content as the ETag.

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () { });
```

Cookies (minutes of validity; extra args mirror PHP setcookie):

```php
return response('Hello World')->cookie('name', 'value', $minutes, $path, $domain, $secure, $httpOnly);
Cookie::queue('name', 'value', $minutes);     // no response instance yet
$cookie = cookie('name', 'value', $minutes);  // not sent until attached
return response('Hello World')->cookie($cookie);
return response('Hello World')->withoutCookies(['name', 'email']);
Cookie::expire('name');
```

`EncryptCookies` encrypts and signs all framework cookies. Exempt specific ones in `bootstrap/app.php`; the page says encryption should generally never be disabled:

```php
$middleware->encryptCookies(except: ['cookie_name']);
```

Response macros, usually in `boot` of `AppServiceProvider`:

```php
Response::macro('caps', function (string $value) {
    return Response::make(strtoupper($value));
});
return response()->caps('foo');
```

## Checked

2026-11-07

Method: read the whole responses page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed returning strings, arrays, models and collections, header/withHeaders/withoutHeader, the cache.headers middleware syntax, cookie arguments, Cookie::queue, withoutCookies, Cookie::expire, EncryptCookies and encryptCookies(except:), and registering Response::macro in AppServiceProvider boot. MDN and php.net links were not opened.
