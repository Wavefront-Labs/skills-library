---
id: computing-software.cloud-infrastructure-engineering.ansible.job-template-instance-and-container-group-assignment
name: job-template-instance-and-container-group-assignment
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, job-templates, jt-instance-group, container-group-jt, instance-groups, container-groups, pod-spec, network-zones]
level: advanced
status: docs-checked
description: "Route a job template's jobs to the right instance group or container group: precedence between template, inventory and organization, prompt on launch, and custom pod specs."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job template instance and container group assignment

Goal: jobs for the DMZ run on DMZ execution nodes, bursty jobs run as pods in OpenShift/Kubernetes,
and nothing lands on a node that cannot reach its targets.

## Precedence
The controller uses the first non-empty list, in this order:
1. **Job template** instance groups (or the groups given at launch if "prompt on launch")
2. **Inventory** instance groups
3. **Organization** instance groups
4. `default` group (if the above are all empty)
Within a list, order matters: the first group with capacity gets the job; later groups are
fallbacks. The job template option "Prevent instance group fallback" stops falling through to the
inventory/org lists (inventories have the same option).

## Pin a template
```yaml
controller_templates:          # infra.aap_configuration controller_job_templates role input
  - name: Patch DMZ web
    inventory: DMZ
    project: linux-ops
    playbook: patch.yml
    instance_groups: [dmz-exec, dmz-exec-dr]     # ordered: primary then fallback
    prevent_instance_group_fallback: true
```

## Container groups
A container group runs each job as a pod in a Kubernetes namespace using a credential
(OpenShift/Kubernetes API bearer token). Customise the pod (check "Customize pod spec" and edit
the Pod spec override):
```yaml
controller_instance_groups:     # infra.aap_configuration role input
  - name: k8s-burst
    is_container_group: true
    credential: k8s-automation-sa
    pod_spec_override: |
      apiVersion: v1
      kind: Pod
      metadata: {namespace: aap-jobs}
      spec:
        serviceAccountName: default
        automountServiceAccountToken: false
        nodeSelector: {workload: automation}
        containers:
          - image: hub.example.com/ee/ee-supported:2.4
            name: worker
            args: [ansible-runner, worker, --private-data-dir=/runner]
            resources:
              requests: {cpu: 500m, memory: 1Gi}
              limits: {memory: 2Gi}
```
The job's EE replaces the container image at runtime; keep `args` exactly as the default spec.

## Choosing
| Need | Use |
|---|---|
| Reach an isolated network segment | Execution nodes in that segment (instance group) |
| Elastic burst, cloud targets, no persistent state | Container group |
| Job needs local files on the node, or long-running | Instance group |

## Gotchas
- Templates prompting for instance groups use the Prompt on Launch field; launch payloads reference
  the groups by ID in the API.
- Container groups have no isolated job capacity accounting; use the `max_concurrent_jobs` and
  `max_forks` settings on instance groups to limit how many jobs and forks can be consumed.
- A job queued forever with "waiting" status usually means every group in its effective list is at capacity or offline; check Instance Groups → capacity.

## Verify
- [ ] Job details → "Instance Group" and "Execution Node" show the expected group/node.
- [ ] Disabling the primary group's nodes makes the next job use the fallback (or stay pending if fallback prevented).

## Checked

- 2026-10-31: instance-group precedence (job template → inventory → organization by way of project,
  default-group fallback), the "Prevent instance group fallback" job template and inventory options,
  the Instance groups field with Prompt on Launch, container groups with the Customize pod spec
  override, and `max_concurrent_jobs`/`max_forks` capacity settings confirmed in AAP 2.5 Using
  automation execution and Configuring automation execution. `controller_job_templates` and
  `controller_instance_groups` role names confirmed in the redhat-cop roles listing.
- Removed: the `ansible.controller.job_template`/`instance_group` module examples (replaced with the
  confirmed role inputs) and the IDs-not-names launch payload detail.
Method: documentation only; no commands were run.
