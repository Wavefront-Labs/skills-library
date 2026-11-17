---
id: computing-software.cybersecurity-defensive.authentik.application-entitlements
name: application-entitlements
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, entitlements, authorization, property-mappings, application-access]
level: practitioner
status: docs-checked
description: "Use authentik application entitlements (2024.12) to manage authorization inside an application, retrieve them in mappings, and bind users or groups."
sources:
  - https://docs.goauthentik.io/add-secure-apps/applications/manage_apps/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control what a user can do within an application, after they already have access to it.

Facts: entitlements are scoped to a single application, names must be unique per application, they can be bound to users and groups (binding policies is not supported), and they are deleted with the application. An app can read them via the `entitlements` scope or via entitlement attributes.

## Create
1. **Applications > Applications**, open the application.
2. **Application entitlements** tab > **New Entitlement**: name, optional **Attributes**, **Create**.
3. Expand the entitlement (caret), **Bind existing group/user**, choose Group or User, **Create**.

## Use in property mappings or policies
```python
entitlements = [entitlement.name for entitlement in request.user.app_entitlements(provider.application)]
return {
    "entitlements": entitlements,
}
```
Attributes stored on entitlements:
```python
attrs = request.user.app_entitlements_attributes(provider.application)
return {
    "my_attr": attrs.get("my_attr")
}
```
Pass the specific application to both helpers.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text. Dropped the proxy outpost X-authentik-entitlements header sentence: the entitlements page does not cover it.

Method: documentation only; no commands were run.
