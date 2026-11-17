---
id: computing-software.web-development.laravel.http-rate-limiters
name: http-rate-limiters
category: computing-software
field: web-development
product: laravel
tags: [laravel, rate-limiting, throttle, routing, limit]
level: practitioner
status: docs-checked
description: "Define named rate limiters with RateLimiter::for and Limit, segment with by(), combine limits, count by response, attach with throttle middleware."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Limiters may be defined in `boot` of `App\Providers\AppServiceProvider` with `RateLimiter::for`; the closure receives the request and returns a `Limit` (or an array of limits). Exceeding the limit returns a 429 automatically.

```php
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});

RateLimiter::for('uploads', function (Request $request) {
    return $request->user()?->vipCustomer() ? Limit::none() : Limit::perHour(10);
});
```

Custom 429 response:

```php
Limit::perMinute(1000)->response(function (Request $request, array $headers) {
    return response('Custom response...', 429, $headers);
});
```

Multiple limits are evaluated in array order. If several use the same `by` value, make each unique by prefixing:

```php
return [
    Limit::perMinute(10)->by('minute:'.$request->user()->id),
    Limit::perDay(1000)->by('day:'.$request->user()->id),
];
```

Response-based limiting: `after` receives the response and returns `true` if it should count toward the limit.

```php
Limit::perMinute(10)->by($request->ip())
    ->after(fn (Response $response) => $response->status() === 404);
```

Attach with the throttle middleware:

```php
Route::middleware(['throttle:uploads'])->group(function () { /* ... */ });
```

With Redis as the cache driver, call `$middleware->throttleWithRedis();` in `withMiddleware` in `bootstrap/app.php` to map `throttle` to `ThrottleRequestsWithRedis`.

## Checked

Date: 2026-11-07

Read: routing.md, Rate Limiting (lines 838-1002).

Matched against the page, claim by claim:

- RateLimiter::for in boot of AppServiceProvider -> :847; Limit class -> :865; 429 automatic; response() -> :883-891
- Limit::none() / perHour -> :896-900; by() -> :906-923
- array of limits evaluated in order; unique by prefixes -> :929-949
- after() counts response when true -> :954-971; throttle:name middleware -> :977-989
- throttleWithRedis maps to ThrottleRequestsWithRedis -> :994-1000

Changes made (trims and rewordings):

- "Define limiters in boot" is an example on the page ("may be defined within the boot method", :847); reworded to "may be defined".

Method: documentation only; no commands were run.
