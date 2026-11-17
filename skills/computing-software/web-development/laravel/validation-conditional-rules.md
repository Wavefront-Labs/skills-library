---
id: computing-software.web-development.laravel.validation-conditional-rules
name: validation-conditional-rules
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, conditional-rules, sometimes, exclude-if]
level: practitioner
status: docs-checked
description: "Add Laravel validation rules conditionally with exclude_if, exclude_unless, sometimes and the Validator sometimes() closure including array items."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Do not validate a field when another field has a given value (`exclude_if`):

```php
$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],
    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],
]);
```

`exclude_unless:has_appointment,true` is the inverse: do not validate the field unless the other field has that value. Both rules also leave the field out of the data returned by `validate` and `validated`.

Validate only when the field is present with `sometimes`:

```php
'email' => ['sometimes', 'required', 'email'],
```

For a field that should always be present but may be empty, see the page's note on optional fields (mark it `nullable`).

Complex conditions: define static rules first, then add rules from a closure that receives an `Illuminate\Support\Fluent` of the input; the rules are added when it returns `true`:

```php
$validator = Validator::make($request->all(), [
    'email' => ['required', 'email'],
    'games' => ['required', 'integer', 'min:0'],
]);

$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {
    return $input->games >= 100;
});

$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

Array items whose index you do not know: the closure takes a second argument, the current item (a `Fluent` when the data is an array, otherwise a string):

```php
$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});
$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed sometimes, Fluent-based conditions and the array item closure. Corrected: the example now matches the page (exclude_if with has_appointment,false for both fields), the exclude_unless inverse and the effect on validated data are stated, and the nullable line points to the page's optional-fields note.
