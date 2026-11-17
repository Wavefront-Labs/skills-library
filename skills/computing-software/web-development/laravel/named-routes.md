---
id: computing-software.web-development.laravel.named-routes
name: named-routes
category: computing-software
field: web-development
product: laravel
tags: [laravel, routing, named-routes, url-generation, redirects]
level: intro
status: docs-checked
description: "Name routes with ->name(), generate URLs and redirects with route() and to_route(), pass parameters, and test the current route name."
sources:
  - https://laravel.com/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Chain `name` onto a route; names should always be unique.

```php
Route::get('/user/profile', [UserProfileController::class, 'show'])->name('profile');
```

Generate URLs and redirects:

```php
$url = route('profile');
return redirect()->route('profile');
return to_route('profile');
```

Parameters go in the second argument and fill the URI placeholders; extra keys become the query string:

```php
Route::get('/user/{id}/profile', function (string $id) { })->name('profile');
$url = route('profile', ['id' => 1, 'photos' => 'yes']);
// http://example.com/user/1/profile?photos=yes
```

For request-wide default values for URL parameters (such as locale) use `URL::defaults`.

Check the current route name, for example in middleware:

```php
if ($request->route()->named('profile')) {
    // ...
}
```

Or use the `Route` facade: `Route::current()`, `Route::currentRouteName()`, `Route::currentRouteAction()`.

Route group name prefixes: `Route::name('admin.')->group(...)` prepends the string exactly as given, so include the trailing `.`.

## Checked

Date: 2026-11-07

Read: routing.md, Named Routes, Route Name Prefixes, Accessing the Current Route (lines 414-500, 564-577, 1023-1037).

Matched against the page, claim by claim:

- name() chain and controller form; names should always be unique -> :416-434
- route(), redirect()->route(), to_route() -> :443-448; parameters and query string -> :451-471
- URL::defaults -> :474; named() on current route -> :493; Route::current/currentRouteName/currentRouteAction -> :1032-1034
- Route::name(admin.) exact prefix, trailing dot -> :568-575

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
