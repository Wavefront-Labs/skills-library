---
id: computing-software.systems-network-administration.linux.gpg-key-signing-and-web-of-trust
name: gpg-key-signing-and-web-of-trust
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, web-of-trust, key-signing, ownertrust, certification-levels, gpg-sign-key, trustdb]
level: practitioner
status: verified
description: "Certify other people's OpenPGP keys and manage trust: verifying fingerprints, sign vs lsign, certification levels, ownertrust, trust models and distributing signatures."
sources:
  - https://github.com/gpg/gnupg/blob/master/doc/gpg.texi
  - https://github.com/gpg/gnupg/blob/master/doc/gpgv.texi
  - https://keys.openpgp.org/about/faq
  - https://wiki.debian.org/Keysigning
licence: Apache-2.0
version: 5
updated: 2026-11-17
---
# Key signing and trust levels

Two different things:
- **Validity**: do I believe this key belongs to that person? Established by signatures (certifications).
- **Ownertrust**: how much do I trust this person to verify *others'* keys? Private to your keyring.

## Verify before signing
Compare the full fingerprint out of band (in person, phone, signed document), and check ID:
```bash
gpg --fingerprint bob@example.com
# 4E1F 799A A4FF 2279 ... - read all 40 hex characters, not just the last 8
```
Short and long key IDs collide; never sign based on them.

## Sign
```bash
gpg --sign-key bob@example.com        # exportable certification
gpg --lsign-key bob@example.com       # local-only: validates the key for you, never exported
gpg --ask-cert-level --sign-key ...   # 0 no claim, 1 persona, 2 casual, 3 extensive check
gpg --edit-key bob@example.com        # 'uid 2' then 'sign' to certify just one user ID
```
Signing a UID asserts both the name and that the email belongs to them, so only sign the user IDs you have checked.
`--default-cert-level 3` records "I have checked this key very carefully" and level 2 "casually". With `--batch` the signing prompts cannot be answered, and a keyring without a secret key has nothing to sign with (`Key not changed so no update needed`).

## Distribute
```bash
gpg --armor --export bob@example.com > bob-signed-by-alice.asc   # send to Bob; he imports and publishes
gpg --send-keys <FPR>     # only with Bob's consent; keys.openpgp.org does not distribute third-party signatures by default
```

## Ownertrust and the trust model
```bash
gpg --edit-key bob@example.com
  trust   # pick the ownertrust level at the prompt; ultimate is meant for your own keys
gpg --check-trustdb
gpg --list-keys bob@example.com    # user ID validity is shown by default (list-option show-uid-validity)
```
Tested: after `lsign` of Ops's key the user ID showed `[  full  ]` and verifying Ops's signature gave `Good signature` with no untrusted-key warning; the local signature was not exported (4 signature packets before and after). With full ownertrust on Ops, a second key signed by Ops showed `[  full  ]` with no signature from me.

Default `pgp` trust model: a key is valid if signed by you, or by enough trusted signers: `--completes-needed` (default 1) fully trusted or `--marginals-needed` (default 3) marginally trusted keys, within `--max-cert-depth` (default 5).
- `trust-model tofu+pgp` in `gpg.conf` combines TOFU (Trust On First Use) with the pgp model; the manual calls TOFU experimental. When a second key appears for the same email address, both keys are marked suspect and a warning is shown on use.
- `trust-model always` skips key validation and treats every key as fully valid; never use it outside scripts with pinned fingerprints.

## Organisational use
Package signing and release verification usually pin a keyring (for example `gpgv --keyring <file>`; `gpgv` otherwise uses `trustedkeys.kbx` or `trustedkeys.gpg`) rather than relying on the web of trust. A company CA key that `lsign`s employee keys plus ownertrust on that CA gives a simple managed trust path.

## Verify
- [ ] `gpg --check-sigs bob@example.com` shows your certification; validity shows `full`.
- [ ] Verifying a file Bob signed reports `Good signature` without the untrusted-key warning.

## Checked
Checked 2026-10-27 against the GnuPG documentation source (github.com/gpg/gnupg doc/gpg.texi and gpgv.texi) and the keys.openpgp.org FAQ.
- `--ask-cert-level` prompts for a level and `--default-cert-level` defines 0 (no claim), 1 (persona), 2 (casual), 3 (extensive); `lsign` makes a non-exportable signature; edit-key `uid N` and `sign` exist.
- `--completes-needed` defaults to 1, `--marginals-needed` to 3, `--max-cert-depth` to 5; `--check-trustdb`; `show-uid-validity` list option defaults to yes.
- `--trust-model` values `pgp` (default for new trust databases), `classic`, `tofu`, `tofu+pgp`, `direct`, `always`, `auto`; TOFU is described as experimental and marks both keys suspect on a conflict; `always` skips validation.
- `gpgv --keyring` and its default `trustedkeys.kbx`/`trustedkeys.gpg`.
- keys.openpgp.org FAQ: third-party signatures are not distributed by default.
- Removed unconfirmed claims: trust menu numbers, validity output tags, caff workflow, apt `signed-by` wording, exact gpg warning text.
Run 2026-11-01 with GnuPG 2.4.5 on Windows (Git Bash), throwaway GNUPGHOME folders in a scratch directory: `--fingerprint`, `--list-keys` validity, `--sign-key` and `--lsign-key` with `--default-cert-level`, `--check-sigs`, `--edit-key` `trust` (via `--command-fd`), `--check-trustdb` (printed `marginals needed: 3  completes needed: 1  trust model: pgp`), `--export` with and without local signatures, `gpgv --keyring` and the default `trustedkeys.kbx`, `--trust-model always`, `--dump-options` listing the options. Not run: the interactive `--ask-cert-level` prompt, `tofu+pgp` conflict handling, `--max-cert-depth`, keyserver distribution; these stay as documented.

Method: documentation plus commands run (GnuPG 2.4.5).
