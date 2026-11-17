---
id: computing-software.web-development.laravel.resource-route-middleware
name: resource-route-middleware
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, middleware, resource-routes, middlewarefor]
level: practitioner
status: docs-checked
description: "Apply or exclude middleware per action on Laravel resource and singleton routes with middleware, middlewareFor and withoutMiddlewareFor."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three methods give per-action control over resource routes.

All routes of a resource or singleton:

```php
Route::resource('users', UserController::class)->middleware(['auth', 'verified']);
Route::singleton('profile', ProfileController::class)->middleware('auth');
```

Specific actions with `middlewareFor` (action or array of actions, middleware or array):

```php
Route::resource('users', UserController::class)->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```

It also works on singleton and API singleton resources:

```php
Route::singleton('profile', ProfileController::class)->middlewareFor('show', 'auth');
Route::apiSingleton('profile', ProfileController::class)->middlewareFor(['show', 'update'], 'auth');
```

Exclude middleware from particular actions with `withoutMiddlewareFor` (the page's example sits inside a group that applies `auth`, `verified` and `subscribed`):

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

## Checked

2026-11-07

Method: read the whole controllers page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed middleware, middlewareFor with string, array and chained forms, singleton and apiSingleton variants, and withoutMiddlewareFor. Corrected: the page does not say the excluded middleware is inherited from a group; the wording now says the page's example sits inside a group.
