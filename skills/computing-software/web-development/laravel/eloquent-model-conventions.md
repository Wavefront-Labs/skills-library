---
id: computing-software.web-development.laravel.eloquent-model-conventions
name: eloquent-model-conventions
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, models, make-model, conventions]
level: practitioner
status: docs-checked
description: "Generate Eloquent models with make:model and configure table, key, timestamps, connection, defaults and strictness using attributes."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate a model (in `app/Models`, extends `Illuminate\Database\Eloquent\Model`):

```shell
php artisan make:model Flight -mfsc      # migration, factory, seeder, controller
php artisan make:model Flight --all      # also policy and form requests (-a)
php artisan make:model Flight -crR       # controller, resource, form requests
php artisan make:model Member --pivot    # pivot model (-p)
php artisan model:show Flight            # overview of attributes and relations
```

Defaults: table is the snake-case plural of the class (`AirTrafficController` uses `air_traffic_controllers`), primary key is an incrementing integer `id`, and `created_at`/`updated_at` exist. Override with attributes:

```php
use Illuminate\Database\Eloquent\Attributes\Table;

#[Table('my_flights')]
#[Table(key: 'flight_id')]
#[Table(key: 'uuid', keyType: 'string', incrementing: false)]
#[Table(timestamps: false)]
#[Table(dateFormat: 'U')]
```

Single-purpose attributes: `#[WithoutIncrementing]`, `#[WithoutTimestamps]`, `#[DateFormat('U')]`, `#[Connection('mysql')]`.

Custom timestamp columns use constants `public const CREATED_AT = 'creation_date';` and `UPDATED_AT`. Skip touching `updated_at` with `Model::withoutTimestamps(fn () => $post->increment('reads'));`.

Composite primary keys are not supported; add extra multi-column unique indexes instead.

Default attribute values use raw storable format:

```php
protected $attributes = ['options' => '[]', 'delayed' => false];
```

Generated database columns can be re-read after insert/update: `#[Refreshes('name')]` or `#[Refreshes(['name', 'slug'])]`.

Strictness, typically in `AppServiceProvider::boot`:

```php
Model::preventLazyLoading(! $this->app->isProduction());
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

The second throws when filling an attribute missing from `fillable`.

## Checked

Date: 2026-11-07

Read: eloquent.md, Generating Model Classes, Eloquent Model Conventions (lines 52-470).

Matched against the page, claim by claim:

- make:model flags --migration/-m, -f, -s, -c, -crR, -mfsc, --all/-a, --pivot/-p, model:show -> :61-107
- snake plural table, AirTrafficController -> air_traffic_controllers -> :131; Table attribute -> :143
- key, keyType, incrementing args; WithoutIncrementing -> :164-198; composite keys unsupported -> :208
- timestamps false, WithoutTimestamps, dateFormat/DateFormat, CREATED_AT/UPDATED_AT, withoutTimestamps -> :280-374
- Connection attribute -> :390; $attributes raw storable format -> :400-419; Refreshes -> :426-444
- preventLazyLoading, preventSilentlyDiscardingAttributes -> :451-469

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
