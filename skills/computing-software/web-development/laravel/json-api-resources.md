---
id: computing-software.web-development.laravel.json-api-resources
name: json-api-resources
category: computing-software
field: web-development
product: laravel
tags: [laravel, api-resources, json-api, sparse-fieldsets, includes]
level: advanced
status: docs-checked
description: "Build JSON:API compliant responses with JsonApiResource: attributes, relationships, include and fields query parameters, type and id, links and meta."
sources:
  - https://laravel.com/docs/eloquent-resources
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Illuminate\Http\Resources\JsonApi\JsonApiResource` extends `JsonResource` and handles resource object structure, relationships, sparse fieldsets, includes and lazy attributes, and sets `Content-Type: application/vnd.api+json`. It serializes responses only; parsing filters and sorts is left to another package.

Generate and return:

```shell
php artisan make:resource PostResource --json-api
```

```php
return new PostResource($post);       // or $post->toResource()
return PostResource::collection(Post::all());   // or Post::all()->toResourceCollection()
```

Output looks like `{"data":{"id":"1","type":"posts","attributes":{"title":"Hello World","body":"This is my first post."}}}`.

Attributes: a `public $attributes = ['title', 'body', 'created_at'];` list read from the model, or override `toAttributes(Request $request)`; closures are evaluated lazily, only if the attribute is needed:

```php
public function toAttributes(Request $request): array
{
    return [
        'title' => $this->title,
        'is_published' => fn () => $this->published_at !== null,
    ];
}
```

Relationships: `public $relationships = ['author', 'comments'];` resolves the Eloquent relation and discovers its resource class, or give key/class pairs (`'author' => UserResource::class`), or override `toRelationships(Request $request)` with closures for control. They are serialized only when requested:

```
GET /api/posts/1?include=author,comments
GET /api/posts/1?include=comments.author
```

The response puts resource identifier objects under `relationships` and full objects in the top-level `included` array. Nested include depth is limited; change it with `JsonApiResource::maxRelationshipDepth(3);` in a service provider.

Type and ID: the type derives from the class name (`PostResource` gives `posts`, `BlogPostResource` gives `blog_posts`), the id from the primary key. Override `toType(Request $request): string` and `toId(Request $request): string`.

Sparse fieldsets: `GET /api/posts?fields[posts]=title,created_at&fields[users]=name`. Disable query string handling with `->ignoreFieldsAndIncludesInQueryString()`. To include all eager-loaded relationships regardless of `include`, call `->includePreviouslyLoadedRelationships()`:

```php
return $post->load('author', 'comments')->toResource()->includePreviouslyLoadedRelationships();
```

Links and meta: override `toLinks(Request $request)` (for example `['self' => route('api.posts.show', $this->resource)]`) and `toMeta(Request $request)`.

## Checked

Date: 2026-11-07

Read: eloquent-resources.md, JSON:API Resources: Introduction through Links and Meta (lines 898-1246).

Matched against the page, claim by claim:

- extends JsonResource, handles structure/relationships/sparse fieldsets/includes/lazy attributes, Content-Type application/vnd.api+json -> :902
- serialization only; filters and sorts need another package (Spatie named) -> :905
- make:resource --json-api -> :910-913; $attributes/$relationships generated -> :916-942
- closure attributes evaluated only when needed -> :1001; toAttributes -> :1003-1020
- relationships only when include requested; key/class pairs; toRelationships closures -> :1026-1069; relationships/included output -> :1079-1122
- maxRelationshipDepth(3) and nested limited by default -> :1134-1139 (skill makes no claim about the default value)
- type derived from class name, PostResource->posts, BlogPostResource->blog_posts, id from primary key, toType/toId -> :1145-1165
- fields[posts]=... -> :1175; ignoreFieldsAndIncludesInQueryString -> :1183; includePreviouslyLoadedRelationships -> :1193-1198
- toLinks/toMeta -> :1204-1225

Changes made (trims and rewordings):

- Example output did not match the page (title only); replaced with the page output at :965-975 including the body attribute.

Method: documentation only; no commands were run.
