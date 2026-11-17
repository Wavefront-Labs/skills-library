---
id: computing-software.web-development.laravel.eloquent-factory-relationships
name: eloquent-factory-relationships
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, factories, relationships, testing]
level: practitioner
status: docs-checked
description: "Build related models with Laravel factories using has, for, hasAttached, magic methods, polymorphic relations, factory-defined relations and recycle."
sources:
  - https://laravel.com/docs/eloquent-factories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Has many with `has` (relationship name assumed as plural model name, or pass it) and magic methods:

```php
User::factory()->has(Post::factory()->count(3))->create();
User::factory()->has(Post::factory()->count(3), 'posts')->create();
User::factory()->hasPosts(3)->create();
User::factory()->hasPosts(3, ['published' => false])->create();
User::factory()->hasPosts(['title' => 'First Post'], ['title' => 'Second Post'])->create();   // per-model state
User::factory()->hasPosts(3, function (array $attributes, User $user) {
    return ['user_type' => $user->type];     // closure gets the parent
})->create();
```

Belongs to with `for`:

```php
Post::factory()->count(3)->for(User::factory()->state(['name' => 'Jessica Archer']))->create();
Post::factory()->count(3)->for($user)->create();       // existing parent
Post::factory()->count(3)->forUser(['name' => 'Jessica Archer'])->create();
```

Many to many uses `has`; pivot attributes need `hasAttached`:

```php
User::factory()->has(Role::factory()->count(3))->create();
User::factory()->hasAttached(Role::factory()->count(3), ['active' => true])->create();
User::factory()->hasAttached(Role::factory(), [['active' => true], ['active' => false]])->create();  // per-model pivot
User::factory()->count(3)->hasAttached($roles, ['active' => true])->create();   // same existing roles on all
User::factory()->hasRoles(1, ['name' => 'Editor'])->create();
```

Polymorphic: morph many works like has many (`Post::factory()->hasComments(3)->create()`). Magic methods do not work for `morphTo`; use `for` with the relationship name:

```php
Comment::factory()->count(3)->for(Post::factory(), 'commentable')->create();
Video::factory()->hasAttached(Tag::factory()->count(3), ['public' => true])->create();
Video::factory()->hasTags(3, ['public' => true])->create();
```

Relationships inside a factory definition: assign a factory to the foreign key; use a closure when a column depends on already-evaluated attributes:

```php
'user_id' => User::factory(),
'user_type' => function (array $attributes) {
    return User::find($attributes['user_id'])->type;
},
```

Recycle one existing model across all relations that need it (for example one airline for both ticket and flight), or a collection from which a random model is chosen:

```php
Ticket::factory()->recycle(Airline::factory()->create())->create();
Ticket::factory()->recycle($airlines)->create();
```

## Checked

Date: 2026-11-07

Read: eloquent-factories.md, Factory Relationships (lines 355-675).

Matched against the page, claim by claim:

- has() with plural relationship name assumed, optional explicit name -> :372-377
- hasPosts magic, attribute override, multiple arrays per-model state, closure with parent -> :401-434
- for() with factory, with instance, forUser magic -> :446-476
- many to many via has(); hasAttached with pivot array, per-model pivot arrays, existing models -> :488-547; hasRoles magic -> :556-560
- morph many same as has many; magic methods not for morphTo, use for() with relationship name -> :566-582; polymorphic many-to-many -> :594-607
- factory in definition for foreign key, closure receives evaluated attributes -> :626, :645
- recycle() single model or collection (random) -> :657-674

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
