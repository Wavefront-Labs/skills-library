---
id: computing-software.web-development.laravel.eloquent-has-one-of-many-and-through
name: eloquent-has-one-of-many-and-through
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, has-one-of-many, has-many-through]
level: advanced
status: docs-checked
description: "Define latestOfMany, oldestOfMany and ofMany relations, convert has-many to has-one, and build hasOneThrough and hasManyThrough relationships."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Has one of many: a `hasOne` that picks one row from many.

```php
return $this->hasOne(Order::class)->latestOfMany();
return $this->hasOne(Order::class)->oldestOfMany();
return $this->hasOne(Order::class)->ofMany('price', 'max');   // column, then min or max
```

`latestOfMany` and `oldestOfMany` sort on the primary key by default, which must be sortable. PostgreSQL cannot run `MAX` on UUID columns, so one-of-many does not work with PostgreSQL UUID columns.

Reuse an existing has-many with `one()`; it also converts `HasManyThrough` to `HasOneThrough`:

```php
return $this->orders()->one()->ofMany('price', 'max');
return $this->deployments()->one()->latestOfMany();
```

Advanced: pass sort columns as an array and a closure adding constraints (latest published price not in the future, ties by greatest id):

```php
return $this->hasOne(Price::class)->ofMany([
    'published_at' => 'max',
    'id' => 'max',
], function (Builder $query) {
    $query->where('published_at', '<', now());
});
```

Has one through (mechanic to owner via car; tables `mechanics`, `cars.mechanic_id`, `owners.car_id`):

```php
return $this->hasOneThrough(Owner::class, Car::class);
```

Has many through (application to deployments via environments):

```php
return $this->hasManyThrough(Deployment::class, Environment::class);
```

First argument is the final model, second the intermediate one. Keys, in order: foreign key on the intermediate model, foreign key on the final model, local key, local key of the intermediate model:

```php
return $this->hasManyThrough(
    Deployment::class, Environment::class,
    'application_id',  // foreign key on environments
    'environment_id',  // foreign key on deployments
    'id',              // local key on applications
    'id'               // local key on environments
);
```

If the relations already exist on the models, use `through`, which reuses their key conventions:

```php
return $this->through('environments')->has('deployments');
return $this->throughEnvironments()->hasDeployments();
```

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Has One of Many, Has One Through, Has Many Through (lines 400-740).

Matched against the page, claim by claim:

- latestOfMany/oldestOfMany sort on primary key which must be sortable -> :433; ofMany(column, min|max) -> :435
- PostgreSQL cannot MAX on UUID, so no one-of-many with PostgreSQL UUID columns -> :448
- one() converts has many and HasManyThrough -> :453, :469-478
- advanced ofMany with array and closure -> Advanced Has One of Many section
- hasOneThrough args and six-key form -> :544-579; through()/throughX magic -> :555, :645-648, :679-682

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
