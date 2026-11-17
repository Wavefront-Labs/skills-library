---
id: computing-software.systems-network-administration.linux.laptop-power-management-tlp
name: laptop-power-management-tlp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tlp, laptop, power-management, battery-charge-thresholds, tlp-stat, power-profiles-daemon]
level: practitioner
status: docs-checked
description: "Configure TLP on Linux laptops: AC vs battery settings in /etc/tlp.conf, battery charge thresholds, USB denylists, tlp-stat checks and conflicts with power-profiles-daemon."
sources:
  - https://linrunner.de/tlp/
  - https://linrunner.de/tlp/settings/index.html
  - https://wiki.archlinux.org/title/TLP
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLP laptop power management

## Install
```bash
apt install tlp tlp-rdw  |  dnf install tlp tlp-rdw
systemctl mask power-profiles-daemon                    # conflicts with TLP (removing the package also works)
systemctl mask systemd-rfkill.service systemd-rfkill.socket   # only when using tlp-rdw
systemctl enable --now tlp
```
(Fedora also conflicts with `tuned`/`tuned-ppd`: follow the TLP Fedora install page, which removes them and, from Fedora 44, enforces the removal.)

## Configure (/etc/tlp.conf or /etc/tlp.d/*.conf)
```ini
TLP_DEFAULT_MODE=BAT                # TLP 1.8 and older; 1.9+ use profiles: TLP_DEFAULT_MODE=BAL (PRF, BAL or SAV) and TLP_PROFILE_AC/BAT (1.10+)
CPU_SCALING_GOVERNOR_ON_AC=performance
CPU_SCALING_GOVERNOR_ON_BAT=powersave
CPU_ENERGY_PERF_POLICY_ON_BAT=power
PLATFORM_PROFILE_ON_BAT=low-power
START_CHARGE_THRESH_BAT0=75        # ThinkPads and many others: keep battery 75-80% when docked
STOP_CHARGE_THRESH_BAT0=80
USB_AUTOSUSPEND=1
USB_DENYLIST="1111:2222"           # vendor:product IDs to exclude from autosuspend (input devices are excluded by default)
WIFI_PWR_ON_BAT=on
RUNTIME_PM_ON_BAT=auto
```
`tlp start` applies; `tlp ac` / `tlp bat` force a mode; `tlp fullcharge BAT0` one-time full charge before travel.

## Check
```bash
tlp-stat -s        # status, mode, conflicts
tlp-stat -b        # battery, thresholds support (natacpi / tpacpi-bat), health
tlp-stat -p        # CPU driver/governor
tlp-stat -w        # warnings
```

## Gotchas
- Charge thresholds depend on vendor support; `tlp-stat -b` tells you if they're writable.
- Desktop environments' power sliders (GNOME) need power-profiles-daemon; with TLP the slider disappears.
- Don't run powertop --auto-tune alongside TLP.

## Verify
- [ ] `tlp-stat -s` shows no conflicts; on battery `tlp-stat -p` shows powersave settings; thresholds respected.

## Checked

2026-10-28

Confirmed: TLP documentation (installation pages for Ubuntu and Fedora, settings for battery thresholds, USB, platform profile, processor, runtime PM, network; usage of tlp ac/bat/fullcharge and tlp-stat; FAQ on power-profiles-daemon and powertop) and the Arch wiki TLP page.

Removed or corrected: The claim that Fedora 41 ships tuned-ppd (the TLP Fedora page ties tuned/tuned-ppd conflicts to Fedora 43 and 44), the unconditional masking of rfkill units (needed only with tlp-rdw), and the specific Logitech USB ID in the denylist example.

Method: documentation only; no commands were run.
