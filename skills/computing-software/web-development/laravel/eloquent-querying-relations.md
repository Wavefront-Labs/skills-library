---
id: computing-software.web-development.laravel.eloquent-querying-relations
name: eloquent-querying-relations
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, wherehas, withcount, aggregates]
level: practitioner
status: docs-checked
description: "Query Eloquent relations with has, whereHas, doesntHave, whereRelation and morph queries, and aggregate related rows with withCount, withSum and loadCount."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calling the relation method gives a query builder: `$user->posts()->where('active', 1)->get();`. Accessing the property (`$user->posts`) lazy loads.

Beware `orWhere` after a relation: `->where('active', 1)->orWhere('votes', '>=', 100)` produces `where user_id = ? and active = 1 or votes >= 100`, which escapes the user constraint. Group it:

```php
$user->posts()->where(function (Builder $query) {
    return $query->where('active', 1)->orWhere('votes', '>=', 100);
})->get();
```

Existence and absence (relations must be in the same database):

```php
Post::has('comments')->get();
Post::has('comments', '>=', 3)->get();
Post::has('comments.images')->get();
Post::whereHas('comments', fn (Builder $q) => $q->where('content', 'like', 'code%'), '>=', 10)->get();
Post::doesntHave('comments')->get();
Post::whereDoesntHave('comments.author', fn (Builder $q) => $q->where('banned', 1))->get();
Post::whereRelation('comments', 'is_approved', false)->get();
Post::whereRelation('comments', 'created_at', '>=', now()->minus(hours: 1))->get();
User::whereAttachedTo($role)->get();      // many-to-many attachment, model or collection
```

Also `orHas`, `orWhereHas`, `orDoesntHave`, `orWhereDoesntHave`, `orWhereRelation`, `whereMorphRelation`.

Morph to:

```php
Comment::whereHasMorph('commentable', [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';
        $query->where($column, 'like', 'code%');
    })->get();
Comment::whereDoesntHaveMorph('commentable', Post::class, fn ($q) => $q->where('title', 'like', 'code%'));
Comment::whereMorphedTo('commentable', $post)->orWhereMorphedTo('commentable', $video)->get();
Comment::whereHasMorph('commentable', '*', fn ($q) => $q->where('title', 'like', 'foo%'));  // extra query to find types
```

Counts and aggregates add `{relation}_count` and `{relation}_{function}_{column}` attributes:

```php
Post::withCount('comments')->get();                    // comments_count
Post::withCount(['votes', 'comments' => fn (Builder $q) => $q->where('content', 'like', 'code%')]);
Post::withCount(['comments', 'comments as pending_comments_count' => fn ($q) => $q->where('approved', false)]);
Post::withSum('comments', 'votes')->get();             // comments_sum_votes
Post::withSum('comments as total_comments', 'votes');  // alias
// also withMin, withMax, withAvg, withExists
$book->loadCount('genres');  $post->loadSum('comments', 'votes');   // after retrieval
```

Call `withCount` and the other aggregates after `select`, or the select replaces them: `Post::select(['title', 'body'])->withCount('comments')`.

Morph-to counts: `ActivityFeed::with(['parentable' => fn (MorphTo $m) => $m->morphWithCount([Photo::class => ['tags'], Post::class => ['comments']])])` and deferred `$activities->loadMorphCount('parentable', [...])`.

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Querying Relations through Counting Related Models (lines 1560-2000).

Matched against the page, claim by claim:

- relationship method is a query builder; orWhere escapes user constraint; SQL shown -> :1592-1628
- has/whereHas/doesntHave/whereRelation/whereAttachedTo; same database only -> :1673-1739, :1690, :1695-1706, :1712-1724
- whereHasMorph, whereMorphedTo, "*" wildcard runs an extra query -> :1805-1821
- withCount/withSum/withMin/withMax/withAvg/withExists naming -> :1884, :1906; call after select -> :1895, :1936
- morphWithCount and loadMorphCount -> :1947-1975

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
