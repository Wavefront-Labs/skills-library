---
id: computing-software.web-development.laravel.eloquent-inserts-updates-and-mass-assignment
name: eloquent-inserts-updates-and-mass-assignment
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, mass-assignment, upsert, dirty-attributes]
level: practitioner
status: docs-checked
description: "Insert and update Eloquent models with save, create, updateOrCreate and upsert, guard mass assignment with Fillable, and inspect dirty or changed attributes."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Insert: set attributes and `save()` (timestamps set automatically), or `create()`:

```php
$flight = new Flight;
$flight->name = $request->name;
$flight->save();
$flight->saveOrFail();                       // wrapped in a transaction
$flight = Flight::create(['name' => 'London to Paris']);
```

Update: retrieve, set, `save()`; `$flight->updateOrFail(['name' => 'Paris to London'])` runs in a transaction. `updateOrCreate` persists either way, and `$flight->wasRecentlyCreated` tells you which happened:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

Mass update: `Flight::where('active', 1)->update(['delayed' => 1]);` returns affected rows and fires no `saving`, `saved`, `updating` or `updated` events.

Mass assignment: all models are protected by default. `create` needs a `Fillable` or `Guarded` attribute, or an attacker could send an extra field such as `is_admin`.

```php
#[Fillable(['name'])]
class Flight extends Model {}
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
#[Fillable(['options->enabled'])]   // JSON columns need each key listed
#[Unguarded]                        // all attributes assignable; hand-craft arrays
```

JSON nested keys are not supported with `Guarded`. Unfillable attributes are silently discarded unless `Model::preventSilentlyDiscardingAttributes($this->app->isLocal())` is set in `boot`.

Upsert (atomic): values, unique-by columns, columns to update. Timestamps are set automatically if enabled on the model:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

All databases except SQL Server need a primary or unique index on the unique-by columns; MariaDB and MySQL ignore that argument and use the table's primary and unique indexes.

Change tracking:

```php
$user->title = 'Painter';
$user->isDirty(); $user->isDirty('title'); $user->isClean(['first_name', 'title']);
$user->save();
$user->wasChanged('title');   // changed when last saved in this request cycle
$user->getOriginal('name');   // value as retrieved
$user->getChanges();          // attributes changed in last save
$user->getPrevious();         // their values before that save
```

## Checked

Date: 2026-11-07

Read: eloquent.md, Inserts, Updates, Mass Assignment, Upserts (lines 788-1120).

Matched against the page, claim by claim:

- save() sets created_at/updated_at -> :825; saveOrFail transaction -> :827; create needs Fillable or Guarded -> :843, :1019
- updateOrFail -> :860; updateOrCreate persists; wasRecentlyCreated -> :866-885
- mass update returns rows, no saving/saved/updating/updated events -> :900-903
- isDirty/isClean/wasChanged/getOriginal/getChanges/getPrevious -> :908-1004
- Fillable, fill, JSON key Fillable([options->enabled]), Guarded no nested JSON -> :1023-1065; Unguarded -> :1070-1084
- preventSilentlyDiscardingAttributes -> :1092-1103
- upsert args, timestamps, SQL Server exception, MariaDB/MySQL ignore -> :1109-1119

Changes made (trims and rewordings):

- Upsert timestamps were stated unconditionally; page says only "if timestamps are enabled on the model" (:1109). Added the condition.
- wasChanged comment "changed in last save" widened to the page wording: last saved within the current request cycle (:939).

Method: documentation only; no commands were run.
