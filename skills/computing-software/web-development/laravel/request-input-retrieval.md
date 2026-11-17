---
id: computing-software.web-development.laravel.request-input-retrieval
name: request-input-retrieval
category: computing-software
field: web-development
product: laravel
tags: [laravel, requests, input, typed-input, query-string, json]
level: practitioner
status: docs-checked
description: "Read Laravel request input with input, query, JSON dot notation and typed getters: string, integer, boolean, array, date, interval, enum."
sources:
  - https://laravel.com/docs/requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Verb-agnostic retrieval:

```php
$input = $request->all();                 // array
$input = $request->collect();             // collection
$request->collect('users')->each(fn (string $user) => ...);
$name = $request->input('name', 'Sally'); // second arg is the default
$request->input('products.0.name');       // dot notation
$request->input('products.*.name');
$request->input();                        // all as associative array
$request->query('name', 'Helen');         // query string only
$request->input('user.name');             // JSON body, needs Content-Type: application/json
$request->name;                           // dynamic property: payload first, then route parameters
```

Typed getters:

```php
$request->string('name')->trim();          // Illuminate\Support\Stringable
$request->integer('per_page');
$request->boolean('archived');             // true for 1, "1", true, "true", "on", "yes"
$request->array('versions');               // empty array if missing
$request->date('birthday');                // Carbon, null if missing
$request->date('elapsed', '!H:i', 'Europe/Madrid'); // format, timezone
$request->interval('duration');            // CarbonInterval
$request->interval('timeout', 'second');   // unit for numeric input
$request->enum('status', Status::class, Status::Pending); // default optional
$request->enums('products', Product::class);
```

An invalid `date` or `interval` value throws `InvalidArgumentException`, so validate first.

Subsets:

```php
$request->only(['username', 'password']);
$request->except('credit_card');
```

`only` does not return keys that are not present on the request.

## Checked

2026-11-07

Method: read the whole requests page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed all/collect, input with defaults and dot notation, wildcard keys, query(), JSON input needing a Content-Type of application/json, dynamic properties (payload first, then route parameters), string/integer/boolean/array/date/interval/enum accessors including the accepted boolean values and the InvalidArgumentException on bad dates, and only/except/only-missing-keys. Linked php.net pages were not opened.
