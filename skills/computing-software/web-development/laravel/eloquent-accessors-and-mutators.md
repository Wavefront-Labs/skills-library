---
id: computing-software.web-development.laravel.eloquent-accessors-and-mutators
name: eloquent-accessors-and-mutators
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, accessors, mutators, attribute]
level: practitioner
status: docs-checked
description: "Define Eloquent accessors and mutators with Attribute::make get and set, build value objects from several columns, and control accessor caching."
sources:
  - https://laravel.com/docs/eloquent-mutators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Accessors and mutators are protected methods named in camelCase after the column, which must return `Illuminate\Database\Eloquent\Casts\Attribute`.

```php
protected function firstName(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => ucfirst($value),
        set: fn (string $value) => strtolower($value),
    );
}

$user->first_name;            // runs get with the raw column value
$user->first_name = 'Sally';  // runs set, stores 'sally'
```

Computed values do not appear in array or JSON output unless appended (see the serialization docs).

Value object from several columns: the `get` closure receives `$attributes` as a second argument; a `set` closure returning an array writes several columns:

```php
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

Caching: Eloquent keeps the instance an accessor returns, so changes to a value object sync back before `save()`:

```php
$user->address->lineOne = 'Updated Address Line 1 Value';
$user->save();
```

Primitive results (strings, booleans) are not cached by default; add `->shouldCache()` for expensive ones (`Attribute::make(get: fn (string $value) => bcrypt(gzuncompress($value)))->shouldCache()`). Turn object caching off with `->withoutObjectCaching()`.

## Checked

Date: 2026-11-07

Read: eloquent-mutators.md, Accessors and Mutators (lines 28-200).

Matched against the page, claim by claim:

- protected camelCase method returning Attribute (mandatory return type) -> :34-36
- get closure gets raw value -> :54, :62; computed values must be appended for array/JSON -> :73
- get closure second argument $attributes -> :78-95
- retained instances, value object changes synced before save -> :101-112
- shouldCache for primitives -> :114-121; withoutObjectCaching -> :125-138
- set closure returning array writes multiple columns, set stores lowercase example -> Defining a Mutator section

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
