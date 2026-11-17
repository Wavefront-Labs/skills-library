---
id: computing-software.web-development.laravel.validation-language-files
name: validation-language-files
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, localization, lang, error-messages]
level: practitioner
status: docs-checked
description: "Customise Laravel validation messages, attribute names and :value text in lang/xx/validation.php, and use Rule builder methods."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The skeleton has no `lang` directory; publish it with `php artisan lang:publish`. `lang/en/validation.php` holds one message per rule; edit it or copy it to another language directory to translate.

Per attribute and rule, in the `custom` array:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

Replace the `:attribute` placeholder via `attributes`:

```php
'attributes' => [
    'email' => 'email address',
],
```

Replace the `:value` placeholder with a friendlier text via `values`. For `'credit_card_number' => ['required_if:payment_type,cc']` the default message ends "when payment type is cc"; with:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

it becomes "The credit card number field is required when payment type is credit card."

Rule builders: `Illuminate\Validation\Rule` has camel-case methods that can be mixed with string rules (IDE autocompletion):

```php
use Illuminate\Validation\Rule;

'name' => [Rule::required(), Rule::string()->max(255)],
'website' => [Rule::nullable(), Rule::activeUrl()],
'terms' => [Rule::acceptedIf('account_type', ['personal', 'business'])],
'email' => [Rule::requiredWithout(['phone', 'mobile'])],
'username' => [Rule::required(), Rule::regex('/^[a-z]+$/i')],
'code' => [Rule::notRegex('/^test-/i')],
```

Other names follow the same pattern, such as `Rule::hexColor()`, `Rule::macAddress()` and `Rule::requiredArrayKeys(['name', 'email'])`.

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed lang:publish, the custom, attributes and values arrays, and the Rule builders for messages.
