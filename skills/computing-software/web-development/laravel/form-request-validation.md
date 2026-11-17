---
id: computing-software.web-development.laravel.form-request-validation
name: form-request-validation
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, form-requests, authorize, attributes]
level: practitioner
status: docs-checked
description: "Build Laravel form requests with make:request: rules, authorize, messages, prepareForValidation, after hooks and the validation PHP attributes."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```shell
php artisan make:request StorePostRequest
```

The class goes to `app/Http/Requests` with `authorize` and `rules` methods (dependencies can be type-hinted in both signatures). Type-hint it on the controller method; validation runs before the method is called.

```php
public function rules(): array
{
    return ['title' => ['required', 'unique:posts', 'max:255'], 'body' => ['required']];
}

public function store(StorePostRequest $request): RedirectResponse
{
    $validated = $request->validated();
    $validated = $request->safe()->only(['name', 'email']);
}
```

Authorization: returning `false` from `authorize` gives a 403 and the controller does not run. Use `$this->user()->can('update', $this->comment)` (route-bound models are properties of the request). Return `true` if authorization is handled elsewhere.

Messages and attribute names:

```php
public function messages(): array { return ['title.required' => 'A title is required']; }
public function attributes(): array { return ['email' => 'email address']; }
```

Prepare input before validation, or normalise after:

```php
protected function prepareForValidation(): void { $this->merge(['slug' => Str::slug($this->slug)]); }
protected function passedValidation(): void { $this->replace(['name' => 'Taylor']); }
```

Extra checks run after validation via `after()`, which returns callables (or invokable classes) receiving a `Validator`:

```php
public function after(): array
{
    return [function (Validator $validator) {
        $validator->errors()->add('field', 'Something is wrong with this field!');
    }];
}
```

Class attributes: `#[StopOnFirstFailure]`, `#[FailOnUnknownFields]` (or `FormRequest::failOnUnknownFields()` in `AppServiceProvider`; `#[FailOnUnknownFields(false)]` opts out), `#[RedirectTo('/dashboard')]`, `#[RedirectToRoute('dashboard')]`, `#[ErrorBag('login')]`. Unknown-field rejection does not replace configuring `$fillable` or `$guarded`.

## Checked

Date: 2026-11-07

Read: validation.md, Form Request Validation (lines 300-700).

Matched against the page, claim by claim:

- type-hint request, validated before controller -> :343; dependencies in rules() and authorize() -> :341, :596
- authorize false -> 403, controller not executed -> :581
- messages(), attributes(), prepareForValidation merge, passedValidation replace -> :650, :656-664
- after() callables -> After Validation hooks section
- StopOnFirstFailure -> :424; FailOnUnknownFields attribute, FormRequest::failOnUnknownFields(), (false) -> :444-484; still configure $fillable/$guarded -> :491
- RedirectTo -> :496-506; RedirectToRoute -> :513-523; ErrorBag -> :533-543

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
