---
id: computing-software.web-development.laravel.eloquent-polymorphic-relationships
name: eloquent-polymorphic-relationships
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, polymorphic, morph-map]
level: advanced
status: docs-checked
description: "Define polymorphic Eloquent relations with morphTo, morphOne, morphMany, morphToMany, morph maps via enforceMorphMap and runtime relations."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A child can belong to more than one model type through one association. The child table holds `<name>_type` and `<name>_id` columns (for example `imageable_type`, `imageable_id`; the type holds a class name such as `App\Models\Post`).

One to one / one to many:

```php
// Child
public function imageable(): MorphTo { return $this->morphTo(); }
// Parents
public function image(): MorphOne { return $this->morphOne(Image::class, 'imageable'); }
public function comments(): MorphMany { return $this->morphMany(Comment::class, 'commentable'); }
```

`$post->image`, and `$image->imageable` returns a `Post` or `User` instance. Custom column names: `return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');` and always pass the relationship name first.

N+1 on `$comment->commentable` after eager loading: use `->morphMany(Comment::class, 'commentable')->chaperone()`, or at run time `Post::with(['comments' => fn ($c) => $c->chaperone()])`.

One of many: `morphOne(Image::class, 'imageable')->latestOfMany()`, `->oldestOfMany()` or `->ofMany('likes', 'max')`.

Many to many: tables `posts`, `videos`, `tags`, and `taggables` (`tag_id`, `taggable_type`, `taggable_id`):

```php
// Post and Video
public function tags(): MorphToMany { return $this->morphToMany(Tag::class, 'taggable'); }
// Tag, one method per parent type
public function posts(): MorphToMany { return $this->morphedByMany(Post::class, 'taggable'); }
public function videos(): MorphToMany { return $this->morphedByMany(Video::class, 'taggable'); }
```

Custom types: store aliases instead of class names so renaming a class does not invalidate rows. Call in `AppServiceProvider::boot`:

```php
Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
$alias = $post->getMorphClass();
$class = Relation::getMorphedModel($alias);
```

When adding a morph map to an existing app, every `*_type` value still holding a fully-qualified class name must be converted to its map name.

Dynamic relationships (mainly for packages), configured in a service provider `boot`; always give explicit key names:

```php
Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Polymorphic Relationships (lines 1060-1560).

Matched against the page, claim by claim:

- _type/_id columns, class-name type -> :1064, :1503
- morphTo/morphOne/morphMany; custom columns with __FUNCTION__ -> One To One / One To Many sections
- chaperone N+1 -> :1306 and following; latestOfMany/oldestOfMany/ofMany -> :1360-1362
- morphToMany/morphedByMany with taggables -> :1410
- enforceMorphMap, getMorphClass, getMorphedModel, existing rows must be converted -> :1510-1529
- dynamic relationships resolveRelationUsing, always explicit keys -> :1548

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
