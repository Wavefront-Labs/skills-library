---
id: computing-software.cybersecurity-defensive.authentik.collect-user-attributes
name: collect-user-attributes
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, prompt-stage, user-write, custom-attributes, enrollment, field-key]
level: practitioner
status: docs-checked
description: "Collect custom user attributes in an authentik enrollment flow using Prompt fields keyed attributes.name and a User Write stage, or set them from an invitation."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/collect-user-attributes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: store values entered at enrolment as user attributes.

## Field key rule
The prompt field's **Field Key** decides where User Write puts the value:
- `username`, `name`, `email`: built-in user fields.
- `attributes.given_name`, `attributes.department`: user attribute of that name.
- `attributes.settings.locale`: nested attribute `settings.locale`.

A key such as plain `department` is available in `prompt_data` to later stages and policies but is NOT stored on the user. Prefix with `attributes.`.

## Steps
1. **Flows and Stages > Prompts > New Prompt**: Name `enrollment-given-name`, Field Key `attributes.given_name`, Label, Type **Text**, Required, Order. Repeat for `attributes.family_name` with a higher Order.
2. **Stages > New Stage > Prompt Stage**, add both prompts to **Fields**.
3. Open the enrolment flow > **Stage Bindings**; bind the Prompt stage before a User Write stage that allows user creation. Order: identification/invitation/verification, Prompt, User Write, optional User Login.

Object attribute definitions only label and validate fields on admin user forms; they do not add fields to enrolment flows.

## From an invitation
Put attributes in the invitation's **Custom attributes** field, with the Invitation stage bound before Prompt and User Write:
```json
{"email": "dominic.roy@example.com", "name": "Dominic Roy",
 "attributes": {"department": "Engineering", "family_name": "Roy", "given_name": "Dominic"}}
```
Dotted keys such as `"attributes.given_name": "Dominic"` also work.

## Sending to an app
Stored attributes are not sent automatically; add a provider property mapping that returns them for the OAuth2 claim or SAML attribute. Check the result in **Directory > Users > Attributes**.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/collect-user-attributes/ (read in full).
