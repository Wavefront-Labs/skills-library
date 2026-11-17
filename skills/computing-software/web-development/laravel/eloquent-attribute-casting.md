---
id: computing-software.web-development.laravel.eloquent-attribute-casting
name: eloquent-attribute-casting
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, casts, json, enums, encrypted]
level: practitioner
status: docs-checked
description: "Configure Eloquent attribute casts: boolean, array, AsArrayObject, AsCollection, datetime formats, enums, encrypted, AsBinary, AsVector and query-time withCasts."
sources:
  - https://laravel.com/docs/eloquent-mutators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define a `casts()` method returning attribute => type:

```php
protected function casts(): array
{
    return ['is_admin' => 'boolean', 'options' => 'array', 'status' => ServerStatus::class];
}
```

Supported types: `array`, `AsFluent::class`, `AsStringable::class`, `AsUri::class`, `AsVector::class`, `boolean`, `collection`, `date`, `datetime`, `immutable_date`, `immutable_datetime`, `decimal:<precision>`, `double`, `encrypted`, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `float`, `hashed`, `integer`, `object`, `real`, `string`, `timestamp`.

`null` attributes are not cast. Never give a cast (or attribute) the same name as a relationship, or cast the primary key. Add a temporary cast with `$user->mergeCasts(['is_admin' => 'integer'])`.

JSON: the `array` cast deserializes on read and serializes on write; update one key with `$user->update(['options->key' => 'value'])` (the column must be mass assignable). `json:unicode` stores unescaped Unicode. You cannot mutate `$user->options['key']` on a plain array cast; use `AsArrayObject::class` or `AsCollection::class`. For SQL NULL instead of JSON null use `AsCollection::nullable()` (also on `AsArrayObject`). Custom collection classes: `AsCollection::using(OptionCollection::class)`, or map items into objects with `AsCollection::of(Option::class)` (the object should implement `Arrayable` and `JsonSerializable`).

Dates: `created_at` and `updated_at` are Carbon; prefer `datetime` or `immutable_datetime`; format with `'created_at' => 'datetime:Y-m-d'`. You may assign a UNIX timestamp, `Y-m-d` string, date-time string, or `DateTime`/`Carbon`. Override array/JSON format with `protected function serializeDate(DateTimeInterface $date): string`. Storage format uses `#[Table(dateFormat: 'U')]`. By default dates serialize to UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`); a custom format uses the Carbon instance's timezone, except `created_at`/`updated_at`, which are always UTC. The docs strongly encourage keeping the app `timezone` at its default `UTC`.

Enums: `'status' => ServerStatus::class`, then compare and assign enum cases. Arrays of enums: `AsEnumCollection::of(ServerStatus::class)` or `AsEnumArrayObject`.

Encrypted: also `AsEncryptedArrayObject` and `AsEncryptedCollection`. The column must be `TEXT` or larger and encrypted values cannot be queried. Key rotation follows the encryption docs.

Binary: for binary `uuid`/`ulid` columns next to an auto-incrementing ID, `'uuid' => AsBinary::uuid()` and `'ulid' => AsBinary::ulid()`; reads return a plain string.

Vector: `'embedding' => AsVector::class` accepts an array or `Arrayable` and returns an array of floats.

Query-time casts for raw selects:

```php
User::select(['users.*', 'last_posted_at' => Post::selectRaw('MAX(created_at)')
    ->whereColumn('user_id', 'users.id')])
    ->withCasts(['last_posted_at' => 'datetime'])->get();
```

## Checked

Date: 2026-11-07

Read: eloquent-mutators.md, Attribute Casting through Query Time Casting (lines 200-735).

Matched against the page, claim by claim:

- supported types list incl. AsVector, real, encrypted variants -> :222-245
- mergeCasts -> :280-283; null not cast; never name a cast like a relationship or cast the primary key -> :290
- array cast, JSON/TEXT column -> :324; json:unicode -> :376; AsCollection::nullable and AsArrayObject nullable -> :439-463; AsCollection::of with Arrayable+JsonSerializable -> :503
- date serialization: UTC ISO-8601 default; custom format uses Carbon timezone; created_at/updated_at always UTC -> :662-664
- serializeDate and Table(dateFormat) -> :637-657
- encrypted: TEXT or larger, cannot query, key rotation link -> :722-729
- AsBinary uuid/ulid -> :581-595; AsVector accepts array or Arrayable, returns floats -> :558-576

Changes made (trims and rewordings):

- "Keep the app timezone at UTC" was an instruction; the page (:662) says users are strongly encouraged to keep the default UTC. Reworded.

Method: documentation only; no commands were run.
