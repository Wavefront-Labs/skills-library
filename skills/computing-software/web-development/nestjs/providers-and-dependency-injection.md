---
id: computing-software.web-development.nestjs.providers-and-dependency-injection
name: providers-and-dependency-injection
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, providers, dependency-injection, injectable, services]
level: intro
status: docs-checked
description: "Create injectable NestJS services, register them in a module, inject by constructor or property, mark optional dependencies and avoid interface injection errors."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A provider is any class Nest's IoC container can inject: services, repositories, factories, helpers. Mark it with `@Injectable()` and list it in a module's `providers` array.

```typescript
@Injectable()
export class CatsService {
  private readonly cats: Cat[] = [];
  create(cat: Cat) { this.cats.push(cat); }
  findAll(): Cat[] { return this.cats; }
}

@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}
}

@Module({ controllers: [CatsController], providers: [CatsService] })
export class AppModule {}
```

Nest resolves dependencies by the constructor parameter type, which TypeScript emits as metadata. The default singleton is created once and shared. Scaffold with `nest g service cats`.

Optional dependencies resolve to `undefined` instead of failing startup; the class supplies the fallback:

```typescript
constructor(@Optional() @Inject('HTTP_OPTIONS') private httpClient: T) {}
```

Property injection suits base classes where passing deps through `super()` is cumbersome:

```typescript
@Injectable()
export class HttpService<T> {
  @Inject('HTTP_OPTIONS')
  private readonly httpClient: T;
}
```

Prefer constructor injection when the class does not extend another.

Gotcha: the annotation must exist at runtime, so a class. If `AppConfig` is an interface or type alias (or a class imported with `import type`), Nest fails at startup with a "Nest can't resolve dependencies" error. Register such values under a token and use `@Inject()`. For retrieving providers manually, use `ModuleRef` or a standalone application.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: @Injectable, providers array, constructor resolution by type, interface injection error, @Optional, property injection, nest g service (components page). Removed: NEST_DEBUG claim (not on the page); invented Verify step.

Method: documentation only; no commands were run.
