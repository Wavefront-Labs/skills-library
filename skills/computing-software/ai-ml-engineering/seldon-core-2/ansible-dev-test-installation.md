---
id: computing-software.ai-ml-engineering.seldon-core-2.ansible-dev-test-installation
name: ansible-dev-test-installation
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, installation, ansible, ansible-playbook, kind-cluster, setup-ecosystem, setup-seldon, seldon-all, private-registry, custom-images, dev-test]
level: practitioner
status: docs-checked
description: "Install Seldon Core 2 and its ecosystem on Kind with Ansible playbooks (seldon-all, kind-cluster, setup-ecosystem, setup-seldon): variables, custom images, uninstall. Dev only."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/ansible.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ansible installation (dev and test only)

The docs warn that the Ansible install of Core and its ecosystem is for dev and testing. For production use the Helm install.

## Prerequisites
Playbooks depend on the `kubernetes.core` collection and need `kubectl`.
```bash
pip install ansible openshift kubernetes docker
ansible-galaxy collection install kubernetes.core
```
Tested on Python 3.8 to 3.11 (Ansible 6.7.0 or 7.2.0, Docker lib 6.0.1, Kubernetes lib 26.1.0) with `kubernetes.core` 2.4.0. Playbooks are in the `ansible` folder of the repo; run from there.

## Playbooks
- `playbooks/seldon-all.yaml`: one command on a fresh Kind cluster. It runs `kind-cluster.yaml`, `setup-ecosystem.yaml` (Kafka, Prometheus, OpenTelemetry, Jaeger) then `setup-seldon.yaml`, using Helm charts from the current checkout. It accepts the variables of the others, e.g. `-e seldon_mesh_namespace=my-seldon-mesh -e install_prometheus=no -e @playbooks/vars/set-custom-images.yaml`.
- Run the three individually for more control, e.g. to install into an existing cluster. Use `-e seldon_mesh_namespace=<ns>` to change the default namespace seldon-mesh.

## Variables
Ecosystem: `seldon_mesh_namespace`, `seldon_kafka_namespace`, `full_install` (default yes), and per-component `install_kafka` (Strimzi), `install_prometheus`, `install_grafana`, `install_certmanager`, `install_jaeger`, `install_opentelemetry`, plus matching `configure_*` flags. For example `-e full_install=no -e install_kafka=yes` installs only Kafka.

Seldon: `seldon_crds_namespace` (default `default`), `install_crds`, `install_components`, `install_servers`.

## Custom images and private registries
Copy `playbooks/vars/set-custom-images.yaml` and pass it with `-e @file`. For private registries set `custom_image_pull_secrets.dockerconfigjson` (path to the auth file, usually the docker config.json written by `docker login`) and `custom_image_pull_secrets.name`. Log in with `-u _json_key` for JSON keys or `-u _json_key_base64` for base64 keys.

To save overrides as a Helm values file set `save_helm_components_overrides=yes`; the default file is `~/seldon_helm_comp_values.yaml`. With that file and a private registry, you must create the pull secret yourself under the same name.

## Uninstall
`kind delete cluster --name seldon`, and optionally remove the cache folder `~/.cache/seldon/`. On a non-Kind cluster you must remove components manually.

## Checked

2026-11-04. Confirmed against kubernetes-installation/ansible.md (Seldon Core 2 docs, v2 branch): dev/test warning, tested Python/library versions, variables and defaults, registry login, uninstall. Removed or corrected: nothing.

Method: documentation only; no commands were run.
