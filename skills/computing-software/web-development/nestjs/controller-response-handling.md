---
id: computing-software.web-development.nestjs.controller-response-handling
name: controller-response-handling
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, controllers, responses, status-codes, redirect]
level: practitioner
status: docs-checked
description: "Control NestJS response status, headers, redirects, async and Observable returns, and use @Res passthrough without breaking interceptors."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/controllers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nest has two response modes. The standard mode returns a value: objects and arrays are serialized to JSON, primitives are sent as-is. Status is 200, except POST which is 201.

```typescript
@Post()
@HttpCode(204)
@Header('Cache-Control', 'no-store')
create() { return 'This action adds a new cat'; }

@Get('docs')
@Redirect('https://docs.nestjs.com', 302)
getDocs(@Query('version') version) {
  if (version === '5') return { url: 'https://docs.nestjs.com/v5/' };
}
```

`@Redirect(url, statusCode)` defaults to 302; a returned object shaped like `HttpRedirectResponse` overrides the decorator arguments. When the status depends on runtime conditions, throw an exception or use the library response object.

Handlers may be `async`, returning a Promise, or return an RxJS Observable; Nest subscribes and resolves the last emitted value.

The library-specific mode injects `@Res()` (alias of `@Response()`). The moment a handler uses `@Res()` or `@Next()`, the standard mode is disabled for that route and you must send the response yourself (`res.status(HttpStatus.CREATED).send()`), otherwise the request hangs. It also loses compatibility with interceptors and `@HttpCode()` / `@Header()`.

To read or tweak the native response while keeping the framework in charge, set passthrough:

```typescript
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.status(HttpStatus.OK);
  return [];
}
```

Gotcha: handlers using `@Res()` become platform-dependent and harder to test, since you must mock the response object.

## Checked

2026-11-04. Read the whole controllers page (`content/controllers.md` in nestjs/docs.nestjs.com). Confirmed the standard versus library-specific modes, 200/201 defaults, `@HttpCode`, `@Header`, `@Redirect` (default `302`, returned object overrides, `HttpRedirectResponse`), async and Observable handlers, `@Res()` as alias of `@Response()`, the request-hangs warning, loss of interceptor/`@HttpCode()`/`@Header()` compatibility, `passthrough`, and the platform-dependence and testing downsides. Nothing removed.
Method: documentation only; no commands were run.
