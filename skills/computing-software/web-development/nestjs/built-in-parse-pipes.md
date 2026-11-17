---
id: computing-software.web-development.nestjs.built-in-parse-pipes
name: built-in-parse-pipes
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, pipes, parseintpipe, validation, transformation]
level: intro
status: docs-checked
description: "Use NestJS built-in Parse pipes (ParseIntPipe, ParseUUIDPipe, DefaultValuePipe and more) to convert and validate route and query parameters."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/pipes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pipes transform or validate handler arguments just before the method runs. A pipe that throws stops the handler; the error goes to the exceptions layer. Built-in pipes from `@nestjs/common`: `ValidationPipe`, `StandardSchemaValidationPipe`, `ParseIntPipe`, `ParseFloatPipe`, `ParseBoolPipe`, `ParseArrayPipe`, `ParseUUIDPipe`, `ParseEnumPipe`, `DefaultValuePipe`, `ParseFilePipe`, `ParseDatePipe`.

Bind at parameter level, passing the class so Nest handles instantiation:

```typescript
@Get(':id')
async findOne(@Param('id', ParseIntPipe) id: number) {
  return this.catsService.findOne(id);
}
```

`GET /abc` yields 400:

```json
{ "statusCode": 400, "message": "Validation failed (numeric string is expected)", "error": "Bad Request" }
```

Pass an instance to customize options:

```typescript
@Param('id', new ParseIntPipe({ errorHttpStatusCode: HttpStatus.NOT_ACCEPTABLE })) id: number
@Param('uuid', new ParseUUIDPipe()) uuid: string
```

`ParseUUIDPipe` accepts any UUID version by default (1 to 8, Nil, Max); pass `version` to restrict it. From NestJS v12.1.2, `version` also accepts numbers (for example `7`) and `'all'`; the `UUIDVersion` type is exported from `@nestjs/common`.

All `Parse*` pipes work on params, query values and body values, and by default throw on `null`/`undefined` unless `optional: true`. To supply defaults for missing query values, put `DefaultValuePipe` first:

```typescript
@Get()
async findAll(
  @Query('activeOnly', new DefaultValuePipe(false), ParseBoolPipe) activeOnly: boolean,
  @Query('page', new DefaultValuePipe(0), ParseIntPipe) page: number,
) {}
```

## Checked

2026-11-04. Read the whole pipes page (`content/pipes.md` in nestjs/docs.nestjs.com). Confirmed the built-in pipe list, parameter binding, the 400 response body, `errorHttpStatusCode`, `ParseUUIDPipe` version behaviour (v12.1.2, `'all'`, `UUIDVersion`), `optional`, and `DefaultValuePipe` ordering. Removed the TypeScript-annotation gotcha and the Verify step (neither is on the page).
Method: documentation only; no commands were run.
