---
id: computing-software.email-administration.dovecot.quick-configuration-single-vmail-user
name: quick-configuration-single-vmail-user
category: computing-software
field: email-administration
product: dovecot
tags: [quick-start, vmail, doveconf-n, passwd-file-passdb, conf-d, dovecot-conf]
level: intro
status: docs-checked
description: "Get a basic working Dovecot: a single vmail user, one dovecot.conf, PAM or passwd-file authentication, and doveconf -n to find the config path."
sources:
  - https://doc.dovecot.org/main/core/config/quick.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The quick guide gives a minimal configuration for a typical environment, with a single `vmail` user, placed in `dovecot.conf`. Create the `vmail` group and user first. The sample starts with `dovecot_config_version` and `dovecot_storage_version` set to the latest version (2.4.0 on the page), then enables `protocols { imap = yes lmtp = yes }`, sets `mail_home = /srv/mail/%{user}`, `mail_driver = sdbox`, `mail_path = ~/mail`, `mail_uid` and `mail_gid` to vmail, an `inbox` namespace with `/` as separator, `passdb pam`, and the `ssl_server_cert_file` and `ssl_server_key_file` paths. `first_valid_uid` defaults to 500, so raise or lower it if vmail's UID is smaller.

Prebuilt packages install config under /etc/dovecot/; find the real path with `doveconf -n | head -n 1`. Source builds install an example at /usr/local/etc/dovecot/dovecot.conf. The default `dovecot.conf` has `!include conf.d/*.conf`, so settings may be split, but a simple setup is easier in one file. The file where a setting is written rarely matters: later settings replace earlier ones, and repeated sections merge.

Authentication. The sample uses PAM for system users, with a PAM file at /etc/pam.d/dovecot containing `auth required pam_unix.so` and `account required pam_unix.so`. For virtual users, first create a simple passwd-like file (`$USER:{PLAIN}password`, written as your own non-root user and moved to /etc/dovecot/) to prove authentication works before moving to a real backend; the guide notes `restorecon` if SELinux is enabled. Use a throwaway password, since login is plaintext until TLS is set up. Switch with `passdb passwd-file { passwd_file_path = ... }` in place of `passdb pam`, then confirm with `doveconf -n passdb`: the output should show the new passdb and no other passdbs and no userdbs.

For other databases, consult the passdb and userdb pages. Let Dovecot autodetect the mail location, or set it manually if detection fails. Maildir or dbox is the recommended mailbox format; mbox is deprecated and for legacy access only. For Maildir, `maildir_very_dirty_syncs = yes` may help performance. Review `imap_client_workarounds` and `pop3_client_workarounds`.

Set the SSL certificate and key paths. `auth_allow_cleartext` defaults to no, so authentication fails when the client does not use SSL; only set it to yes if you cannot offer SSL. If the storage is NFS or another shared remote filesystem, read the NFS page. Reading all shipped config files once is suggested to see settings you may want.

## Checked

2026-11-08. Read the Quick Configuration page in full. Added the sample configuration contents, PAM file lines, passwd-file test step, mailbox format guidance and the cleartext default.

Method: documentation only; no commands were run.
