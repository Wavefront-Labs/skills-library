---
id: computing-software.systems-network-administration.linux.linux-ima-evm-integrity-measurement
name: linux-ima-evm-integrity-measurement
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ima, evm, integrity-measurement, ima-appraisal, remote-attestation, keylime]
level: practitioner
status: docs-checked
description: "Use Linux IMA and EVM: enable measurement and appraisal policies, read the IMA log, sign files with evmctl, tie measurements to the TPM for attestation, and avoid boot lockouts."
sources:
  - https://www.kernel.org/doc/html/latest/security/IMA-templates.html
  - https://ima-doc.readthedocs.io/en/latest/
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_monitoring_and_updating_the_kernel/enhancing-security-with-the-kernel-integrity-subsystem_managing-monitoring-and-updating-the-kernel
  - https://keylime.dev/
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/ima_policy
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/evm
  - https://github.com/systemd/systemd/blob/main/src/core/ima-setup.c
  - https://github.com/linux-integrity/ima-evm-utils
  - https://github.com/keylime/keylime/blob/master/keylime/cmd/create_policy.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Integrity Measurement Architecture (IMA/EVM)

- **IMA measurement**: hash files as they are executed/opened and record them in a log, extending a TPM PCR (a policy rule's `pcr=` option selects it).
- **IMA appraisal**: refuse to execute/open files whose hash or signature (in `security.ima` xattr) is wrong.
- **EVM**: protects the security xattrs themselves (HMAC or signature over `security.ima`, `security.selinux`, mode, owner).

## Turn on measurement
Kernel command line:
```
ima_policy=tcb ima_hash=sha256
```
`ima_policy=` accepts the built-in policies `tcb`, `appraise_tcb`, `secure_boot`, `fail_securely` and `critical_data`; `tcb` measures programs executed, files mmapped for exec and files opened for read by root. `ima_hash=` defaults to sha1.
```bash
cat /sys/kernel/security/ima/policy                       # active rules
head /sys/kernel/security/ima/ascii_runtime_measurements  # PCR, template hash, template, file hash, path
wc -l /sys/kernel/security/ima/ascii_runtime_measurements
```
Custom policy: write rules to `/etc/ima/ima-policy` (systemd loads this file at boot if IMA is available) e.g.
```
measure func=BPRM_CHECK mask=MAY_EXEC
measure func=MMAP_CHECK mask=MAY_EXEC
measure func=MODULE_CHECK
```
Valid `func=` values include `BPRM_CHECK`, `MMAP_CHECK`, `CREDS_CHECK`, `FILE_CHECK` and `MODULE_CHECK`; see the `ima_policy` ABI documentation for the full grammar.

## Appraisal (enforcement)
1. Label first in fix mode: boot with `ima_appraise=fix ima_policy=appraise_tcb` (`appraise_tcb` appraises all files owned by root), then access the files so their hashes are written.
2. Or sign: `evmctl ima_sign --key /etc/keys/privkey_ima.pem /usr/local/bin/app` (see evmctl for the keyring the public certificate must be in).
3. Switch to `ima_appraise=enforce`. `ima_appraise=` takes `off`, `enforce`, `fix` or `log`.
Test on a VM with console access: a file missing its xattr becomes un-executable, and appraising `/sbin/init` wrong means an unbootable system. Keep `ima_appraise=fix` boot entry as fallback.

## EVM
`evmctl` (ima-evm-utils) creates and verifies IMA/EVM signatures. EVM is controlled through `/sys/kernel/security/evm`; see the EVM ABI documentation for the bit values to write after loading keys.

## Attestation
The IMA log plus a TPM quote of the PCR it extends lets a remote verifier check that the log wasn't altered and that only allowlisted files ran. Keylime implements this with runtime policies; `keylime_create_policy` builds one from an IMA measurement list (`-m`/`--ima-measurement-list`, default `/sys/kernel/security/ima/ascii_runtime_measurements`) and writes it with `-o`:
```bash
keylime_create_policy -m /sys/kernel/security/ima/ascii_runtime_measurements -o policy.json
```

## Pitfalls
- Log grows with every unique file: policies measuring all reads fill memory on busy hosts.
- Files on filesystems without xattr support can't carry `security.ima`; exclude such filesystems with `fsmagic=` in the policy.
- Updating files without refreshing their IMA signature or hash breaks enforcement.

## Verify
- [ ] Measurement log contains entries for executed binaries; the PCR matches a replay of the log.
- [ ] In enforce mode, executing a modified copy of a binary is denied.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (kernel-parameters `ima_policy=`, `ima_appraise=`, `ima_hash=`; ABI testing `ima_policy` and `evm`), the systemd `ima-setup.c` source, ima-evm-utils `evmctl.c` and the Keylime `create_policy.py` source on 2026-10-26. Confirmed: built-in policy names, tcb and appraise_tcb scopes, `ima_appraise` values, `ima_hash` default sha1, `/etc/ima/ima-policy` loaded by systemd, `/sys/kernel/security/ima/policy`, `evmctl ima_sign --key`, `/sys/kernel/security/evm`, `keylime_create_policy -m/-o`. Bug fixed: the policy rule `func=FILE_MMAP` is not a valid function name; the documented value is `MMAP_CHECK`. Removed: PCR 10 as a fixed value, RHEL rpm-plugin, `.ima` keyring and dracut claims, the audit record name and the find one-liner.

Method: documentation only; no commands were run.
