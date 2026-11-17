---
id: computing-software.web-development.angular.injection-context
name: injection-context
category: computing-software
field: web-development
product: angular
tags: [angular, di, inject, injection-context, runininjectioncontext, assertininjectioncontext, ng0203]
level: practitioner
status: docs-checked
description: "Where inject() works in Angular: constructors, field initializers, factories, guards; runInInjectionContext, assertInInjectionContext and error NG0203."
sources:
  - https://angular.dev/guide/di/dependency-injection-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
DI relies on a runtime context where the current injector is available. You have an injection context:
- during construction (the `constructor`) of a class instantiated by DI, such as an `@Injectable` or `@Component`,
- in field initializers of such classes,
- in the factory function for `useFactory` of a `Provider` or an `@Injectable`,
- in the `factory` function of an `InjectionToken`,
- within a stack frame that runs in an injection context.

Some APIs are designed to run in one, such as router guards, so `inject` works inside the guard function:

```ts
const canActivateTeam: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  return inject(PermissionsService).canActivate(inject(UserToken), route.params.id);
};
```

Run code in a context you do not already have with `runInInjectionContext`, passing an injector such as `EnvironmentInjector`. `inject` returns an instance only if that injector can resolve the token.

```ts
@Service()
export class HeroService {
  private environmentInjector = inject(EnvironmentInjector);
  someMethod() {
    runInInjectionContext(this.environmentInjector, () => {
      inject(SomeService);
    });
  }
}
```

Assert the context with `assertInInjectionContext`, passing a reference to the calling function so the error message points to the right API:

```ts
export function injectNativeElement<T extends Element>(): T {
  assertInInjectionContext(injectNativeElement);
  return inject(ElementRef).nativeElement;
}
```

Calling such a helper in a field initializer works (`readonly hostEl = injectNativeElement<HTMLElement>();`); calling it in a method like `onAction()` fails because it runs outside an injection context.

Calling `inject` or `assertInInjectionContext` outside a context throws error NG0203.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/di/dependency-injection-context (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
