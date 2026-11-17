---
id: computing-software.web-development.laravel.route-groups
name: route-groups
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, route-groups, prefix, subdomain, middleware]
level: practitioner
status: docs-checked
description: "Share middleware, controller, subdomain, URI prefix and name prefix across many Laravel routes with Route groups."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Groups share attributes across routes. Nested groups merge: middleware and `where` conditions are merged, names and prefixes are appended, and namespace delimiters and URI slashes are added where appropriate.

Middleware (executed in the listed order):

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () { /* first and second */ });
});
```

Shared controller:

```php
Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

Subdomain routing, capturing a subdomain parameter (the page's example callback takes `$account` first, then `$id`):

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) { });
});
```

URI prefix:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () { /* /admin/users */ });
});
```

Name prefix (include the trailing dot):

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () { })->name('users'); // admin.users
});
```

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed nested group merging, middleware order, controller groups, domain/subdomain groups, prefix and name prefixes with the trailing dot. Corrected: the page does not say subdomain parameters are passed first; the skill now only describes what the example shows.
