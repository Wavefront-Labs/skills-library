---
id: computing-software.cybersecurity-defensive.keycloak.password-policy-spi
name: password-policy-spi
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, password-policy-spi, passwordpolicyprovider, validation, policyerror]
level: practitioner
status: docs-checked
description: "Add a custom Keycloak password policy by implementing PasswordPolicyProvider and its factory, returning PolicyError to reject."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/password-policy-spi.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# password policy spi
A password policy provider validates a candidate password when a user updates credentials, when an administrator sets a password through the Admin Console or Admin REST API, and when a user registers. A realm stores its password policy as one string of tokens, for example `length(12) and specialChars(2)`; the provider receives each token's value as a single string.

Implement `PasswordPolicyProvider` and `PasswordPolicyProviderFactory` from `org.keycloak.policy`. The provider returns `null` to accept and a `PolicyError` (message key plus arguments) to reject; `parseConfig(String)` converts the raw value, and throwing `PasswordPolicyConfigException` rejects an invalid value (the Admin Console shows the error when the policy is saved). The parsed value is available via `PasswordPolicy#getPolicyConfig(providerId)`:
```java
public PolicyError validate(String user, String password) {
    int max = context.getRealm().getPasswordPolicy()
            .getPolicyConfig(MaxAcmePasswordPolicyProviderFactory.ID);
    if (countOccurrences(password, "acme") > max) {
        return new PolicyError("invalidPasswordMaxAcmeMessage", max);
    }
    return null;
}
```
Factory methods: `getId()`, `getDisplayName()` (label in the *Add policy* drop-down), `getConfigType()` (`PasswordPolicyProvider.INT_CONFIG_TYPE` numeric input, `STRING_CONFIG_TYPE` text input, or `null` for an on/off policy), `getDefaultConfigValue()` and `isMultiplSupported()` (return false). A policy needing several parameters must define its own format inside the single value, for example `myPolicy(3,true)` is received as `3,true`.

Messages: the key passed to `PolicyError` is resolved from the theme message bundles (login theme for registration and required password updates, admin theme for the Admin Console and Admin REST API). Ship `theme-resources/messages/messages_en.properties` in the provider JAR, one file per locale. Tooltip text comes from `passwordPoliciesHelp.<policy id>` in `theme-resources/messages/admin-messages_en.properties`; without it the raw key shows.

Register the factory in `META-INF/services/org.keycloak.policy.PasswordPolicyProviderFactory`, deploy the JAR like any provider. After the server restarts the policy appears in the *Add policy* drop-down of *Authentication* > *Policies*.

## Checked
2026-11-03. Confirmed against server_development/topics/password-policy-spi.adoc. Removed (not on the page): the "slow external services" and "service-created passwords" gotchas, the Verify step, and the "Password policy" tab-name wording (page says Authentication, Policies tab).
Method: documentation only; no commands were run.
