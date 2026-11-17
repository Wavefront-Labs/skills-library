---
id: computing-software.web-development.nestjs.injection-tokens-interfaces
name: injection-tokens-interfaces
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, dependency-injection, tokens, symbols, abstract-classes]
level: practitioner
status: docs-checked
description: "Inject NestJS dependencies typed by interfaces using Symbol or string tokens, or use an abstract class as both contract and token."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/dependency-injection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TypeScript interfaces and types are erased at compile time, so they cannot be DI tokens. Two patterns solve this.

Symbol or string token with `@Inject()`:

```typescript
export interface LoggerService { log(message: string): void; }
export const LOGGER_SERVICE = Symbol('LOGGER_SERVICE');

@Injectable()
export class PinoLoggerService implements LoggerService {
  log(message: string) { /* ... */ }
}

@Module({
  providers: [{ provide: LOGGER_SERVICE, useClass: PinoLoggerService }],
})
export class AppModule {}

@Injectable()
export class CatsService {
  constructor(@Inject(LOGGER_SERVICE) private readonly logger: LoggerService) {}
}
```

Abstract class as contract and token (no `@Inject()` needed):

```typescript
export abstract class LoggerService {
  abstract log(message: string): void;
}

{ provide: LoggerService, useClass: PinoLoggerService }

constructor(private readonly logger: LoggerService) {}
```

Strings, symbols and enums are all valid token values. Symbols have unique runtime identity, which avoids accidental collisions between unrelated providers using the same string, so they suit libraries and larger apps. Export the symbol from a shared file and reuse the same instance where the provider is registered and injected.

Choosing: symbol or string when the token should be decoupled from a class; abstract class when one artifact should be contract plus token with simpler injection; plain interface when only compile-time checking is needed.

Gotcha: each `Symbol('X')` call has its own unique runtime identity, so export the symbol from a shared file and reuse that same instance wherever the provider is registered and injected; a second `Symbol('LOGGER_SERVICE')` is a different token.

## Checked

2026-11-04. Read the whole custom providers page (`content/fundamentals/dependency-injection.md` in nestjs/docs.nestjs.com), including the "Interfaces and abstract classes" section. Confirmed interface erasure, the Symbol token with `@Inject()`, the abstract-class contract and token, symbol, string and enum tokens, symbol identity and the shared-file advice, and the choosing guidance. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
