---
id: computing-software.cybersecurity-defensive.pomerium.rego-policy-inputs
name: rego-policy-inputs
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [rego, opa, databroker-record, policy-inputs, enterprise-policy]
level: advanced
status: docs-checked
description: "Write Pomerium Enterprise Rego policies, the allow and deny output forms, special reasons, input fields and the databroker record function."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authorization.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rego is Enterprise only. A policy uses either PPL or Rego, never both; setting one disables the other in the console. The docs strongly advise PPL unless Rego is needed.

**Outputs**: `allow` and `deny` accept a boolean, a single-element array with a boolean, a boolean plus a reason, or a boolean plus a reason plus data. Examples: `allow := true`, `deny := [true, "unauthorized"]`.

Special reasons:
- `user-unauthenticated` triggers sign-in redirect.
- `device-unauthenticated` prompts device registration.

**Inputs** on `input`:
- `http.*`: method, hostname, path, url, headers, client_certificate fields, ip, session.id, is_valid_client_certificate (session data is under `input.http.session`). Absent on SSH routes.
- `ssh.*`: username, publickey.

**Function**: `get_databroker_record(record_type, record_id)` returns Databroker data. The docs' example looks up the user's session and user records, checks the `given_name` claim against a list fetched with `http.send`, and returns an allow or a not-allowed result with reasons `custom-rego-authorized`, `custom-rego-unauthorized` or `user-unauthenticated`.

Apply it through the Console editor.

## Checked

2026-11-04. Confirmed against the Pomerium Policy Language page (Rego section): Enterprise only, PPL or Rego exclusive, four output forms, two special reasons, input fields, SSH note, get_databroker_record, example policy. Corrected the example result description to the reasons the page's policy returns.

Method: documentation only; no commands were run.
