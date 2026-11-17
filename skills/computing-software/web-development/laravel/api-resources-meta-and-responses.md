---
id: computing-software.web-development.laravel.api-resources-meta-and-responses
name: api-resources-meta-and-responses
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, api-resources, meta, responses, headers]
level: practitioner
status: docs-checked
description: "Add meta and links to Laravel API resources with with() and additional(), and customise the outgoing response with response() and withResponse()."
sources:
  - https://laravel.com/docs/eloquent-resources
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Meta inside the resource: include `links` or `meta` in `toArray`. Extra `links`/`meta` you define are merged with paginator output, never overriding it.

Top-level meta only when the resource is outermost: define `with(Request $request): array`:

```php
public function with(Request $request): array
{
    return ['meta' => ['key' => 'value']];
}
```

From the route or controller, `additional()` is available on all resources:

```php
return User::all()->load('roles')->toResourceCollection()->additional(['meta' => ['key' => 'value']]);
```

Pivot data under a custom accessor name (not `pivot`) uses `whenPivotLoadedAs`:

```php
'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {
    return $this->subscription->expires_at;
}),
```

Customise the HTTP response. Chain `response()`, which returns an `Illuminate\Http\JsonResponse`:

```php
return User::find(1)->toResource()->response()->header('X-Value', 'True');
```

Or define `withResponse` on the resource, called when it is the outermost resource:

```php
public function withResponse(Request $request, JsonResponse $response): void
{
    $response->header('X-Value', 'True');
}
```

## Checked

Date: 2026-11-07

Read: eloquent-resources.md, Adding Meta Data, Resource Responses (lines 820-900, 1248-1310).

Matched against the page, claim by claim:

- links/meta inside toArray -> :824; never override paginator links/meta, merged -> :843
- with() only for outermost resource -> :848, :870; additional() on all resources -> :888-895
- whenPivotLoadedAs for accessor other than pivot -> :801-816
- response() returns JsonResponse with header(); withResponse(Request, JsonResponse) for outermost -> :1275-1303

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
