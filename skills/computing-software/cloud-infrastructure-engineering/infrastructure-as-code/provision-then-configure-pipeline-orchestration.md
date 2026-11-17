---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.provision-then-configure-pipeline-orchestration
name: provision-then-configure-pipeline-orchestration
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, config-vs-provisioning, provision-configure-pipeline, terraform-ansible, ci-pipeline]
level: practitioner
status: docs-checked
description: "Orchestrate Terraform provisioning followed by Ansible configuration in one pipeline: outputs to inventory handoff, readiness waits, failure handling and reruns."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/output", "https://github.com/ansible-collections/cloud.terraform", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Provision-then-configure pipeline

Run provisioning (Terraform) first, hand the resulting host list to Ansible, wait for the new hosts to be reachable, then configure and verify. Keep these as separate pipeline stages: plan, provision (behind an approval gate), configure, verify.

## Handing results from Terraform to Ansible
1. **Outputs file:** `terraform output -json` prints all root-module outputs as a JSON object (a stable format for automation; the default human-readable format can change). Save it as a pipeline artifact and read it with a small script or `add_host`. `-raw NAME` prints a single string, number or boolean with no escaping, for shell use. Only root-module outputs are shown, so re-export child-module outputs from the root. `-json` and `-raw` print sensitive values in plain text, so treat the artifact as secret.
2. **cloud.terraform collection** (Ansible Core 2.15+): provides the inventory plugins `cloud.terraform.terraform_provider` (inventory from a Terraform state file) and `cloud.terraform.terraform_state` (inventory from resources created by cloud providers), the lookup `cloud.terraform.tf_output` (reads state file outputs), and the modules `cloud.terraform.terraform` (manages a deployment and plans), `terraform_output` and `plan_stash` (base64 encode or decode a plan file).
3. Install collections in the pipeline from a `requirements.yml` with `ansible-galaxy collection install -r requirements.yml`; a `version` key pins a version.

## Readiness
New instances are not immediately reachable. Start the configure play with `ansible.builtin.wait_for_connection`, with `gather_facts: false`, then run `ansible.builtin.setup` to gather facts:
- It waits up to `timeout` seconds (default 600), polls every `sleep` seconds (default 1), starts polling after `delay` seconds (default 0), and retries a stuck connection after `connect_timeout` (default 5).
- It uses Ansible's own transport and ping modules, so a pass means a real end-to-end connection works.

## Failure handling
- Configure failed: rerun only the configure stage; do not re-provision.
- Provision partially failed: Terraform state reflects what exists; rerun apply.
- Destroying on configure failure is tempting in ephemeral environments only.

## Verify
- [ ] Rerunning the pipeline on an existing stack makes no Terraform changes and zero Ansible changes.

## Checked
Method: docs-checked 2026-11-09 against the terraform output command page, the cloud.terraform GitHub README, and the ansible.builtin.wait_for_connection module page.
Removed as unconfirmed: the GitLab CI sketch, aws_ec2 tag-based dynamic inventory, the ansible/ansible provider ansible_host claim, `cloud-init status --wait`, local-exec and AAP workflow remarks, and the "preferred" ranking of handoff options.
