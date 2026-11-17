---
id: computing-software.web-development.laravel.eloquent-saving-related-models
name: eloquent-saving-related-models
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, relationships, attach, sync, associate, touches]
level: practitioner
status: docs-checked
description: "Save related Eloquent models with save, create, associate, attach, detach, sync, toggle and updateExistingPivot, and touch parent timestamps."
sources:
  - https://laravel.com/docs/eloquent-relationships
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Call the relation method (not the property) to add children; the foreign key is set for you:

```php
$post->comments()->save(new Comment(['message' => 'A new comment.']));
$post->comments()->saveMany([new Comment([...]), new Comment([...])]);
$comment = $post->comments()->create(['message' => 'A new comment.']);
$post->comments()->createMany([['message' => 'A'], ['message' => 'B']]);
$user->posts()->createQuietly([...]);   // createManyQuietly; no events
```

`save` and `saveMany` do not add the new models to relations already loaded in memory; call `$post->refresh()` before reading `$post->comments`. `create` takes arrays, so mass assignment rules apply. `findOrNew`, `firstOrNew`, `firstOrCreate` and `updateOrCreate` also work on relations.

Save a model plus its loaded relations with `$post->push();` (`pushQuietly()` raises no events).

Belongs to: set or clear the parent with `associate` and `dissociate`, then save the child:

```php
$user->account()->associate(Account::find(10));
$user->save();
$user->account()->dissociate();
$user->save();
```

Many to many pivot operations:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
$user->roles()->attach([1 => ['expires' => $expires], 2 => ['expires' => $expires]]);
$user->roles()->detach($roleId);          // detach() with no argument detaches all
$user->roles()->detach([1, 2, 3]);
$user->roles()->sync([1, 2, 3]);          // IDs not listed are removed
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
$user->roles()->syncWithoutDetaching([1, 2, 3]);
$user->roles()->toggle([1, 2, 3]);
$user->roles()->updateExistingPivot($roleId, ['active' => false]);
```

`detach` removes only the intermediate row; both models remain. Transactional variants roll back on exception: `attachOrFail`, `detachOrFail`, `syncOrFail`, `syncWithoutDetachingOrFail`, `toggleOrFail`.

Touch parent timestamps when a child is updated by listing relation names in the `Touches` attribute:

```php
#[Touches(['post'])]
class Comment extends Model
{
    public function post(): BelongsTo { return $this->belongsTo(Post::class); }
}
```

Parent timestamps update only when the child is updated with Eloquent's `save`.

## Checked

Date: 2026-11-07

Read: eloquent-relationships.md, Inserting and Updating Related Models (lines 2380-2643).

Matched against the page, claim by claim:

- save/saveMany/create/createMany; not added to loaded relations, use refresh -> :2399-2404
- createQuietly/createManyQuietly -> :2456-2461; findOrNew/firstOrNew/firstOrCreate/updateOrCreate -> :2471; mass assignment -> :2474
- push/pushQuietly -> :2421-2427; associate/dissociate
- attach/detach(no arg detaches all)/sync/syncWithPivotValues/syncWithoutDetaching/toggle/updateExistingPivot -> :2521-2590
- OrFail variants transactional -> :2592
- Touches attribute, parent updated only via Eloquent save -> :2618-2643

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
