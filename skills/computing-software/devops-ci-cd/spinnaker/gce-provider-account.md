---
id: computing-software.devops-ci-cd.spinnaker.gce-provider-account
name: gce-provider-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [gce, google-cloud, provider, service-account, iam, clouddriver, accounts]
level: practitioner
status: docs-checked
description: "Create a GCE service account with the required compute and IAM roles and add it as a Spinnaker google account in clouddriver config."
sources:
  - https://spinnaker.io/docs/setup/install/providers/gce/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In Google Compute Engine an Account maps to a credential that authenticates against one GCP project. You need a project and `gcloud` installed and authenticated (check with `gcloud info`).

**Service account roles** granted at project level:
- `roles/compute.instanceAdmin` to create and modify instances;
- `roles/compute.networkAdmin` for network settings;
- `roles/compute.securityAdmin` for firewall rules;
- `roles/compute.storageAdmin` for images and disks;
- `roles/iam.serviceAccountActor`, needed because Packer downloads service account keys to bake GCE images remotely.

The page creates the account with `gcloud iam service-accounts create`, binds each role with `gcloud projects add-iam-policy-binding`, and writes a JSON key with `gcloud iam service-accounts keys create` to a local file you choose.

**Add to Spinnaker** in the clouddriver configuration:

```yaml
google:
  enabled: true
  accounts:
    - name: account-name
      project: <PROJECT_ID>
      jsonPath: /mnt/configmap/file.json
```

More account properties are in the GoogleConfigurationProperties class in the clouddriver-google source (linked from the page). With a large number of accounts the page recommends setting `google.health.verifyAccountHealth: false` and checking logs for account access health instead.

## Checked

2026-11-04. Role list, the Packer rationale, key creation and the clouddriver YAML and verifyAccountHealth advice were confirmed on the Google Compute Engine provider page. Removed: the `hal config provider google` commands and the ADC TODO note (neither on the page now).

Method: documentation only; no commands were run.
