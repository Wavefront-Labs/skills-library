---
id: computing-software.web-development.laravel.rate-limiter-attempts
name: rate-limiter-attempts
category: computing-software
field: web-development
product: laravel
tags: [laravel, rate-limiting, ratelimiter, cache, throttling]
level: practitioner
status: docs-checked
description: "Rate limit any action with the RateLimiter facade: attempt, tooManyAttempts, increment, remaining, availableIn, clear, and the cache limiter store."
sources:
  - https://laravel.com/docs/rate-limiting
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `RateLimiter` facade limits any action within a time window, backed by your cache. It uses the `default` cache store unless the `cache` config file defines a `limiter` key:

```php
'default' => env('CACHE_STORE', 'database'),
'limiter' => 'redis',
```

`attempt` returns `false` when no attempts remain, otherwise the callback's result or `true`. The optional fourth argument is the decay rate in seconds:

```php
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function () { /* Send message... */ },
    $decayRate = 120,
);
if (! $executed) { return 'Too many messages sent!'; }
```

Manual control:

```php
if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);
    return 'You may try again in '.$seconds.' seconds.';
}
RateLimiter::increment('send-message:'.$user->id);
```

For endpoints with many simultaneous requests, check the value returned by `increment` instead of separate `tooManyAttempts` and `increment` calls. On the `redis`, `memcached` or `database` stores it increments atomically so each concurrent request gets a unique count:

```php
if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) { /* too many */ }
```

Other calls: `RateLimiter::remaining($key, $perMinute)`, `RateLimiter::increment($key, amount: 5)`, and `RateLimiter::clear($key)` to reset attempts.

For rate limiting incoming HTTP requests, the page points to the rate limiter middleware docs (the `throttle` middleware on the routing page).

## Checked

2026-11-07

Method: read the whole rate-limiting page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed the default cache store versus the `limiter` cache key, attempt return values, the decay argument, tooManyAttempts/availableIn/increment, atomic increment on redis, memcached and database, remaining, increment(amount:) and clear. Corrected: the closing note now says the rate-limiting page only points to the rate limiter middleware docs; the `throttle` middleware name is confirmed on the routing page, which is now listed in sources.
