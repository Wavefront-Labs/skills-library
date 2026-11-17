---
id: computing-software.web-development.laravel.api-resources-basics
name: api-resources-basics
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, api-resources, json, collections, pagination]
level: practitioner
status: docs-checked
description: "Transform Eloquent models to JSON with make:resource, JsonResource, ResourceCollection, toResource discovery, data wrapping and paginated responses."
sources:
  - https://laravel.com/docs/eloquent-resources
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate into `app/Http/Resources`:

```shell
php artisan make:resource UserResource
php artisan make:resource User --collection      # or name it UserCollection
```

A resource extends `Illuminate\Http\Resources\Json\JsonResource` and returns an array from `toArray(Request $request)`. Property and method access on `$this` proxies to the model.

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'posts' => PostResource::collection($this->posts),
    ];
}

return new UserResource(User::findOrFail($id));
return User::findOrFail($id)->toResource();                    // convention-based discovery
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

Discovery looks for a resource named after the model (optionally suffixed `Resource`) in the nearest `Http\Resources` namespace. Override with `#[UseResource(CustomUserResource::class)]` on the model, or `#[UseResourceCollection(CustomUserCollection::class)]` for collections.

Collections:

```php
return UserResource::collection(User::all());
return User::all()->toResourceCollection();
return new UserCollection(User::all());
```

A dedicated `ResourceCollection` is needed to add meta; its `toArray` returns `['data' => $this->collection, 'links' => ['self' => 'link-value']]`. `UserCollection` maps items to `UserResource`; change that with `#[Collects(Member::class)]`. Collection keys are reset to numeric order; keep them with `#[PreserveKeys]` on the resource, for example `UserResource::collection(User::all()->keyBy->id)`.

Data wrapping: the outermost resource is wrapped in `data`. Disable it in `AppServiceProvider::boot` with `JsonResource::withoutWrapping();`; this does not remove `data` keys you add yourself. Laravel never double-wraps. Paginated responses are always wrapped because they carry `links` and `meta`.

Pagination: pass a paginator to a collection or call `User::paginate()->toResourceCollection()`. The response includes `links` (first, last, prev, next) and `meta` (current_page, from, last_page, path, per_page, to, total). Customise with a `paginationInformation($request, $paginated, $default)` method on the resource, which returns the (modified) `$default` array, for example `$default['links']['custom'] = 'https://example.com';`.

## Checked

Date: 2026-11-07

Read: eloquent-resources.md, Introduction, Generating Resources, Concept Overview, Resource Collections, Data Wrapping, Pagination (lines 1-620).

Matched against the page, claim by claim:

- make:resource User --collection or name ending Collection -> :43-48
- toArray(Request) and $this proxies to model -> :74, :89
- toResource() discovery: name matches model, optional Resource suffix, nearest Http\Resources namespace -> :106; UseResource attribute -> :108-119; UseResourceCollection -> :154-165
- toResourceCollection() -> :149, :152 (suffix Collection)
- dedicated ResourceCollection needed to add meta; data/links example -> :181-187, :206
- UserCollection maps to UserResource, Collects attribute -> :271-281
- keys reset to numeric order, PreserveKeys, keyBy->id example -> :238, :248, :262
- outermost wrapped in data; withoutWrapping in AppServiceProvider; does not remove your own data keys -> :428, :447, :478
- Laravel never double-wraps -> :485; paginated always wrapped even with withoutWrapping -> :511
- links first/last/prev/next and meta current_page..total -> :527-541; paginationInformation($request,$paginated,$default) -> :602-617

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
