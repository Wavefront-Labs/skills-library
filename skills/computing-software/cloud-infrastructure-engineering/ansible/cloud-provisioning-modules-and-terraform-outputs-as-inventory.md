---
id: computing-software.cloud-infrastructure-engineering.ansible.cloud-provisioning-modules-and-terraform-outputs-as-inventory
name: cloud-provisioning-modules-and-terraform-outputs-as-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, config-vs-provisioning, cloud-modules, amazon-aws-modules, terraform-inventory, terraform-output-inventory, cloud-terraform]
level: advanced
status: docs-checked
description: "Provision cloud resources with amazon.aws and azure.azcollection modules, or hand Terraform-built hosts to Ansible via the cloud.terraform inventory plugin and terraform_output."
sources: ["https://docs.ansible.com/ansible/latest/collections/amazon/aws/ec2_instance_module.html", "https://docs.ansible.com/ansible/latest/collections/azure/azcollection/azure_rm_virtualmachine_module.html", "https://github.com/ansible-collections/cloud.terraform", "https://raw.githubusercontent.com/ansible-collections/cloud.terraform/main/plugins/inventory/terraform_provider.py", "https://raw.githubusercontent.com/ansible-collections/cloud.terraform/main/plugins/modules/terraform_output.py", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud provisioning modules, and Terraform outputs as inventory

Neither amazon.aws, azure.azcollection nor cloud.terraform ships with ansible-core; install the collections first.

## Option A: provision with Ansible modules
Fine for small estates, ephemeral test environments, or an Ansible-only team. Identity comes from names, tags and filters, not a state file.
```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - amazon.aws.ec2_instance:
        name: "web-{{ item }}"
        instance_type: t3.small
        image_id: "{{ ami_id }}"
        vpc_subnet_id: "{{ subnet_id }}"
        security_groups: [web-sg]
        tags: {role: web, env: stage, managed_by: ansible}
        exact_count: 1
        filters: {"tag:Name": "web-{{ item }}", instance-state-name: [running, pending]}
        region: eu-west-1
        wait: true
      loop: [1, 2]
      register: ec2
```
- `ec2_instance` options used: `name`, `instance_type`, `image_id`, `vpc_subnet_id`, `security_groups`, `tags`, `filters`, `region`, `wait` (default true). `exact_count` was added in amazon.aws 2.2.0.
- `module_defaults` accepts the `group/aws` action group, so `region` can be set once per play instead of per task.
- After creating, add hosts with `ansible.builtin.add_host` (`name`, `groups`) and wait for SSH with `ansible.builtin.wait_for_connection` (defaults: `timeout` 600, `sleep` 1, `delay` 0, `connect_timeout` 5). Inspect the registered result (`-v`) for the exact instance keys before templating them: the return docs list `instance_id` and `public_ip_address`.
- Azure equivalent: `azure.azcollection.azure_rm_virtualmachine` with `name`, `resource_group`, `vm_size`, `image`, `admin_username`, `ssh_public_keys` (Linux), `tags` and `state` (`present` or `absent`). Removal is `state: absent` explicitly; nothing tracks resources deleted from the playbook, which is the main reason larger estates use Terraform.

## Option B: Terraform provisions, Ansible configures
1. **Cloud inventory plugin** on tags Terraform sets (for example `amazon.aws.aws_ec2` with `keyed_groups`). Decoupled and works for anything in the account.
2. **`cloud.terraform.terraform_provider` inventory plugin** reads Terraform resources of type `ansible_host` and `ansible_group` from state. A host resource has `name`, `groups` and `variables`; a group resource has `name`, `children` and `variables`.
```yaml
# inventories/stage/terraform.yml
plugin: cloud.terraform.terraform_provider
project_path: ../../terraform/envs/stage
```
   Plugin options (source): `plugin`, `project_path` (a string or a list of paths), `state_file`, `search_child_modules` (documented default false; set it explicitly to include resources from child modules) and `binary_path`. It runs `terraform show`, so the directory must be initialised, and it does not support caching. A host name seen twice across projects raises a warning. The README also lists a `terraform_state` inventory plugin; its options were not read here.
3. **`cloud.terraform.terraform_output` module** returns outputs: `project_path`, `state_file` (not compatible with remote state), `workspace`, `binary_path`, `name` (one output) and `format` (`json` default, or `raw`, which requires `name`). It returns `outputs` (a dict; read `.outputs.<Name>.value`) or, when `name` is given, `value`. The README also lists a `tf_output` lookup, a `terraform` module and `plan_stash`.
```yaml
- cloud.terraform.terraform_output:
    project_path: ../../terraform/envs/stage
    name: lb_dns
  register: lb
```

## Gotchas
- Do not manage the same resource with both tools.
- State can contain secrets; scope who can read it.
- New instances need time to accept SSH: `wait_for_connection` before configuring.

## Verify
- [ ] `ansible-inventory -i inventories/stage --graph` lists the Terraform-created hosts in the right groups.

## Checked
Date: 2026-11-07. Read: the ec2_instance and azure_rm_virtualmachine module pages (parameter tables and return sections; the nesting of the registered instance keys was ambiguous in the text I could read, so no key path is given), the wait_for_connection and add_host pages, the module_defaults page (for `group/aws`), the cloud.terraform README, and the full source of the terraform_provider inventory plugin and the terraform_output module on GitHub (the terraform module pages on docs.ansible.com return 404, so the source is cited instead). Not read: the terraform, terraform_state and tf_output sources, and the Terraform-side provider that defines `ansible_host`.
Corrected: `backend_type` and `backend_config` are not options of `terraform_provider` (they were attributed to it); the plugin needs an initialised directory because it runs `terraform show`.
Removed as not on a read page: the HCL `ansible_host` example with `aws_instance` references, `item.instances[0].private_ip_address`, the `ansible/ansible` provider name, the "run terraform apply from AWX" claim, the `keyed_groups` on `tags.role` detail, and the example `group/aws` region mapping.
Method: documentation only; no commands were run.
