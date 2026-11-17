---
id: computing-software.devops-ci-cd.spinnaker.cloud-foundry-provider-account
name: cloud-foundry-provider-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [cloud-foundry, provider, clouddriver-local, accounts, foundation, api-endpoint]
level: practitioner
status: docs-checked
description: "Add a Cloud Foundry account to Spinnaker in clouddriver-local.yml, including the required endpoints, onlySpinnakerManaged and when to skip SSL validation."
sources:
  - https://spinnaker.io/docs/setup/install/providers/cf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In Cloud Foundry an Account maps to a user account on a CF foundation (a BOSH Director and all the VMs it deploys). You can add several accounts for one or more foundations. The only prerequisite is that each foundation's API endpoint is reachable from Spinnaker.

Enable the provider and add the account to the clouddriver list in `clouddriver-local.yml`:

```yaml
cloudfoundry:
  enabled: true
  accounts:
    - name: my-cf-account
      api: api.sys.endpoint.for.foundation
      user: username
      password: password
      environment: whatever
      appsManagerUrl: http://apps.sys.endpoint.for.foundation
      metricsUrl: http://metrics.sys.endpoint.for.foundation
      skipSslValidation: true|false
      onlySpinnakerManaged: true
```

- `skipSslValidation: true` may be necessary for an API endpoint with a self-signed certificate or one from an internal CA; turning it on generates a warning.
- `onlySpinnakerManaged: true` caches only things Spinnaker has deployed.

## Checked

2026-11-04. Account meaning, prerequisite, the clouddriver-local.yml block, skipSslValidation and onlySpinnakerManaged were confirmed on the Cloud Foundry provider page. Removed: the `hal config provider cloudfoundry` commands, Halyard connectivity-check behaviour and the post-apply visibility claim (not on the page).

Method: documentation only; no commands were run.
