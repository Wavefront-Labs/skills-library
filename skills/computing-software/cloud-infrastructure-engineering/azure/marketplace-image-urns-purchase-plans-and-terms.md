---
id: computing-software.cloud-infrastructure-engineering.azure.marketplace-image-urns-purchase-plans-and-terms
name: marketplace-image-urns-purchase-plans-and-terms
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-images, marketplace-terms, image-urn, purchase-plan, marketplace-images, nva]
level: practitioner
status: docs-checked
description: "Deploy Marketplace VM images reliably: find URNs and versions, accept legal terms once per subscription, pass plan info on VMs and gallery images, and read plan errors."
sources: ["https://learn.microsoft.com/azure/virtual-machines/linux/cli-ps-findimage", "https://learn.microsoft.com/cli/azure/vm/image/terms", "https://learn.microsoft.com/azure/virtual-machines/marketplace-images", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/error-messages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marketplace image URNs, plans and terms

**Goal:** pipelines that deploy third-party images without failing on purchase validation.

## Find the image
A URN is `Publisher:Offer:Sku:Version`; the version can be replaced with `latest`. Consider pinning an explicit version in production and updating it deliberately.
```bash
az vm image list-publishers --location westus --output table
az vm image list-offers --location westus --publisher RedHat --output table
az vm image list-skus --location westus --publisher RedHat --offer RHEL --output table
az vm image list --location westus --publisher RedHat --offer RHEL --sku 9_1 --all --output table
```
Pass the URN column to `az vm create --image`. `az vm image list` without `--all` shows a cached list of popular images (including `UrnAlias` values such as `Ubuntu2204`); with `--all` it can take several minutes. Canonical's Ubuntu offer names changed: `UbuntuServer` before 20.04, `0001-com-ubuntu-server-focal` for 20.04 and `0001-com-ubuntu-server-jammy` for 22.04.

## Check whether the image has a plan
```bash
az vm image show --location westus --urn bitnami:rabbitmq:rabbitmq:latest
```
If the `plan` property is not null, the image has extra license and purchase terms to accept before programmatic deployment, and you must pass the plan parameters when you deploy (name, product, publisher; some images also have a promotion code).

## Accept terms (once per subscription per image)
```bash
az vm image terms show   --urn bitnami:rabbitmq:rabbitmq:latest
az vm image terms accept --urn bitnami:rabbitmq:rabbitmq:latest
```
`show` returns `licenseTextLink` and `accepted`; after `accept` it must report `"accepted": true`. Accepting terms enables programmatic deployment in that subscription. `az vm image terms cancel` also exists.

## Pass the plan when creating the VM
```bash
az vm create -g rg -n vm1 --admin-username azureuser --generate-ssh-keys \
  --image bitnami:rabbitmq:rabbitmq:latest \
  --plan-name rabbitmq --plan-product rabbitmq --plan-publisher bitnami
```
In an ARM template the VM resource carries a `plan` object with `name`, `publisher` and `product`.

## Gallery image definitions and existing VHDs
- If you still have the source VM, read the plan with PowerShell `$vm.Plan` (after `Get-AzVM`) or `az vm get-instance-view -g rg -n vm --query plan`.
- When creating a gallery image definition in PowerShell, pass `-PurchasePlanPublisher`, `-PurchasePlanProduct` and `-PurchasePlanName` to `New-AzGalleryImageDefinition`; when creating a VM from it, pass the definition's purchase plan with `Set-AzVMPlan -Publisher -Product -Name`.
- For a VHD from a VM created from a paid Marketplace image, create the new VM with `--attach-os-disk` plus `--plan-name`, `--plan-publisher` and `--plan-product`. If the original VM is gone and you did not record the plan, Learn says to file a support request (VM name, subscription ID and the time stamp of the delete).

## Errors
- `VMMarketplaceInvalidInput`: "Creating a virtual machine from Marketplace image requires Plan information in the request" (add the plan); "The purchase information does not match" (the plan does not match the image); "Creating a virtual machine from a non Marketplace image does not need Plan information" (remove the plan).
- If you get a message about accepting terms, run `az vm image terms accept` and confirm `"accepted": true`.

## Check
`az vm image terms show --urn <URN> --query accepted` is true in each target subscription.

## Checked
Date: 2026-11-07
Read in full: Learn "Find Azure Marketplace image information using the Azure CLI" (URN format, list commands, plan check, terms, `--plan-*` flags, existing VHD section), "Supply Azure Marketplace purchase plan information when creating images" (PowerShell `-PurchasePlan*`, `Set-AzVMPlan`, ARM `plan` object), the `az vm image terms` reference (accept/cancel/show, `--urn`), and "Understand common error messages when you manage virtual machines in Azure" (the three `VMMarketplaceInvalidInput` messages).
Removed or replaced: the Palo Alto example URNs and version, Bicep snippet (page shows ARM JSON), `az sig image-definition` `--plan-*` flags (the page only shows PowerShell), `MarketplacePurchaseEligibilityFailed` and `ResourcePurchaseValidationFailed`, claims about CSP/EA/private Marketplace restrictions, pay-as-you-go versus BYOL billing, and the subscription-vending advice. Short flags `-p`/`-f` replaced by the long flags used on the page. `--query accepted` is my own JMESPath over the documented `accepted` field.
Method: documentation only; no commands were run.
