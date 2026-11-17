---
id: computing-software.systems-network-administration.linux.gpg-keys-signing-and-verification
name: gpg-keys-signing-and-verification
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, gpg, gnupg, gpg-key-generation, full-gen-key, gpg2, signing, key-verification, detached-signature, verify-download, checksum-signature, keyserver, fingerprint, revocation-certificate, subkeys, gpg-agent, encrypt-file, symmetric-encryption, ssh-via-gpg, repo-signing, package-signing, lpic-1, security, sysadmin, git-signing, gpg-export, key-backup]
level: practitioner
status: verified
description: "Use GnuPG on Linux: keys with subkeys and a revocation cert, verify signed downloads, sign files and packages, encrypt for a recipient, manage gpg-agent and keyservers."
sources:
  - https://www.gnupg.org/documentation/manuals/gnupg/
  - https://github.com/gpg/gnupg/blob/master/doc/gpg.texi
  - https://www.kernel.org/signature.html
  - https://keys.openpgp.org/about
  - https://github.com/rpm-software-management/rpm/blob/master/docs/man/rpmsign.1.scd
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# GPG keys, signing and verification — prove where a file came from

**Goal:** verify that what you downloaded is what the author signed, sign your own
artefacts so others can do the same, and keep a key you can rotate and revoke.

## 1. Verify a download (the thing you do most)
```bash
# 1. get the signer's key via a trusted channel (project site, keybase, WKD), not a bare keyserver search
gpg --locate-keys torvalds@kernel.org                    # locate by email using the --auto-key-locate methods
gpg --keyserver hkps://keys.openpgp.org --recv-keys <FINGERPRINT>
gpg --fingerprint <FINGERPRINT>                          # compare the WHOLE fingerprint with the published one
# 2. verify
gpg --verify linux-6.10.tar.sign linux-6.10.tar           # detached signature (kernel.org signs the UNCOMPRESSED .tar, so unxz first)
sha256sum -c --ignore-missing SHA256SUMS && gpg --verify SHA256SUMS.gpg SHA256SUMS   # signed checksum list
gpg --verify release.tar.gz.asc release.tar.gz            # always name the data file
```
Reading the result: `Good signature from "…"` plus a warning that the key is not certified with a
trusted signature is **normal** (the exact wording varies by version) — the signature is cryptographically valid; the warning
says you haven't personally marked the key trusted. "BAD signature" = tampered or wrong file.
"No public key" = import the key first. Check the fingerprint printed matches the one you
verified out-of-band; a "Good signature" from a random key proves nothing.

Mark a key you've verified: `gpg --edit-key <FPR>` → `trust` and pick a level at the prompt, or `gpg --lsign-key <FPR>`.

## 2. Your own key
```bash
gpg --full-generate-key                       # interactive: pick an ECC (Curve25519) key and an expiry such as 2y
gpg --quick-generate-key "Ops Team <ops@example.com>" ed25519 cert 2y   # certify-only primary …
gpg --quick-add-key <FPR> ed25519 sign 1y     # … then subkeys for daily work
gpg --quick-add-key <FPR> cv25519 encr 1y
gpg --quick-add-key <FPR> ed25519 auth 1y     # for SSH via gpg-agent
gpg --gen-revoke <FPR> > revoke.asc            # interactive (asks for a reason, refuses --batch); make this NOW, store offline with the primary key
gpg --armor --export <FPR> > ops.pub.asc; gpg --armor --export-secret-keys <FPR> > ops.sec.asc   # backup (encrypted media)
gpg --export-secret-subkeys <FPR> > subkeys.gpg   # laptop gets only subkeys; primary stays offline
gpg -K --with-subkey-fingerprint               # "sec#" = primary secret key taken offline (good on a laptop)
gpg --quick-set-expire <FPR> 2y; gpg --quick-set-expire <FPR> 1y '*'   # extend before expiry; re-publish
gpg --keyserver hkps://keys.openpgp.org --send-keys <FPR>   # see the keyserver's about page for how identities are published
```
Expiry is not a security feature; it's a dead-man switch so lost keys stop being used.
gpg 2.4 also writes a revocation certificate to `openpgp-revocs.d/<FPR>.rev` in the home directory when it creates a key; copy it offline too.
Extending expiry is a one-liner; losing the revocation cert and the primary key is forever.

## 3. Sign and encrypt
```bash
gpg --detach-sign --armor release.tar.gz           # release.tar.gz.asc; -u <FPR> to pick a key
gpg --clearsign CHANGELOG                          # inline, readable
gpg --sign --encrypt --recipient alice@example.com --armor secrets.env   # signed+encrypted for alice
gpg --decrypt secrets.env.asc > secrets.env
gpg --symmetric --cipher-algo AES256 backup.tar     # passphrase-only; fine for ad-hoc transfer
git config --global user.signingkey <SUBKEY-FPR>! && git config --global commit.gpgsign true   # "!" forces that subkey
```
Encrypting to an imported key you have not certified fails in `--batch` mode with `Unusable public key`; `--lsign-key` it first (or `--trust-model always` when you pinned the fingerprint).

Repository/package signing: `rpmsign --addsign pkg.rpm`, with the signing identity set by the
`%_openpgp_sign_id` macro (`%_gpg_name` is the legacy name); apt repo `Release` files via
`gpg --clearsign -o InRelease Release`. Clients then need your public key: see `signed-by=` in
sources.list(5) for apt, `rpm --import` for RPM.

