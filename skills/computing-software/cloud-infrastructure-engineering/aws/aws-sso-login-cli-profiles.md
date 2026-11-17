---
id: computing-software.cloud-infrastructure-engineering.aws.aws-sso-login-cli-profiles
name: aws-sso-login-cli-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, identity-center, aws-sso-login, sso-session, sso-cli, profiles, sdk-credentials]
level: practitioner
status: docs-checked
description: "Use Identity Center credentials from the CLI and SDKs: sso-session profiles, aws sso login, token refresh, generating many-account profiles and tool compatibility."
sources: ["https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/sso/utils.py", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/sso/login.py", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/configure/exportcreds.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `aws sso login` and Identity Center CLI profiles

## 1. Config with a shared sso-session
`~/.aws/config`:
```ini
[sso-session corp]
sso_start_url = https://corp.awsapps.com/start
sso_region = eu-west-1
sso_registration_scopes = sso:account:access

[profile dev]
sso_session = corp
sso_account_id = 111111111111
sso_role_name = Developer
region = eu-west-1

[profile prod-ro]
sso_session = corp
sso_account_id = 222222222222
sso_role_name = ReadOnly
region = eu-west-1
```
`aws configure sso` writes this interactively. One login serves every profile using the session.

## 2. Login and use
```bash
aws sso login --sso-session corp          # browser, Authorization Code flow (default for sso-session profiles)
aws sso login --sso-session corp --use-device-code   # Device Code flow instead; --no-browser stops the CLI opening a browser
aws s3 ls --profile dev
export AWS_PROFILE=prod-ro
aws sso logout
```
- Token cache: `~/.aws/sso/cache/`.
- `aws sso login` uses the Authorization Code flow only for profiles that use an `sso-session`; legacy profiles (with `sso_start_url` directly in the profile) use the device code flow.
- `aws sso logout` ends the session.

## 3. Many accounts
The IAM Identity Center portal API has `ListAccounts` and `ListAccountRoles` operations (`aws sso list-accounts --access-token <token>`, `aws sso list-account-roles --access-token <token> --account-id <id>`), which take the access token from the login cache. Use them to generate one profile per account and role, or create profiles with `aws configure sso`.

## 4. Tool compatibility
Tools that cannot read SSO profiles can be given short-lived credentials: `aws configure export-credentials --profile dev --format env` prints `export AWS_ACCESS_KEY_ID=...` lines (the `env-no-export` and PowerShell formats also exist), and a profile's `credential_process` can call that command. Check each SDK or tool's documentation for sso-session support.

## Gotchas
- If a command reports that the SSO token is missing or expired, run `aws sso login --sso-session corp` again.
- Legacy profiles with `sso_start_url` directly in the profile (no sso-session) use the older login flow; prefer the sso-session format.
- `sso_region` is where Identity Center lives, not the region you work in.

## Verify
- [ ] `aws sts get-caller-identity --profile dev` returns the expected account and the assumed role for the profile.
- [ ] Commands keep working across the session lifetime without repeated browser logins.
- [ ] No static access keys in `~/.aws/credentials` for human use.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch source (customizations/sso, configure/exportcreds.py, configure/sso.py) and the botocore SSO portal service model.
Confirmed: sso-session section keys sso_start_url, sso_region, sso_registration_scopes; profile keys sso_session, sso_account_id, sso_role_name; aws sso login --sso-session, --use-device-code, --no-browser and the Authorization Code versus device code flow selection; token cache directory ~/.aws/sso/cache; aws sso logout; ListAccounts and ListAccountRoles operations taking an access token; export-credentials formats.
Removed as unconfirmed: PKCE wording, refresh-token behaviour, role-credential cache path, jq token extraction, third-party helper tools, SDK and Terraform compatibility claim, ~8 hour and 1 hour timing.
Method: documentation only; no commands were run.
