---
id: computing-software.web-development.nestjs.validation-pipe-class-validator
name: validation-pipe-class-validator
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, validation, validationpipe, class-validator, dto]
level: practitioner
status: docs-checked
description: "Validate NestJS request DTOs globally with ValidationPipe and class-validator, with whitelist, forbidNonWhitelisted, transform and arrays."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm i --save class-validator class-transformer`. Bind globally:

```typescript
app.useGlobalPipes(new ValidationPipe());
```

DTOs must be concrete classes; TypeScript emits no metadata for interfaces or generics, and a type-only import (`import type`) is erased at runtime.

```typescript
export class CreateUserDto {
  @IsEmail()
  email: string;
  @IsNotEmpty()
  password: string;
}
```

An invalid body yields `400` with `{"statusCode":400,"error":"Bad Request","message":["email must be an email"]}`. Validate params with a class too (`FindOneParams` with `@IsNumberString() id: string`).

Options on the constructor:
- `whitelist: true` strips properties with no validation decorator; add `forbidNonWhitelisted: true` to reject instead.
- `transform: true` turns payloads into DTO instances and converts primitives: `@Param('id') id: number` really is a number.
- `disableErrorMessages: true` hides details in production.
- `exceptionFactory`, `errorHttpStatusCode`, `stopAtFirstError`, `groups`, `skipMissingProperties`, `errorFormat: 'list' | 'grouped'`.

Arrays are not validated by the pipe (no metadata for generics). Use `ParseArrayPipe`:

```typescript
@Post()
createBulk(@Body(new ParseArrayPipe({ items: CreateUserDto })) createUserDtos: CreateUserDto[]) {}

@Get()
findByIds(@Query('ids', new ParseArrayPipe({ items: Number, separator: ',' })) ids: number[]) {}
```

Without `transform`, convert explicitly with `ParseIntPipe` or `ParseBoolPipe` (there is no `ParseStringPipe`).

Gotcha: for WebSockets and microservices, return `WsException` or `RpcException` from `exceptionFactory`, because the default throws an HTTP exception.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: global ValidationPipe, DTO class rule, 400 body, params validation, option table, errorFormat, ParseArrayPipe, transform, WsException note (validation page). Removed: invented Verify step.

Method: documentation only; no commands were run.
