---
id: computing-software.cybersecurity-defensive.endpoint-security.ima-evm-linux
name: ima-evm-linux
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [ima-evm, linux-ima, integrity-measurement-architecture, evm, file-signature-appraisal, tpm-attestation, application-control]
level: sme
status: docs-checked
description: "Use Linux IMA and EVM: measurement and appraisal policies, signing files with evmctl, TPM-backed measurement logs, keyrings, and labelling in fix mode before enforcing."
sources: ["https://www.kernel.org/doc/html/latest/security/IMA-templates.html", "https://sourceforge.net/p/linux-ima/wiki/Home/", "https://github.com/linux-integrity/ima-evm-utils", "https://keylime.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IMA and EVM on Linux

- **IMA (Integrity Measurement Architecture)**: keeps a runtime measurement list of files per policy; if a TPM exists, the aggregate is extended into a PCR (default PCR 10, `CONFIG_IMA_MEASURE_PCR_IDX`) so tampering with the list is detectable. IMA-appraisal validates a file against its `security.ima` attribute locally; IMA-audit logs hashes to the audit log. Measurement, appraisal and audit can be used independently.
- **EVM (Extended Verification Module)**: detects offline tampering with security xattrs (`security.selinux`, `security.SMACK64`, `security.ima`, `security.capability`) using an HMAC-SHA1 in `security.evm` or a digital signature.
- Both complement LSM mandatory access control (SELinux, Smack). EVM and IMA-measurement work without a TPM, but without hardware-backed detection.

## Measurement (detect) first
- Boot parameters: `ima_policy=` (`tcb`, `appraise_tcb`, `secure-boot`; no default since Linux 4.13), `ima_template=` (default `ima-ng` since 3.13), `ima_hash=` (default sha256 since 3.13), `ima_audit=1` for extra messages. Fedora/RHEL may also need `ima=on`.
- Read the list as root from `/sys/kernel/security/ima/ascii_runtime_measurements` (securityfs must be mounted). The first entry, `boot_aggregate`, is a SHA1 over TPM PCRs 0-7 (zeroes with no TPM).
- Custom policy is loaded via `/sys/kernel/security/ima/policy`; the wiki says systemd reads `/etc/ima/ima-policy` and dracut `/etc/sysconfig/ima-policy`. If rules use LSM labels, load the LSM policy first. The default policy skips pseudo filesystems.
- Mount filesystems with `iversion` (or `rootflags=i_version`) or files are re-measured on every access.
- Templates: `ima-ng` is `d-ng|n-ng` (hash with algorithm, unbounded name); `ima-sig` adds the file signature; `evm-sig` adds EVM signature and xattr data. Pick with `ima_template=` or define one with `ima_template_fmt=`.
- Remote attestation: Keylime (CNCF sandbox project) provides remote boot attestation and Linux IMA runtime integrity monitoring using a TPM 2.0 root of trust, with Agent, Registrar, Tenant and Verifier components. Its page gives no detail on allowlist handling; read its run-time attestation guide for that.
- Check logs offline with `evmctl ima_measurement` (recalculates PCR values from the binary list and compares them with TPM PCRs) and `evmctl ima_boot_aggregate`.

## Appraisal (enforce)
1. Label first: boot with `ima_appraise_tcb` and `ima_appraise=fix` (and `evm=fix` if using EVM), touch root-owned files so xattrs are written, then reboot without `fix`.
2. Signed immutable files: `evmctl sign --imasig` (or `evmctl ima_sign`) writes `security.ima`; the wiki uses an RSA private key. `--imahash` stores a hash instead of a signature for files that change.
3. Keys: create `_ima` / `_evm` keyrings and load public keys with `evmctl import`; load them early (initramfs). EC keys need Linux 5.13+ per the evmctl page.
4. Policy keywords are `appraise` and `dont_appraise`; the built-in `appraise_tcb` appraises all root-owned files except pseudo filesystems.
5. `ima_appraise=` modes: `off`, `enforce` (default), `fix` (update `security.ima` to the existing hash for unsigned files). The wiki lists a `log` mode but does not describe it; test its behaviour yourself.

## Gotchas
- The wiki's FAQ: if the system will not boot after enabling appraisal, the filesystem was not labelled with `security.ima` and `security.evm` first. Keep a rescue boot path without the policy.
- Zero (0x00) measurement entries come from a file opened for read and write at once (logs are typical).
- After suspend/resume the list may fail to verify; the wiki suggests `tpm.suspend_pcr=<unused PCR>`.
- EVM HMAC mode relies on a machine-held key; a digital signature (evmctl `-o` portable format) does not.
- Not covered by the sources: interpreter/script handling and performance overhead; test on your workload.

## Verify
- [ ] Measurement list is populated and `evmctl ima_measurement` agrees with the TPM PCR.
- [ ] In enforce mode, an unsigned test binary is refused and an integrity audit record appears (verify on a test host).

## Checked
Method: 2026-11-08 read the kernel IMA templates page, the linux-ima wiki, the ima-evm-utils README and keylime.dev; removed claims about RPM IMA signatures, a specific appraise rule syntax, interpreter behaviour and overhead as unsupported. Template, boot parameter, fix-mode, EVM and evmctl claims unchanged or tightened to the pages.
