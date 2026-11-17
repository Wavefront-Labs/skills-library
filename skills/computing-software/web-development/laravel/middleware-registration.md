---
id: computing-software.web-development.laravel.middleware-registration
name: middleware-registration
category: computing-software
field: web-development
product: laravel
tags: [laravel, middleware, bootstrap-app, aliases, groups, priority]
level: practitioner
status: docs-checked
description: "Register Laravel middleware in bootstrap/app.php: global stack, route assignment, exclusion, groups, aliases and execution priority."
sources:
  - https://laravel.com/docs/middleware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registration happens in the `withMiddleware` closure in `bootstrap/app.php`.

Global: `$middleware->append(EnsureTokenIsValid::class);` (end) or `prepend` (start). To manage the default stack yourself pass it to `$middleware->use([...])`.

Routes: `->middleware(EnsureTokenIsValid::class)` or an array. Exclude from a group's route with `->withoutMiddleware([...])`, or from a whole group with `Route::withoutMiddleware([...])->group(...)`. It can only remove route middleware, not global middleware.

Groups:

```php
$middleware->appendToGroup('group-name', [First::class, Second::class]);
$middleware->prependToGroup('group-name', [First::class, Second::class]);
Route::middleware(['group-name'])->group(function () { });
```

Default `web` group: EncryptCookies, AddQueuedCookiesToResponse, StartSession, ShareErrorsFromSession, PreventRequestForgery, SubstituteBindings. Default `api` group: SubstituteBindings. Modify them:

```php
$middleware->web(append: [EnsureUserIsSubscribed::class]);
$middleware->api(prepend: [EnsureTokenIsValid::class]);
$middleware->web(replace: [StartSession::class => StartCustomSession::class]);
$middleware->web(remove: [StartSession::class]);
```

Redefine a whole group with `$middleware->group('web', [...])`.

Aliases:

```php
$middleware->alias(['subscribed' => EnsureUserIsSubscribed::class]);
```

Built-in aliases include `auth`, `auth.basic`, `auth.session`, `cache.headers`, `can`, `guest`, `password.confirm`, `precognitive`, `signed`, `throttle`, `verified`.

Priority, when order cannot be controlled at assignment:

```php
$middleware->priority([ /* full ordered list */ ]);
$middleware->prependToPriorityList(before: SubstituteBindings::class, prepend: EnsureTokenIsValid::class);
$middleware->appendToPriorityList(after: SubstituteBindings::class, append: EnsureUserIsSubscribed::class);
```

## Checked

Date: 2026-11-07

Read: middleware.md, Registering Middleware (lines 115-417).

Matched against the page, claim by claim:

- append/prepend/use in withMiddleware -> :127-150
- middleware(), array, withoutMiddleware, group exclusion, route middleware only -> :164-206
- appendToGroup/prependToGroup -> :218-226; web/api default group members -> :251-264; web()/api() append/prepend/replace/remove -> :275-302; group() redefine -> :311
- alias() and default alias table -> :341, :361-372
- priority(), prependToPriorityList, appendToPriorityList -> :383, :404-412

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
