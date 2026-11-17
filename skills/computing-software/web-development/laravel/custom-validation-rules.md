---
id: computing-software.web-development.laravel.custom-validation-rules
name: custom-validation-rules
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, custom-rules, make-rule, closures]
level: advanced
status: docs-checked
description: "Write custom Laravel validation rules as rule objects with make:rule, closures, translated failures, DataAwareRule and implicit rules."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate a rule object (placed in `app/Rules`):

```shell
php artisan make:rule Uppercase
php artisan make:rule Uppercase --implicit
```

A rule has one `validate` method receiving the attribute, value and a `$fail` callback:

```php
class Uppercase implements ValidationRule
{
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}

$request->validate(['name' => ['required', 'string', new Uppercase]]);
```

Translated message, with optional replacements and language:

```php
$fail('validation.uppercase')->translate();
$fail('validation.location')->translate(['value' => $this->value], 'fr');
```

Need all the data under validation? Implement `Illuminate\Contracts\Validation\DataAwareRule` and its `setData(array $data): static`, called before validation. Need the validator? Implement `ValidatorAwareRule` with `setValidator(Validator $validator): static`.

One-off rule as a closure:

```php
'title' => ['required', 'max:255', function (string $attribute, mixed $value, Closure $fail) {
    if ($value === 'foo') {
        $fail("The {$attribute} is invalid.");
    }
}],
```

Implicit rules: when an attribute is missing or an empty string, normal rules (including custom ones) do not run, so `Validator::make(['name' => ''], ['name' => ['unique:users,name']])->passes()` is `true`. A rule that must run on empty values has to imply required, which `--implicit` generates. An implicit rule only implies the attribute is required; whether it invalidates a missing or empty attribute is up to you.

## Checked

Date: 2026-11-07

Read: validation.md, Custom Validation Rules (lines 3085-3267).

Matched against the page, claim by claim:

- make:rule, --implicit -> :3094, :3260-3263; single validate method with attribute, value, $fail -> :3100
- translate() with replacements and language -> :3140-3150
- DataAwareRule::setData called before validation; ValidatorAwareRule::setValidator -> :3154-3214
- closure rules; implicit rules and unique example; implies required, up to you -> :3248-3267

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
