---
id: computing-software.web-development.laravel.redirect-responses
name: redirect-responses
category: computing-software
field: web-development
product: laravel
tags: [laravel, responses, redirects, flash-data, session]
level: intro
status: docs-checked
description: "Return Laravel redirects with redirect(), back(), route and action targets, away() for external URLs, with() flash data and withInput."
sources:
  - https://laravel.com/docs/responses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redirects are `Illuminate\Http\RedirectResponse` instances.

```php
return redirect('/dashboard');
return back()->withInput();   // previous location; needs the web middleware group (uses session)
return redirect()->route('login');
return redirect()->route('profile', ['id' => 1]);
return redirect()->route('profile', [$user]);   // model ID extracted automatically
return redirect()->action([UserController::class, 'profile'], ['id' => 1]);
return redirect()->away('https://www.google.com');
```

`redirect()` with no arguments returns an `Illuminate\Routing\Redirector`. `away` creates a redirect without any extra URL encoding, validation or verification.

To change the value placed in a route parameter from a model, use `/profile/{id:slug}` or override `getRouteKey` on the model:

```php
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

Flash data in the same chain:

```php
return redirect('/dashboard')->with('status', 'Profile updated!');
```

```blade
@if (session('status'))
    <div class="alert alert-success">{{ session('status') }}</div>
@endif
```

Flash the current input (used after validation errors) to repopulate forms:

```php
return back()->withInput();
```

## Checked

2026-11-07

Method: read the whole responses page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed redirect(), back()->withInput(), route and route-parameter redirects including a model argument and getRouteKey, the {id:slug} form, action redirects, away() skipping encoding/validation/verification, and with() flashing plus the Blade session('status') read. The Inertia and Vue/Svelte tab examples were read but are not part of this skill.
