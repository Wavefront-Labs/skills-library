---
id: computing-software.software-engineering.quarkus.quarkus-permissions-allowed-checkers
name: quarkus-permissions-allowed-checkers
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, permissionsallowed, permissionchecker, rolesallowed, security-annotations, custom-permission, authorization]
level: advanced
status: docs-checked
description: "Use Quarkus security annotations: RolesAllowed property expressions, deny-unannotated settings, PermissionsAllowed, PermissionChecker and custom Permission classes."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-authorize-web-endpoints-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus annotation-based authorization

## Annotations

`@DenyAll`, `@PermitAll` (even unauthenticated), `@RolesAllowed`, `io.quarkus.security.Authenticated` (same as `@RolesAllowed("**")`), `@PermissionsAllowed`, `@AuthorizationPolicy`. HTTP permissions (`quarkus.http.auth.`) are checked before these annotations, so `@PermitAll` cannot override an HTTP-level restriction.

Defaults: `quarkus.security.jaxrs.deny-unannotated-endpoints=true` makes unannotated REST endpoints behave as `@DenyAll`; `quarkus.security.jaxrs.default-roles-allowed=role1,role2` sets default roles (`**` means any authenticated user; cannot be combined with deny-unannotated); `quarkus.security.deny-unannotated-members=true` denies unannotated members in classes that have annotated methods.

`@RolesAllowed` accepts property expressions: `"${admin-role}"`, `"${tester.group}-${tester.role}"`, and defaults `"${customer:User}"`, resolved at runtime. A list-valued property such as `all-roles=Administrator,Software,Tester,User` is treated as a List. Profile prefixes work, for example `%dev.secured=**`.

When implementing an interface, put class-level annotations on the implementing class and method-level ones on the implementing method. Secured subresource locators must not be default interface methods.

## @PermissionsAllowed

- Repeated annotations on a method: all required. Within one annotation, at least one of the values unless `inclusive=true`.
- `"see:detail"` is name `see` and action `detail`. Escape a literal colon as `resource\\:name:action`; in `application.properties` write `\\\\:`.
- `permission = CustomPermission.class` selects a custom `java.security.Permission`; the default is `io.quarkus.security.StringPermission`. The class has exactly one constructor: first parameter `String` name, optional second `String[]` actions, further parameters matched by name to the secured method's arguments. `params = "beanParam.securityContext.userPrincipal.name"` reaches into a `@BeanParam`.
- Not repeatable on a class. Does not work with custom Jakarta REST SecurityContexts.
- Grant permissions from roles: `quarkus.http.auth.policy.role-policy1.permissions.admin=create,update,read`, with `permission-class=org.acme.crud.CRUDResource$CustomPermission` for custom ones. Register custom permission classes for reflection (`@RegisterForReflection`) for native builds unless used in a `permission` attribute.

## @PermissionChecker

Mark a CDI bean method instead of granting permissions to the identity:

```java
@PermissionsAllowed("rename-project")
@POST
public void renameProject(@RestPath String projectName, @RestForm String newName) { ... }

@PermissionChecker("rename-project")
boolean canRenameProject(SecurityIdentity identity, String projectName) { ... }
```

Rules: the value must string-equal the `@PermissionsAllowed` value (escape characters included); return `boolean` or `Uni<Boolean>`; no private methods; bean must be normal scoped or `@Singleton` (not `@Dependent`); with `inclusive=true` there must be one checker per permission; checkers run on the event loop, so add `@Blocking` to run on a worker thread. A `SecurityIdentity` parameter can be declared on any checker method; see the page's `canDeleteFile` example for a checker that takes the secured method's argument.

A meta-annotation can wrap `@PermissionsAllowed(value = "write", permission = CustomPermission.class)`.

## Checked

2026-11-07. Matched against the text (with includes) of: security-authorize-web-endpoints-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that checker parameters are matched by name to the secured method's; the page only shows a `SecurityIdentity` parameter and the `canDeleteFile` example that takes the secured method's argument.

Method: documentation only; no commands were run.
