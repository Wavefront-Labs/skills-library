---
id: computing-software.web-development.nestjs.execution-context-and-arguments-host
name: execution-context-and-arguments-host
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, execution-context, argumentshost, guards, microservices]
level: advanced
status: docs-checked
description: "Write generic NestJS guards, filters and interceptors that work across HTTP, RPC, WebSockets and GraphQL using ArgumentsHost and ExecutionContext."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/execution-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ArgumentsHost` wraps the arguments passed to a handler. In HTTP/Express it is `[request, response, next]`; in GraphQL `[root, args, context, info]`. Nest hands you a `host` in places like an exception filter's `catch()`.

Detect the context with `host.getType()`, which returns `'http'`, `'rpc'` or `'ws'` (packages add more, e.g. `host.getType<GqlContextType>() === 'graphql'` with `GqlContextType` from `@nestjs/graphql`):

```typescript
if (host.getType() === 'http') { /* REST only */ }
else if (host.getType() === 'rpc') { /* microservice only */ }
```

Avoid raw indexing like `host.getArgs()` or `host.getArgByIndex(0)`, which couples code to one context. Switch instead:

```typescript
const ctx = host.switchToHttp();   // switchToRpc(), switchToWs()
const request = ctx.getRequest<Request>();
const response = ctx.getResponse<Response>();
```

`WsArgumentsHost` offers `getData<T>()` and `getClient<T>()`; `RpcArgumentsHost` offers `getData<T>()` and `getContext<T>()`.

`ExecutionContext` extends `ArgumentsHost` (used in guards and interceptors) with:

```typescript
getClass<T>(): Type<T>;   // controller class
getHandler(): Function;   // handler about to run
```

For `POST` to `CatsController.create()`: `ctx.getHandler().name` is `"create"` and `ctx.getClass().name` is `"CatsController"` (the class, not an instance). These are the targets you pass to `Reflector` to read decorator metadata.

Gotcha: `getClass()` returns the class itself; metadata read with `Reflector` must use `getHandler()` for method-level and `getClass()` for controller-level metadata.

## Checked

2026-11-04. Read the whole execution context page (`content/fundamentals/execution-context.md` in nestjs/docs.nestjs.com). Confirmed `ArgumentsHost` argument shapes, `getType()` values and the `GqlContextType` import, the warning against `getArgs()`/`getArgByIndex()`, the `switchTo*` helpers, `WsArgumentsHost` and `RpcArgumentsHost` methods, `ExecutionContext` `getClass()`/`getHandler()` and the `create`/`CatsController` example, and the `Reflector` handler versus class targets. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
