---
id: computing-software.web-development.nestjs.middleware-error-handling
name: middleware-error-handling
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, middleware, exceptions, authentication, error-handling]
level: practitioner
status: docs-checked
description: "Handle errors thrown from NestJS middleware by throwing HttpException, async rejections or next(error), and understand that only global filters apply."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Exceptions thrown by middleware bound through `MiddlewareConsumer` go to Nest's exceptions layer, like handler errors.

Synchronous:

```typescript
@Injectable()
export class AuthMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    if (!req.headers.authorization) {
      throw new UnauthorizedException();
    }
    next();
  }
}
```

Async: declare `use()` as `async` (or return a Promise) so a rejection is forwarded:

```typescript
async use(req: Request, res: Response, next: NextFunction) {
  const user = await this.authService.verify(req.headers.authorization);
  if (!user) throw new UnauthorizedException();
  req['user'] = user;
  next();
}
```

Callback style, handy when wrapping Express middleware:

```typescript
return next(new UnauthorizedException());
```

Gotchas:
- Middleware runs before a handler is selected, so only global exception filters (`app.useGlobalFilters()` or `APP_FILTER`) catch these errors; method or controller `@UseFilters()` are not invoked and `@UseFilters()` on a middleware class is unsupported.
- Middleware registered with `app.use()` is handled by Express or Fastify, not Nest's middleware module. Prefer throwing or `next(err)` in consumer-bound middleware.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: throwing HttpException, async rejection, next(error), global-filters-only warning, app.use() hint (middlewares page, Error handling). Removed: guard advice not on the page; invented Verify step.

Method: documentation only; no commands were run.
