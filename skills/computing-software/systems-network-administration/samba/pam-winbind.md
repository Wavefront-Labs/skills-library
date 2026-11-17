---
id: computing-software.systems-network-administration.samba.pam-winbind
name: pam-winbind
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, pam-winbind, pam, mkhomedir, krb5-auth, winbind, authentication]
level: advanced
status: docs-checked
description: "Configure pam_winbind for domain logins: module options, defaults, Kerberos ticket caching, home directory creation and PAM stack placement."
sources:
  - https://www.samba.org/samba/docs/current/man-html/pam_winbind.8.html
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pam winbind
Options (set in the PAM config or in `/etc/security/pam_winbind.conf`; PAM config values take precedence):
- `debug`, `debug_state`: syslog output.
- `require_membership_of=[SID or NAME]`: auth declaration only.
- `try_first_pass`, `use_first_pass`, `use_authtok`, `try_authtok`: token handling.
- `krb5_auth`: Kerberos against an AD DC with samlogon fallback (must be enabled explicitly).
- `krb5_ccache_type=[type]`: DEFAULT, KCM, KEYRING, FILE, WRFILE or a prefixed path; empty by default (no ticket cache kept).
- `cached_login`: needs smb.conf `winbind offline logon = yes` (default no).
- `silent`.
- `mkhomedir`: create the home on the fly; session block only.
- `warn_pwd_expire`: default 14 days.

Example stack lines:
```
auth      required    pam_winbind.so  use_first_pass
account   required    pam_winbind.so  use_first_pass
password  sufficient  pam_winbind.so
session   required    pam_winbind.so
```
Put auth/account after the pam_unix entries, the password line before pam_pwcheck, and the session line near the top because it may fetch Kerberos tickets.

The Samba wiki says these settings could also be necessary in `/etc/security/pam_winbind.conf`: `krb5_auth = yes` and `krb5_ccache_type = FILE`.

Remember `winbind refresh tickets` (default no) controls renewing tickets.

## Checked

2026-11-04. Confirmed against the pam_winbind(8) manual page: every option listed, krb5_ccache_type values and the empty default, warn_pwd_expire default 14, example stack and ordering advice; against smb.conf(5): winbind offline logon and winbind refresh tickets defaults; against the Samba wiki member page: the pam_winbind.conf settings. Removed the unconfirmed module-types line; reworded the MIT Kerberos sentence.
Method: documentation only; no commands were run.
