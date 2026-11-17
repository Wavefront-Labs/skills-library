---
id: computing-software.web-development.nestjs.custom-validation-pipes
name: custom-validation-pipes
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, pipes, validation, zod, class-validator]
level: advanced
status: docs-checked
description: "Write a custom NestJS PipeTransform using ArgumentMetadata, with Zod schemas or class-validator and class-transformer, and bind it per method, param or globally."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/pipes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pipe implements `PipeTransform<T, R>` with `transform(value, metadata: ArgumentMetadata)`. The returned value replaces the argument. `ArgumentMetadata` has `type` (`'body' | 'query' | 'param' | 'custom'`), `metatype` (e.g. `String`; `Object` if the param is typed as an interface, `undefined` in plain JS), `data` (the string passed to the decorator) and `schema` (a Standard Schema attached via decorator options).

Zod pipe:

```typescript
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodType) {}
  transform(value: unknown, metadata: ArgumentMetadata) {
    try {
      return this.schema.parse(value);
    } catch (error) {
      throw new BadRequestException('Validation failed');
    }
  }
}

@Post()
@UsePipes(new ZodValidationPipe(createCatSchema))
async create(@Body() createCatDto: CreateCatDto) {}
```

Zod needs `strictNullChecks` enabled in `tsconfig.json`. A pipe can also target one parameter: `@Body(new ZodValidationPipe(createCatSchema)) body: CreateCatDto`.

class-validator variant (TypeScript only; `npm i --save class-validator class-transformer`):

```typescript
@Injectable()
export class ValidationPipe implements PipeTransform<any> {
  async transform(value: any, { metatype }: ArgumentMetadata) {
    if (!metatype || !this.toValidate(metatype)) return value;
    const object = plainToInstance(metatype, value);
    const errors = await validate(object);
    if (errors.length > 0) throw new BadRequestException('Validation failed');
    return value;
  }
  private toValidate(metatype: Function): boolean {
    return ![String, Boolean, Number, Array, Object].includes(metatype);
  }
}
```

Decorate the DTO with `@IsString()`, `@IsInt()` etc.; `plainToInstance` is needed because the deserialized body carries no type information. Global binding: `app.useGlobalPipes(new ValidationPipe())` or `{ provide: APP_PIPE, useClass: ValidationPipe }`.

Gotcha: these are teaching samples; the docs point to the built-in `ValidationPipe` and `StandardSchemaValidationPipe` for production.

## Checked

2026-11-04. Read the whole pipes page (`content/pipes.md` in nestjs/docs.nestjs.com). Confirmed `PipeTransform<T, R>`, `ArgumentMetadata` fields, the interface-to-`Object` warning, the Zod pipe and `@UsePipes()`/parameter binding, the `strictNullChecks` warning, the class-validator and class-transformer pipe and `plainToInstance` reason, `useGlobalPipes()` and `APP_PIPE`, and the pointer to the built-in pipes. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
