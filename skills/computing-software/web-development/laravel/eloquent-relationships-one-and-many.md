---
id: computing-software.web-development.laravel.eloquent-relationships-one-and-many
name: eloquent-relationships-one-and-many
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, has-one, has-many, belongs-to]
level: practitioner
status: docs-checked
description: "Define Eloquent hasOne, hasMany and belongsTo relationships with custom keys, chaperone, withDefault and whereBelongsTo."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Relationships are methods on the model that return a relation object; they also act as query builders: `$user->posts()->where('active', 1)->get();`. Access the results as dynamic properties: `User::find(1)->phone`.

```php
public function phone(): HasOne       { return $this->hasOne(Phone::class); }
public function comments(): HasMany   { return $this->hasMany(Comment::class); }
public function user(): BelongsTo     { return $this->belongsTo(User::class); }
```

Key conventions for `hasOne`/`hasMany`: the child has `<snake_parent>_id` (for `Post`, `post_id`) matching the parent's primary key. Override with arguments:

```php
$this->hasOne(Phone::class, 'foreign_key', 'local_key');
$this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

For `belongsTo`, the foreign key is the relationship method name plus `_` and the parent's primary key column (a `user` method implies `user_id`). Override: `$this->belongsTo(User::class, 'foreign_key', 'owner_key');`.

N+1 trap: eager loading `comments` does not hydrate `$comment->post` on each child. Add `chaperone()`:

```php
return $this->hasMany(Comment::class)->chaperone();
Post::with(['comments' => fn ($comments) => $comments->chaperone()])->get();   // at run time
```

Default models (Null Object pattern) work on `belongsTo`, `hasOne`, `hasOneThrough` and `morphOne`:

```php
return $this->belongsTo(User::class)->withDefault();
return $this->belongsTo(User::class)->withDefault(['name' => 'Guest Author']);
return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
    $user->name = 'Guest Author';
});
```

Query children of a belongs-to relationship without writing the foreign key:

```php
Post::whereBelongsTo($user)->get();
Post::whereBelongsTo($users)->get();            // collection: belongs to any
Post::whereBelongsTo($user, 'author')->get();   // name the relationship
```

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Introduction, One to One, One to Many, Belongs To (lines 60-420).

Matched against the page, claim by claim:

- relationship methods are query builders; dynamic properties -> :67
- hasOne/hasMany/belongsTo conventions, custom keys -> :112, :157, :310-324
- chaperone N+1 -> :239; default models on belongsTo, hasOne, hasOneThrough, morphOne -> :339
- whereBelongsTo with model, collection, relationship name -> Querying Belongs To Relationships section

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
