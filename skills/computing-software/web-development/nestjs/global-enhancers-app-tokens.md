---
id: computing-software.web-development.nestjs.global-enhancers-app-tokens
name: global-enhancers-app-tokens
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, guards, pipes, interceptors, filters, dependency-injection]
level: practitioner
status: docs-checked
description: "Register global NestJS guards, pipes, interceptors and filters either with useGlobal methods or APP_ tokens so they can inject dependencies."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/guards.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/pipes.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/interceptors.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/exception-filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each cross-cutting component can be bound at parameter/method, controller, or global scope. For global scope there are two routes.

Imperative (no DI, because it runs outside any module):

```typescript
const app = await NestFactory.create(AppModule);
app.useGlobalGuards(new RolesGuard());
app.useGlobalPipes(new ValidationPipe());
app.useGlobalInterceptors(new LoggingInterceptor());
app.useGlobalFilters(new HttpExceptionFilter());
```

Declarative with DI, inside any module:

```typescript
import { APP_GUARD, APP_PIPE, APP_INTERCEPTOR, APP_FILTER } from '@nestjs/core';

@Module({
  providers: [
    { provide: APP_GUARD, useClass: RolesGuard },
    { provide: APP_PIPE, useClass: ValidationPipe },
    { provide: APP_INTERCEPTOR, useClass: LoggingInterceptor },
    { provide: APP_FILTER, useClass: HttpExceptionFilter },
  ],
})
export class AppModule {}
```

The component is global regardless of the module that registers it; the docs recommend the module where the class is defined. `useClass` is not the only way to register a custom provider.

Binding by class (`@UseGuards(RolesGuard)`) leaves instantiation to Nest and enables DI; passing an in-place instance (`new RolesGuard()`) is also allowed. For filters the docs add that binding by class reduces memory usage because Nest can reuse instances.

Gotchas:
- `useGlobalGuards()` and `useGlobalPipes()` do not set up components for connected microservices in a hybrid application (see the hybrid application docs to change it); `useGlobalFilters()` does not cover gateways or hybrid apps.
- `APP_GUARD` can be registered several times; all run in registration order. These tokens are pseudo-providers and cannot be fetched with `app.get()`.

## Checked

2026-11-04. Read the whole guards, pipes, interceptors and exception filters pages (`content/guards.md`, `pipes.md`, `interceptors.md`, `exception-filters.md` in nestjs/docs.nestjs.com). Confirmed the `useGlobal*()` methods, the no-DI limitation outside modules, the `APP_*` tokens and that they are global whichever module registers them, the hybrid-app notices for guards, pipes and filters, repeated `APP_GUARD` registration in order, the pseudo-provider note and the filter memory hint. Removed: the "memory" claim for guards (only the filters page makes it), the `useFactory` example (the pages only say `useClass` is not the only way) and the invented console-log Verify step.
Method: documentation only; no commands were run.
