---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-references
name: mr-references
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, reference, nameref, selector, matchcontrollerref]
level: practitioner
status: docs-checked
description: "Reference one managed resource from another by external name, nameRef, selector, or controller reference."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Four ways to point a managed resource at another. Example: a Subnet needing a VPC.

1. External name: put the provider-side ID directly, `vpcId: vpc-01353cfe93950a8ff` (see EXTERNAL-NAME in `kubectl get vpc`).
2. Name reference: use the Kubernetes object name with the `...Ref` field.

```yaml
spec:
  forProvider:
    vpcIdRef:
      name: my-test-vpc
```

3. Selector: the most flexible form, matching labels.

```yaml
    vpcIdSelector:
      matchLabels:
        my-label: label-value
```

4. Controller reference: `matchControllerRef` matches only a resource with the same Kubernetes controller reference, that is, one composed by the same composite resource. This avoids needing unique labels when every composed VPC shares the same label, for example when an InternetGateway needs the VPC from its own XR.

The field names (`vpcId`, `vpcIdRef`, `vpcIdSelector`) are defined by the provider, so check the provider's API for each reference.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the claims about resolve-once behaviour, Ref-versus-Selector advice, and the matchControllerRef: true syntax (the page names the option but shows no value).

Method: documentation only; no commands were run.
