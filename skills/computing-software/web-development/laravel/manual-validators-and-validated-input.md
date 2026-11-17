---
id: computing-software.web-development.laravel.manual-validators-and-validated-input
name: manual-validators-and-validated-input
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, validator, error-bags, validated-input, messagebag]
level: practitioner
status: docs-checked
description: "Create validators with Validator::make, named error bags, custom messages, after callbacks, safe() validated input and MessageBag methods."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Manual validator:

```php
$validator = Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
]);
if ($validator->stopOnFirstFailure()->fails()) {
    return redirect('/post/create')->withErrors($validator)->withInput();
}
$validated = $validator->validated();
```

`withErrors` accepts a validator, a `MessageBag` or an array. To keep the automatic redirect/JSON behaviour call `->validate()` or `->validateWithBag('post')` on the validator.

Named bags for several forms on one page: `redirect('/register')->withErrors($validator, 'login');` then `{{ $errors->login->first('email') }}`.

Messages (third argument) and attribute names (fourth):

```php
$messages = [
    'required' => 'The :attribute field is required.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'email.required' => 'We need to know your email address!',
];
Validator::make($input, $rules, $messages, ['email' => 'email address']);
```

Other placeholders: `:other`, `:size`, `:values`.

After callbacks (closures or invokable classes receiving the `Validator`):

```php
$validator->after(function ($validator) {
    $validator->errors()->add('field', 'Something is wrong with this field!');
});
```

Validated data: `$request->validated()`, or `safe()` returning `Illuminate\Support\ValidatedInput` with `only`, `except`, `all`, `merge(['name' => 'Taylor Otwell'])` and `collect()`; it can be iterated and read like an array (`$validated['email']`).

MessageBag: `$errors->first('email')`, `get('email')`, `get('attachments.*')`, `all()`, `has('email')`.

## Checked

Date: 2026-11-07

Read: validation.md, Manually Creating Validators, Working With Validated Input, Working With Error Messages (lines 700-960).

Matched against the page, claim by claim:

- Validator::make, stopOnFirstFailure -> :720-723; withErrors; validate()/validateWithBag -> :740-746
- named error bags -> Named Error Bags section
- messages third arg, :attribute :input :min :max :other :size :values -> :779-782; attributes fourth arg
- after callbacks -> Performing Additional Validation section
- validated()/safe() ValidatedInput only/except/all/merge/collect, iterable -> :867-890
- MessageBag first/get/get(attachments.*)/all/has -> :923 and nearby

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
