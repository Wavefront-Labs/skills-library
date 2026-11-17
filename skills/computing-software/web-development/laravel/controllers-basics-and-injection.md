---
id: computing-software.web-development.laravel.controllers-basics-and-injection
name: controllers-basics-and-injection
category: computing-software
field: web-development
product: laravel
tags: [laravel, controllers, invokable, dependency-injection, artisan]
level: intro
status: docs-checked
description: "Generate Laravel controllers with make:controller, write single action __invoke controllers, and use constructor and method injection."
sources:
  - https://laravel.com/docs/controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controllers group request handling and are stored in `app/Http/Controllers` by default. They need not extend a base class.

```shell
php artisan make:controller UserController
php artisan make:controller ProvisionServer --invokable
```

```php
class UserController extends Controller
{
    public function show(string $id): View
    {
        return view('user.profile', ['user' => User::findOrFail($id)]);
    }
}

Route::get('/user/{id}', [UserController::class, 'show']);
```

Route parameters are passed to the method. A single action controller defines `__invoke` and is routed by class name alone:

```php
Route::post('/server', ProvisionServer::class);
```

Controller stubs can be customised through stub publishing.

Constructor injection: the service container resolves controllers, so type-hinted constructor dependencies are injected.

```php
public function __construct(protected UserRepository $users) {}
```

Method injection: type-hint dependencies such as `Illuminate\Http\Request` on methods; list route arguments after the other dependencies.

```php
Route::put('/user/{id}', [UserController::class, 'update']);

public function update(Request $request, string $id): RedirectResponse
{
    return redirect('/users');
}
```

## Checked

Date: 2026-11-07

Read: controllers.md, Introduction, Basic Controllers, Single Action Controllers, Dependency Injection and Controllers (lines 1-114, 726-815).

Matched against the page, claim by claim:

- stored in app/Http/Controllers by default -> :25; need not extend base class -> :74
- make:controller --invokable -> :106-109; __invoke routed by class name -> :86-100
- stub publishing -> :113
- constructor injection via service container -> :732-748
- method injection, route arguments listed after other dependencies -> :755, :781-809

Changes made (trims and rewordings):

- "live in app/Http/Controllers" was stronger than the page ("By default, controllers are stored in"); now says by default.

Method: documentation only; no commands were run.
