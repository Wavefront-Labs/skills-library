---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-workload-identity-federation-sts-errors
name: troubleshooting-workload-identity-federation-sts-errors
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-troubleshooting, sts-token-exchange-errors, invalid-grant, unauthorized-client, iam-credentials]
level: practitioner
status: docs-checked
description: "Diagnose Workload Identity Federation failures: 401 on federated tokens, STS invalid_grant and invalid_request, JWK and issuer problems, AWS headers, the 127-byte subject, 429s."
sources: ["https://cloud.google.com/iam/docs/troubleshooting-workload-identity-federation", "https://cloud.google.com/iam/docs/reference/sts/rest/v1/TopLevel/token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Workload Identity Federation (STS errors)

Two hops fail independently: **(1)** the Security Token Service `token` method exchanges the external
credential for a federated access token (request fields `grantType`
`urn:ietf:params:oauth:grant-type:token-exchange`, `audience` = full provider resource name,
`subjectTokenType`, `requestedTokenType`); **(2)** a service account impersonation call
(`GenerateAccessToken`) turns that into an unrestricted access token.

## Decode the external token first
```bash
cut -d. -f2 <<<"$TOKEN" | tr '_-' '/+' | base64 -d 2>/dev/null | jq '{iss,aud,sub,exp}'
```

## Errors documented by Google
| Error | Cause and fix |
|---|---|
| `401 UNAUTHENTICATED ... Expected OAuth 2 access token` on a Google API | the API method does not accept federated access tokens; exchange it with `GenerateAccessToken` for an unrestricted token |
| `FAILED_PRECONDITION ... Org Policy violated for value` with `constraints/iam.workloadIdentityPoolProviders` | the identity provider is not allowlisted by that org policy; allowlist it |
| `Input JWK is not in a valid json format` (OIDC provider) | remove the `x5c` and `x5t` fields from the JWK |
| `invalid_grant: Error connecting to the given credential's issuer.` | Google cannot fetch your IdP's OIDC metadata document or JWKS: make the endpoints publicly reachable and OIDC-compliant; also check the token's `iss` |
| `invalid_grant: The given AWS request doesn't contain all the required headers.` | the `GetCallerIdentity` token headers must be only `Authorization`, `host`, `x-amz-date`, `x-goog-cloud-target-resource` (full provider resource name) and, with temporary credentials, `x-amz-security-token`; no extra signed headers such as `x-amz-content-sha256`, and an empty body |
| `invalid_request: The size of mapped attribute google.subject exceeds the 127 bytes limit` | shorten the mapping, e.g. `google.subject=assertion.sub.extract('/users/{sub_claim}')` |
| `429 quota_exceeded ... sts.googleapis.com/requests` | project exceeded the STS rate quota: find that metric on the IAM Quota page, confirm usage, request an increase |

An attribute-condition rejection, audience or issuer mismatch also surfaces as an STS error: compare the
decoded token's `aud`, `iss` and claims with the provider's allowed audiences, issuer URI, attribute
mapping and attribute condition.

## Hop 2 (impersonation)
A permission denied on `iam.serviceAccounts.getAccessToken` means the principal or `principalSet`
has no `roles/iam.workloadIdentityUser` binding on the service account, or the mapped attribute value
in the binding differs from the token's (case, renamed org or repo). Check:
```bash
gcloud iam service-accounts get-iam-policy <SA> --format=json | jq '.bindings[]|select(.role=="roles/iam.workloadIdentityUser")'
```

## Gotchas
- Attribute mapping errors break every exchange; test with a known token.

## Verify
- [ ] A manual exchange with `gcloud auth login --cred-file=<CRED_CONFIG>` succeeds and `gcloud auth print-access-token` returns a token.

## Checked
2026-10-31. Confirmed against "Troubleshoot Workload Identity Federation" (the errors in the table) and the
STS `token` method reference (request fields). Removed: error strings for audience, issuer, stale-token,
`invalid_target` and "caller identity does not match" cases, the JWKS-upload advice, the AWS `extract`
expression, the soft-delete period, the Data Access audit-log instructions and the 5-minute propagation figure
because the pages do not state them.
Method: documentation only; no commands were run.
