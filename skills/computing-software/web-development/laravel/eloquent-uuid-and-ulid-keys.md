---
id: computing-software.web-development.laravel.eloquent-uuid-and-ulid-keys
name: eloquent-uuid-and-ulid-keys
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, uuid, ulid, primary-keys]
level: practitioner
status: docs-checked
description: "Use UUID or ULID primary keys in Eloquent models with the HasUuids and HasUlids traits, custom generators and extra unique-id columns."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Swap auto-incrementing keys for UUIDs (36 characters) with `HasUuids`. The table needs a UUID-equivalent primary key column.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;

class Article extends Model
{
    use HasUuids;
}

$article = Article::create(['title' => 'Traveling to Europe']);
$article->id; // "018f2b5c-6a7f-7b12-9d6f-2f8a4e0c9c11"
```

By default `HasUuids` generates UUIDv7 identifiers, which are more efficient for indexed storage because they sort lexicographically.

Override generation and choose which columns receive IDs:

```php
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();   // Ramsey\Uuid\Uuid
}

public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

ULIDs are 26 characters and also lexicographically sortable. Use `Illuminate\Database\Eloquent\Concerns\HasUlids` and a ULID-equivalent primary key column:

```php
class Article extends Model
{
    use HasUlids;
}
$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

## Checked

Date: 2026-11-07

Read: eloquent.md, UUID and ULID Keys (lines 210-276).

Matched against the page, claim by claim:

- HasUuids, 36 characters -> :213-215; UUIDv7 default sortable -> :233
- newUniqueId and uniqueIds -> :235-257
- HasUlids, 26 characters, lexicographically sortable -> :259

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
