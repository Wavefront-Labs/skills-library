---
id: computing-software.data-engineering.apache-hadoop.yarn-docker-containers
name: yarn-docker-containers
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, docker, container-executor, linuxcontainerexecutor]
level: advanced
status: docs-checked
description: "Running YARN containers in Docker: LinuxContainerExecutor and allowed-runtimes, container-executor.cfg [docker] keys, YARN_CONTAINER_RUNTIME_* variables and host prerequisites."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/DockerContainers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YARN on Docker

The page opens with a security warning: Docker integrates with powerful kernel features, so admins must understand Docker security before enabling this.

Host prerequisites: `container-executor` owned root:hadoop with 6050 permissions; Docker daemon and client on every NodeManager that will run Docker containers; large images pre-pulled (for example `docker pull library/openjdk:8`) to avoid job start timeouts, since MapReduce and Spark treat tasks silent for more than 10 minutes as stalled. Confirm the LCE works for ordinary containers first; if NodeManagers fail to start, suspect binary ownership or permissions.

yarn-site.xml:
- `yarn.nodemanager.container-executor.class` = `org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor`
- `yarn.nodemanager.linux-container-executor.group` must match container-executor.cfg
- `yarn.nodemanager.runtime.linux.allowed-runtimes` = `default,docker` (allowed values default, docker, javasandbox)
- `...docker.allowed-container-networks` (default `host,none,bridge`) and `...docker.default-container-network` (default `host`, must be in the allowed set)
- Other optional keys: `...docker.privileged-containers.allowed` (false), `...privileged-containers.acl`, `...host-pid-namespace.allowed` (false), `...delayed-removal.allowed` (false), `...stop.grace-period` (10), `...image-update` (false), `...capabilities`, user-remapping keys.

container-executor.cfg (owned by root, mode 0400, Java properties format; the group key plus a `[docker]` section):
- `module.enabled` must be true to launch Docker containers
- `docker.binary` (default /usr/bin/docker)
- `docker.allowed.capabilities`, `.devices`, `.networks`, `.volume-drivers`, `.runtimes` (by default nothing allowed)
- `docker.allowed.ro-mounts`, `docker.allowed.rw-mounts`: nothing allowed by default; YARN local directories must be listed in rw-mounts if containers need them; containers may not mount a parent of the cfg directory read-write
- `docker.privileged-containers.enabled` (default false), `docker.privileged-containers.registries`, `docker.trusted.registries`, `docker.host-pid-namespace.enabled`, `docker.no-new-privileges.enabled`, `docker.inspect.max.retries` (10, 3 s apart)
- Optional general keys `min.user.id`, `banned.users` (default yarn, mapred, hdfs, bin), `allowed.system.users`; a user in both banned and allowed is banned.

Privileged containers: allowed only with an ENTRYPOINT-enabled image and `docker.privileged-containers.enabled`; the privileged registries list falls back to `docker.trusted.registries` if unset; `library` trusts official Docker Hub images. Privileged containers do not set uid:gid and honour the image USER entry.

Per-application environment variables (the first two are required):
- `YARN_CONTAINER_RUNTIME_TYPE=docker`
- `YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=<image>`
- Optional: `..._RUN_OVERRIDE_DISABLE`, `..._CONTAINER_NETWORK`, `..._PORTS_MAPPING`, `..._CONTAINER_PID_NAMESPACE`, `..._RUN_PRIVILEGED_CONTAINER` (leave unset rather than false), `..._MOUNTS`, `..._TMPFS_MOUNTS`, `..._DELAYED_REMOVAL`, `..._SERVICE_MODE`, `..._CLIENT_CONFIG`.
- `YARN_CONTAINER_RUNTIME_DOCKER_MOUNTS` is `source:dest[:ro|rw]` comma-separated (rw if unset; bind propagation options allowed); the source must equal or sit under a whitelisted directory. Example: admin whitelists `/sys/fs/cgroup` read-only, user requests `/sys/fs/cgroup:/sys/fs/cgroup:ro`.

Image requirements: the application owner must exist in the image, matched by UID (YARN runs `docker run --user uid:gid`, e.g. nobody as 99:99 on CentOS in non-secure mode); for Hadoop jobs the image needs a JRE and Hadoop libraries with JAVA_HOME, HADOOP_COMMON_PATH, HADOOP_HDFS_HOME, HADOOP_MAPRED_HOME, HADOOP_YARN_HOME and HADOOP_CONF_DIR set, with versions compatible with the cluster. Without an ENTRYPOINT, `/bin/bash` and `find` must exist in the image.

Cgroups: only the Docker `cgroupfs` driver is supported; with `systemd` launch fails (the page shows the exit code 7 error) and the daemon's `native.cgroupdriver` must be changed.

User management options listed: static uid/gid in the image (non-secure testing only), bind-mounting /etc/passwd and /etc/group read-only (testing only), or SSSD.

## Checked

Method: 2026-11-08, read the project's DockerContainers markdown source through the privileged-container and image-requirement sections; later sections (services, registry setup) were scanned by search only and are not covered here. Removed an unsupported "Verify" step; the earlier text had no errors in the keys it listed; added defaults, privileged-container rules and user-management options. Other items were unchanged.
