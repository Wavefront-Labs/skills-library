---
id: computing-software.web-development.nestjs.request-lifecycle-order
name: request-lifecycle-order
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, request-lifecycle, middleware, guards, interceptors]
level: practitioner
status: docs-checked
description: "Know the exact NestJS order of middleware, guards, interceptors, pipes and exception filters across global, controller and route scopes."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/request-lifecycle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Order of a request:

1. Incoming request
2. Middleware: global (`app.use()`) first, then module-bound by path. Between modules: global modules (`@Global()`), then root module, then others ordered by distance from root.
3. Guards: global, controller, route; within a level in binding order. `@UseGuards(Guard1, Guard2)` on the class and `@UseGuards(Guard3)` on the handler run 1, 2, 3.
4. Interceptors (pre-controller): global, controller, route.
5. Pipes: global, controller, route, then route-parameter pipes.
6. Controller handler, then service.
7. Interceptors (post-request): route, controller, global (first-in, last-out, since they are RxJS Observables).
8. Exception filters: route, controller, global.
9. Server response.

Pipe detail: pipes passed to `@UsePipes()` run in order, but among several parameters Nest processes the last parameter first. For

```typescript
@UsePipes(GeneralValidationPipe)
@Controller('cats')
export class CatsController {
  @UsePipes(RouteSpecificPipe)
  @Patch(':id')
  updateCat(@Body() body, @Param() params, @Query() query) {}
}
```

`GeneralValidationPipe` runs on `query`, then `params`, then `body`, then `RouteSpecificPipe` in the same order; parameter-specific pipes follow.

Filters are the only component not resolved global-first: Nest checks route-bound, then controller, then global filters. One filter catching an exception stops others from seeing it; use inheritance to chain.

"Global" means registered with `app.useGlobalGuards()` (or a similar method) or an `APP_*` token such as `APP_GUARD`. Filters only run for uncaught exceptions; exceptions you catch yourself do not trigger them. Errors from middleware reach only global filters. Errors from pipes, controllers and services can be read in an interceptor's `catchError`.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: component order, pipe parameter order, filter order, interceptor first-in last-out, filters and middleware errors (request-lifecycle page). Removed: generic useGlobalX wording; invented Verify step.

Method: documentation only; no commands were run.
