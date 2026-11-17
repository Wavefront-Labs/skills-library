---
id: computing-software.web-development.laravel.route-parameters-and-constraints
name: route-parameters-and-constraints
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, route-parameters, regex-constraints, where]
level: practitioner
status: docs-checked
description: "Capture required and optional route parameters, constrain them with where helpers or Route::pattern, and allow encoded slashes."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Parameters sit in `{}` braces, use alphabetic characters and underscores, and are injected by order, not by argument name. List them after container-injected dependencies.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) { });
Route::get('/user/{id}', function (Request $request, string $id) { });
```

Optional parameter: add `?` and give the variable a default.

```php
Route::get('/user/{name?}', function (?string $name = null) { return $name; });
```

Constraints (a non-matching request returns 404):

```php
->where('name', '[A-Za-z]+');
->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
->whereNumber('id')->whereAlpha('name');
->whereAlphaNumeric('name');
->whereUuid('id');
->whereUlid('id');
->whereIn('category', ['movie', 'song', 'painting']);
```

Global constraint, in `boot` of `App\Providers\AppServiceProvider`:

```php
Route::pattern('id', '[0-9]+');
```

All characters except `/` are allowed in parameter values. To allow `/`, use `->where('search', '.*')`; encoded forward slashes are only supported in the last route segment.

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed brace syntax, underscore allowance, parameter injection order and listing parameters after dependencies, optional parameters with defaults, where/whereNumber/whereAlpha/whereAlphaNumeric/whereUuid/whereUlid/whereIn, 404 on constraint failure, Route::pattern in AppServiceProvider boot, the `.*` slash workaround and the last-segment-only note.
