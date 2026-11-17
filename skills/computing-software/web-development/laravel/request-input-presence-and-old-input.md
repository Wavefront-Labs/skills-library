---
id: computing-software.web-development.laravel.request-input-presence-and-old-input
name: request-input-presence-and-old-input
category: computing-software
field: web-development
product: laravel
tags: [laravel, requests, input, flash, old-input, trimstrings, cookies]
level: practitioner
status: docs-checked
description: "Test input presence with has, filled and missing, merge input, flash old input, read cookies, and control TrimStrings normalization in Laravel."
sources:
  - https://laravel.com/docs/requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Presence checks:

```php
$request->has('name');                 // array: all present
$request->hasAny(['name', 'email']);
$request->whenHas('name', fn (string $input) => ..., fn () => ...);
$request->filled('name');              // present and not an empty string
$request->isNotFilled(['name', 'email']);
$request->anyFilled(['name', 'email']);
$request->whenFilled('name', fn (string $input) => ...);
$request->missing('name');
$request->whenMissing('name', fn () => ...);
```

Merging (merge overwrites existing keys; mergeIfMissing does not):

```php
$request->merge(['votes' => 0]);
$request->mergeIfMissing(['votes' => 0]);
```

Old input is flashed to the session for the next request:

```php
$request->flash();
$request->flashOnly(['username', 'email']);
$request->flashExcept('password');
return redirect('/form')->withInput($request->except('password'));
$username = $request->old('username');
```

In Blade: `<input type="text" name="username" value="{{ old('username') }}">` (null if no old input). Validation features may flash input automatically.

Cookies: framework cookies are encrypted and signed, so client changes make them invalid. Read with `$request->cookie('name')`.

Normalization: the global `TrimStrings` and `ConvertEmptyStringsToNull` middleware trim strings and turn empty strings into `null`. Remove both with `$middleware->remove([...])` in `bootstrap/app.php`, or skip for some requests:

```php
$middleware->convertEmptyStringsToNull(except: [fn (Request $request) => $request->is('admin/*')]);
$middleware->trimStrings(except: [fn (Request $request) => $request->is('admin/*')]);
```

## Checked

2026-11-07

Method: read the whole requests page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed has/hasAny/whenHas/filled/isNotFilled/anyFilled/whenFilled/missing/whenMissing, merge versus mergeIfMissing, flash/flashOnly/flashExcept, withInput(except), old() and the Blade old helper, cookie retrieval, the TrimStrings and ConvertEmptyStringsToNull middleware and their opt-out closures. Linked Symfony and MDN pages were not opened.
