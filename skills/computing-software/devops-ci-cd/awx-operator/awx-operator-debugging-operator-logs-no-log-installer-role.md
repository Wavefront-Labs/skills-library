---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-debugging-operator-logs-no-log-installer-role
name: awx-operator-debugging-operator-logs-no-log-installer-role
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, debugging, logs, no-log, installer-role, ansible-runner, molecule]
level: practitioner
status: docs-checked
description: "Debug failed AWX deployments from operator logs, no_log, resource inspection and by running the installer role locally."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/troubleshooting/debugging.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator debugging operator logs no log installer role

The operator runs the `installer` role inside its container. If the AWX CR status is `Failed`, read the manager logs:

```sh
kubectl logs deployments/awx-operator-controller-manager -c awx-manager -f
```

Inspect managed resources (awx, awxbackup, awxrestore, pod, deployment, pvc, service, ingress, route, secrets, serviceaccount) with `kubectl describe`, `kubectl get ... -o yaml`, `kubectl logs` and `kubectl exec -it`.

Show output of tasks hidden by `no_log`: set it false on the spec and failed task output appears in the operator logs:

```yaml
spec:
  service_type: nodeport
  no_log: false
```

Iterating on the installer without redeploying the operator:
1. Do the basic install, then `ansible-galaxy collection install -r molecule/requirements.yml` and `pip install -r molecule/requirements.txt`.
2. Scale the operator down so it does not overwrite your changes: `kubectl scale deployment awx-operator-controller-manager --replicas=0`.
3. Create `run.yml` with `hosts: localhost` and `roles: [installer]`.
4. Create `vars.yml` with `ansible_operator_meta` (name and namespace), `set_self_labels: false`, `update_status: false`, `service_type: nodeport`; the vars file replaces the AWX resource, so put overrides such as `image`, `image_version` and `image_pull_policy` there.
5. Run `ansible-playbook run.yml -e @vars.yml -v`.

## Checked

2026-11-09. Confirmed the log command, resource list, no_log setting and every step of the local installer iteration against the AWX Operator debugging page (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/troubleshooting/debugging.md
