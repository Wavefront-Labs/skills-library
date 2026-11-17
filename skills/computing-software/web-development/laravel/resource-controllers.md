---
id: computing-software.web-development.laravel.resource-controllers
name: resource-controllers
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, resource-routes, crud, api-resource]
level: practitioner
status: docs-checked
description: "Register CRUD routes with Route::resource and apiResource, generate resource controllers, limit actions, handle soft deletes and missing models."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate and register:

```shell
php artisan make:controller PhotoController --resource
php artisan make:controller PhotoController --model=Photo --resource --requests
php artisan make:controller PhotoController --api
```

`--model` type-hints the model; `--requests` generates form requests for store and update; `--api` omits `create` and `edit`.

```php
Route::resource('photos', PhotoController::class);
Route::resources(['photos' => PhotoController::class, 'posts' => PostController::class]);
Route::softDeletableResources([...]); // all use withTrashed
```

Routes created: GET `/photos` index, GET `/photos/create` create, POST `/photos` store, GET `/photos/{photo}` show, GET `/photos/{photo}/edit` edit, PUT/PATCH `/photos/{photo}` update, DELETE `/photos/{photo}` destroy. Route names are `photos.index` and so on.

Partial routes:

```php
Route::resource('photos', PhotoController::class)->only(['index', 'show']);
Route::resource('photos', PhotoController::class)->except(['create', 'store', 'update', 'destroy']);
Route::apiResource('photos', PhotoController::class); // no create or edit
Route::apiResources([...]);
```

Missing implicit model (default 404):

```php
Route::resource('photos', PhotoController::class)
    ->missing(fn (Request $request) => Redirect::route('photos.index'));
```

Soft-deleted models: `->withTrashed()` allows them for `show`, `edit` and `update`; pass an array such as `->withTrashed(['show'])` for a subset.

Supplemental routes must be defined before the `Route::resource` call, or the resource routes may take precedence:

```php
Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

## Checked

2026-11-07

Method: read the whole controllers page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed make:controller --resource/--model/--requests/--api, Route::resource and resources, softDeletableResources, the seven-route table and names, only/except, apiResource, missing(), withTrashed() with an action subset, and the warning about supplemental routes. Read the controllers page in full (812 lines).
