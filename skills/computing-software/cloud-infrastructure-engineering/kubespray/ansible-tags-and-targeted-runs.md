---
id: computing-software.cloud-infrastructure-engineering.kubespray.ansible-tags-and-targeted-runs
name: ansible-tags-and-targeted-runs
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ansible, tags, skip-tags, download, preinstall, resolvconf]
level: advanced
status: docs-checked
description: "Run only part of a Kubespray playbook with --tags and --skip-tags, using the tag table (download, upload, resolvconf, preinstall, etcd, network) and the page's example commands."
sources:
  - https://kubespray.io/docs/ansible/ansible.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Playbooks define many tags. Useful groups from the page's table: `preinstall` (preliminary configuration), `facts`, `bootstrap_os`, `download` (fetching container images to a delegate host), `upload` (distributing images and binaries), `upgrade`, `etcd` and `etcd-secrets`, `network`, `cni`, `calico`, `cilium`, `flannel`, `node`, `control-plane`, `kubelet`, `kube-proxy`, `nginx` (LB for kube-apiserver), `coredns`, `nodelocaldns`, `resolvconf`, `apps`, `helm`, `metallb`, `kube-vip`, `reset`, `win_nodes`.

Documented examples:

```ShellSession
ansible-playbook -i inventory/sample/inventory.ini cluster.yml --tags preinstall,facts --skip-tags=download,bootstrap_os
```

The page describes this as applying only DNS configuration tasks and skipping everything related to host OS configuration and downloading container images.

```ShellSession
ansible-playbook -i inventory/sample/inventory.ini -e dns_mode='none' cluster.yml --tags resolvconf
```

Only removes the cluster DNS resolver IP from the hosts' `/etc/resolv.conf`.

```ShellSession
ansible-playbook -i inventory/sample/inventory.ini cluster.yml \
    -e '{"download_run_once": true, "download_localhost": true}' \
    --tags download --skip-tags upload,upgrade
```

Prepares all container images locally on the runner without installing or uploading anything.

The page's own caution: use `--tags` and `--skip-tags` only if you are 100% sure what you are doing.

## Checked

2026-11-04. The tag names and the three example commands were confirmed on the Ansible tags and Example commands sections of the Ansible page.

Method: documentation only; no commands were run.