## 4. gpg-agent, smartcards, SSH
```bash
gpgconf --kill gpg-agent; gpg-connect-agent /bye   # restart agent after config changes
# ~/.gnupg/gpg-agent.conf
default-cache-ttl 3600
max-cache-ttl 28800
enable-ssh-support
pinentry-program <path to a pinentry program>
```
`export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)`; `ssh-add -L` lists what the agent offers. Keys on active cards are always offered; for an on-disk key set the
`Use-for-ssh` attribute in its key file (the `sshcontrol` file is deprecated). YubiKey/OpenPGP card: `gpg --card-status`,
`gpg --edit-key <FPR>` → `keytocard` moves subkeys onto the card (one-way). "No pinentry" /
"Inappropriate ioctl for device" in scripts → `export GPG_TTY=$(tty)` (the gpg-agent manual says to add it to your shell startup file) or use `--pinentry-mode loopback`.

## 5. Hygiene
- Keyservers are untrusted directories: use `keys.openpgp.org` (verified emails, no
  third-party signatures) and always compare fingerprints with a trusted source.
- Keep `~/.gnupg` private (mode 700); gpg warns about unsafe home directory permissions (`--no-permission-warning` silences it).
- Automation keys (CI signing): a dedicated key with only a signing subkey, passphrase
  supplied via `--batch --pinentry-mode loopback --passphrase-fd 0` (gpg 2.1+ needs loopback with `--passphrase-fd`) from a secret store, never in the repo.
- Rotate: new subkeys, publish, keep the old ones (they still verify old signatures); revoke
  only when compromised (`gpg --import revoke.asc && gpg --send-keys`).

## Verify
- [ ] `gpg --verify` of a known release (e.g. a kernel tarball) prints `Good signature` with the maintainer's published fingerprint.
- [ ] `gpg -K` shows `sec#` on daily-use machines; `revoke.asc` and the primary key are backed up offline.
- [ ] A file you signed verifies on another machine after importing only your public key.

## Checked
Checked 2026-10-27 against the GnuPG documentation source (github.com/gpg/gnupg doc/gpg.texi, gpg-agent.texi, tools.texi), kernel.org signature page, keys.openpgp.org about page, the rpmsign(1) source and the coreutils manual.
- `--quick-generate-key USER-ID [algo [usage [expire]]]`, `--quick-add-key`, `--quick-set-expire fpr expire [*]`, `--export-secret-subkeys`, `--locate-keys` (uses `--auto-key-locate`), `--detach-sign`, `--symmetric --cipher-algo`, `--send-keys`, `--recv-keys`.
- gpg manual: verifying a detached signature without naming the data file is strongly discouraged; `--passphrase-fd` needs `--batch` and, from 2.1, `--pinentry-mode loopback`.
- kernel.org signatures are made against the uncompressed tarball.
- `--with-subkey-fingerprint` is the option name (singular); `sec#` means taken offline; unsafe permissions are a warning, not a refusal.
- gpg-agent: `enable-ssh-support`, `default-cache-ttl` (default 600 s), `max-cache-ttl`, `pinentry-program`, `GPG_TTY=$(tty)`, active cards always offered, `sshcontrol` deprecated in favour of `Use-for-ssh`; `gpgconf --kill`.
- rpmsign: `--addsign`, `%_openpgp_sign_id` with `%_gpg_name` as the legacy macro; coreutils checksum `--ignore-missing`.
- Corrected: plural `--with-subkey-fingerprints`, `sshcontrol` guidance, auto-lookup of the data file. Removed unconfirmed: full-generate menu number, `dpkg-sig`/`debsign`, `apt-key` and keyring directory statements, pinentry path, keyserver email-verification aside.
Run 2026-11-01 with GnuPG 2.4.5 on Windows (Git Bash) in a throwaway GNUPGHOME inside a scratch folder (throwaway keys with empty passphrases via --batch --pinentry-mode loopback; the real keyring was not touched): `--quick-generate-key` (cert), `--quick-add-key` (sign, encr, auth), `-K --with-subkey-fingerprint` (an import of only `--export-secret-subkeys` output shows `sec#`), `--quick-set-expire` in both forms, `--export`/`--export-secret-keys`/`--export-secret-subkeys`, `--detach-sign --armor`, `--clearsign`, `--sign --encrypt --recipient`, `--decrypt`, `--symmetric --cipher-algo AES256`, `--verify` (good; BAD after the file changed; the `not certified with a trusted signature` warning; a signature file alone makes gpg assume the data file), `sha256sum -c --ignore-missing` with a signed checksum list, `gpgconf --kill gpg-agent`, `gpg-connect-agent /bye`, agent option defaults (`default-cache-ttl` 600), `--passphrase-fd 0` with loopback, `gpg --dearmor` and `--show-keys`. Not run: `--locate-keys`, `--recv-keys` and `--send-keys` (network), smartcards and `keytocard`, `enable-ssh-support` with ssh, rpmsign and apt signing, the permission warning (this Windows build printed none at mode 755), kernel.org verification; these stay as documented.

Method: documentation plus commands run (GnuPG 2.4.5).
