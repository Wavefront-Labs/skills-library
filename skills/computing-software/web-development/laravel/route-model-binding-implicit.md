---
id: computing-software.web-development.laravel.route-model-binding-implicit
name: route-model-binding-implicit
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, model-binding, eloquent, scoped-bindings, enums]
level: practitioner
status: docs-checked
description: "Implicit route model binding: match variable names to segments, custom keys, RouteKey attribute, scoped bindings, soft deletes, missing() and enums."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A type-hinted Eloquent model whose variable name matches the route segment is injected automatically; a missing model gives 404.

```php
Route::get('/users/{user}', function (User $user) { return $user->email; });
```

Soft-deleted models are not retrieved unless you chain `->withTrashed()`.

Custom key per route: `Route::get('/posts/{post:slug}', ...)`. To make binding always use a column other than `id` for a model class, apply the attribute:

```php
use Illuminate\Database\Eloquent\Attributes\RouteKey;

#[RouteKey('slug')]
class Post extends Model { }
```

Scoping: with a custom-keyed nested parameter, Laravel scopes the child through the parent's relationship (guessed as the plural of the parameter name, here `posts` on `User`).

```php
Route::get('/users/{user}/posts/{post}', fn (User $user, Post $post) => $post)->scopeBindings();
Route::scopeBindings()->group(function () { /* ... */ });
// ->withoutScopedBindings() turns scoping off
```

Customise the not-found result:

```php
Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

Implicit enum binding: type-hint a string-backed enum; the route runs only if the segment is a valid value, otherwise 404.

```php
Route::get('/categories/{category}', function (Category $category) { return $category->value; });
```

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed implicit binding, withTrashed(), {post:slug} custom keys, the RouteKey attribute, child-binding conventions, scopeBindings and withoutScopedBindings, missing(), and enum binding returning 404. Corrected: the sentence about the attribute now matches the page's wording (a column other than id for a given model class).
