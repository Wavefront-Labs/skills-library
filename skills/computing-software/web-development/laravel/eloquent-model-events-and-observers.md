---
id: computing-software.web-development.laravel.eloquent-model-events-and-observers
name: eloquent-model-events-and-observers
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, events, observers, model-lifecycle]
level: practitioner
status: docs-checked
description: "Hook into Eloquent model lifecycle events with dispatchesEvents, closures and observers, handle events after commit, and mute events when needed."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Events dispatched: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`. Names ending `-ing` fire before changes persist, `-ed` after. `saving`/`saved` fire on create or update even when attributes are unchanged.

Map events to event classes (each receives the model in its constructor):

```php
protected $dispatchesEvents = [
    'saved' => UserSaved::class,
    'deleted' => UserDeleted::class,
];
```

Closures, registered in `booted`; wrap in `queueable()` to run in the background:

```php
protected static function booted(): void
{
    static::created(function (User $user) { /* ... */ });
    static::created(queueable(function (User $user) { /* ... */ }));
}
```

(`use function Illuminate\Events\queueable;`)

Observers group listeners in one class whose methods are named after the events:

```shell
php artisan make:observer UserObserver --model=User
```

Places the observer in `app/Observers` (created if missing) with `created`, `updated`, `deleted`, `restored` and `forceDeleted` methods, each taking the model. Register with an attribute or in `AppServiceProvider::boot`:

```php
#[ObservedBy([UserObserver::class])]
class User extends Authenticatable {}

User::observe(UserObserver::class);
```

Implement `Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit` on the observer to run handlers only after the surrounding database transaction commits; with no transaction they run immediately.

Mass updates and deletes dispatch no `saved`, `updated`, `deleting` or `deleted` events because models are never retrieved.

Mute events:

```php
$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();
    return User::find(2);
});
$user->saveQuietly();
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```

## Checked

Date: 2026-11-07

Read: eloquent.md, Events (lines 1775-2010).

Matched against the page, claim by claim:

- event list incl. trashed, forceDeleting, replicating -> :1781; -ing before / -ed after; saving/saved fire even if unchanged -> :1783
- $dispatchesEvents -> :1785-1810; mass update/delete skip saved/updated/deleting/deleted -> :1816
- closures in booted, queueable -> :1821-1852
- make:observer --model, app/Observers, five methods -> :1860-1917; ObservedBy and observe() -> :1919-1945
- ShouldHandleEventsAfterCommit, immediate when no transaction -> :1953
- withoutEvents, saveQuietly/deleteQuietly/forceDeleteQuietly/restoreQuietly -> :1978-2008

Changes made (trims and rewordings):

- Skill said the command creates "app/Observers/UserObserver.php"; the page says only that the observer is placed in app/Observers (:1866). Reworded to the directory.

Method: documentation only; no commands were run.
