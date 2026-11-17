---
id: computing-software.web-development.laravel.route-redirect-view-and-list
name: route-redirect-view-and-list
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, redirect, view-routes, route-list, artisan]
level: intro
status: docs-checked
description: "Use Route::redirect, permanentRedirect and Route::view shortcuts, and inspect routes with php artisan route:list options."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shortcuts avoid a full route or controller for simple cases.

Redirects return `302` by default:

```php
Route::redirect('/here', '/there');
Route::redirect('/here', '/there', 301);
Route::permanentRedirect('/here', '/there'); // 301
```

Reserved parameter names in redirect routes: `destination` and `status`.

View routes take a URI, a view name and optional data:

```php
Route::view('/welcome', 'welcome');
Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

Reserved parameter names in view routes: `view`, `data`, `status` and `headers`.

List routes:

```shell
php artisan route:list
php artisan route:list -v            # show middleware
php artisan route:list -vv           # expand middleware groups
php artisan route:list --path=api    # only URIs containing a string
php artisan route:list --except-vendor
php artisan route:list --only-vendor
```

By default `route:list` does not display the middleware assigned to each route; add `-v` for that.

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed Route::redirect (302 default, third argument, permanentRedirect), the reserved destination and status parameters, Route::view and its reserved parameters, and route:list with -v, -vv, --path, --except-vendor and --only-vendor.
