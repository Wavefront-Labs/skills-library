---
id: computing-software.devops-ci-cd.spinnaker.gcs-artifact-account
name: gcs-artifact-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [artifacts, gcs, google-cloud, service-account, accounts]
level: practitioner
status: docs-checked
description: "Configure a GCS artifact account so stages can read objects from buckets: a roles/storage.admin service account key and a clouddriver-local.yml entry."
sources:
  - https://spinnaker.io/docs/setup/other_config/artifacts/gcs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stages that read data from artifacts can consume GCS objects once a GCS artifact account exists. You need a GCP project to host a bucket and `gcloud` installed and authenticated (`gcloud info` checks this).

**Credentials.** Spinnaker needs a service account with the `roles/storage.admin` role and a downloaded JSON key. The page creates the account with `gcloud iam service-accounts create`, binds the role with `gcloud projects add-iam-policy-binding --role roles/storage.admin --member serviceAccount:$SA_EMAIL`, and writes the key with `gcloud iam service-accounts keys create $SERVICE_ACCOUNT_DEST --iam-account $SA_EMAIL`.

**Spinnaker settings.** Put the key either in a secrets manager (used by reference) or in a volume mounted into the clouddriver pods by modifying the clouddriver `deployment.yaml`. Then add to `clouddriver-local.yml`:

```yaml
artifacts:
  enabled: true
  gcs:
    enabled: true
    accounts:
      - name: my-gcs-artifact-account
        ## This can be a secret reference
        json-path: /mnt/secrets/service-account-file.json
```

Last, redeploy clouddriver with these changes.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Configuring GCS Artifact Credentials page. Confirmed the role requirement, key creation commands and the clouddriver-local.yml block. Replaced the old Halyard commands (not on the current page) and removed the unconfirmed ordering remark, the hal deploy apply reminder and the trigger-guide link.
