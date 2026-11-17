---
id: computing-software.cloud-infrastructure-engineering.azure.resource-provider-and-preview-feature-registration
name: resource-provider-and-preview-feature-registration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-provider-registration, feature-registration, az-provider, missingsubscriptionregistration, preview-features]
level: practitioner
status: docs-checked
description: "Register Azure resource providers and preview features (AFEC), fix MissingSubscriptionRegistration, and control provider registration from Terraform and vending pipelines."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/management/resource-providers-and-types", "https://learn.microsoft.com/azure/azure-resource-manager/management/preview-features", "https://learn.microsoft.com/azure/azure-resource-manager/troubleshooting/error-register-resource-provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource provider and preview feature registration

**Goal:** new subscriptions can deploy everything the workload needs without "MissingSubscriptionRegistration"
failures mid-pipeline.

## Providers
```bash
az provider list --query "[?registrationState=='Registered'].namespace" -o tsv
az provider show -n Microsoft.ContainerService --query registrationState
az provider register -n Microsoft.ContainerService --wait
az provider show -n Microsoft.Web --query "resourceTypes[?resourceType=='sites'].locations"   # where available
```
- Registration is per subscription. It needs the `*/register/action` permission (included in Contributor and Owner).
- You can't unregister a provider while resource types from it still exist in the subscription.

## Preview features
```bash
az feature register --namespace Microsoft.ContainerService --name <FeatureName>
az feature show --namespace Microsoft.ContainerService --name <FeatureName> --query properties.state
# when state = Registered, refresh the provider so it picks the flag up
az provider register -n Microsoft.ContainerService
az feature list --query "[?properties.state=='Registered'].name" -o tsv
```
States: check with `az feature show` until the state is Registered, then re-register the provider.

## Error decoding
`MissingSubscriptionRegistration: The subscription is not registered to use namespace 'Microsoft.X'` -> register it.
`NoRegisteredProviderFound: No registered resource provider found for location and API version` -> check the api-version and the resource type's supported locations (`az provider show`).

## Gotchas
- Policy "Allowed resource types" can still deny resources from a registered provider.

## Verify
- [ ] Vending baseline lists required providers and the pipeline shows them Registered before workload deploys.

## Checked
2026-10-28. Confirmed on the resource-providers-and-types, preview-features and error pages: `az provider list|show|register`, `az feature register|show|list`, `*/register/action` included in Contributor and Owner, cannot unregister while resource types exist, `MissingSubscriptionRegistration` and `NoRegisteredProviderFound` messages. CLI flags passed the CLI reference check.
Removed (not confirmed): the auto-register claim, Pending-means-manual-approval claim, the Terraform provider registration settings, and the subscription-wide / cannot-unregister preview gotchas.

Method: documentation only; no commands were run.
