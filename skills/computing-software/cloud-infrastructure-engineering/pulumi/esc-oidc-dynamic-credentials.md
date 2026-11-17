---
id: computing-software.cloud-infrastructure-engineering.pulumi.esc-oidc-dynamic-credentials
name: esc-oidc-dynamic-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, esc-oidc, dynamic-credentials, aws-login, fn-open-aws-login]
level: practitioner
status: docs-checked
description: "Replace long-lived cloud keys with ESC OIDC dynamic credentials using fn::open::aws-login: inputs, session scoping, sharing a login environment, other providers."
sources:
  - https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/aws-login/
  - https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESC OIDC dynamic credentials

Login providers issue short-lived credentials for downstream services, invoked through `fn::open::<name>-login`. OIDC is the recommended mode wherever supported. Providers: `aws-login`, `azure-login`, `gcp-login`, `vault-login`, `infisical-login` (OIDC or static), `doppler-login`, `snowflake-login` (OIDC), `gh-login` (app credentials), plus `oidc` (mint a raw token for an audience) and `debug-oidc-claims` (preview claims without signing).

```yaml
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          duration: 1h
          roleArn: arn:aws:iam::012345678912:role/role-abcd123
          sessionName: pulumi-esc
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
    AWS_REGION: us-west-2
```
With OIDC, Pulumi Cloud exchanges a short-lived token for temporary credentials by assuming an IAM role. Before using `oidc`, register Pulumi Cloud as an OIDC identity provider in your AWS account and create an IAM role whose trust policy allows it (see "Configuring OpenID Connect for AWS"). The same variables serve the Pulumi AWS provider, the `aws` CLI and the AWS SDKs.

**Static** (`static:` with `accessKeyId`, `secretAccessKey` wrapped in `fn::secret`) works as a fallback; either way `aws-login` outputs `accessKeyId`, `secretAccessKey`, `sessionToken`, so consumers don't change. Prefer OIDC: static keys are long-lived and rotated manually.

**Scope a session** with two optional `oidc` inputs: `subjectAttributes` (customize the `sub` claim, e.g. `currentEnvironment.name`, so the role's trust policy can restrict which environments may assume it) and `policyArns` (effective permissions are the intersection of the role and these policies).

**Share one login.** Define `aws-login` once in its own environment (e.g. `myorg/aws/login`), import it (`imports: [aws/login]`), and chain it with `login: ${aws.login}` into `aws-secrets` or `aws-parameter-store`. The trust policy then only has to cover the one base environment.

## Gotchas
- Dynamic values are generated fresh on each open and never stored in the environment.
- Validate with `pulumi env open <org>/<project>/<environment>`.

## Checked
2026-11-03. Confirmed on the aws-login and Login providers pages. Removed: the issuer URL and audience claims, exact `sub` format, `duration`-vs-role max-session claim, `esc run ... aws sts` Verify and the subject-claim-per-trigger tip.
Method: documentation only; no commands were run.
