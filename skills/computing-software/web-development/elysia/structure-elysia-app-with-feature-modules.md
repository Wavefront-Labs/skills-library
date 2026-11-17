---
id: computing-software.web-development.elysia.structure-elysia-app-with-feature-modules
name: structure-elysia-app-with-feature-modules
category: computing-software
field: web-development
product: elysia
tags: [elysia, best-practice, mvc, controller, service, model, key-concept]
level: advanced
status: docs-checked
description: "Organise an Elysia app into feature folders with an Elysia instance as controller, abstract-class services, TypeBox models, and method chaining for inference."
sources:
  - https://elysiajs.com/essential/best-practice.html
  - https://elysiajs.com/key-concept.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: lay out a codebase that keeps Elysia's type inference intact while following MVC-like separation.

## Folder structure

Elysia is unopinionated; absent a preference the docs recommend feature folders:

```
src/modules/auth/index.ts   (Elysia controller)
src/modules/auth/service.ts (service)
src/modules/auth/model.ts   (model)
src/modules/user/...
src/utils/...
```

## Responsibilities

- Controller (`index.ts`): `export const auth = new Elysia({ prefix: '/auth' })` handles routing, request validation and cookies, calling `Auth.signIn(body)`.
- Service: business logic decoupled from Elysia. If it needs no stored property use `export abstract class Auth { static async signIn(...) }` to avoid allocating an instance; it may `throw status(400, '...')` directly.
- Model: `export const AuthModel = { signInBody: t.Object({...}), ... } as const` plus optional `export type AuthModel = { [k in keyof typeof AuthModel]: UnwrapSchema<typeof AuthModel[k]> }`.

Use `response: { 200: AuthModel.signInResponse, 400: AuthModel.signInInvalid }` to enforce return types.

## Controller rules

1 Elysia instance = 1 controller. Do not pass a whole `Context` into a controller class (`static root(context: Context)`): Elysia's context type depends on plugins and chaining, so it is hard to type and loses integrity. Destructure what you need (`({ body }) => Controller.greet(body)`) or use plain classes unrelated to HTTP.

## Services

Non-request services: static classes or functions. Request-dependent services: an Elysia instance, e.g. `new Elysia({ name: 'Auth.Service' }).macro({ isSignIn: { resolve({ cookie, status }) {...} } })`, applied with `.use()`; the `name` makes it a singleton via deduplication. `decorate` only for request-dependent properties (requestIP, requestTime, session).

## Models

Reuse the validation schema instead of separate interfaces, and do not declare class instances or interfaces as models. Use `UnwrapSchema` or `typeof schema.static` for the TS type.

## Type inference rules (key concept)

- Always use method chaining; unchained calls (`app.state(...)` on a separate line) lose the new type.
- Use inline handler functions for accurate inference.

## Gotchas

- `cookie.name` may appear possibly undefined under strictNullChecks; the cookie is a Proxy so it is always defined, only `.value` can be undefined. Use a cookie schema or relax strictNullChecks.

## Checked

2026-11-07. Read in full: essential/best-practice and key-concept (Method Chaining, Type Inference). Confirmed the feature folder layout, controller, service and model roles, abstract-class services, the one-instance-one-controller rule and the Context-passing warning, request-dependent services with a named macro instance, `decorate` guidance, model rules, the cookie Proxy note, and the chaining and inline-function rules. Nothing removed.

Method: documentation only; no commands were run.
