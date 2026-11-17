---
id: computing-software.web-development.laravel.validation-quickstart
name: validation-quickstart
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, request-validate, errors, forms]
level: intro
status: docs-checked
description: "Validate Laravel requests with $request->validate, bail, nested dot rules, nullable fields, @error and the 422 JSON error format."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Call `validate` on the request. On failure an `Illuminate\Validation\ValidationException` is thrown: a traditional request redirects to the previous URL (errors and input flashed to the session); an XHR/JSON request gets a `422 Unprocessable Entity` JSON response.

```php
$validated = $request->validate([
    'title' => ['bail', 'required', 'unique:posts', 'max:255'],
    'body' => ['required'],
    'author.name' => ['required'],
    'publish_at' => ['nullable', 'date'],
]);
$validated = $request->validateWithBag('post', [ /* rules */ ]);
```

`bail` stops running rules on an attribute after the first failure; rules run in assigned order. Use dot syntax for nested fields; escape a literal period with a backslash (`'v1\.0'`).

Optional fields: `TrimStrings` and `ConvertEmptyStringsToNull` are in the global stack, so mark optional fields `nullable` or `null` counts as invalid for rules like `date`.

Display errors. The `web` group's `ShareErrorsFromSession` shares `$errors` (an `Illuminate\Support\MessageBag`) with every view:

```blade
@if ($errors->any())
    <ul>@foreach ($errors->all() as $error)<li>{{ $error }}</li>@endforeach</ul>
@endif

<input name="title" class="@error('title') is-invalid @enderror" value="{{ old('title') }}">
@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

`@error('title', 'post')` takes a named error bag. Input is flashed automatically, so `old('title')` repopulates the form.

JSON error format flattens nested keys with dots:

```json
{ "message": "The team name field must be a string. (and 4 more errors)",
  "errors": { "team_name": ["..."], "users.0.email": ["..."] } }
```

Built-in messages are in `lang/en/validation.php`; publish the `lang` directory with `php artisan lang:publish`.

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed validate and ValidationException with 422 for JSON, validateWithBag, bail, dot syntax and escaped periods, nullable, ShareErrorsFromSession, the MessageBag $errors variable, @error, old(), the JSON error format and lang:publish.
