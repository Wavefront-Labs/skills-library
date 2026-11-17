---
id: computing-software.web-development.nestjs.http-exceptions-and-error-codes
name: http-exceptions-and-error-codes
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, exceptions, httpexception, error-handling, errorcode]
level: intro
status: docs-checked
description: "Throw NestJS HttpException and built-in exceptions with custom bodies, cause, description and machine-readable errorCode, and know what the default filter returns."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/exception-filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The built-in global filter handles `HttpException` and subclasses; anything else becomes `{ "statusCode": 500, "message": "Internal server error" }`.

```typescript
throw new HttpException('Forbidden', HttpStatus.FORBIDDEN);
```

Constructor: `response` (string or object, the body), `status` (use the `HttpStatus` enum) and optional `options` with `cause`. A string replaces only `message`; an object replaces the entire body:

```typescript
throw new HttpException({
  status: HttpStatus.FORBIDDEN,
  error: 'This is a custom message',
}, HttpStatus.FORBIDDEN, { cause: error });
```

The `cause` is never serialized; it exists for logging. An `Error` instance passed as `response` is not serialized either (you get the default body), so pass it as `cause`.

Built-in subclasses (all from `@nestjs/common`) include `BadRequestException`, `UnauthorizedException`, `NotFoundException`, `ForbiddenException`, `ConflictException`, `UnprocessableEntityException`, `InternalServerErrorException`, `ServiceUnavailableException`, `GatewayTimeoutException` and others. Their options take `cause` and `description`:

```typescript
throw new BadRequestException('Something bad happened', {
  cause: new Error(),
  description: 'Some error description',
});
```

Machine-readable code in the response body via `errorCode`, also available on `HttpException`:

```typescript
throw new BadRequestException('Password is too weak', { errorCode: 'WEAK_PASSWORD' });
// { message, error: 'Bad Request', statusCode: 400, errorCode: 'WEAK_PASSWORD' }
```

For custom exceptions extend `HttpException`: `super('Forbidden', HttpStatus.FORBIDDEN)`.

Gotcha: `HttpException` extends `IntrinsicException`, so built-in filters do not log it (same for `WsException` and `RpcException`); add a custom filter to log. A thrown `http-errors`-style error with `statusCode` and `message` is passed through; on v12.2+ if `expose` is false the reason phrase is sent instead.

Verify: throw `BadRequestException` with an `errorCode` and check the JSON includes it.

## Checked

2026-11-04. Read the whole exception filters page (`content/exception-filters.md` in nestjs/docs.nestjs.com). Confirmed the default 500 body, `HttpException` arguments and `cause`, the `Error`-as-response hint, the built-in exception list, `cause` and `description` options, `errorCode`, custom exceptions, `IntrinsicException` logging behaviour and the `http-errors` hint including the v12.2 `expose` behaviour. The Verify step is kept because the page shows the `errorCode` in the response body.
Method: documentation only; no commands were run.
