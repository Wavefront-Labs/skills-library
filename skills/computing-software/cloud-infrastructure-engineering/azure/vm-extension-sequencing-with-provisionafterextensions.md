---
id: computing-software.cloud-infrastructure-engineering.azure.vm-extension-sequencing-with-provisionafterextensions
name: vm-extension-sequencing-with-provisionafterextensions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vmss, vm-extensions, provisionafterextensions, extension-sequencing, arm-template]
level: practitioner
status: docs-checked
description: "Order scale set extensions deterministically with provisionAfterExtensions: what is and isn't sequenced, model rules and troubleshooting."
sources: ["https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-extension-sequencing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension sequencing

**Goal:** the domain join happens before the app installer, and the monitoring agent before the health extension -
every time, on every instance.

## Scale sets: provisionAfterExtensions
Sequencing is not mandatory: unless specified, extensions on a scale set instance can be provisioned in any order.
Add the `provisionAfterExtensions` property, an array of extension **names**, to an extension in the scale set model:
```json
"virtualMachineProfile": { "extensionProfile": { "extensions": [
  { "name": "ExtensionA", "properties": { "publisher": "ExtensionA.Publisher", "type": "ExtensionA",
      "typeHandlerVersion": "1.0", "autoUpgradeMinorVersion": true, "settings": {} } },
  { "name": "ExtensionB", "properties": { "provisionAfterExtensions": ["ExtensionA"],
      "publisher": "ExtensionB.Publisher", "type": "ExtensionB",
      "typeHandlerVersion": "2.0", "autoUpgradeMinorVersion": true, "settings": {} } }
] } }
```
Rules from the documentation:
- Every extension named in the array must be fully defined in the scale set model.
- A sequence only orders the named extensions. Extensions outside any sequence can be provisioned before, after or
  during it. To guarantee nothing else runs mid-sequence, sequence all extensions in the model.
- An extension you depend on must have a `settings` property under `properties`; an empty `{}` is fine.
- Circular dependencies (A -> B -> C -> A) are not allowed.
- To remove an extension, first make sure no other extension lists it in `provisionAfterExtensions`.

## Single VMs
For standalone VMs, extensions are separate child resources; order them in a template with `dependsOn` on the previous
extension resource.

## Verify
- [ ] Instance view of an instance shows extension execution order as designed (compare status times).

## Checked
2026-10-27. Confirmed against Learn "Sequence extension provisioning in Virtual Machine Scale Sets" (property name,
extension-name array, model definition rules, circular dependency and settings rules, optional sequencing). Removed
(not in the fetched page): the CLI `--provision-after-extensions` flag, specific extension types and handler versions
in the old Bicep example, "failed extension stops later ones", "changing order takes effect on reimage", the single
Custom Script Extension and 90 minute timeout gotchas, and the health-extension repair claim. The `dependsOn` advice for
single VMs is standard ARM behaviour but is not on the fetched page.
Method: documentation only; no commands were run.
