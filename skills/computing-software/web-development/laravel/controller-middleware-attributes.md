---
id: computing-software.web-development.laravel.controller-middleware-attributes
name: controller-middleware-attributes
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, middleware, php-attributes, authorization]
level: practitioner
status: docs-checked
description: "Assign middleware inside Laravel controllers with HasMiddleware or the Middleware, WithoutMiddleware and Authorize PHP attributes."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Route-level: `Route::get('/profile', [UserController::class, 'show'])->middleware('auth');`

In the controller, implement `HasMiddleware` with a static `middleware` method; `only` and `except` limit actions and closures are allowed:

```php
use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }
}
```

Attributes do the same. Method-level attributes merge with class-level ones:

```php
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
#[Middleware('log', only: ['index'])]
class UserController
{
    #[Middleware('subscribed')]
    public function index() { }
}
```

Exclude middleware with `WithoutMiddleware` (supports `only` and `except`):

```php
#[WithoutMiddleware('subscribed', except: ['index'])]
class UserController
{
    #[WithoutMiddleware(EnsureTokenIsValid::class)]
    public function index() { }
}
```

Class-level `WithoutMiddleware` is inherited by child controllers. It can only remove route middleware, not global middleware.

`Authorize` is a shortcut for the `can` middleware. First argument is the ability; second is the model class, route parameter or parameters passed to the policy:

```php
#[Authorize('create', [Comment::class, 'post'])]
public function store(Post $post) { }

#[Authorize('delete', 'comment')]
public function destroy(Comment $comment) { }
```

## Checked

Date: 2026-11-07

Read: controllers.md, Controller Middleware, Middleware Attributes, Authorization Attributes (lines 114-285).

Matched against the page, claim by claim:

- route ->middleware(auth) -> :121; HasMiddleware + static middleware() + new Middleware(only/except) -> :124-150
- closures allowed -> :152-169
- attributes Illuminate\Routing\Attributes\Controllers\Middleware with only/except -> :181-190; method-level merged with class level -> :192
- WithoutMiddleware with only/except; inherited by child controllers; route middleware only -> :225-251
- Authorize shortcut for can; first arg ability, second model class/route parameter(s) -> :256-283

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
