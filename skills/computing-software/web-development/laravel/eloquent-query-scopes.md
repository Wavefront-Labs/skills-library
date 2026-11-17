---
id: computing-software.web-development.laravel.eloquent-query-scopes
name: eloquent-query-scopes
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, scopes, global-scopes, local-scopes]
level: practitioner
status: docs-checked
description: "Define Eloquent global scopes with make:scope and ScopedBy, local scopes with the Scope attribute, dynamic scope parameters and withAttributes."
sources:
  - https://laravel.com/docs/eloquent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global scope: constrains every query for a model. Generate with `php artisan make:scope AncientScope` (placed in `app/Models/Scopes`), implement `Illuminate\Database\Eloquent\Scope::apply`:

```php
class AncientScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

If a scope adds columns to the select, use `addSelect`, not `select`, so the existing select is not replaced.

Apply it with an attribute, or register in `booted`:

```php
#[ScopedBy([AncientScope::class])]
class User extends Model {}

protected static function booted(): void
{
    static::addGlobalScope(new AncientScope);
    static::addGlobalScope('ancient', function (Builder $builder) {   // anonymous, needs a name
        $builder->where('created_at', '<', now()->minus(years: 2000));
    });
}
```

Remove for a query:

```php
User::withoutGlobalScope(AncientScope::class)->get();
User::withoutGlobalScope('ancient')->get();
User::withoutGlobalScopes()->get();
User::withoutGlobalScopes([FirstScope::class, SecondScope::class])->get();
User::withoutGlobalScopesExcept([SecondScope::class])->get();
```

Local scope: add the `Scope` attribute to a protected model method that returns the same builder or `void`. Extra parameters follow `$query`:

```php
#[Scope]
protected function popular(Builder $query): void { $query->where('votes', '>', 100); }

#[Scope]
protected function ofType(Builder $query, string $type): void { $query->where('type', $type); }

User::popular()->active()->orderBy('created_at')->get();
User::ofType('admin')->get();
```

Inside the model, call scopes through a builder such as `static::query()->ofType('admin')`.

Combining scopes with `or` needs closures for correct grouping, or the higher-order form:

```php
User::popular()->orWhere(function (Builder $query) { $query->active(); })->get();
User::popular()->orWhere->active()->get();
```

Pending attributes: `$query->withAttributes(['hidden' => true]);` inside a scope adds where conditions and also sets those attributes on models created through the scope, so `Post::draft()->create(['title' => 'In Progress'])->hidden` is `true`. Pass `asConditions: false` to skip the where conditions.

## Checked

Date: 2026-11-07

Read: eloquent.md, Query Scopes (lines 1440-1750).

Matched against the page, claim by claim:

- global scope: make:scope into app/Models/Scopes, apply(Builder, Model) -> :1451, :1460-1480; addSelect note -> :1484
- ScopedBy; booted + addGlobalScope; anonymous name -> :1489-1559
- withoutGlobalScope(s) and withoutGlobalScopesExcept -> :1564-1590
- Scope attribute, protected, same builder or void -> :1596-1598, :1689; dynamic scopes -> :1659-1686
- orWhere closure grouping and higher-order orWhere -> :1642-1654
- withAttributes adds where conditions and creates with attributes; asConditions false -> :1694-1734

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
