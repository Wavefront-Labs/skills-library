---
id: computing-software.cybersecurity-defensive.keycloak.authz-js-policy-deployment
name: authz-js-policy-deployment
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, javascript-policy, policy-evaluation-api, script-provider, abac]
level: practitioner
status: docs-checked
description: "Write Keycloak JavaScript authorization policies with the Evaluation API and deploy them from a JAR rather than uploading scripts."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/policy-js-policy.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authz js policy deployment
A JavaScript policy defines permission conditions in code against the Evaluation API; it is one of the rule-based policy types and can express RBAC, ABAC or a mix.

By default JavaScript policies cannot be uploaded to the server; the docs say to prefer deploying them directly to the server as a JAR (script providers, see the server developer guide). Once deployed, select the script from the list of available policy providers when creating the policy (policy listing, JavaScript item).

The `$evaluation` object implements `org.keycloak.authorization.policy.evaluation.Evaluation`. The documented examples use `$evaluation.getContext()` (attributes, identity), `$evaluation.getRealm()`, `$evaluation.getPermission()` (add claims for the resource server) and `$evaluation.grant()`. Examples from the docs:
```javascript
const context = $evaluation.getContext();
const contextAttributes = context.getAttributes();
if (contextAttributes.containsValue('kc.client.network.ip_address', '127.0.0.1')) {
    $evaluation.grant();
}
```
```javascript
const identity = $evaluation.getContext().getIdentity();
if (identity.hasRealmRole('keycloak_user')) { $evaluation.grant(); }
// client role: identity.hasClientRole('my-client', 'my-client-role')
```
Other documented checks: `realm.isUserInRealmRole('marta', 'role-a')`, `realm.isUserInClientRole(...)`, `realm.isGroupInRole('/Group A/Group D', 'role-a')`, `realm.isUserInGroup('marta', '/Group A/Group B')`, and `permission.addClaim('claim-a', 'claim-a')` to push claims to the resource server.

Warning from the docs: if a policy uses ABAC, make sure users cannot edit the protected attributes and that those attributes are read-only (see the threat model mitigation chapter).

## Checked
2026-11-03. Confirmed against authorization_services/topics/policy-js-policy.adoc: default upload restriction, deployed-JAR flow, `Evaluation` interface, each example call, the ABAC read-only warning. Removed (not on the page): `deny()`, the "no grant means no grant" and performance advice, the Affirmative-strategy gotcha, and the Evaluate-tab Verify step.
Method: documentation only; no commands were run.
