---
id: computing-software.web-development.laravel.eloquent-large-result-sets
name: eloquent-large-result-sets
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, chunk, lazy, cursor, memory]
level: practitioner
status: docs-checked
description: "Process many Eloquent records without exhausting memory using chunk, chunkById, lazy, lazyById and cursor, and know when each is safe."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`all()` and `get()` return an `Illuminate\Database\Eloquent\Collection` and may run out of memory on tens of thousands of rows.

`chunk` runs one query per chunk and passes each to a closure:

```php
Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) { /* ... */ }
});
```

If you filter on a column you also update while iterating, use `chunkById`, which always fetches models with an `id` greater than the last of the previous chunk:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById` and `lazyById` add their own where conditions, so group your own conditions in a closure:

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) { /* ... */ }, column: 'id');
```

`lazy` also queries in chunks but returns a flattened `LazyCollection` stream:

```php
foreach (Flight::lazy() as $flight) { /* ... */ }
Flight::where('departed', true)->lazyById(200, column: 'id')->each->update(['departed' => false]);
```

`lazyByIdDesc` orders by descending id.

`cursor` runs a single query and hydrates models only as iterated, using PHP generators, so one model is in memory at a time. It returns a `LazyCollection`:

```php
$users = User::cursor()->filter(fn (User $user) => $user->id > 500);
```

Limits: `cursor` cannot eager load relationships (use `lazy` instead), and it can still run out of memory because the PDO driver buffers all raw results internally; for very large sets prefer `lazy`.

## Checked

Date: 2026-11-07

Read: eloquent.md, Collections, Chunking Results, Chunking Using Lazy Collections, Cursors (lines 532-657).

Matched against the page, claim by claim:

- all/get return Eloquent Collection; memory on tens of thousands -> :535, :560
- chunk, one query per chunk -> :562-575; chunkById id greater than last -> :577-584; group conditions -> :586-596
- lazy returns flattened LazyCollection; lazyById; lazyByIdDesc -> :602-620
- cursor single query, generators, one model in memory, cannot eager load, PDO buffer -> :627-656

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
