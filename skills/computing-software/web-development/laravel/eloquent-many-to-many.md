---
id: computing-software.web-development.laravel.eloquent-many-to-many
name: eloquent-many-to-many
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, belongs-to-many, pivot]
level: practitioner
status: docs-checked
description: "Define Eloquent belongsToMany relations with custom pivot tables, withPivot, wherePivot, orderByPivot and custom Pivot models, plus scoped relations."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tables: `users`, `roles`, and an intermediate table named by joining the two model names alphabetically (`role_user`) with `user_id` and `role_id`.

```php
public function roles(): BelongsToMany { return $this->belongsToMany(Role::class); }
// inverse on Role:
public function users(): BelongsToMany { return $this->belongsToMany(User::class); }

return $this->belongsToMany(Role::class, 'role_user');                        // table
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');  // keys: this model, then related
```

Pivot columns are on each related model's `pivot` attribute. Only keys are present unless declared:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
return $this->belongsToMany(Role::class)->withTimestamps();   // needs both created_at and updated_at
return $this->belongsToMany(Podcast::class)->as('subscription')->withTimestamps();
// then $podcast->subscription->created_at
```

Filter and order by pivot columns when defining the relation:

```php
->wherePivot('approved', 1)
->wherePivotIn('priority', [1, 2])      // wherePivotNotIn
->wherePivotBetween('created_at', [$from, $to])   // wherePivotNotBetween
->wherePivotNull('expired_at')          // wherePivotNotNull
->withPivotValue('approved', 1)         // filter AND set when creating
->orderByPivotDesc('created_at')        // orderByPivot
```

`wherePivot` only filters; it does not set the value on newly created pivot rows, so use `withPivotValue` for both.

Custom pivot model: `->using(RoleUser::class)`; extend `Illuminate\Database\Eloquent\Relations\Pivot` (or `MorphPivot` for polymorphic many-to-many). Pivot models may not use `SoftDeletes`. If the pivot has an auto-incrementing key, mark it `#[Table(incrementing: true)]`. When the pivot defines `belongsTo` relations to both sides, `->using(RoleUser::class)->chaperone()` hydrates them (pass `chaperone(declaring: 'role', related: 'user')` for non-standard names).

Scoped relationships: build narrower relations from a broader one, and use `withAttributes` so created models get the attributes too:

```php
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);   // featured = true
$this->posts()->withAttributes(['featured' => true], asConditions: false);
```

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Many to Many (lines 745-1060).

Matched against the page, claim by claim:

- role_user alphabetical, user_id/role_id -> :752, :813
- withPivot, only keys by default -> :869; timestamps need both columns -> :882; as() accessor
- wherePivot family and withPivotValue; wherePivot does not set value on create -> :910-943; orderByPivot -> :949-954
- custom pivot ->using, Pivot/MorphPivot; no SoftDeletes -> :1000; Table(incrementing: true) -> :1005-1011
- chaperone on pivot with declaring/related names -> :1021, :1053-1058
- scoped relationships withAttributes, asConditions false -> :718-741

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
