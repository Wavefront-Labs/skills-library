---
id: computing-software.cloud-infrastructure-engineering.docker.docker-bench-and-cis-benchmark-remediation
name: docker-bench-and-cis-benchmark-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-bench, cis-docker, cis-benchmark, hardening, bench-run, docker-bench-output, cis-host-configuration, auditd-docker-rules, cis-daemon-configuration, cis-container-runtime, cis-images, bench-exceptions]
level: advanced
description: "Run docker-bench-security, read its WARN/INFO/PASS output by CIS section (host, daemon, files, images, runtime), fix the common findings and track justified exceptions."
sources: ["https://github.com/docker/docker-bench-security", "https://www.cisecurity.org/benchmark/docker", "https://docs.docker.com/engine/security/", "https://docs.docker.com/reference/cli/dockerd/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Bench and CIS Docker Benchmark remediation

## Run it
```sh
git clone https://github.com/docker/docker-bench-security.git && cd docker-bench-security
sudo sh docker-bench-security.sh -l /var/log/docker-bench.log
sudo sh docker-bench-security.sh -c container_images,container_runtime   # only some groups
sudo sh docker-bench-security.sh -e check_2_2 -i ci-                      # exclude a check; include containers whose names match
```
Options from the README: `-l FILE` log file, `-c` run only the listed checks or groups,
`-e` exclude checks or groups, `-i` / `-x` include or exclude containers and images by name
pattern, `-t` by label, `-u` trusted users, `-p` suppress remediation text. By default it runs
all CIS tests and writes `docker-bench-security.log` and `docker-bench-security.log.json` to
the log folder in the current directory (inside the container, `/usr/local/bin/log/`). CIS-based
checks are named `check_<section>_<number>`; community checks `check_c_<number>`. The README says
the prebuilt `docker/docker-bench-security` image is out of date and a manual build is required,
and that the containerised run uses heavy privileges (host filesystem, PID and network).

The check numbering and exact wording belong to the CIS Docker Benchmark; read the current
benchmark for the authoritative text (the README cites two examples: 2.2 logging level `info`
and 4.5 content trust). Groups of checks, with the fixes that map to documented settings:

**Host configuration**: a separate partition for the Docker data root, audit rules for Docker
files and binaries (the README notes the audit checks fall back to `/etc/audit/audit.rules`
when `auditctl` is missing), and only trusted users in the `docker` group.

**Daemon configuration** (`daemon.json`, all keys exist in the dockerd reference): `icc`,
`live-restore`, `userland-proxy`, `no-new-privileges`, a `log-driver` with rotation options
such as `max-size`, `userns-remap`, `insecure-registries` empty, TLS on any TCP socket,
`authorization-plugins` where required.

**Daemon files**: ownership and permissions of the service and socket units, `/etc/docker`,
certificates and `daemon.json` (see the benchmark for the expected modes).

**Images and build files**: a non-root `USER`, trusted base images, HEALTHCHECK, no secrets in
Dockerfiles, content trust.

**Container runtime**: no `--privileged`, dropped capabilities, no sensitive host mounts,
read-only root filesystem, memory, CPU and PID limits, no host network, PID or IPC sharing,
`no-new-privileges`, no docker.sock mounts, seccomp and AppArmor not unconfined.

## Exceptions
Not every warning applies (for example privileged mode for a CI Docker-in-Docker runner). Track each as:
check ID, host/container scope, justification, compensating control, owner, review date.
Feed `-e` exclusions from that register so the bench report stays meaningful, and re-review
quarterly. Version the register with the host config code.

## Verify
Rerun after fixes and compare the JSON logs between runs to catch regressions.

## Checked
Date: 2026-10-26. Documentation: docker/docker-bench-security README (last commit 2026-06-04); docker/docs dockerd reference for the daemon.json keys. Confirmed: options `-l -c -e -i -x -t -u -p`, group names, default log files and in-container path, check naming, out-of-date image note, privilege note, auditctl fallback, the listed daemon.json keys. Removed as unconfirmed (the CIS Docker Benchmark text sits behind a registration form and was not read): check numbers, the auditd rule block, `[PASS]/[WARN]/[INFO]` and score description, file mode values, `on-failure:5`, setuid advice.
Method: documentation only; no commands were run.
