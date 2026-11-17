---
id: computing-software.web-development.laravel.eloquent-factories-basics
name: eloquent-factories-basics
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, factories, testing, seeding, faker]
level: practitioner
status: docs-checked
description: "Define Laravel model factories with make:factory, states, callbacks and sequences, and create models with make and create, count, overrides and trashed."
sources:
  - https://laravel.com/docs/eloquent-factories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate with `php artisan make:factory PostFactory` (placed in `database/factories`). A factory extends `Illuminate\Database\Eloquent\Factories\Factory` and returns default attributes from `definition()`, using the `fake()` Faker helper (locale: `faker_locale` in `config/app.php`).

```php
public function definition(): array
{
    return [
        'name' => fake()->name(),
        'email' => fake()->unique()->safeEmail(),
        'password' => static::$password ??= Hash::make('password'),
    ];
}
```

Models find their factory through the `HasFactory` trait: class `Database\Factories\<Model>Factory`. Otherwise use `#[UseFactory(FlightFactory::class)]` on the model, or override `protected static function newFactory()` returning `FlightFactory::new()`, then put `#[UseModel(Flight::class)]` on the factory.

States are discrete modifications built with `state`, which gets the raw attributes array:

```php
public function suspended(): Factory
{
    return $this->state(fn (array $attributes) => ['account_status' => 'suspended']);
}
User::factory()->count(5)->suspended()->make();
User::factory()->state(['name' => 'Abigail Otwell'])->make();
```

Soft-deletable models get a built-in `trashed` state: `User::factory()->trashed()->create();`.

Callbacks: register `afterMaking` and `afterCreating` in a `configure(): static` method (called automatically), or inside a state method.

Create models:

```php
$user = User::factory()->make();                   // not persisted
$users = User::factory()->count(3)->create();      // persisted with save()
$user = User::factory()->create(['name' => 'Abigail']);
```

Mass assignment protection is disabled when creating models with factories.

Sequences alternate attribute values; a closure receives the `Sequence` with an `$index` property:

```php
User::factory()->count(10)->state(new Sequence(['admin' => 'Y'], ['admin' => 'N']))->create();
User::factory()->count(10)->state(new Sequence(fn (Sequence $s) => ['name' => 'Name '.$s->index]))->create();
User::factory()->count(2)->sequence(['name' => 'First User'], ['name' => 'Second User'])->create();
```

## Checked

Date: 2026-11-07

Read: eloquent-factories.md in full (676 lines).

Matched against the page, claim by claim:

- make:factory, database/factories -> :88-91; definition() and fake() -> :49-74; faker_locale in config/app.php -> :77
- HasFactory convention Database\Factories\<Model>Factory -> :98; UseFactory -> :104; newFactory + UseModel -> :111-137
- state() receives raw attributes array -> :144-159; trashed state built in -> :165-170
- configure() with afterMaking/afterCreating, auto-called; also inside states -> :176-222
- make vs create (uses save) -> :231-236, :279; count() -> :242; attribute override and state([]) -> :260-270
- mass assignment protection disabled -> :274
- Sequence arrays, closure, $index, sequence() -> :308-352

Changes made (trims and rewordings):

- The UseModel attribute is shown after the newFactory override; reworded "and put" to "then put" so it is not presented as an alternative to UseFactory.

Method: documentation only; no commands were run.
