---
id: computing-software.web-development.laravel.validation-arrays
name: validation-arrays
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, arrays, nested-input, rule-foreach]
level: practitioner
status: docs-checked
description: "Validate arrays in Laravel: allowed keys, dot and wildcard notation, Rule::forEach, and :index, :position and :ordinal-position message placeholders."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Allowed keys: `array:name,username` fails if extra keys are present. In general, list the allowed keys; otherwise `validate` and `validated` return the whole array including keys no nested rule validated.

```php
Validator::make($input, ['user' => ['array:name,username']]);
```

Nested input with dot notation and the `*` wildcard:

```php
Validator::make($request->all(), [
    'photos.profile' => ['required', 'image'],
    'users.*.email' => ['email', 'unique:users'],
    'users.*.first_name' => ['required_with:users.*.last_name'],
]);
```

A wildcard also works in language-file custom messages:

```php
'custom' => [
    'users.*.email' => ['unique' => 'Each user must have a unique email address'],
],
```

Rules depending on each element's value use `Rule::forEach`; the closure receives the value and the fully-expanded attribute name and returns the rules:

```php
'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
    return [
        Rule::exists(Company::class, 'id'),
        new HasPermission('manage-company', $value),
    ];
}),
```

Message placeholders for the failing item: `:index` (starts at 0), `:position` (starts at 1), `:ordinal-position` (1st, 2nd...):

```php
Validator::validate($input, [
    'photos.*.description' => ['required'],
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

Deeper levels use `second-index`, `second-position`, `third-index`, `third-position` and so on, for example `'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.'`.

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed array rule key lists, wildcard rules, custom messages, Rule::forEach, and :index, :position, :ordinal-position and second-index placeholders. Corrected: the page says to list allowed keys in general, not always.
