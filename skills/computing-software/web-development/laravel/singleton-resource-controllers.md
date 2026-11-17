---
id: computing-software.web-development.laravel.singleton-resource-controllers
name: singleton-resource-controllers
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, singleton-resources, routing, api-singleton]
level: advanced
status: docs-checked
description: "Register single-instance resources with Route::singleton, nest them, and enable creatable, destroyable and apiSingleton variants."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A singleton resource has one and only one instance (a user's profile, an image's thumbnail).

```php
Route::singleton('profile', ProfileController::class);
```

Routes registered carry no identifier and no creation routes:
- GET `/profile` show (`profile.show`)
- GET `/profile/edit` edit (`profile.edit`)
- PUT/PATCH `/profile` update (`profile.update`)

Nested inside a standard resource, `photos` gets the standard routes and `thumbnail` is a singleton:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
// /photos/{photo}/thumbnail, /photos/{photo}/thumbnail/edit
```

`creatable()` adds create (`/photos/{photo}/thumbnail/create`), store (POST) and destroy (DELETE) routes:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

`destroyable()` registers the DELETE route but not creation or storage:

```php
Route::singleton(...)->destroyable();
```

API singletons skip `create` and `edit`; `creatable` on them registers `store` and `destroy`:

```php
Route::apiSingleton('profile', ProfileController::class);
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

## Checked

2026-11-07

Method: read the whole controllers page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed the singleton route tables, nested singleton, creatable and destroyable options, and apiSingleton behaviour with creatable. Read the controllers page in full.
