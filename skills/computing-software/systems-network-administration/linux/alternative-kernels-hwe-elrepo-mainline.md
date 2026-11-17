---
id: computing-software.systems-network-administration.linux.alternative-kernels-hwe-elrepo-mainline
name: alternative-kernels-hwe-elrepo-mainline
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-upgrade, hwe-kernel, elrepo, mainline-kernel, kernel-ml, kernel-lt, ubuntu-hwe, uek, newer-hardware, lpic-2, sysadmin]
level: practitioner
status: gated
description: "Run a newer kernel than the distro default for new hardware or features: Ubuntu HWE, ELRepo kernel-lt/ml on RHEL clones, Ubuntu mainline builds, and the support trade-offs."
sources:
  - https://ubuntu.com/kernel/lifecycle
  - https://kernel.ubuntu.com/mainline/
  - https://elrepo.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Alternative kernels: HWE, ELRepo, mainline

**Goal:** get drivers/features from a newer kernel while staying as supportable as possible.
Order of preference: vendor-supported newer stream → reputable third-party repo → mainline
build (testing only).

## 1. Ubuntu HWE (supported)
The Ubuntu LTS enablement (HWE) stack provides a newer kernel and X11 support for an existing LTS release.
```bash
sudo apt-get install --install-recommends linux-generic-hwe-24.04   # Ubuntu's documented command for 24.04, desktop and server
hwe-support-status --verbose                                  # check whether the HWE stack is still supported
apt install linux-generic                                     # GA kernel meta-package (then remove the HWE meta-package)
```
Desktop installations of 24.04 default to tracking HWE; server installations default to the GA kernel and offer the enablement kernel as optional. The HWE stacks of 20.04 and 22.04 follow Ubuntu's Rolling Update Model (see the kernel release cycle page). Some desktop machines are on a separate OEM track: `ubuntu-drivers list-oem` non-empty means the machine runs the OEM cadence instead of HWE.

## 2. ELRepo kernels on RHEL/Alma/Rocky (community)
```bash
# follow the ELRepo installation instructions at elrepo.org for your release (release RPM and GPG key; verify the key fingerprint there) (gated: unconfirmed, source is paywalled or blocked)
dnf --enablerepo=elrepo-kernel install kernel-ml    # mainline-based kernel (gated: unconfirmed, source is paywalled or blocked)
dnf --enablerepo=elrepo-kernel install kernel-lt    # longterm kernel (gated: unconfirmed, source is paywalled or blocked)
grubby --default-kernel                              # shows the default boot kernel
```
ELRepo is a community repository, not part of the distribution vendor's supported kernel stream. Check whether your third-party kernel modules (vendor drivers, ZFS) are built for the kernel you install, since they may not load. (gated: unconfirmed, source is paywalled or blocked) The elrepo.org wiki answered automated requests with HTTP 429, so the repository commands and kernel descriptions above could not be checked.

## 3. Ubuntu mainline builds (test only)
Download the `linux-image-unsigned-*`, `linux-modules-*` and headers `.deb`s for one version from
kernel.ubuntu.com/mainline (the packages are named "unsigned") and `dpkg -i *.deb`. The mainline index carries the notices "ANY PRODUCTION USE DISCOURAGED AND AT OWN RISK" and "For debugging purposes only". With Secure Boot enabled, an unsigned kernel needs a signing key your firmware or shim trusts; DKMS modules may not build against it. Use it to bisect a regression or
confirm a fix landed upstream, then go back.

## 4. Decide
| Need | Choice |
|---|---|
| New laptop/server hardware on Ubuntu LTS | HWE |
| Newer driver on a RHEL clone | the vendor's newer minor release first; a third-party kernel only if that is not enough |
| Prove an upstream bug fix | mainline build, temporary |

## Gotchas
- Secure Boot: a third-party kernel must be signed with a key the firmware or shim trusts, or it will not boot.
- Keep the distro kernel installed as fallback; set the default deliberately with grubby/GRUB_DEFAULT.
- Vendor support contracts usually require the distro kernel for tickets.

## Verify
- [ ] `uname -r` shows the intended stream after reboot; `dmesg` has no taint warnings you didn't expect.
- [ ] The distro kernel still boots from the menu.
- [ ] Out-of-tree modules (`dkms status`) built for the new version.

## Checked
Checked 2026-10-27 against ubuntu.com/kernel/lifecycle, the kernel.ubuntu.com mainline index and the v6.17 build listing, and the Fedora grubby(8) man page.
- Ubuntu: `linux-generic-hwe-24.04` is the documented command for 24.04; desktop installs of 22.04 and 24.04 track HWE while servers default to GA; the 20.04 and 22.04 HWE stacks follow the Rolling Update Model; `hwe-support-status --verbose` and `ubuntu-drivers list-oem` are on the lifecycle page.
- Mainline: package names `linux-image-unsigned-*`, `linux-modules-*`, `linux-headers-*`; the index says production use is discouraged and the builds are for debugging only.
- grubby has `--default-kernel`.
- Not confirmed: ELRepo repository commands and kernel-ml/kernel-lt descriptions (elrepo.org returned HTTP 429), marked with the gated marker above. Removed unconfirmed claims: the six-month HWE cadence, `linux-oem-*`/`linux-lowlatency` support statement, RHEL kABI and Oracle UEK statements, vendor driver-disk advice.
Method: documentation only; no commands were run.
