---
id: computing-software.cybersecurity-defensive.system-hardening.docker-bench-security
name: docker-bench-security
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [container-hardening, docker-bench, cis-docker-benchmark, docker-bench-security, compliance-scanning, host-audit]
level: practitioner
status: docs-checked
description: "Run docker-bench-security against Docker hosts, interpret WARN results by CIS section, decide fixes versus documented exceptions and track the score over time."
sources: ["https://github.com/docker/docker-bench-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker-bench-security

**Goal:** a repeatable CIS Docker Benchmark check of hosts, daemon config, images and running containers, with tracked remediation.

## Run
```
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security && sudo sh docker-bench-security.sh -l docker-bench.log
```
The tests are based on the CIS Docker Benchmark v1.6.0 and need Docker 1.13.0 or later. The repository README
documents a container form (`docker run --rm --net host --pid host --userns host --cap-add audit_control` plus
read-only host mounts and `--label docker_bench_security`); copy its exact mounts from the README.

Options: `-l FILE` log to FILE, `-c CHECK` run only the listed check ids or groups, `-e CHECK` exclude them,
`-i INCLUDE` only containers or images whose name matches a pattern, `-x EXCLUDE` exclude matching names, `-t LABEL`
filter by label, `-n LIMIT` cap items in JSON output, `-p` disable remediation text, `-b` no colours. Check ids look
like `check_2_2`; groups include `container_images` and `container_runtime`, e.g. `-c container_images -e check_4_5`.
By default it writes `docker-bench-security.log` and `docker-bench-security.log.json` in a `log` folder under the
current directory.

## Sections
Checks are numbered by CIS section (`check_<section>_<number>`; community additions are `check_c_<number>`). For example 2.2 is the daemon logging level and 4.5 is Docker content trust. Take section titles from the CIS Docker Benchmark.

## Triage
- Section 5 WARNs on running containers are usually the most valuable: `--privileged`, docker.sock mounts, host network/PID, writable root filesystem, no memory limit, running as root.
- Some checks are informational rather than failures, or not applicable (Swarm on non-swarm hosts).
- Fix in the source of truth (compose files, Helm charts, daemon.json via config management), not by hand on hosts.
- Record exceptions with reason and owner (e.g. a monitoring agent needing host PID).

## Track
Ship JSON to the SIEM or a dashboard; score per host per week; fail CI image builds on image-level findings using an image scanner.

## Gotchas
- Kubernetes nodes with containerd have no Docker daemon; use a Kubernetes benchmark tool instead.
- Running the bench itself needs privileged access (host PID, network and an added capability); run it from a trusted image or source.

## Verify
- [ ] Bench results stored for every Docker host with trend.
- [ ] No section 5 WARNs without a documented exception.

## Checked
2026-10-31. Confirmed against the docker-bench-security README: CIS Docker Benchmark v1.6.0 basis, Docker 1.13.0
minimum, option list (-b -l -c -e -i -x -t -n -p), check id naming, group names, default log file names, container
run flags. Removed unconfirmed: the `-c check_2,check_5` and `-i <name>` forms (corrected), log file names used
before, the per-section topic list, Trivy, Dockle and kube-bench names, INFO/NOTE result labels.
Method: documentation only; no commands were run.
