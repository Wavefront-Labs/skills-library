---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workload-identity-federation-from-aws
name: workload-identity-federation-from-aws
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-aws, aws-to-gcp-federation, aws-iam-role, workload-identity-pool, getcalleridentity, sts-token-exchange, credential-configuration-file, multi-cloud-identity, keyless-auth]
level: advanced
status: docs-checked
description: "Let AWS workloads call Google APIs with their IAM role instead of a key: AWS provider in a workload identity pool, role ARN mapping, IAM grants, credential config."
sources: ["https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds", "https://cloud.google.com/iam/docs/workload-identity-federation#aws", "https://cloud.google.com/sdk/gcloud/reference/iam/workload-identity-pools/providers/create-aws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload Identity Federation from AWS

**Goal:** an EC2 instance, Lambda or ECS task authenticates to GCP by signing an AWS
`GetCallerIdentity` request with its own role credentials — no Google key file stored in AWS.

## 1. Pool and provider
```bash
gcloud iam workload-identity-pools create aws-pool --location=global --display-name="AWS workloads"
gcloud iam workload-identity-pools providers create-aws aws-prod --workload-identity-pool=aws-pool --location=global \
  --account-id=123456789012 \
  --attribute-mapping="google.subject=assertion.arn,attribute.aws_role=assertion.arn.extract('assumed-role/{role}/'),attribute.account=assertion.account" \
  --attribute-condition="assertion.account=='123456789012'"
```
`assertion.arn` for an EC2 role looks like `arn:aws:sts::123456789012:assumed-role/<RoleName>/<i-instanceid>`
— hence the `extract` to get a stable role name (`google.subject` cannot exceed 127 characters, so a
long ARN needs a shorter mapped subject when sessions vary).

## 2. Grant IAM
```bash
gcloud iam service-accounts add-iam-policy-binding gcs-writer@<P>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/aws-pool/attribute.aws_role/ec2-uploader"
```
Or skip the SA and grant roles directly to the `principalSet` on the bucket/project for
services that support federated principals directly (see the *federated identity supported products* page);
impersonating an SA is the fallback where a product does not.

## 3. Credential configuration on the AWS side
```bash
gcloud iam workload-identity-pools create-cred-config \
  projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/aws-pool/providers/aws-prod \
  --service-account=gcs-writer@<P>.iam.gserviceaccount.com --aws --enable-imdsv2 \
  --output-file=gcp-cred.json
```
Ship `gcp-cred.json` (unlike a service account key it has no private key and need not be kept confidential) to the workload and set
`GOOGLE_APPLICATION_CREDENTIALS=/path/gcp-cred.json`. Client libraries then: read AWS creds, sign a
`GetCallerIdentity` request, exchange it at `sts.googleapis.com` for a federated token, then
`generateAccessToken` for the SA. The file is portable across instances with the same role.

Where the AWS metadata server is not available, the gcloud CLI and libraries read `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, `AWS_REGION` (or `AWS_DEFAULT_REGION`) and optionally `AWS_SESSION_TOKEN` from the
environment. Without `--service-account`, the library uses the federated token directly (direct resource access).

## 4. Test from the instance
```bash
gcloud auth login --cred-file=gcp-cred.json
gcloud storage ls gs://<BUCKET>
gcloud auth print-access-token
```

## Gotchas
- The workload must be able to reach the STS and IAM Credentials endpoints named in the credential configuration file.
- `attribute-condition` is your allowlist; without it any role in the AWS account can federate (still needs IAM, but limit it).
- EC2 instances that use IMDSv2 need `--enable-imdsv2` when generating the credential configuration; Google's guide says to follow the gcloud instructions, not the console ones, for IMDSv2 instances.

## Verify
- [ ] From EC2 with the role: a client-library call succeeds with no `.json` key present.
- [ ] From the same instance under a different role: STS exchange rejected by the attribute condition.
- [ ] `gcloud iam workload-identity-pools providers describe` shows the expected mapping and condition.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud reference pages for `providers create-aws`, `workload-identity-pools create` and `create-cred-config` (`--account-id`, `--attribute-mapping`, `--attribute-condition`, `--enable-imdsv2`, `--service-account`, `--output-file`), and the Workload Identity Federation with AWS guide (attribute mapping with `assertion.arn.extract(...)`, 127-character `google.subject` limit, AWS environment-variable fallback, credential configuration holds no private key).
- Removed unconfirmed claims: one-provider-per-account rule, Lambda/ECS credential-URI details, 5-minute clock-skew limit, SCP/VPC-endpoint failure mode, audit-log field names, the "1 h" token note and the `cut` pipe.

Method: documentation only; no commands were run.
