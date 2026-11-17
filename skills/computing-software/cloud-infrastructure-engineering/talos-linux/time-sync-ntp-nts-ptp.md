---
id: computing-software.cloud-infrastructure-engineering.talos-linux.time-sync-ntp-nts-ptp
name: time-sync-ntp-nts-ptp
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [time-sync, ntp, nts, ptp, timesyncconfig, certificates, hypervisor]
level: practitioner
status: docs-checked
description: "Talos time sync: default Cloudflare NTP with NTS, TimeSyncConfig for NTS, PTP devices, disabling or bootTimeout, boot-clock caveats, and the get timestatus and timeservers checks."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/time-sync.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos does not require synchronised time, but certificates expire, so sync is recommended (Ceph also needs it). The API starts even when the clock is wrong and rotates its certificates after an NTP jump; `kubelet` and `etcd` wait for sync because they cannot rotate certificates gracefully. Default server is `time.cloudflare.com`, queried with NTS when no servers are configured anywhere; servers from DHCP, kernel args or platform metadata always use plain NTP.

Observe:

```shell
talosctl get timestatus
talosctl get timeservers
talosctl logs controller-runtime | grep -i time.Sync
```

Enable NTS for explicit servers (hostnames only; IPs are rejected; key exchange on TCP 4460, NTP on UDP 123; changing it needs no reboot):

```yaml
apiVersion: v1alpha1
kind: TimeSyncConfig
ntp:
  useNTS: true
  servers:
    - time.cloudflare.com
```

Boot clock: the NTS TLS handshake needs a valid clock. For the first few attempts before any sync Talos ignores only certificate validity dates (chain and hostname still checked) and logs a warning. Encrypted DNS validates strictly, so keep a plain DNS nameserver if the clock may be wrong at boot.

PTP on a hypervisor: check `talosctl ls /sys/class/ptp/`, then:

```yaml
apiVersion: v1alpha1
kind: TimeSyncConfig
ptp:
  devices:
    - /dev/ptp0
```

Disable with `enabled: false` (Talos assumes time is in sync), or best-effort with `bootTimeout: 2m`.

## Checked

Default server, NTS rules (hostnames only, ports 4460 and 123, no reboot), boot-clock fallback, encrypted DNS caveat, PTP configuration and the disable and bootTimeout documents confirmed on the page.

Method: docs-checked 2026-11-09 against the raw Time Synchronization page (v1.15 folder), read in full.
