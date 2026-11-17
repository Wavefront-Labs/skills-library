---
id: computing-software.web-development.laravel.route-model-binding-explicit
name: route-model-binding-explicit
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, model-binding, route-bind, resolve-route-binding]
level: advanced
status: docs-checked
description: "Register explicit route model bindings with Route::model and Route::bind, or override resolveRouteBinding and resolveChildRouteBinding on the model."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Explicit bindings are defined at the beginning of the `boot` method of `AppServiceProvider`.

Bind a parameter name to a model class:

```php
public function boot(): void
{
    Route::model('user', User::class);
}

Route::get('/users/{user}', function (User $user) { });
```

A request to `users/1` injects the `User` with ID 1; no match gives 404.

Custom resolution logic with `Route::bind`; the closure receives the URI segment value and returns the instance to inject:

```php
Route::bind('user', function (string $value) {
    return User::where('name', $value)->firstOrFail();
});
```

Or override on the Eloquent model:

```php
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

When a route uses implicit binding scoping, `resolveChildRouteBinding($childType, $value, $field)` resolves the child binding of the parent model:

```php
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

## Checked

2026-11-07

Method: read the whole routing page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed Route::model, Route::bind, resolveRouteBinding, resolveChildRouteBinding, and registering bindings in the boot method.
