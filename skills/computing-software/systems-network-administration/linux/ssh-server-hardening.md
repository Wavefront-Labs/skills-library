---
id: computing-software.systems-network-administration.linux.ssh-server-hardening
name: ssh-server-hardening
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, sshd, ssh-server, ssh-hardening, sshd-config, openssh, key-only-auth, permitrootlogin, allowgroups, match-block, ssh-ca, certificates, sftp-chroot, 2fa, pam-google-authenticator, ssh-audit, kexalgorithms, rhcsa, security, sysadmin, sshd-t, sshd-config-d, login-grace-time, maxauthtries, ssh-port]
level: practitioner
status: verified
description: "Harden and operate OpenSSH server: key-only auth, root/group restrictions, Match blocks, modern ciphers, SSH certificates, SFTP chroot, MFA, safe config testing."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keygen.1
  - https://github.com/jtesta/ssh-audit
  - https://github.com/google/google-authenticator-libpam/blob/master/README.md
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-port.8
  - https://github.com/firewalld/firewalld/blob/main/doc/xml/firewall-cmd.xml.in
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# SSH server hardening — close the obvious doors without closing your own

**Goal:** an sshd that accepts only keys (or keys+MFA) for named groups, uses modern
crypto, logs usefully, and can be reconfigured safely over SSH itself.

## 1. The drop-in (needs an `Include` line in sshd_config; otherwise edit `/etc/ssh/sshd_config`)
```bash
# /etc/ssh/sshd_config.d/10-hardening.conf   (the first obtained value wins and Include files are read in lexical order, so low numbers win)
PermitRootLogin no               # or prohibit-password for key-only root on appliances
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
AllowGroups ssh-users wheel
MaxAuthTries 3                   # default 6
LoginGraceTime 30                # default 120 seconds
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no          # enable per-host in a Match block if needed
AllowTcpForwarding no            # same; bastions need yes
PermitEmptyPasswords no
UseDNS no
LogLevel VERBOSE                 # default is INFO
Banner /etc/issue.net
```
- Keep a `Match` for the ops team or bastion: 
  ```
  Match Group ops
      AllowTcpForwarding yes
      AllowAgentForwarding yes
  ```
  A `Match` block applies until the next `Match` line or the end of the file, so put Match blocks last.
- Some distributions manage algorithm lists through a system-wide crypto policy; check your distribution's
  documentation before overriding them. Otherwise set explicitly (`ssh -Q kex`, `ssh -Q cipher`, `ssh -Q mac` list what your build supports):
  ```
  KexAlgorithms mlkem768x25519-sha256,sntrup761x25519-sha512,curve25519-sha256
  Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
  MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
  HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
  ```
  Choose the host keys sshd offers with `HostKey` lines; `ssh-keygen -A` creates any missing host keys of the default types.
  The third-party `ssh-audit` tool can grade the result from another machine.

## 2. Apply without lockout
```bash
sshd -t                                   # syntax check
sshd -T -C user=alice,host=1.2.3.4,addr=1.2.3.4 | grep -iE 'passwordauth|allowgroups|permitroot'  # effective config incl. Match
```
Then reload sshd with your init system (the unit name is distribution-specific). Keep your current session open and
open a **second** connection to test; only then close the first.
Changing `Port`: also `semanage port -a -t ssh_port_t -p tcp 2222` (SELinux) and the
firewall (`firewall-cmd --add-port=2222/tcp --permanent`) **before** reloading.

## 3. Authorized keys controls
- `AuthorizedKeysFile .ssh/authorized_keys /etc/ssh/authorized_keys/%u` — central,
  root-owned keys that users cannot edit (good for automation accounts).
- Options in the key line: `restrict,command="/usr/local/bin/backup-shell",from="10.0.0.0/8" ssh-ed25519 AAAA…`
  for single-purpose keys (`restrict` disables pty/forwarding/agent/X11).
- `AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys` + `AuthorizedKeysCommandUser nobody`
  pulls keys from AD/IPA via SSSD.
- `StrictModes yes` (default) rejects keys when the home directory, `~/.ssh` or authorized_keys is writable by
  others. `chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys`.

