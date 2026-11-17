---
id: computing-software.web-development.nestjs.query-parameters-and-parsers
name: query-parameters-and-parsers
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, query-parameters, express, fastify, parsing]
level: practitioner
status: docs-checked
description: "Read NestJS query parameters, convert numeric values with pipes, and enable nested or array query parsing on Express, Fastify or the Node adapter."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/controllers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `@Query()` to read the query string:

```typescript
@Get()
async findAll(@Query('age') age: number, @Query('breed') breed: string) {
  return `filtered by age: ${age} and breed: ${breed}`;
}
```

`GET /cats?age=2&breed=Persian` gives `age` as the string `'2'`. The `number` annotation does not convert; apply a pipe such as `ParseIntPipe` (`@Query('age', ParseIntPipe) age: number`).

`@Body()`, `@Query()`, `@Param()` and `@RawBody()` also accept an options object with `schema` and `pipes`, which attaches a Standard Schema compatible schema (Zod, Valibot, ArkType):

```typescript
@Get(':id')
findOne(@Param('id', { schema: z.coerce.number().int().positive() }) id: number) {
  return this.catsService.findOne(id);
}
```

The schema is only metadata. Register the built-in `StandardSchemaValidationPipe` or a custom pipe that reads `metadata.schema` to actually validate.

For nested objects or arrays (`?filter[where][name]=John`, `?item[]=1&item[]=2`) configure the adapter parser.

Express:

```typescript
const app = await NestFactory.create<NestExpressApplication>(AppModule);
app.set('query parser', 'extended');
```

Fastify (install `qs` with `npm install qs`):

```typescript
new FastifyAdapter({
  routerOptions: { querystringParser: (str) => qs.parse(str) },
})
```

Node adapter: `new NodeAdapter({ querystringParser: (str) => qs.parse(str) })`.

Gotcha: values are always strings unless a pipe or transform converts them.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: @Query behaviour, strings not converted, ParseIntPipe, schema and pipes options, extended query parser, Fastify routerOptions.querystringParser, Node adapter option, qs (controllers page). Removed: invented Verify step.

Method: documentation only; no commands were run.
