---
id: computing-software.devops-ci-cd.spinnaker.azure-provider-account
name: azure-provider-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [azure, provider, service-principal, key-vault, vm-scale-sets, clouddriver-local, accounts]
level: practitioner
status: docs-checked
description: "Set up the Azure provider: service principal, Key Vault holding the default VM username and SSH key, and the clouddriver-local.yml azure account with its SSH-versus-password flag."
sources:
  - https://spinnaker.io/docs/setup/install/providers/azure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In Azure an Account maps to a credential able to authenticate against one subscription. You need a **service principal** and a **Key Vault** that stores the default username and SSH public key used for deployed VM Scale Sets. The page assumes Azure CLI 2.0.

**Steps (all from the page):**
1. `az login`, `az account list`, then `az account set --subscription $SUBSCRIPTION_ID`.
2. `az ad sp create-for-rbac --name "Spinnaker" --role contributor --scopes /subscriptions/${SUBSCRIPTION_ID}`; note the app id and tenant id. The app key (password) is also needed when creating the account; you are prompted for it on standard input because it is sensitive.
3. `az group create` a resource group in an available location (`az account list-locations --query [].name` lists them).
4. Create a globally uniquely named Key Vault with `az keyvault create --enabled-for-template-deployment true`, run `az keyvault set-policy --secret-permissions get --spn $APP_ID`, and set secrets `VMUsername` and `VMSshPublicKey`. To use a password instead, set `VMPassword` rather than `VMSshPublicKey`.

**Add the account** in `clouddriver-local.yml` (the page's current form):

```yaml
azure:
  enabled: true
  accounts:
    - name: my-azure-account
      clientId: <APP_ID>
      tenant-id: <TENANT_ID>
      subscriptionId: <SUBSCRIPTION_ID>
      defaultKeyValue: <VAULT_NAME>
      defaultResourceGroup: <RESOURCE_GROUP>
      packerResourceGroup: <RESOURCE_GROUP>
      useSshPublicKey: true
      appKey:
      regions:
      - regionname
```

- The SSH public key is used to provision VM scale sets by default; set `useSshPublicKey: false` to use the password. The secrets live in the Key Vault named by the account, under the names `VMPassword` and `VMSshPublicKey`.
- If you lose the app key, `az ad sp credential reset --name $APP_ID` generates a new one.
- Default regions are eastus and westus; set `regions` to use others.
- The full property list is the AzureConfigurationProperties class, linked from the page.

## Checked

2026-11-04. Confirmed against the Azure provider page: prerequisite steps, secret names, the account YAML, `useSshPublicKey`, default regions and the key reset command. Removed: the `hal config provider azure` commands and the Halyard 1.19 default claim (the page now configures clouddriver-local.yml and does not mention Halyard commands or versions).

Method: documentation only; no commands were run.
