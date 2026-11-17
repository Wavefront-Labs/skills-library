---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-bootstrap-secrets-outside-user-data
name: ec2-bootstrap-secrets-outside-user-data
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, user-data, user-data-secrets, bootstrap-secrets, secrets-manager, parameter-store, iam-role]
level: practitioner
status: docs-checked
description: "Keep secrets out of EC2 user data: why it leaks, fetching from Secrets Manager or SecureString at boot with the instance role, restricting access, and cleaning up existing leaks."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/secure-string-parameter-kms-encryption.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-secretsmanager.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrap secrets without putting them in user data

## 1. Why user data is the wrong place
- Retrievable from the instance at `http://169.254.169.254/latest/user-data` by anything running on the instance.
- Readable through the API by anyone allowed `ec2:DescribeInstanceAttribute` (attribute `userData`).
- Stored in launch templates and CloudFormation templates, visible in consoles and IaC state.
- AWS treats user data as opaque data returned exactly as supplied, limited to 16 KB; it is not a secret store, and a retrieval of it is not a Secrets Manager retrieval (Secrets Manager logs each secret retrieval to CloudTrail).

## 2. Fetch at boot with the instance role
User data contains only *references*:
```bash
#!/bin/bash
set -euo pipefail
REGION=$(TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 60'); \
  curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/region)
DB_PASS=$(aws secretsmanager get-secret-value --region "$REGION" --secret-id prod/app/db \
  --query SecretString --output text | jq -r .password)
API_KEY=$(aws ssm get-parameter --region "$REGION" --name /prod/app/api-key --with-decryption \
  --query Parameter.Value --output text)
install -m 600 -o app -g app /dev/null /etc/app/secrets.env
printf 'DB_PASS=%s\nAPI_KEY=%s\n' "$DB_PASS" "$API_KEY" > /etc/app/secrets.env
```
Better still: have the **application** read the secret at startup (SDK + caching) so rotation
works without re-provisioning; then nothing lands on disk.

Instance role policy (least privilege):
```json
{"Effect": "Allow", "Action": ["secretsmanager:GetSecretValue"],
 "Resource": "arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:prod/app/db-*"},
{"Effect": "Allow", "Action": ["ssm:GetParameter"], "Resource": "arn:aws:ssm:<REGION>:<ACCOUNT_ID>:parameter/prod/app/*"},
{"Effect": "Allow", "Action": "kms:Decrypt", "Resource": "<KMS_KEY_ARN>",
 "Condition": {"StringEquals": {"kms:ViaService": ["secretsmanager.<REGION>.amazonaws.com", "ssm.<REGION>.amazonaws.com"]}}}
```
SecureString parameters need `kms:Decrypt` on a customer managed key; access to the default `aws/ssm` key cannot be controlled by IAM or key policy. Private subnets: interface endpoints for Secrets Manager, Systems Manager and KMS (or NAT).

## 3. Cleaning up a leak
1. Rotate the exposed secret immediately (assume compromise).
2. Remove from launch templates (new version, set default), CloudFormation templates
   (use dynamic references such as `{{resolve:secretsmanager:...}}`), and running instances
   (change the user data attribute with `modify-instance-attribute` while the instance is stopped).
3. Search: `aws ec2 describe-launch-template-versions ... --query '...UserData'` | base64 -d | grep -i pass.

## Gotchas
- Script output on Linux goes to `/var/log/cloud-init-output.log`, so `set -x` there would write secret values into the log; don't trace secret lines.
- The IMDS PUT response hop limit and IMDSv2 still matter: a container on the host that can reach IMDS can read the instance role credentials.

## Verify
- [ ] `curl .../latest/user-data` on the instance shows no secret values.
- [ ] CloudTrail shows `GetSecretValue` from the instance role at boot.
- [ ] Rotating the secret and restarting the app picks up the new value without changing user data.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (user data, instance metadata retrieval, IMDS hop limit), the Secrets Manager and Systems Manager Parameter Store guides, the CloudFormation dynamic references page and the botocore EC2 model.
- User data URI, 16 KB limit, opaque-data behaviour, the `userData` attribute in `DescribeInstanceAttribute` and the stopped-instance requirement for editing confirmed.
- `secretsmanager:GetSecretValue`, `kms:Decrypt` for SecureString on a customer managed key, the no-IAM-control note for `aws/ssm`, CloudTrail logging of secret retrievals and `{{resolve:secretsmanager:...}}` confirmed.
- `/var/log/cloud-init-output.log` as the script output location confirmed on the user data page.
- Removed the claims that user data is "not encrypted with your KMS key / not rotated / not audited per read" in that wording and the CloudFormation `NoEcho` advice, which the pages read do not state.

Method: documentation only; no commands were run.
