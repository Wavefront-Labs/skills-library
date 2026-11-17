---
id: computing-software.cybersecurity-defensive.trivy.scan-rootfs-and-speed-up-traversal
name: scan-rootfs-and-speed-up-traversal
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-rootfs, rootfs, host-scan, pkg-types, skip-dirs, filesystem-traversal]
level: advanced
status: docs-checked
description: "Use trivy rootfs for host machines and unpacked filesystems, and avoid full traversal with --pkg-types os when only OS packages matter."
sources:
  - https://trivy.dev/latest/docs/guide/target/rootfs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`trivy rootfs /path/to/rootfs` is for special cases: a host machine, a root filesystem embedded in a Dockerfile, or an unpacked filesystem. The page stresses that rootfs scanning works differently from filesystem scanning, and that CI/CD scans of local projects should use `trivy fs`.

Red Hat limitation: vulnerability scanning of Red Hat systems has a known restriction around content manifests; see the Red Hat coverage page before relying on results.

Performance: by default Trivy walks every file under the root to find scan targets. If you only need files at known absolute locations, the walk can be avoided. Scanning only OS packages performs no full traversal:

```bash
trivy rootfs --pkg-types os --scanners vuln /
```

When scanning language-specific packages or secrets the traversal is unavoidable because Trivy cannot know where those files are. To keep the walk cheaper, exclude directories you do not need with `--skip-dirs` (documented on the file selection page).

## Checked

2026-11-03. Read and confirmed against the Rootfs page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
