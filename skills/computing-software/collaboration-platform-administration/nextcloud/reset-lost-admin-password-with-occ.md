---
id: computing-software.collaboration-platform-administration.nextcloud.reset-lost-admin-password-with-occ
name: reset-lost-admin-password-with-occ
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [password-reset, occ, user-resetpassword, admin-recovery, login]
level: intro
status: draft
description: "Recover a lost Nextcloud admin password through the email reset link, another admin, or occ user:resetpassword as the web server user."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/reset_admin_password.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: regain access to an admin account.

Try the options in this order.

1. The reset link on the login screen. It appears after a failed login attempt. It only works if the account has an email address entered on its Personal page, so the server can send the link.

2. Ask another Nextcloud admin to reset the password.

3. If neither is possible, use `occ` on the server, as the web server user:

```
sudo -E -u www-data php /var/www/nextcloud/occ user:resetpassword admin
Enter a new password:
Confirm the new password:
Successfully reset password for admin
```

If the account is not named `admin`, substitute the user id. Adjust the install path and web server user for your system.

The reset needs shell access on the server, and the command asks for the new password twice, so nothing sensitive goes on the command line.

Check: log in with the new password, then set an email address on the Personal page so option 1 works next time.
