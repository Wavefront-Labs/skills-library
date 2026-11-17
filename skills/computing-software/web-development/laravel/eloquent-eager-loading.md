---
id: computing-software.web-development.laravel.eloquent-eager-loading
name: eloquent-eager-loading
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, eager-loading, n-plus-one, lazy-loading]
level: practitioner
status: docs-checked
description: "Avoid N+1 queries in Eloquent with with, nested and constrained eager loads, withWhereHas, load, automatic eager loading and preventLazyLoading."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
N+1: looping `Book::all()` and reading `$book->author->name` runs one query plus one per book (26 queries for 25 books). Eager load: `Book::with('author')->get();` runs two queries.

```php
Book::with(['author', 'publisher'])->get();
Book::with('author.contacts')->get();
Book::with(['author' => ['contacts', 'publisher']])->get();
Book::with('author:id,name,book_id')->get();   // always include id and foreign keys
```

Default eager loads via `protected $with = ['author'];` on the model. Per query: `Book::without('author')->get();` or `Book::withOnly('genre')->get();`.

Constrain eager loads:

```php
User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%')->orderBy('created_at', 'desc');
}])->get();
User::withWhereHas('posts', fn ($query) => $query->where('featured', true))->get();  // filter parents and load matches
```

`morphTo` relations run one query per type:

```php
ActivityFeed::query()->with(['parentable' => function (MorphTo $morphTo) {
    $morphTo->morphWith([Event::class => ['calendar'], Photo::class => ['tags'], Post::class => ['author']]);
}])->get();

Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => fn ($query) => $query->whereNull('hidden_at'),
        Video::class => fn ($query) => $query->where('type', 'educational'),
    ]);
}])->get();
```

Lazy eager loading after retrieval:

```php
$books->load('author', 'publisher');
$author->load(['books' => fn ($query) => $query->orderBy('published_date', 'asc')]);
$book->loadMissing('author');
$activities->loadMorph('parentable', [Event::class => ['calendar'], Post::class => ['author']]);
```

Automatic eager loading, in `AppServiceProvider::boot`, lazy-eager-loads any relationship you access for the whole retrieved collection:

```php
Model::automaticallyEagerLoadRelationships();
$users->withRelationshipAutoloading();   // opt in for one collection instead
```

Prevent lazy loading, so violations throw `Illuminate\Database\LazyLoadingViolationException`:

```php
Model::preventLazyLoading(! $this->app->isProduction());
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    info("Attempted to lazy load [{$relation}] on model [" . $model::class . "].");
});
```

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Eager Loading through Preventing Lazy Loading (lines 2000-2400).

Matched against the page, claim by claim:

- 25 books -> 26 queries -> :2016
- with() variants, nested, column selection with id and foreign keys -> :2115
- $with default, without(), withOnly() -> Eager Loading By Default section
- constraints, withWhereHas -> :2172, :2240
- morphWith, constrain, load, loadMissing, loadMorph -> Eager Loading Morph To Relationships / Lazy Eager Loading
- automaticallyEagerLoadRelationships and withRelationshipAutoloading -> :2296-2333
- preventLazyLoading, LazyLoadingViolationException, handleLazyLoadingViolationUsing -> :2355-2362

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
