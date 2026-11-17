---
id: computing-software.systems-network-administration.dns-dhcp.tftp-server-and-blocksize-tuning
name: tftp-server-and-blocksize-tuning
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, tftpd, tftp-blocksize, tftp, network-boot, tftpd-hpa]
level: practitioner
status: verified
description: "Run a TFTP server for network boot (tftpd-hpa, dnsmasq), tune blksize and windowsize, fix permissions and path issues, and diagnose slow or failed transfers."
sources:
  - https://www.rfc-editor.org/rfc/rfc1350
  - https://www.rfc-editor.org/rfc/rfc2348
  - https://www.rfc-editor.org/rfc/rfc7440
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TFTP server and blksize

TFTP (UDP 69, then a random server port per transfer) still bootstraps PXE, phones and network devices.

## tftpd-hpa
`/etc/default/tftpd-hpa`:
```
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure --blocksize 1468 -v"
```
`--secure` changes the root directory on startup so clients request `pxelinux.0`, not `/srv/tftp/pxelinux.0` (the man page
recommends it for security and boot-ROM compatibility). `--blocksize` sets the maximum permitted block size, range 512 to
65464. Add `--create` only if devices upload configs (otherwise only existing, publicly writable files can be uploaded).
`-v` raises logging verbosity and can be repeated. Debian's package reads `/etc/default/tftpd-hpa` with exactly the
variables `TFTP_USERNAME`, `TFTP_DIRECTORY`, `TFTP_ADDRESS` and `TFTP_OPTIONS` (default address `:69`, directory
`/srv/tftp`).

dnsmasq: `enable-tftp`, `tftp-root=/srv/tftp`, `tftp-secure` (all in the dnsmasq man page; with `tftp-root` set, paths
containing `..` are rejected).

## Block size and window size
Default 512-byte blocks with one-ACK-per-block make a 30 MB kernel/WinPE transfer painfully slow over
any latency. Options:
- `blksize` (RFC 2348): valid values 8 to 65464 octets (data only, excluding the 4-byte TFTP header). 1468 is
  1500 - 20 (IP) - 8 (UDP) - 4 (TFTP header), so it fits a 1500 MTU; bigger blocks fragment and may be dropped by firewalls.
  Tested against a local tftpy 0.8.7 server with a raw UDP client: `blksize 1468` and `65464` were granted in an OACK
  (opcode 6) and the first DATA packet carried exactly that many bytes; without options the reply was DATA with 512.
- `windowsize` (RFC 7440): several blocks per ACK, fewer round trips on high-latency paths; both ends must support it,
  so confirm the OACK in a capture.
Better: chainload iPXE and fetch kernels over HTTP.

## Firewalls and NAT
The data transfer comes from a new server port (measured: requests to 6969 were answered from a different UDP port
for each transfer); stateful firewalls need a TFTP helper (Linux has the `nf_conntrack_tftp` module) or open ranges.
Through NAT, TFTP breaks without a helper.

## Troubleshooting
| Symptom | Cause |
|---------|-------|
| `File not found` | path mismatch (absolute vs chroot), case sensitivity, filename option 67 typo |
| `Permission denied` | file not world-readable (`chmod 644`; tftpd-hpa serves only publicly readable files unless `--permissive`), SELinux labelling |
| Transfer starts then times out | blksize too large / fragments dropped, firewall helper missing |
| Very slow | 512-byte blocks over latency |

```
tftp 10.0.0.20 -c get pxelinux.0     # test (tftp-hpa client); atftp --option "blksize 1468" --get -r file 10.0.0.20
```

## Verify
- [ ] A test client downloads the boot file with negotiated blksize (OACK seen in a capture) at expected speed.
