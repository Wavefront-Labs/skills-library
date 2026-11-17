---
id: computing-software.web-development.laravel.validation-files-and-passwords
name: validation-files-and-passwords
category: computing-software
field: web-development
product: laravel
tags: [laravel, validation, file-uploads, passwords, rule-objects]
level: practitioner
status: docs-checked
description: "Validate uploads with the File rule builder and image dimensions, and enforce passwords with Password::min, uncompromised and Password::defaults."
sources:
  - https://laravel.com/docs/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Files with the fluent builder:

```php
use Illuminate\Validation\Rules\File;

'attachment' => ['required', File::types(['mp3', 'wav'])->min(1024)->max(12 * 1024)],
'attachment' => ['required', File::types(['mp3', 'wav'])->min('1kb')->max('10mb')],
```

`types` takes extensions but validates the MIME type by reading the file contents. Size suffixes: `kb`, `mb`, `gb`, `tb`.

Images (jpg, jpeg, png, bmp, gif, webp, avif, heic, heif) with dimension limits:

```php
File::image()->min(1024)->max(12 * 1024)
    ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500));
File::image(allowSvg: true);
```

SVG is rejected by default because of XSS risk. The `extensions:jpg,png` rule checks the user-assigned extension, so never rely on it alone; combine it with `mimes` or `mimetypes`.

Passwords with `Illuminate\Validation\Rules\Password`:

```php
'password' => ['required', 'confirmed', Password::min(8)],
Password::min(16)->max(256);
Password::min(8)->letters();
Password::min(8)->mixedCase();
Password::min(8)->numbers();
Password::min(8)->symbols();
Password::min(8)->uncompromised(3);   // allow at most 3 appearances in a leak
```

`uncompromised` uses the k-Anonymity model with haveibeenpwned.com; by default one appearance in a leak means compromised.

Shared defaults in a service provider `boot`:

```php
Password::defaults(function () {
    $rule = Password::min(8);
    return $this->app->isProduction() ? $rule->mixedCase()->uncompromised() : $rule;
});
'password' => ['required', Password::defaults()],
Password::min(8)->rules([new ZxcvbnRule]);   // extra rules
```

For the HTML `passwordrules` attribute use `Password::defaults()->toPasswordRulesString()`.

## Checked

2026-11-07

Method: read the whole validation page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed File::types, the kb/mb/gb/tb size units, the image rule and allowSvg, the extensions warning, the Password builder methods, uncompromised(3), Password::defaults and toPasswordRulesString.
