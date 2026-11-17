---
id: computing-software.collaboration-platform-administration.matrix-synapse.sso-user-mapping-providers
name: sso-user-mapping-providers
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, sso, mapping-provider, oidc, saml, localpart, display-name, module-api, failures]
level: sme
status: docs-checked
description: "Write a custom Synapse SSO mapping provider for OIDC or SAML: required methods, the failures counter for dedup, localpart None to prompt, confirm_localpart."
sources:
  - https://element-hq.github.io/synapse/latest/sso_mapping_providers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A mapping provider is a Python class, loaded from a module importable by Synapse (typically in the same virtualenv), that turns attributes of an SSO response into Matrix user attributes. It is supported for OpenID and SAML. The provider decides whether to assign a Matrix ID from the attributes or leave it unset, in which case Synapse serves an HTML page where the user picks a username. When you assign IDs, you must normalise attributes into a valid Matrix ID per the spec.

Point Synapse at a custom module via `oidc_providers.user_mapping_provider.module` or `saml2_config.user_mapping_provider.module`, with module-specific options in the matching `config` key. The default options belong to the built-in provider (`JinjaOidcMappingProvider`, `DefaultSamlMappingProvider`); comment them out when using your own.

**OIDC provider methods:**

- `__init__(self, parsed_config, module_api)` and a `@staticmethod` `parse_config(config)` whose return value is passed to `__init__` at startup.
- `get_remote_user_id(self, userinfo)` returns the unique, immutable identifier, commonly `sub`.
- `async map_user_attributes(self, userinfo, token, failures)` returns a dict with `localpart`, optional `confirm_localpart`, `display_name`, `picture` and `emails`.
- `async get_extra_attributes(self, userinfo, token)` returns JSON-serialisable extras for the login response; do not overwrite standard login response fields.

If the localpart is already taken, Synapse calls the mapping method again with `failures` incremented, so you should return a deduplicated value such as `john.doe1`. A `localpart` of `None` prompts for a username, and `confirm_localpart: True` asks the user to accept or change the proposed one. The localpart is used only at first login; once associated with the remote user ID it cannot be updated.

**SAML provider** uses `get_saml_attributes(config)` (static; returns required and optional attribute sets), `get_remote_user_id(saml_response, client_redirect_url)` and `saml_response_to_user_attributes(...)` returning `mxid_localpart`, `displayname` and `emails`. It may raise `RedirectException` to collect more information, then must redirect back to `client_redirect_url` or finish registration through `ModuleApi`.

## Checked

Method: docs-checked 2026-11-09 against docs/sso_mapping_providers.md (Synapse develop branch, raw markdown, read in full).
