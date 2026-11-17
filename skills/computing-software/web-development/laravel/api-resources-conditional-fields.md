---
id: computing-software.web-development.laravel.api-resources-conditional-fields
name: api-resources-conditional-fields
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, api-resources, conditional-attributes, whenloaded]
level: practitioner
status: docs-checked
description: "Include fields in Laravel API resources conditionally with when, mergeWhen, whenLoaded, whenCounted, whenAggregated and whenPivotLoaded."
sources:
  - https://laravel.com/docs/eloquent-resources
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keys whose value comes from these helpers are removed from the response when the condition fails.

```php
'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
'secret' => $this->when($request->user()->isAdmin(), fn () => 'secret-value'),   // lazy value
'name' => $this->whenHas('name'),             // only if present on the model
'name' => $this->whenNotNull($this->name),
```

Several attributes on one condition:

```php
$this->mergeWhen($request->user()->isAdmin(), [
    'first-secret' => 'value',
    'second-secret' => 'value',
]),
```

Do not use `mergeWhen` in arrays that mix string and numeric keys, or whose numeric keys are not sequential.

Relationships appear only if already loaded, which avoids N+1 problems in resources. Pass the relationship name, not the relationship:

```php
'posts' => PostResource::collection($this->whenLoaded('posts')),
```

Counts (after `$user->loadCount('posts')`) and other aggregates:

```php
'posts_count' => $this->whenCounted('posts'),
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),   // also sum, min, max
```

Pivot data from many-to-many relations; pass the pivot table name, or a custom pivot model instance:

```php
'expires_at' => $this->whenPivotLoaded('role_user', function () {
    return $this->pivot->expires_at;
}),
'expires_at' => $this->whenPivotLoaded(new Membership, fn () => $this->pivot->expires_at),
```

## Checked

Date: 2026-11-07

Read: eloquent-resources.md, Conditional Attributes, Conditional Relationships, counts, aggregates, pivot (lines 620-820).

Matched against the page, claim by claim:

- when(cond, value|closure) -> :638, :650; whenHas -> :655-658; whenNotNull -> :661-664
- mergeWhen and warning about mixed/non-sequential numeric keys -> :690-697
- whenLoaded takes the relationship name, avoids N+1 -> :702-704, :720
- loadCount + whenCounted -> :735-752; whenAggregated avg/sum/min/max -> :761-767
- whenPivotLoaded(table, closure) and custom pivot model instance -> :773, :793-799

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
