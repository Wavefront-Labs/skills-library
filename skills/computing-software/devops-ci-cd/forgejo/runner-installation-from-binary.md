---
id: computing-software.devops-ci-cd.forgejo.runner-installation-from-binary
name: runner-installation-from-binary
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [forgejo-runner-install, gpg-verify, runner-user, generate-config]
level: practitioner
status: docs-checked
description: "Download and verify the forgejo-runner binary, create a runner user and generate a config file."
sources:
  - https://forgejo.org/docs/latest/admin/actions/installation/binary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Git, tested from version 2.24.3.

Steps from the docs:

1. Find the latest version from `https://data.forgejo.org/api/v1/repos/forgejo/runner/releases/latest` and download `forgejo-runner-<version>-linux-<arch>` from `code.forgejo.org/forgejo/runner/releases/download/...`, plus the matching `.asc` file.
2. Verify the signature with `gpg --verify forgejo-runner.asc forgejo-runner` after fetching key `EB114F5E6C0DC2BCDD183550A4B61A2DC5923710` from `hkps://keys.openpgp.org`. Expect a good signature from "Forgejo <contact@forgejo.org>", aka "Forgejo Releases <release@forgejo.org>".
3. `chmod +x`, then copy to `/usr/local/bin/forgejo-runner`; test with `forgejo-runner -v`.
4. Create the daemon user: `useradd --create-home runner`. For Docker, add it to the docker group with `usermod -aG docker runner`; Podman needs no particular permissions, but the system must be configured to run the Podman service (see the runner-podman-socket-setup skill).
5. As that user, generate the config: `forgejo-runner generate-config > /path/to/runner-home/runner-config.yml`.

The runner relies on application containers (Docker, Podman) or system containers (LXC) to isolate workflows. Using Docker inside workflows (for example `docker build`) is a separate, optional configuration described in the Docker access page.

The runner needs Git installed and was tested with a minimum of Git 2.24.3. After copying the binary to /usr/local/bin, running forgejo-runner -v confirms the version. The container environment (Docker, Podman or LXC) is installed and configured independently of the runner.

## Checked

Date: 2026-11-07
Confirmed against the "Installation from binary" page, read in full including its code blocks and the latest-release JSON endpoint it uses (the release API returns a `name` field and linux amd64/arm64 assets with matching `.asc` files): the Git 2.24.3 requirement, the download URL layout and `.asc` file, the key id and `hkps://keys.openpgp.org` keyserver, `gpg --verify`, `chmod +x`, copying to `/usr/local/bin/forgejo-runner`, `forgejo-runner -v`, `useradd --create-home runner`, `usermod -aG docker runner`, the Podman note, `forgejo-runner generate-config`, and the Docker-in-workflows note.
Corrected: the expected gpg signer was only "Forgejo Releases"; the page shows "Forgejo <contact@forgejo.org>" aka "Forgejo Releases <release@forgejo.org>". The Podman line now says the Podman service still has to be configured.
Method: documentation only; no commands were run.
