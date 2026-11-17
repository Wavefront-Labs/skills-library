---
id: computing-software.cloud-infrastructure-engineering.google-cloud.deploying-cloud-run-functions-with-config-and-secrets
name: deploying-cloud-run-functions-with-config-and-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, gcloud-functions-deploy, functions-2nd-gen, functions-secrets-env, env-vars-functions, secret-manager]
level: practitioner
status: docs-checked
description: "Deploy Cloud Run functions with gcloud (functions deploy or run deploy --function), set runtime and build env vars, mount Secret Manager secrets, and pin runtime service accounts."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/functions/deploy", "https://docs.cloud.google.com/functions/docs/configuring/env-var", "https://docs.cloud.google.com/run/docs/configuring/services/secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Cloud Run functions with config and secrets

## 1. Deploy
```bash
gcloud functions deploy resize-image --gen2 --region=europe-west2 \
  --runtime=python312 --source=. --entry-point=handle \
  --trigger-http --no-allow-unauthenticated \
  --service-account=resize-fn@<P>.iam.gserviceaccount.com \
  --memory=512Mi --cpu=1 --timeout=120s --max-instances=20 --concurrency=10 \
  --env-vars-file=env.prod.yaml \
  --set-secrets=API_KEY=thumbor-api-key:3,/etc/secrets/tls.pem=tls-cert:latest \
  --set-build-env-vars=KEY=VALUE
```
Functions are Cloud Run services underneath, so Cloud Run settings (secrets, env vars, service identity) apply to them.

## 2. Config
- Runtime env: `--set-env-vars` (destructive: it deletes variables not in the new list), or `--env-vars-file` (a local YAML file such as `KEY: "value"`, or a `.env` file).
- Build env: `--set-build-env-vars` sets key-value pairs for the build.
- Variables defined in the container runtime contract are reserved (for example `PORT`, and `FUNCTION_TARGET` and `FUNCTION_SIGNATURE_TYPE` are set for functions); keys cannot be empty, contain `=`, or start with `X_GOOGLE_`.

## 3. Secrets
`NAME=secret:version` exposes the secret as an env var (resolved at **instance start**; Google advises pinning a version rather than `latest`); `/path=secret:version` mounts it as a file (Cloud Run fetches the latest version from Secret Manager when you use `latest`). The service identity needs `roles/secretmanager.secretAccessor`, and the deployer needs `roles/iam.serviceAccountUser` on that identity. Multiple secrets cannot be mounted at the same path.

## 4. Inspect
```bash
gcloud functions describe resize-image --region=<R>
```

## Gotchas
- Without `--service-account` the function runs as a default service account; use a dedicated one with least privilege.
- 1st gen functions differ (1 concurrent request per instance, different retry configuration); do not mix generations.
- Pin dependency versions in `requirements.txt` or `package.json` so builds are repeatable.

## Verify
- [ ] `describe` shows the intended service account, secret references and env; no secret values appear in the output.
- [ ] Invoking with an identity token succeeds; an unauthenticated request is rejected.

## Checked

2026-10-24, gcloud functions deploy reference and the Cloud Run environment-variable and secrets pages on docs.cloud.google.com. Confirmed: `--env-vars-file` YAML or .env format, destructive `--set-env-vars`, `--set-build-env-vars`, `--set-secrets` grammar for env var and file mounts, env-var secrets resolved at instance start, pin-a-version advice, `roles/secretmanager.secretAccessor`, reserved variable rules, one secret per mount path. Removed unconfirmed claims: `gcloud run deploy --function`, the Python package-manager build variable, default-SA Editor statement, `--gen2` default, Cloud Build log command, `--format` expression.

Method: documentation only; no commands were run.
