---
id: computing-software.cybersecurity-defensive.keycloak.custom-rest-endpoint-extension
name: custom-rest-endpoint-extension
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, rest-endpoint, realm-resource-provider, jax-rs, extension]
level: practitioner
status: docs-checked
description: "Add a custom Keycloak REST endpoint with RealmResourceProvider, beans.xml and a Provider annotation, using blocking handlers only."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/extensions.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom rest endpoint extension
Keycloak can be extended with custom REST endpoints, custom SPIs and custom JPA entities. For an endpoint implement `RealmResourceProviderFactory` and `RealmResourceProvider`. The provider's key method is:
```java
Object getResource();
```
It returns an object that acts as a JAX-RS resource.

The server only recognises and registers the resource as a valid endpoint if both hold:
- an empty file named `beans.xml` under `META-INF`;
- the JAX-RS class is annotated with `jakarta.ws.rs.ext.Provider`.

Package and deploy like any provider: a `META-INF/services/<factory interface>` file naming the factory, the JAR copied to the providers directory, then `kc.sh build` or a non-optimized start.

Constraints from the docs:
- Other JAX-RS components such as filters and interceptors can be installed but are not officially supported.
- To match Keycloak's transaction-per-request lifecycle, use only blocking, synchronous endpoints. Asynchronous endpoints (`AsyncResponse`, returning `CompletableFuture` or `CompletionStage`) should be avoided.

## Checked
2026-11-03. Confirmed against server_development/topics/extensions.adoc and providers.adoc (Registering provider implementations). Removed (not on the pages): the `/realms/<realm>/<provider-id>/` path, the `AppAuthManager` authentication advice, the "silently absent (404)" gotcha and the Verify step.
Method: documentation only; no commands were run.
