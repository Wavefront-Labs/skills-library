---
id: computing-software.messaging-and-integration.dapr.self-hosted-airgap-install-bundle
name: self-hosted-airgap-install-bundle
category: computing-software
field: messaging-and-integration
product: dapr
tags: [self-hosted, airgap, offline, installer-bundle, dapr-init, from-dir, slim]
level: practitioner
status: docs-checked
description: "Initialise Dapr offline from a Dapr Installer Bundle with dapr init --from-dir, with or without Docker via --slim, and the Redis and Zipkin containers to run manually for parity."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/self-hosted/self-hosted-airgap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Normal `dapr init` downloads binaries and pulls images. For offline hosts, download a Dapr Installer Bundle first from the dapr/installer-bundle releases (for example `daprbundle_linux_amd64.tar.gz` or `daprbundle_windows_amd64.zip`); it packages the CLI, runtime and dashboard, so no binaries or Docker images are fetched during init.

Setup: unpack the bundle, copy the `dapr` binary (`dapr.exe` on Windows) somewhere on the path (`/usr/local/bin` on Linux/macOS; on Windows create a directory and add it to the system PATH), or just use the CLI inside the bundle.

With Docker available, run from the bundle directory:

```bash
dapr init --from-dir .
```

From another directory pass the full bundle path. Linux users who run Docker with sudo must use `sudo dapr init`. The output ends with the `daprd` binary installed and the `dapr_placement` container running.

Without Docker, add `--slim` so only the binaries are installed and no default config files or containers are created:

```bash
dapr init --slim --from-dir .
```

The output reports the `daprd` and `placement` binaries installed.

To emulate the online default environment, start the two containers yourself:

```
docker run --name "dapr_zipkin" --restart always -d -p 9411:9411 openzipkin/zipkin
docker run --name "dapr_redis" --restart always -d -p 6379:6379 redislabs/rejson
```

## Checked

2026-11-08. Installer Bundle download, setup, dapr init --from-dir with and without --slim, the sudo note, expected output and the two docker run commands confirmed on the offline or airgap page. Changed: removed a remark about Redis and Zipkin images in an offline registry, which the page does not state.

Method: documentation only; every cited page read in full; no commands were run.
