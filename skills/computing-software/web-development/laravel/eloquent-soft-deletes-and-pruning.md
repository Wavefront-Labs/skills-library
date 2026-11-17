---
id: computing-software.web-development.laravel.eloquent-soft-deletes-and-pruning
name: eloquent-soft-deletes-and-pruning
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, soft-deletes, prunable, delete, replicate]
level: practitioner
status: docs-checked
description: "Delete Eloquent models with delete, destroy and queries, use SoftDeletes with restore and withTrashed, prune old rows with Prunable, and replicate models."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Delete:

```php
$flight->delete();
$flight->deleteOrFail();             // in a transaction
Flight::destroy(1);  Flight::destroy([1, 2, 3]);
Flight::forceDestroy(1);             // permanent, for soft-delete models
$deleted = Flight::where('active', 0)->delete();
```

`destroy` loads each model so `deleting`/`deleted` events fire. Mass deletes via a query do not dispatch them, because models are never retrieved.

Soft deletes: add `use SoftDeletes;` to the model and `$table->softDeletes();` in a migration (`dropSoftDeletes()` to remove). `delete()` sets `deleted_at` (cast to Carbon) and queries exclude those rows.

```php
$flight->trashed();
$flight->restore();
Flight::withTrashed()->where('airline_id', 1)->restore();   // mass restore fires no events
$flight->forceDelete();
Flight::withTrashed()->where('account_id', 1)->get();
Flight::onlyTrashed()->where('airline_id', 1)->get();
$flight->history()->withTrashed()->get();                   // also on relationships
```

Pruning: add `Prunable` (or `MassPrunable`) and implement `prunable()` returning a query:

```php
use Prunable;
public function prunable(): Builder
{
    return static::where('created_at', '<=', now()->minus(months: 1));
}
protected function pruning(): void { /* e.g. delete stored files */ }
```

Schedule it in `routes/console.php`: `Schedule::command('model:prune')->daily();`. Models are auto-detected in `app/Models`; otherwise pass `'--model' => [Address::class, Flight::class]`, or exclude with `'--except'`. Preview with `php artisan model:prune --pretend`. Soft-deleted models matching the query are permanently deleted. `MassPrunable` uses mass-deletion queries, so `pruning` and the `deleting`/`deleted` events do not run.

Replicate creates an unsaved copy; pass attributes to exclude:

```php
$billing = $shipping->replicate()->fill(['type' => 'billing']);
$billing->save();
$copy = $flight->replicate(['last_flown', 'last_pilot_id']);
```

Compare models with `$post->is($other)` and `isNot`, which check primary key, table and connection. They also work on `belongsTo`, `hasOne`, `morphTo` and `morphOne` relations without a query: `$post->author()->is($user)`.

## Checked

Date: 2026-11-07

Read: eloquent.md, Deleting Models, Soft Deleting, Querying Soft Deleted Models, Pruning Models, Replicating Models, Comparing Models (lines 1121-1300, 1300-1440, 1752-1773).

Matched against the page, claim by claim:

- deleteOrFail, destroy variants, forceDestroy; destroy loads each model; mass delete no events -> :1134-1180
- SoftDeletes, softDeletes()/dropSoftDeletes(), deleted_at cast to Carbon, trashed -> :1185-1227
- restore, mass restore no events, forceDelete, withTrashed, onlyTrashed on relations -> :1232-1298
- Prunable/MassPrunable, prunable(), pruning(), model:prune schedule, --model, --except, --pretend, soft-deleted force deleted, MassPrunable skips pruning and events -> :1303-1376
- replicate and exclusion array -> :1404-1438; is/isNot compare key, table, connection; work on belongsTo/hasOne/morphTo/morphOne -> :1755-1773

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
