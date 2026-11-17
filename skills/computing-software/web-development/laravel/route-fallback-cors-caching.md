---
id: computing-software.web-development.laravel.route-fallback-cors-caching
name: route-fallback-cors-caching
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, fallback, cors, route-cache, method-spoofing]
level: practitioner
status: docs-checked
description: "Fallback routes, form method spoofing, CORS config publishing and route:cache for production in Laravel routing."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fallback route: runs when no other route matches. It is typically defined in `routes/web.php`, so the `web` middleware group applies; you may add more middleware.

```php
Route::fallback(function () {
    // ...
});
```

Form method spoofing: HTML forms do not support PUT, PATCH or DELETE, so add a hidden `_method` field, or use the `@method` Blade directive:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

CORS: `OPTIONS` requests are handled automatically by the `HandleCors` middleware in the global stack. To customise values, publish the config, which creates `config/cors.php`:

```shell
php artisan config:publish cors
```

Route cache: in production it drastically cuts route registration time. Generate it only during deployment, because new routes need a fresh cache:

```shell
php artisan route:cache
php artisan route:clear
```

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed Route::fallback, HTTP method spoofing with @method and _method, the HandleCors middleware in the global stack, config:publish cors, and route:cache/route:clear. Corrected: the page says the fallback route is typically defined in routes/web.php so the web middleware applies; the skill had stated it as always.
