---
id: computing-software.web-development.laravel.nested-resource-routes
name: nested-resource-routes
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, resource-routes, nested-resources, shallow, scoped]
level: practitioner
status: docs-checked
description: "Nest, shallow-nest, scope, rename and localise Laravel resource routes with dot notation, shallow, scoped, names, parameters and resourceVerbs."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nest with dot notation; URIs look like `/photos/{photo}/comments/{comment}`:

```php
Route::resource('photos.comments', PhotoCommentController::class);
```

Shallow nesting drops the parent ID where the child ID is unique. Index, create and store keep the parent (`/photos/{photo}/comments`); show, edit, update and destroy use `/comments/{comment}`:

```php
Route::resource('photos.comments', CommentController::class)->shallow();
```

Scoped nesting turns on implicit-binding scoping and picks the child field:

```php
Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
// /photos/{photo}/comments/{comment:slug}
```

Laravel guesses the parent relationship name as the plural of the parameter (`comments` on `Photo`).

Rename routes:

```php
Route::resource('photos', PhotoController::class)->names(['create' => 'photos.build']);
```

Rename parameters (default is the singular of the resource name):

```php
Route::resource('users', AdminUserController::class)->parameters(['users' => 'admin_user']);
// /users/{admin_user}
```

Localise the `create` and `edit` verbs at the start of `boot` in `AppServiceProvider`; the pluralizer language is configured separately in localization:

```php
Route::resourceVerbs(['create' => 'crear', 'edit' => 'editar']);
// /publicacion/crear and /publicacion/{publicacion}/editar
```

## Checked

Date: 2026-11-07

Read: controllers.md, Nested Resources, Scoping Nested Resources, Shallow Nesting, Naming Resource Routes, Naming Resource Route Parameters, Scoping Resource Routes, Localizing Resource URIs (lines 440-560).

Matched against the page, claim by claim:

- dot notation photos.comments -> section Nested Resources; shallow() table index/create/store keep parent, show/edit/update/destroy do not -> :463-483
- names([...]) -> :495-497; parameters() with singularized default -> :503
- scoped([comment=>slug]); parent relationship guessed as plural of parameter (comments on Photo) -> :522-538
- resourceVerbs in boot of AppServiceProvider; pluralizer languages configured elsewhere -> :543-558

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
