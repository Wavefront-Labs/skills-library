---
id: computing-software.web-development.laravel.routing-basics-and-files
name: routing-basics-and-files
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, routes, api-routes, php]
level: intro
status: docs-checked
description: "Define Laravel routes in routes/web.php and routes/api.php, pick router verb methods, and customise route loading in bootstrap/app.php."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Routes live in the `routes` directory and are loaded by `bootstrap/app.php`. `routes/web.php` routes get the `web` middleware group (session state, CSRF protection). Enable a stateless API with `php artisan install:api`, which installs Sanctum and creates `routes/api.php` (the `api` middleware group, `/api` prefix applied automatically).

```php
Route::get('/greeting', function () { return 'Hello World'; });
Route::get('/user', [UserController::class, 'index']);
```

Change the API prefix:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
)
```

Router methods: `get`, `post`, `put`, `patch`, `delete`, `options`, `query` (the QUERY verb; in the `web` group it is CSRF protected). `Route::match(['get', 'post'], '/', ...)` handles several verbs; `Route::any` handles all. When routes share a URI, define the specific-verb routes before `any`, `match` and `redirect` routes.

Type-hint dependencies (for example `Illuminate\Http\Request`) in the callback and the service container injects them.

HTML forms pointing at POST, PUT, PATCH or DELETE routes in the web file need `@csrf` or the request is rejected.

Add a separate route file with a `then` closure in `withRouting`:

```php
then: function () {
    Route::middleware('api')->prefix('webhooks')->name('webhooks.')
        ->group(base_path('routes/webhooks.php'));
},
```

Passing a `using` closure instead means no HTTP routes are registered by the framework and you register all of them yourself.

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed the routes directory and bootstrap/app.php loading, the web and api groups, install:api creating routes/api.php with Sanctum, the /api prefix and apiPrefix customisation, the HTTP verb list including query, match/any ordering, Request injection, CSRF token requirements for web forms, and closure-based route registration.
