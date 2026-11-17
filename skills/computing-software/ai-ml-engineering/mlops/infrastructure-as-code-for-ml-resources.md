---
id: computing-software.ai-ml-engineering.mlops.infrastructure-as-code-for-ml-resources
name: infrastructure-as-code-for-ml-resources
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, ml-infrastructure-as-code, terraform, sagemaker, vertex-ai, azure-ml]
level: practitioner
status: draft
description: "Manage ML platform resources with Terraform: workspaces, compute, registries, endpoints and IAM per environment, keeping model versions owned by pipelines."
sources:
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sagemaker_endpoint
  - https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/vertex_ai_endpoint
  - https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/machine_learning_workspace
  - https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace-terraform
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Infrastructure as code for ML resources

**Goal:** every ML environment (dev, staging, prod) is reproducible from code, reviewed in pull requests, and model deployments do not fight Terraform state.

## What IaC owns
| Layer | Examples | Owner |
|---|---|---|
| Foundations | VPC/subnets, private endpoints, KMS keys, buckets, container registries | Terraform |
| ML platform | SageMaker domain, Vertex/Azure ML workspace, compute clusters, feature store, tracking server | Terraform |
| Identity | pipeline, training, serving roles and least-privilege policies | Terraform |
| Pipelines | pipeline definitions, schedules | CI deploys (SDK) or Terraform |
| Model versions on endpoints | which model serves what traffic | Deployment pipeline |

Keeping rapidly changing model versions out of Terraform avoids drift fights and slow applies. If Terraform does create the endpoint, pass the model as a variable set by CI, or use `lifecycle { ignore_changes = [...] }` on fields the deployment pipeline manages.

## Examples
```hcl
resource "aws_sagemaker_endpoint_configuration" "churn" {
  name = "churn-${var.model_version}"
  production_variants {
    variant_name           = "primary"
    model_name             = aws_sagemaker_model.churn.name
    instance_type          = "ml.m5.xlarge"
    initial_instance_count = 2
  }
  kms_key_arn = aws_kms_key.ml.arn
  lifecycle { create_before_destroy = true }
}
resource "aws_sagemaker_endpoint" "churn" {
  name                 = "churn"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.churn.name
}
```
Endpoint configs are immutable: new name per change plus `create_before_destroy` gives a blue/green swap.
```hcl
resource "azurerm_machine_learning_workspace" "ml" {
  name                          = "mlw-${var.env}"
  location                      = var.location
  resource_group_name           = azurerm_resource_group.ml.name
  application_insights_id       = azurerm_application_insights.ml.id
  key_vault_id                  = azurerm_key_vault.ml.id
  storage_account_id            = azurerm_storage_account.ml.id
  public_network_access_enabled = false
  identity { type = "SystemAssigned" }
}
```

## Structure
- One root module per environment (or workspaces) with shared modules (`modules/ml-workspace`); separate state per environment, remote backend with locking.
- Promote by applying the same module version to staging then prod.
- Policy checks (OPA/Conftest, Checkov) for encryption, public access, and GPU instance allow-lists.
- Tag resources with team, cost centre and environment for GPU cost allocation.

## Gotchas
- Console-created resources drift; import them (`terraform import` or `import` blocks) before managing.
- Deleting a workspace or bucket in a plan destroys experiments and artifacts; set `prevent_destroy` on stateful resources.
- Provider support lags new ML features; fall back to the cloud CLI/SDK in the pipeline for unsupported settings rather than hand-editing.

## Verify
- [ ] `terraform plan` on a clean checkout shows no changes for each environment.
- [ ] A new environment can be stood up from code alone.
- [ ] Model deployment does not cause Terraform drift.
