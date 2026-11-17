---
id: computing-software.cloud-infrastructure-engineering.ansible.running-ansible-in-azure-devops-pipelines
name: running-ansible-in-azure-devops-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ci-pipelines, azure-devops, azure-pipelines, secure-files, variable-groups, environments-approvals, ssh-key, ansible-lint]
level: practitioner
status: draft
description: "Run lint, check-mode and deploy stages for Ansible in Azure Pipelines: agent setup, SSH keys as secure files, vault password from Key Vault variable groups, and environment approvals."
sources: ["Microsoft Learn - Azure Pipelines YAML schema reference (https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/)", "Microsoft Learn - Use secure files and InstallSSHKey task (https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/install-ssh-key-v0)", "Microsoft Learn - Link a variable group to Azure Key Vault secrets"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running Ansible in Azure DevOps pipelines

Goal: every PR lints and dry-runs, merges to main deploy to staging automatically and to
production after an approval — with no secrets in the repo or logs.

## Prerequisites in Azure DevOps
- **Variable group** `ansible-secrets` linked to Key Vault (secrets: `ANSIBLE-VAULT-PASSWORD`, any cloud creds). Key Vault names use dashes; they become `$(ANSIBLE-VAULT-PASSWORD)`.
- **Secure file** `deploy_ed25519` (SSH private key) and the `known_hosts` lines.
- **Environments** `staging` and `production`, with Approvals and checks on production.
- Agents: Microsoft-hosted `ubuntu-latest` if targets are reachable from the internet; otherwise a self-hosted agent pool inside the network.

## azure-pipelines.yml
```yaml
trigger: {branches: {include: [main]}}
pr: {branches: {include: [main]}}
pool: {vmImage: ubuntu-latest}
variables:
  - group: ansible-secrets
  - name: PIP_CACHE_DIR
    value: $(Pipeline.Workspace)/.pip

stages:
  - stage: Validate
    jobs:
      - job: lint
        steps:
          - task: UsePythonVersion@0
            inputs: {versionSpec: "3.12"}
          - script: pip install -r requirements.txt && ansible-galaxy collection install -r collections/requirements.yml -p ./collections
          - script: ansible-lint --format sarif > ansible-lint.sarif || (cat ansible-lint.sarif; exit 1)
          - script: ansible-playbook -i inventories/staging site.yml --syntax-check

  - stage: Staging
    dependsOn: Validate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: deploy_staging
        environment: staging
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/deploy-steps.yml
                  parameters: {inventory: inventories/staging}

  - stage: Production
    dependsOn: Staging
    jobs:
      - deployment: deploy_prod
        environment: production        # approval gate configured on the environment
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/deploy-steps.yml
                  parameters: {inventory: inventories/production}
```
`templates/deploy-steps.yml`:
```yaml
parameters:
  - name: inventory
    type: string
steps:
  - checkout: self
  - task: InstallSSHKey@0
    inputs:
      knownHostsEntry: $(KNOWN_HOSTS)
      sshKeySecureFile: deploy_ed25519
  - script: pip install -r requirements.txt && ansible-galaxy collection install -r collections/requirements.yml -p ./collections
  - script: |
      umask 077
      printf '%s' "$VAULT_PASS" > "$(Agent.TempDirectory)/vault_pass"
      ansible-playbook -i ${{ parameters.inventory }} site.yml --vault-password-file "$(Agent.TempDirectory)/vault_pass" --diff
    env:
      VAULT_PASS: $(ANSIBLE-VAULT-PASSWORD)    # secrets reach scripts only when mapped
      ANSIBLE_FORCE_COLOR: "1"
  - script: rm -f "$(Agent.TempDirectory)/vault_pass"
    condition: always()
```

## Gotchas
- Secret variables are not passed to scripts automatically; map them via `env:` as above.
- `deployment` jobs do not check out the repo by default; add `- checkout: self`.
- The vault password file lives in the agent temp dir with `umask 077` and is deleted in an `always()` step; on self-hosted agents that matters because the disk persists between runs.
- Microsoft-hosted agents have changing IPs; firewall allow-lists need a self-hosted pool or Azure service tags.

## Verify
- [ ] PR runs only the Validate stage; main runs Staging then waits on the Production approval.
- [ ] Pipeline logs show `***` where secrets would appear and no vault password file remains on the agent.
