---
id: computing-software.web-development.laravel.eloquent-serialization
name: eloquent-serialization
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, serialization, json, hidden, appends]
level: practitioner
status: docs-checked
description: "Serialize Eloquent models to arrays and JSON, hide or whitelist attributes with Hidden and Visible, append accessors, and control date formats."
sources:
  - https://laravel.com/docs/eloquent-serialization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conversion:

```php
User::with('roles')->first()->toArray();   // recursive: attributes and loaded relations
User::first()->attributesToArray();        // attributes only
User::all()->toArray();
$user->toJson();  $user->toJson(JSON_PRETTY_PRINT);
(string) User::find(1);                    // calls toJson
Route::get('/users', fn () => User::all());   // returned models serialize to JSON
```

Loaded relationships appear as attributes; the relationship's JSON key is snake_case even though the method is camelCase. For finer control see API resources.

Hide attributes (and relationships, by method name) with `#[Hidden(['password'])]`, or allow-list with `#[Visible(['first_name', 'last_name'])]`, which hides everything else.

Per-instance changes:

```php
$user->makeVisible('attribute')->toArray();   // mergeVisible(['name', 'email'])
$user->makeHidden('attribute')->toArray();    // mergeHidden([...])
$user->setVisible(['id', 'name'])->toArray();
$user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

Append values that have no column: define an accessor, then list the snake_case name:

```php
protected function isAdmin(): Attribute
{
    return new Attribute(get: fn () => 'yes');
}
// always appended:
#[Appends(['is_admin'])]
class User extends Model {}
// at run time:
$user->append('is_admin')->toArray();
$user->mergeAppends(['is_admin', 'status'])->toArray();
$user->setAppends(['is_admin'])->toArray();
$user->withoutAppends()->toArray();
```

Appended attributes respect the model's visible and hidden settings.

Dates: override `serializeDate` for all dates (does not affect storage), or set a format per attribute in `casts()`:

```php
protected function serializeDate(DateTimeInterface $date): string { return $date->format('Y-m-d'); }
'birthday' => 'date:Y-m-d',
'joined_at' => 'datetime:Y-m-d H:00',
```

## Checked

Date: 2026-11-07

Read: eloquent-serialization.md in full (249 lines).

Matched against the page, claim by claim:

- toArray recursive, attributesToArray, collection toArray -> :25-49
- toJson with options, string cast, return from routes, snake_case relationship key -> :54-83
- Hidden/Visible attributes, relationships hidden by method name -> :88-124
- makeVisible/mergeVisible/makeHidden/mergeHidden/setVisible/setHidden -> :129-150
- accessor + Appends, snake_case, respects visible/hidden -> :156-197; append/mergeAppends/setAppends/withoutAppends -> :202-216
- serializeDate not affecting storage; casts date:Y-m-d -> :224-248

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
