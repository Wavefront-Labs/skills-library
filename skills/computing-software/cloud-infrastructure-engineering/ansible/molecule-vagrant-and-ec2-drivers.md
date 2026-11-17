---
id: computing-software.cloud-infrastructure-engineering.ansible.molecule-vagrant-and-ec2-drivers
name: molecule-vagrant-and-ec2-drivers
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, molecule, vagrant-driver, ec2-driver, molecule-plugins, delegated-driver, vm-testing, role-testing]
level: advanced
status: docs-checked
description: "Test roles on real VMs with Molecule using the Vagrant and EC2 drivers from molecule-plugins, or the default delegated driver with your own create/destroy playbooks."
sources: ["molecule-plugins repository (https://github.com/ansible-community/molecule-plugins)", "molecule-plugins Vagrant driver README (https://github.com/ansible-community/molecule-plugins/blob/main/doc/vagrant/README.rst)", "molecule-plugins EC2 platform options (https://github.com/ansible-community/molecule-plugins/blob/main/doc/ec2/platforms.rst)", "Molecule configuration, delegated driver (https://github.com/ansible/molecule/blob/main/docs/configuration.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Molecule with Vagrant and EC2 drivers

Goal: test what containers cannot — kernel modules, systemd as PID 1 with real boot, SELinux,
firewalld, reboots, Windows — on disposable VMs, locally (Vagrant) or in CI (EC2).

## Install
```bash
pip install molecule 'molecule-plugins[vagrant]'      # relies on the vagrant command line plus a provider (libvirt, VirtualBox, ...)
pip install molecule 'molecule-plugins[ec2]' boto3     # the ec2 extra adds no packages; needs the amazon.aws collection and AWS credentials in the environment
molecule drivers                                        # lists available drivers
```

## Vagrant scenario
`molecule/vagrant/molecule.yml`:
```yaml
driver:
  name: vagrant
  provider: {name: libvirt}          # or virtualbox
platforms:
  - name: el9
    box: <vagrant-box-name>
    box_version: <pinned box version>
    memory: 2048
    cpus: 2
    interfaces:
      - {network_name: private_network, ip: 192.168.121.50}
provisioner: {name: ansible}
verifier: {name: ansible}
```
`molecule test -s vagrant` runs create → converge → idempotence → verify → destroy.

## EC2 scenario
```yaml
driver: {name: ec2}
platforms:
  - name: el9-ec2
    image: <ami-id>                     # or image_owner + image_name / image_filters
    instance_type: t3.small
    vpc_subnet_id: <subnet-id>
    region: eu-west-1
    tags: {owner: ci, purpose: molecule}
    boot_wait_seconds: 60
```
Unless you supply `private_key_path` the driver generates a key for the run (`key_inject_method` is `cloud-init` or `ec2`). Unless you list existing `security_groups` it creates a security group that allows incoming SSH and ICMP and all outgoing traffic; pass `security_group_rules` (handed to `amazon.aws.ec2_group`) to restrict sources. Credentials and region come from the AWS environment variables or `aws_profile`.

## Alternative: default (delegated) driver
The delegated (`default`) driver leaves provisioning to you: you write `create.yml`/`destroy.yml` in the scenario using any modules and must provide the instance-config data (address, user, identity file or password, port, instance name); the destroy playbook must reset it. More code, but no plugin coupling.

## Gotchas
- A failed or cancelled CI run can leave EC2 instances running; tag them (`tags`) and run a reaper job.
- Vagrant relies on the vagrant command line, which is known to be problematic to install on several platforms; the README lists tested platform and provider combinations.
- `molecule test` destroys at the end; use `molecule converge` + `molecule login` to debug, `molecule destroy` when done.
- Boxes/AMIs drift; pin `box_version` or the AMI id for reproducible results.

## Verify
- [ ] `molecule test -s vagrant` passes including idempotence on a clean host.
- [ ] After the EC2 scenario, no instance with the molecule tag is left running.

## Checked

Checked 2026-10-26 against molecule-plugins main (README, `doc/vagrant/README.rst`, `doc/ec2/platforms.rst`, `pyproject.toml` extras) and Molecule configuration documentation (delegated driver). Confirmed: extras names, Vagrant platform keys (`box`, `box_version`, `memory`, `cpus`, `interfaces` with `network_name` and `ip`, provider `name`), EC2 platform keys (`image`, `image_owner`, `image_name`, `instance_type`, `vpc_subnet_id`, `region`, `tags`, `boot_wait_seconds`), key and security group behaviour, the `molecule drivers` command and the delegated driver instance-config contract. Removed the unconfirmed box name, nested virtualisation, reaper query and `Molecule 6+` driver claims.

Method: documentation only; no commands were run.
