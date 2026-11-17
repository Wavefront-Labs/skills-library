---
id: computing-software.web-development.nestjs.middleware-class-and-consumer
name: middleware-class-and-consumer
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, middleware, middlewareconsumer, routing, express]
level: practitioner
status: docs-checked
description: "Create NestJS class or functional middleware and apply it in configure() with MiddlewareConsumer, forRoutes, exclude, wildcards and global app.use."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Middleware runs before the route handler and gets `req`, `res` and `next`. It must call `next()` or end the response, otherwise the request hangs. Write a class (with `@Injectable()`, implementing `NestMiddleware`, DI supported) or a plain function:

```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log('Request...');
    next();
  }
}
export function logger(req: Request, res: Response, next: NextFunction) { next(); }
```

Register in the module class, not in `@Module()`:

```typescript
@Module({ imports: [CatsModule] })
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware)
      .exclude({ path: 'cats', method: RequestMethod.POST }, 'cats/{*splat}')
      .forRoutes(CatsController);
  }
}
```

`forRoutes()` takes strings, a `{ path, method }` object, or controller classes. `configure()` may be async. `apply()` accepts several middleware that run in order: `consumer.apply(cors(), helmet(), logger)`.

Wildcards need a name in this path syntax: `'abcd/*splat'` matches `abcd/1` but not `abcd/`; `'abcd/{*splat}'` makes it optional.

Global middleware: `app.use(logger)`. It cannot use the DI container, so use functional middleware there or bind a class with `.forRoutes('*')`.

Gotchas:
- With Express, Nest registers `json` and `urlencoded` body parsers by default; to customize them via the consumer set `bodyParser: false` in `NestFactory.create()`.
- `exclude()` paths are written without the global prefix. If an exclusion matches a path that is excluded from the global prefix and has no parameters or wildcards, the middleware is skipped for it too. `'health/*splat'` does not match `/health` itself, so list `'health'` as well.
- Express and Fastify have different middleware signatures.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: class and functional middleware, configure(), forRoutes/exclude/apply, splat wildcards, global app.use, bodyParser gotcha, exclude and global prefix (middlewares page). Removed: invented Verify step; reworded the global-prefix exclusion note to match the page.

Method: documentation only; no commands were run.
