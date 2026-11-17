---
id: computing-software.web-development.laravel.eloquent-retrieving-single-models
name: eloquent-retrieving-single-models
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, find, first-or-create, aggregates, subqueries]
level: practitioner
status: docs-checked
description: "Retrieve single Eloquent models with find, first, OrFail and firstOrCreate, refresh models, run aggregates and use subquery selects and ordering."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Models are query builders; add constraints then `get()`:

```php
$flights = Flight::where('active', 1)->orderBy('name')->limit(10)->get();
```

Single records:

```php
$flight = Flight::find(1);
$flight = Flight::where('active', 1)->first();
$flight = Flight::firstWhere('active', 1);
$flight = Flight::findOr(1, fn () => /* fallback */ null);
$flight = Flight::where('legs', '>', 3)->firstOr(fn () => /* fallback */ null);
```

`findOrFail` and `firstOrFail` throw `Illuminate\Database\Eloquent\ModelNotFoundException`; uncaught, it becomes a 404 response:

```php
Route::get('/api/flights/{id}', fn (string $id) => Flight::findOrFail($id));
```

Retrieve or create (second array is merged only when creating):

```php
$flight = Flight::firstOrCreate(['name' => 'London to Paris'], ['delayed' => 1, 'arrival_time' => '11:30']);
$flight = Flight::firstOrNew(['name' => 'Tokyo to Sydney']);   // not persisted; call save()
```

Aggregates return scalars: `Flight::where('active', 1)->count();` and `->max('price')`.

Refreshing: `$flight->fresh()` returns a newly queried model and leaves the instance alone; `$flight->refresh()` re-hydrates the existing instance and its loaded relationships. Inside a transaction, `$flight->refreshForUpdate()` reloads with a `FOR UPDATE` lock.

Subquery selects pull related data in one query:

```php
Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```

Subquery ordering: pass the subquery to `orderByDesc`:

```php
Destination::orderByDesc(
    Flight::select('arrived_at')->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')->limit(1)
)->get();
```

## Checked

Date: 2026-11-07

Read: eloquent.md, Retrieving Models, Retrieving Single Models / Aggregates (lines 471-790).

Matched against the page, claim by claim:

- where/orderBy/limit/get -> :490; fresh vs refresh vs refreshForUpdate (FOR UPDATE) -> :502-530
- find/first/firstWhere/findOr/firstOr -> :696-721; findOrFail/firstOrFail, ModelNotFoundException, 404 -> :726-742
- firstOrCreate/firstOrNew merge semantics -> :747-775; aggregates -> :780-786
- subquery select and ordering -> :664-690

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
