---
id: computing-software.web-development.nestjs.controller-routing-basics
name: controller-routing-basics
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, controllers, routing, decorators, http]
level: intro
status: docs-checked
description: "Define NestJS controllers with route prefixes, HTTP method decorators, route and host parameters, and register them in a module so requests reach handlers."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/controllers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controllers handle incoming requests and return responses. A class is a controller when decorated with `@Controller()`, optionally with a path prefix.

```typescript
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';

@Controller('cats')
export class CatsController {
  @Post()
  create(@Body() createCatDto: CreateCatDto) { return 'adds a cat'; }

  @Get()
  findAll(@Query() query: ListAllEntities) { return 'all cats'; }

  @Get(':id')
  findOne(@Param('id') id: string) { return `cat #${id}`; }
}
```

The route is the controller prefix plus the method decorator path, so `@Get('breed')` inside `@Controller('cats')` maps `GET /cats/breed`. The method name is arbitrary. Decorators exist for `@Get()`, `@Post()`, `@Put()`, `@Delete()`, `@Patch()`, `@Options()`, `@Head()`, `@QueryMethod()` (the QUERY method, named to avoid clashing with `@Query()`) and `@All()`.

Parameter decorators map to the platform request: `@Req()`, `@Res()`, `@Next()`, `@Session()`, `@Param(key?)`, `@Body(key?)`, `@Query(key?)`, `@Headers(name?)`, `@Ip()`, `@HostParam()`.

Sub-domain routing uses the `host` option, with tokens read by `@HostParam()`:

```typescript
@Controller({ host: ':account.example.com' })
export class AccountController {
  @Get()
  getInfo(@HostParam('account') account: string) { return account; }
}
```

Controllers must be listed in a module, otherwise Nest never instantiates them:

```typescript
@Module({ controllers: [CatsController] })
export class AppModule {}
```

Use plain classes (not interfaces) for DTOs such as `CreateCatDto`, because interfaces are erased at compile time and pipes need the runtime metatype. Scaffold with `nest g controller cats`.

Gotcha: Fastify does not support nested routers, so host-based routing needs the Express or Node adapter. Wildcards: `'abcd/*'` works on both; mid-path asterisks are unsupported on Fastify.

## Checked

2026-11-04. Read the whole controllers page (`content/controllers.md` in nestjs/docs.nestjs.com). Confirmed `@Controller()` prefixes, route composition (`GET /cats/breed`), arbitrary method names, the list of HTTP method decorators including `@QueryMethod()` and `@All()`, the parameter decorator table, `host` and `@HostParam()`, the Fastify sub-domain warning, wildcard behaviour on Express and Fastify, controllers needing a module, class-over-interface DTOs and `nest g controller`. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
