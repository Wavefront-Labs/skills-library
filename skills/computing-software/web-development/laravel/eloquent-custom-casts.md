---
id: computing-software.web-development.laravel.eloquent-custom-casts
name: eloquent-custom-casts
category: computing-software
field: web-development
product: laravel
tags: [laravel, eloquent, custom-casts, value-objects, castables]
level: advanced
status: docs-checked
description: "Write custom Eloquent casts with make:cast and CastsAttributes: value objects, inbound-only casts, cast parameters, comparison and Castable classes."
sources:
  - https://laravel.com/docs/eloquent-mutators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate a cast into `app/Casts`: `php artisan make:cast AsJson`. Implement `Illuminate\Contracts\Database\Eloquent\CastsAttributes` with `get` (raw value to cast value) and `set` (cast value to storable value):

```php
class AsJson implements CastsAttributes
{
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
// model: protected function casts(): array { return ['options' => AsJson::class]; }
```

Value objects over several columns: `get` builds the object from `$attributes`; `set` returns an array of column => value (return a single storable value if only one column is involved). Changes to the object sync back before `save()`. For `toArray`/`toJson`, implement `Arrayable` and `JsonSerializable` on the object, or have the cast implement `SerializesCastableAttributes` with a `serialize(Model $model, string $key, mixed $value, array $attributes)` method. Resolved objects are cached; disable with `public bool $withoutObjectCaching = true;` on the cast class.

Inbound-only casts transform values being set and do nothing on read. Implement `CastsInboundAttributes` (only `set`), or generate with `php artisan make:cast AsHash --inbound`:

```php
class AsHash implements CastsInboundAttributes
{
    public function __construct(protected string|null $algorithm = null) {}
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return is_null($this->algorithm) ? bcrypt($value) : hash($this->algorithm, $value);
    }
}
// 'secret' => AsHash::class.':sha256'
```

Parameters follow the class name after `:`, comma-delimited, and go to the cast constructor.

Custom change detection: implement `ComparesCastableAttributes` with `compare(Model $model, string $key, mixed $firstValue, mixed $secondValue): bool`, returning `true` when values are equal; Eloquent uses it to decide what to save.

Castables: attach a value object that implements `Illuminate\Contracts\Database\Eloquent\Castable` instead of a cast class; `castUsing(array $arguments)` returns the caster class name (or, for a self-contained object, an anonymous class implementing `CastsAttributes`):

```php
'address' => Address::class,
'address' => Address::class.':argument',   // $arguments passed to castUsing
```

## Checked

Date: 2026-11-07

Read: eloquent-mutators.md, Custom Casts through Castables (lines 735-1100).

Matched against the page, claim by claim:

- make:cast, CastsAttributes get/set -> Custom Casts section
- value objects: sync before save; Arrayable+JsonSerializable or SerializesCastableAttributes -> :910, :931
- withoutObjectCaching public property -> :917-922
- CastsInboundAttributes / make:cast --inbound, AsHash with parameters after colon -> :950-1000
- ComparesCastableAttributes::compare -> Comparing Cast Values section; Castable::castUsing -> Castables section

Changes made: none; every claim above is stated by the page at the cited lines.

Method: documentation only; no commands were run.
