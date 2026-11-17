---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-dynamic-resource-allocation
name: kubeflow-pipelines-dynamic-resource-allocation
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [dynamic-resource-allocation, dra, resource-claim, kfp-kubernetes, gpu-claim]
level: advanced
status: docs-checked
description: "Attach Kubernetes Dynamic Resource Allocation claims such as GPUs to KFP tasks with kubernetes.add_resource_claim from the kfp-kubernetes extension."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/dynamic-resource-allocation.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/platform-specific-features.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines dynamic resource allocation

DRA lets a cluster allocate GPUs and other devices via resource claims, managed by a DRA driver. Use it when your admin runs a DRA driver; for the device-plugin approach use `.set_accelerator_type()` and `.set_accelerator_limit()` instead.

Prerequisites:
- KFP SDK and backend versions with DRA support.
- Kubernetes 1.31 or newer with the `DynamicResourceAllocation` feature (enabled by default and GA from 1.34).
- A compatible DRA driver installed.
- A `ResourceClaimTemplate` created by the administrator in the namespace where the task runs. KFP does not create or manage claims or templates.

Install the extension: `pip install kfp[kubernetes]`.

```python
from kfp import dsl, kubernetes

@dsl.pipeline
def training_pipeline():
    workload_task = run_workload()
    kubernetes.add_resource_claim(
        workload_task,
        resource_claim_template_name='gpu-claim-template')
```

At runtime KFP adds the claim to the pod spec and a reference to the `main` container; Kubernetes creates the claim from the template and schedules the pod once the resource is available. Call `add_resource_claim()` once per template for several claims.

A claim allocates the device but does not install libraries; use an image and framework configuration compatible with the driver.

`kfp-kubernetes` is also the platform-specific library for features like `kubernetes.CreatePVC` to create a PVC (for example with `access_modes`, `size` and `storage_class_name`) and mount it into tasks.

When a pipeline input should choose the claim, use `kubernetes.add_resource_claim_json(task, resource_claim_json=param)` and pass `kubernetes.ResourceClaimConfig(resource_claim_template_name=...)` as the run argument; the JSON key is `resourceClaimTemplateName`.

Limits: DRA claims are Kubernetes-specific, are not portable to other KFP backends and have no effect in local execution. A missing or invalid driver, template or cluster configuration can leave the Pod pending, and an older KFP backend can reject the platform configuration of a pipeline compiled with a newer SDK.

## Checked

2026-11-09: confirmed against the Kubeflow website pages "Use Kubernetes Dynamic Resource Allocation" (read in full) and "Platform-specific features" (the CreatePVC section), both under content/en/docs/components/pipelines/user-guides/core-functions/. Nothing removed.

Method: docs-checked 2026-11-09 against the Kubeflow website dynamic-resource-allocation and platform-specific-features pages (raw markdown).
