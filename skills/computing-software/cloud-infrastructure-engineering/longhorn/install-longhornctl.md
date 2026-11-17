---
id: computing-software.cloud-infrastructure-engineering.longhorn.install-longhornctl
name: install-longhornctl
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [longhornctl, cli, install, checksum, binary]
level: intro
status: docs-checked
description: "Download, verify and install the longhornctl v1.13.0 binary for amd64 or arm64 and confirm it with longhornctl version."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/longhornctl/install-longhornctl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install the Longhorn CLI, used for example to check nodes before installing Longhorn.

1. Download the binary (`amd64` or `arm64`):

```bash
ARCH="amd64"
curl -LO "https://github.com/longhorn/cli/releases/download/v1.13.0/longhornctl-linux-${ARCH}"
```

2. Validate the checksum:

```bash
curl -LO "https://github.com/longhorn/cli/releases/download/v1.13.0/longhornctl-linux-${ARCH}.sha256"
echo "$(cat longhornctl-linux-${ARCH}.sha256 | awk '{print $1}') longhornctl-linux-${ARCH}" | sha256sum --check
```

3. Install:

```bash
sudo install longhornctl-linux-${ARCH} /usr/local/bin/longhornctl
```

4. Verify:

```bash
longhornctl version
```

Building from source is described in the build section of the longhorn/cli GitHub README at tag 1.13.0.

The page does not list other subcommands or flags. The Helm and kubectl install guides mention using `longhornctl` optionally to check the environment for potential issues.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/longhornctl/install-longhornctl/

No claim needed changing.

Method: documentation only; no commands were run.
