---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-groups-custom-attributes-user-migration
name: cognito-groups-custom-attributes-user-migration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, cognito-user-pools, cognito-groups, custom-attributes, user-migration, user-migration-trigger, lambda-triggers, cognito-groups-claim, import-users, attribute-permissions, rbac]
level: practitioner
status: docs-checked
description: "Model authorisation data in Cognito user pools: groups with precedence and IAM roles, custom attributes and write permissions, and user import or migration trigger."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-user-groups.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-using-import-tool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognito groups, custom attributes and user migration

**Goal:** roles and tenant data travel in the tokens (`cognito:groups`, `custom:tenant_id`)
in a way users cannot tamper with, and existing users from a legacy system move into the
pool without a forced password reset.

## 1. Groups
```bash
aws cognito-idp create-group --user-pool-id <POOL> --group-name admins --precedence 1 \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/app-admin        # role optional, used by identity pools
aws cognito-idp admin-add-user-to-group --user-pool-id <POOL> --username alice --group-name admins
aws cognito-idp admin-list-groups-for-user --user-pool-id <POOL> --username alice
```
- ID and access tokens carry `cognito:groups` and `cognito:roles`; the ID token's
  `cognito:preferred_role` comes from the group with the lowest precedence number (zero is the
  top value; equal precedence with different role ARNs leaves the claim unset).
- Authorise in the API on the **access token** groups (API Gateway Cognito authorizer,
  `aws-jwt-verify`); do not trust group names sent by the client.
- Tokens already issued keep the groups they were minted with; sign the user out
  (`admin-user-global-sign-out`) for urgent removals.
- Quotas (quotas page, read 2026-10-27): 100 groups per user, 10,000 groups per user pool; groups
  are for roles, not for per-object permissions.

## 2. Custom attributes
```bash
aws cognito-idp add-custom-attributes --user-pool-id <POOL> \
  --custom-attributes Name=tenant_id,AttributeDataType=String,Mutable=true,StringAttributeConstraints="{MinLength=1,MaxLength=64}"
```
- Appear as `custom:tenant_id`. They **cannot be removed or renamed**, and type/mutability
  cannot be changed after creation; pools are limited to 50 custom attributes. Name
  carefully.
- App client attribute permissions: remove `custom:tenant_id` (and roles-like attributes)
  from the client's **write** attributes so users cannot set it with `UpdateUserAttributes`;
  only the backend sets it with `admin-update-user-attributes`.
- Required-attribute choices are fixed at pool creation; you cannot switch an attribute
  between required and not required afterwards.
- Use a pre-token-generation trigger to add derived claims instead of storing everything
  as attributes.

## 3. Bringing users in
| Method | Passwords | When |
|---|---|---|
| CSV **user import job** | By default not imported; users must reset (`RESET_REQUIRED`). If you name a hashing algorithm at job creation and include hashes in the CSV, users arrive `CONFIRMED` with their passwords | Bulk move; use the reset path when hashes are unavailable or incompatible |
| **User migration Lambda trigger** | Validated against the old system at first sign-in, then stored by Cognito | Gradual, transparent migration |
Migration trigger handler:
```python
def handler(event, _):
    if event["triggerSource"] == "UserMigration_Authentication":
        user = legacy_login(event["userName"], event["request"]["password"])   # your old auth
        if not user: raise Exception("Bad credentials")
    elif event["triggerSource"] == "UserMigration_ForgotPassword":
        user = legacy_lookup(event["userName"])
        if not user: raise Exception("User not found")
    event["response"]["userAttributes"] = {"email": user.email, "email_verified": "true",
                                           "custom:tenant_id": user.tenant}
    event["response"]["finalUserStatus"] = "CONFIRMED"
    event["response"]["messageAction"] = "SUPPRESS"
    return event
```
- The trigger fires only when the user does not exist in the pool and the sign-in is
  `USER_PASSWORD_AUTH`, `ADMIN_USER_PASSWORD_AUTH` or `USER_AUTH` with a password (or the
  forgot-password flow); SRP and passwordless sign-in never invoke it.
  Enable `ALLOW_USER_PASSWORD_AUTH` on the client during migration, then switch back to SRP.
- Return `userAttributes` including every attribute the pool marks required, or no profile is created.
- Lambda must answer within 5 seconds (not adjustable); keep the legacy check fast.
- Run both methods: trigger for active users, import (with reset or hashes) for the long tail
  when you turn off the legacy system.

## Gotchas
- Custom attribute values are strings in the token even for Number type.
- Adding a user to a group does not change already-issued tokens.

## Verify
- [ ] Decoded access token for an admin contains `cognito:groups: ["admins"]`.
- [ ] `UpdateUserAttributes` with `custom:tenant_id` from the client fails with `NotAuthorizedException`.
- [ ] A legacy user signs in once, appears as `CONFIRMED` in the pool, and the second sign-in no longer invokes the trigger.

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide (user groups, user attributes, migrate user trigger, import tool, Lambda trigger overview), the Cognito quotas page and the botocore cognito-idp model.
- Corrected: CSV import can now carry password hashes (users arrive CONFIRMED); `cognito:roles` appears in both ID and access tokens while `cognito:preferred_role` is an ID-token claim; the migration trigger also fires for USER_AUTH with a password and needs every required attribute in `userAttributes`.
- Confirmed: 50 custom attributes, permanent (no removal, rename or type/mutability change), string-only in the ID token, 100 groups per user and 10,000 per pool, precedence rules, 5 second trigger timeout.
- Removed: unconfirmed alias gotcha and "custom attributes cannot be required" wording.

Method: documentation only; no commands were run.
