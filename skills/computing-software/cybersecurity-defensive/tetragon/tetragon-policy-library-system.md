---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-library-system
name: tetragon-policy-library-system
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [policylib-system, tetragon, fileless-execution, ebpf-audit, kernel-modules]
level: practitioner
status: docs-checked
description: "Audit fileless execution, BPF activity, kernel modules, library loads and outbound connections with Tetragon policy library entries."
sources:
  - "https://tetragon.io/docs/policy-library/observability/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/policylibrary/bpf.yaml"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/policylibrary/modules.yaml"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/policylibrary/library.yaml"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/policylibrary/egress.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon policy library: system and network activity

Goal: audit stealthy execution and system-level activity. Each entry pairs a TracingPolicy (or none) with a jq filter on the event stream.

## Fileless and deleted binaries (no policy)
Standard `process_exec` observability is enough, with Process Credentials visibility enabled. Both example jq filters select `process_exec` events where `binary_properties.file` is set. Evidence: a binary like `/proc/self/fd/3` whose `binary_properties` inode shows zero `links`. Fileless runs use `memfd_create()` or shared memory.

## Policies in examples/policylibrary
- `bpf.yaml` (`bpf-library-policy`): hooks `bpf_check` (arg type `bpf_attr`), `security_perf_event_alloc`, `security_bpf_map_alloc` (before Linux 6.9) and `security_bpf_map_create` (6.9+) both with `ignore: callNotFound: true`, plus `security_file_permission` and `security_mmap_file` with `Prefix` `/sys/fs/bpf` matches. Filter `function_name | test("bpf_check")` and print `bpf_attr_arg.ProgType`.
- `modules.yaml` (`monitor-kernel-modules`): hooks `security_kernel_module_request` (string arg, automatic loads) and `security_kernel_read_file` with `matchArgs` index 1 Equal "2" (READING_MODULE, explicit loads). Filter on `security_kernel_module_request` and print `args[0].string_arg`.
- `library.yaml` (`loader`): `spec.loader: true` with option `disable-kprobe-multi` value "1". Events are `process_loader`; filter prints `.process_loader.path`.
- `egress.yaml`: hooks `tcp_connect` with arg type `sock` and `matchArgs` operator `NotDAddr` over `127.0.0.1`, `${PODCIDR}` and `${SERVICECIDR}`. Set `PODCIDR=$(kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}')`; find SERVICECIDR per platform (GKE via `gcloud container clusters describe`, Kind via kube-apiserver `--service-cluster-ip-range`). Filter `function_name | test("tcp_connect")` and print `sock_arg` saddr/sport -> daddr/dport.

Egress auditing surfaces unexpected or malicious reverse shells.

## Checked

2026-11-08. Read in full: the Tetragon observability policy library page (raw markdown `docs/content/en/docs/policy-library/observability/_index.md`) and the `bpf.yaml`, `modules.yaml`, `library.yaml` and `egress.yaml` policies. Confirmed hooks, selectors, options, jq filters, the Linux 6.9 `security_bpf_map_create` rename and the SERVICECIDR lookups. The page's `sshd.yaml` entry is not covered by this skill.

Method: documentation only; no commands were run.
