---
id: computing-software.cloud-infrastructure-engineering.kubespray.offline-python-packages-and-running-airgapped
name: offline-python-packages-and-running-airgapped
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [offline, python, pypi, pip, proxy, container-image]
level: practitioner
status: docs-checked
description: "Supply Kubespray Python dependencies offline via the Kubespray container image, an HTTP proxy or an internal PyPi server, then run cluster.yml as usual."
sources:
  - https://kubespray.io/docs/operations/offline-environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray itself needs Python packages. Two ways to get them into an air-gapped network:

**Recommended: the Kubespray container image.** All required packages are baked into the image from Quay. Copy it into your private registry and you are done.

**Manual installation.** Check `requirements.txt` against what your OS package manager provides. For the missing ones, either use a proxy with internet access (typically in a DMZ) or run a PyPi server in your network.

With an HTTP(S) proxy:

```bash
sudo pip install --proxy=https://[username:password@]proxyserver:port -r requirements.txt
```

With an internal PyPi server:

```bash
# If you host all required packages
pip install -i https://pypiserver/pypi -r requirements.txt

# If you only need the ones missing from the OS package manager
pip install -i https://pypiserver/pypi package_you_miss
```

**Running.** With artifacts in place and the inventory configured, run the regular playbook:

```bash
ansible-playbook -i inventory/my_airgap_cluster/hosts.yaml -b cluster.yml
```

If you use the container image, mount your inventory into the container and run the same `ansible-playbook` command inside it, as the page's docker run example for the image from a private registry shows.

## Checked

The install routes and the run command were confirmed in the Install Kubespray Python Packages and Run Kubespray as usual sections of the Offline environment page.

Method: docs-checked 2026-11-09 against the Kubespray docs/operations/offline-environment.md page (full file read).
