---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-jobs-in-azure-pipelines-and-jenkins
name: terraform-jobs-in-azure-pipelines-and-jenkins
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, azure-pipelines, jenkins, cicd, plan-artifact, approvals, workload-identity-federation, azure-devops]
level: practitioner
status: docs-checked
description: "Terraform plan, approve, apply in Azure Pipelines (OIDC service connection, environment approvals) and Jenkins (input directive), applying a saved plan file."
sources: ["https://learn.microsoft.com/en-us/azure/devops/pipelines/process/environments", "https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/azure-cli-v2", "https://raw.githubusercontent.com/hashicorp/terraform-provider-azurerm/main/website/docs/guides/service_principal_oidc.html.markdown", "https://www.jenkins.io/doc/book/pipeline/syntax/", "https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Terraform in Azure Pipelines and Jenkins

Same shape on both: init, plan to a file, keep the plan for review, a human gate, apply
that exact file. HashiCorp's automation tutorial gives the core sequence
`terraform init -input=false`, `terraform plan -out=tfplan -input=false`,
`terraform apply -input=false tfplan`, and says setting `TF_IN_AUTOMATION` to any
non-empty value makes minor output adjustments that de-emphasize commands to run.

## Plan-file facts that apply to both
- Passing a saved plan to `terraform apply` skips the approval prompt (passing the file is
  the approval), and `-auto-approve` is ignored with a saved plan.
- The plan file holds the full configuration, the state and any variables, in cleartext
  even for values hidden in terminal output. Treat the archived working directory as
  sensitive. Supply provider credentials through environment variables rather than
  variables, since those are not stored in the plan.
- The plan can contain absolute paths. Extract the archived configuration at an identical
  absolute path before apply; the tutorial suggests running in a container to control this.
- Terraform plan with `-detailed-exitcode` returns 0 (no changes), 1 (error), 2 (changes).

## Azure Pipelines
Use a workload identity federation service connection and pass its token to the azurerm
provider from `AzureCLI@2`. With `addSpnToEnvironment: true` (default false) the task
exposes `servicePrincipalId`, `idToken` (for federation) and `tenantId` to the script
(`$servicePrincipalId` in shell scripts).
```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: sc-prod-oidc
    scriptType: bash
    scriptLocation: inlineScript
    addSpnToEnvironment: true
    inlineScript: |
      export ARM_USE_OIDC=true ARM_OIDC_TOKEN=$idToken ARM_CLIENT_ID=$servicePrincipalId \
             ARM_TENANT_ID=$tenantId ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
      terraform init -input=false
      terraform plan -input=false -out=tfplan
```
- The azurerm OIDC guide describes `ARM_OIDC_TOKEN` as the variable for a token from your
  OIDC provider, with `ARM_CLIENT_ID`, `ARM_TENANT_ID` and `ARM_SUBSCRIPTION_ID` for the
  identity. It also describes an Azure DevOps mode where the provider requests its own
  token: set `ARM_USE_OIDC: true`, `SYSTEM_ACCESSTOKEN: $(System.AccessToken)`,
  `SYSTEM_OIDCREQUESTURI: $(System.OidcRequestUri)` and
  `ARM_ADO_PIPELINE_SERVICE_CONNECTION_ID`. It recommends the `AzureCLI@2` task, and
  requires at least one task in the pipeline to reference the service connection, or the
  agent fails with `No service connection found with identifier`.
- Environments: a `deployment` job targets an `environment`, and resource owners define
  approvals and checks on the environment that must be satisfied before a stage consuming
  it begins. The environment Creator, Administrator and User roles (not Reader) can manage
  approvals and checks. Environments are not available in Classic pipelines. Put the apply
  stage in a deployment job on a prod environment so the approval gates it.
- Pass the saved plan between stages as a pipeline artifact (publish after plan,
  download in the deployment job), then repeat the OIDC setup before `terraform apply
  -input=false tfplan`.

## Jenkins
Declarative syntax elements confirmed by the Jenkins syntax page:
```groovy
pipeline {
  agent none
  options { disableConcurrentBuilds() }
  stages {
    stage('Approve') {
      input { message 'Apply the reviewed plan?'; submitter 'infra-approvers' }
      steps { echo 'approved' }
    }
  }
}
```
- `input` directive: the stage pauses after options are applied and before the stage's
  `agent` block or `when` condition is evaluated, so a stage-level `input` does not hold
  an executor. `submitter` is a comma-separated list of users or external groups allowed to
  approve (default: any user); `submitterParameter` records who approved.
- `agent none` at top level means each stage needs its own `agent`.
- `disableConcurrentBuilds()` queues a build when one is already running, protecting shared
  resources. `timeout` can be set per pipeline or per stage; at stage level the agent
  allocation time counts toward the limit.
- `when { environment name: 'X', value: 'y' }` runs a stage conditionally, for example
  after a plan step sets a variable from the `-detailed-exitcode` result.
- `credentials()` in an `environment` block reads Jenkins credentials by id.
- Carry the plan file and lock file from plan to apply however your Jenkins setup allows
  (this page does not specify a mechanism), and apply with `terraform init -input=false`
  then `terraform apply -input=false tfplan`.

## Verify
- [ ] Apply stage applies the saved `tfplan`, never a fresh plan.
- [ ] Approval is restricted to named approvers (environment checks, or `submitter`).
- [ ] No static cloud secrets in pipeline variables; plan archive access is restricted.

## Checked
Checked 2026-11-08 against Microsoft Learn (Environments, AzureCLI@2), the azurerm OIDC guide, the Jenkins Pipeline syntax page, HashiCorp's automation tutorial and the plan/apply command pages.
Removed as not stated by the pages: `TerraformTaskV4@4` and extension notes, the `hashicorp/terraform` image and `--entrypoint=` argument, `stash`/`unstash`, `archiveArtifacts`, `ansiColor`, `withCredentials` AWS binding, Lockable Resources `lock`, the pinned Terraform version, "same version" and state-moved apply behaviour. Added: plan-file sensitivity and absolute-path notes, `input` directive timing and `submitter`.
Method: docs-only read of cited pages, 2026-11-08
