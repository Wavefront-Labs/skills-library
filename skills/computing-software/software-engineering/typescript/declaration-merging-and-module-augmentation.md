---
id: computing-software.software-engineering.typescript.declaration-merging-and-module-augmentation
name: declaration-merging-and-module-augmentation
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsconfig, typescript-build, module-augmentation, declaration-merging, global-augmentation, interface-merging]
level: practitioner
status: verified
description: "Extend third-party and global types safely with interface merging, module augmentation (Express Request, Vue, env vars) and global augmentation, and debug why it doesn't apply."
sources:
  - https://www.typescriptlang.org/docs/handbook/declaration-merging.html
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html
  - https://expressjs.com/en/guide/using-middleware.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaration merging and module augmentation

**Goal:** add fields to types you do not own (a framework's request object, `process.env`, `Window`) in one typed place.

## 1. What merges
- Interfaces with the same name in the same scope merge their members.
- Namespaces merge with namespaces, classes, functions and enums (adding static members).
- Type aliases (`type X = ...`) never merge; that is a reason libraries expose extension points as interfaces.

## 2. Module augmentation
```ts
// src/types/express.d.ts
import "express";                         // makes this file a module so it augments, not replaces
declare module "express-serve-static-core" {
  interface Request {
    user?: { id: string; roles: string[] };
    requestId: string;
  }
}
```
Augment the module that actually **declares** the interface (`express-serve-static-core` for Express's `Request`), found via go-to-definition.

Other common targets:
```ts
declare module "vue" { interface ComponentCustomProperties { $t: (k: string) => string } }
declare module "fastify" { interface FastifyRequest { user: User } }
declare module "@tanstack/react-router" { interface Register { router: typeof router } }
```
You can add members, not new top-level exports, and not change existing member types incompatibly.

## 3. Global augmentation
```ts
// src/types/env.d.ts
export {};
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      NODE_ENV: "development" | "test" | "production";
    }
  }
  interface Window { dataLayer: unknown[] }
}
```
Typing `ProcessEnv` asserts presence without checking it; validate env at startup (Zod/envalid) and export a typed config object instead where possible.

## 4. When the augmentation does not apply
- File not included: check `tsc --listFiles | grep express.d.ts`, `include` globs, and that `.d.ts` is not under an excluded folder.
- File is a script instead of a module (no import/export) for module augmentation: it then declares an ambient module that **replaces** the real one, making everything else `any` or missing.
- Wrong module specifier (augmenting `"express"` instead of the declaring module).
- Duplicate package versions in `node_modules` (two `@types/express-serve-static-core`): augmentation lands on one copy.

## Gotchas
- Augmentations are global to the compilation: test files and app share them; keep them in one `src/types/` folder.
- Marking augmented fields required (`requestId: string`) is a promise that middleware always sets it; make them optional if any route can skip the middleware.
- Libraries should not augment globals in their published types unless that is their purpose; it leaks into every consumer.

## Verify
- `req.user` autocompletes in a handler file without imports from the types file, and removing the types file causes compile errors there.