## 4. SSH certificates (fleet-scale, no key sprawl)
```bash
ssh-keygen -t ed25519 -f /etc/ssh/ca_user -C "user CA"                    # on the CA host
ssh-keygen -s /etc/ssh/ca_user -I alice -n alice,ops -V +8h alice.pub     # short-lived cert
# server:
TrustedUserCAKeys /etc/ssh/ca_user.pub
AuthorizedPrincipalsFile /etc/ssh/principals/%u                           # lines: alice / ops
```
Users present `alice-cert.pub` alongside their key; no per-host authorized_keys. Revoke
with `RevokedKeys /etc/ssh/revoked_keys` (`ssh-keygen -k`). Host certs
(`HostCertificate`) + `@cert-authority` in `known_hosts` end "host key changed" prompts.

## 5. MFA and SFTP-only users
```
# /etc/pam.d/sshd:  auth required pam_google_authenticator.so nullok
# sshd_config:
KbdInteractiveAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```
(`nullok` lets users without a token in while rolling out; remove afterwards.)
```
Match Group sftponly
    ChrootDirectory /srv/sftp/%u          # root-owned, not writable by the user; upload dir inside
    ForceCommand internal-sftp -u 0027
    AllowTcpForwarding no
    X11Forwarding no
```

## 6. Monitoring
Read sshd's messages in the journal or authentication log; pair with fail2ban or firewall rate limits on the SSH
port. `LogLevel` (default INFO) sets sshd's verbosity; avoid DEBUG levels, which the manual says violate users' privacy.

## Failure modes
- Locked out after `AllowGroups`: your user isn't in the group (or the group name is a
  group not resolvable by the system). Console access or cloud serial console; this is why
  you test in a second session.
- A setting you changed is overridden by another included file read earlier: check the effective value with `sshd -T`.
- `sshd -T` prints the default `PermitRootLogin prohibit-password` as `without-password` (seen on OpenSSH 10.0).
- Agent forwarding to an untrusted host lets its root use your keys; prefer
  `ProxyJump` on the client side.

## Verify
- [ ] `ssh -o PreferredAuthentications=password user@host` is refused immediately.
- [ ] `sshd -T` shows `permitrootlogin no`, `passwordauthentication no`, your `allowgroups`.
- [ ] `ssh-audit` reports no weak algorithms; a fresh login is logged by sshd.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1), semanage-port(8), firewall-cmd documentation source and the google-authenticator-libpam README.
Confirmed: option names and defaults (PermitRootLogin default prohibit-password, MaxAuthTries 6, LoginGraceTime 120, LogLevel INFO), first-value-wins and Include ordering, Match scope, AuthenticationMethods, StrictModes, AuthorizedKeysFile tokens, AuthorizedKeysCommand and principals options, TrustedUserCAKeys, ChrootDirectory ownership rule, `ForceCommand internal-sftp -u`, `sshd -t` and `sshd -T -C`, algorithm names (ML-KEM and sntrup761 key exchange, chacha20-poly1305, AES-GCM, -etm MACs, rsa-sha2-*), `semanage port -a -t ssh_port_t -p tcp`, `firewall-cmd --add-port --permanent`, and `pam_google_authenticator.so nullok`.
Corrected: `ssh-keygen -A` also regenerates ecdsa host keys, so it cannot be used to leave them out. Removed as unconfirmed: the Include version gate, crypto-policy commands, distribution unit names and socket activation, log message text, the claim that LogLevel VERBOSE logs key fingerprints, lastb, cloud-init and SSSD group naming details.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (OpenSSH 10.0p2): the whole drop-in accepted by sshd -t; sshd -T -C with and without the Match Group block; first value wins across Include files in lexical order; defaults (MaxAuthTries 6, LoginGraceTime 120, LogLevel INFO); ssh -Q listing mlkem768x25519-sha256, sntrup761x25519-sha512, chacha20-poly1305, aes-gcm and -etm MACs; ssh-keygen -A regenerating a deleted ecdsa key; a bad option failing sshd -t; ForceCommand internal-sftp -u 0027 with ChrootDirectory shown by sshd -T; user certificate signing, -L, and -k revocation list; AuthorizedKeysFile %u token. Not run: real logins, SELinux and firewall commands, google-authenticator PAM, ChrootDirectory ownership enforcement.
