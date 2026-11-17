---
id: computing-software.web-development.laravel.middleware-defining-and-params
name: middleware-defining-and-params
category: computing-software
field: web-development
product: laravel
tags: [laravel, middleware, handle, parameters, terminable]
level: practitioner
status: docs-checked
description: "Write Laravel middleware with make:middleware, run logic before or after the request, pass parameters, and use terminate after the response."
sources:
  - https://laravel.com/docs/middleware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```shell
php artisan make:middleware EnsureTokenIsValid
```

Classes land in `app/Http/Middleware`, are resolved via the container (constructor type-hints work), and pass the request on by calling `$next($request)`.

```php
public function handle(Request $request, Closure $next): Response
{
    if ($request->input('token') !== 'my-secret-token') {
        return redirect('/home');
    }
    return $next($request);
}
```

Before vs after: do work before calling `$next` to act before the app handles the request; assign `$response = $next($request);` first, then work, then `return $response;` to act after.

Parameters arrive after `$next`:

```php
public function handle(Request $request, Closure $next, string $role): Response { /* ... */ }

Route::put('/post/{id}', fn (string $id) => ...)->middleware(EnsureUserHasRole::class.':editor');
// several parameters, comma separated
->middleware(EnsureUserHasRole::class.':editor,publisher');
```

Terminable middleware: define `terminate(Request $request, Response $response): void`. With a FastCGI server it is called automatically after the response is sent. Add the middleware to routes or global middleware in `bootstrap/app.php`.

Laravel resolves a fresh instance for `terminate`. To reuse the same instance as `handle`, register it as a singleton in `register` of `AppServiceProvider`:

```php
$this->app->singleton(TerminatingMiddleware::class);
```

## Checked

Date: 2026-11-07

Read: middleware.md, Defining Middleware, Middleware Parameters, Terminable Middleware (lines 21-110, 418-520).

Matched against the page, claim by claim:

- make:middleware, app/Http/Middleware, container-resolved -> :27-30, :64
- handle with $next; before/after -> :50-55, :69-113
- parameters after $next, colon and comma syntax -> :423, :452-468
- terminate with FastCGI, request+response -> :473, :499-506; fresh instance, singleton in register -> :508-519

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
