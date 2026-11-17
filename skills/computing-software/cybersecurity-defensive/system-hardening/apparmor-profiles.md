---
id: computing-software.cybersecurity-defensive.system-hardening.apparmor-profiles
name: apparmor-profiles
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, apparmor, mac, aa-genprof, complain-mode, enforce-mode, ubuntu-hardening]
level: advanced
status: docs-checked
description: "Confine services with AppArmor on Ubuntu and Debian: check status, generate and tune profiles in complain mode, enforce them and debug DENIED log entries."
sources: ["https://github.com/canonical/ubuntu-server-documentation/blob/main/docs/how-to/security/apparmor.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/apparmor.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tutorials/security/apparmor.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppArmor profiles

**Goal:** network-facing and high-risk processes run under enforced AppArmor profiles that allow only what they need.

## Status
- `aa-status` shows AppArmor state and loaded profiles (Ubuntu installs and loads AppArmor by default).
- Profiles and abstractions live in `/etc/apparmor.d/`; for packages that support it, local rules go in `/etc/apparmor.d/local/` (local includes) so a package upgrade does not trigger a conffile prompt.
- Package `apparmor-profiles` ships additional profiles; `apparmor-profiles-extra` carries experimental ones that are not expected to work out of the box; `apparmor-utils` provides the command-line tools.

## Build a profile
1. `aa-genprof /usr/local/bin/myapp` (interactive): exercise the app, then answer prompts (allow/deny, glob paths).
2. Or put an existing profile in complain mode with `aa-complain /etc/apparmor.d/usr.local.bin.myapp`, run the app through real workloads, then run `aa-logprof` to scan the logs for AppArmor audit messages and update the profile.
3. Review the resulting rules; prefer specific paths and shared abstractions (`#include <abstractions/base>`, `nameservice`).
4. Enforce: `aa-enforce /etc/apparmor.d/usr.local.bin.myapp`; reload after edits with `apparmor_parser -r <file>`.

## Example rules
```
/usr/local/bin/myapp {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  capability net_bind_service,
  /etc/myapp/** r,
  /var/lib/myapp/** rw,
  deny /etc/shadow r,
}
```

## Debug
Denials appear in `dmesg` (and any log that collects kernel messages) as `apparmor="DENIED"` entries with fields such as `operation=`, `profile=`, `name=` and `requested_mask=`. Explicit `deny` rules write nothing to the logs, so a silent failure can still be a deny rule.

## Containers
Docker applies `docker-default`; custom per container `--security-opt apparmor=myprofile`; Kubernetes sets `securityContext.appArmorProfile` (`type`: `RuntimeDefault`, `Localhost` or `Unconfined`, plus `localhostProfile`); the field exists from Kubernetes 1.30 and the AppArmor feature is GA from 1.31.

## Verify
- [ ] Internet-facing services appear as enforce in `aa-status`.
- [ ] No DENIED events during a full functional test after enforcing.

## Checked
Checked 2026-10-25 against the Ubuntu Server documentation (canonical/ubuntu-server-documentation, last commit 2026-10-16), the Docker Engine AppArmor page (docker/docs, 2026-10-23) and the Kubernetes AppArmor tutorial, security-context task and AppArmor feature-gate file (kubernetes/website, 2026-10-24). Confirmed: aa-status, aa-genprof, aa-complain, aa-enforce, aa-logprof, apparmor_parser -r, /etc/apparmor.d/local/, package names, DENIED log format and fields, explicit deny rules not logged, docker-default and `--security-opt apparmor=`, Kubernetes `appArmorProfile` field and its GA version. Removed unconfirmed aa-autodep, owner and network-rule details, journalctl and auditd log locations.

Method: documentation only; no commands were run.
