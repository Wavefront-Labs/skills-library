---
id: computing-software.cloud-infrastructure-engineering.kubespray.ansible-environment-troubleshooting-and-container-image
name: ansible-environment-troubleshooting-and-container-image
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ansible, troubleshooting, ansible-library, container-image, quay, docker]
level: practitioner
status: docs-checked
description: "Fix Ansible version and module problems with ANSIBLE_LIBRARY or run Kubespray from the pre-built quay.io image with the inventory and SSH key bind-mounted."
sources:
  - https://kubespray.io/docs/ansible/ansible.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrong versions of Ansible, collections or Python dependencies cause problems. Kubespray ships custom modules, so Ansible must be told where they are by setting `ANSIBLE_LIBRARY` to the `library` directory of the checkout:

```ShellSession
export ANSIBLE_LIBRARY=<kubespray_dir>/library`
```

A simple way to get matching versions is the pre-built image on Quay. Check out the tag, pull the same image tag, and use bind mounts for the inventory and SSH key:

```ShellSession
git checkout v2.30.0
docker pull quay.io/kubespray/kubespray:v2.30.0
docker run --rm -it --mount type=bind,source="$(pwd)"/inventory/sample,dst=/inventory \
  --mount type=bind,source="${HOME}"/.ssh/id_rsa,dst=/root/.ssh/id_rsa \
  quay.io/kubespray/kubespray:v2.30.0 bash
# Inside the container you may now run the kubespray playbooks:
ansible-playbook -i /inventory/inventory.ini --private-key /root/.ssh/id_rsa cluster.yml
```

The example shows the playbooks run from inside the container with the inventory at `/inventory`.

## Checked

2026-11-04. ANSIBLE_LIBRARY and the docker run example were confirmed under Troubleshooting Ansible issues. Removed the tag-matching advice and the offline remark, which were not confirmed.

Method: documentation only; no commands were run.
