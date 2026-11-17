---
id: computing-software.email-administration.mailcow.mailcow-password-and-two-factor-reset
name: mailcow-password-and-two-factor-reset
category: computing-software
field: email-administration
product: mailcow
tags: [reset-admin-password, mysql-password-reset, remove-tfa, sogo-tool-preferences, mailcow-reset-admin]
level: advanced
status: docs-checked
description: "Recover access by resetting the mailcow admin password, MariaDB users or a user's two-factor login from the command line."
sources: ["https://docs.mailcow.email/troubleshooting/debug-reset_pw/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Resetting passwords and two-factor in mailcow

Admin account: run `./helper-scripts/mailcow-reset-admin.sh` in the mailcow directory; it resets the admin account to a random password. Older installations may find the script in the mailcow root.

MySQL: stop the stack, then open the MariaDB client through the docker command in the docs (after `source mailcow.conf` for `DBUSER`, `DBPASS`, `DBNAME`). Find the database name with `show databases;` (typically `mailcow_database`), list users with `SELECT user FROM mysql.user;`, then run `FLUSH PRIVILEGES;`. On MariaDB 10.4 and newer use `ALTER USER 'mailcow'@'%' IDENTIFIED BY '...'` and the same for `root` at `%` and `localhost`, then flush again. On older MariaDB versions both `password` and `authentication_string` exist and should be set with `UPDATE mysql.user SET ... = PASSWORD('...')`.

Remove two-factor for the web UI from the host: `source mailcow.conf` and then `docker compose exec mysql-mailcow mysql -u${DBUSER} -p${DBPASS} ${DBNAME} -e "DELETE FROM tfa WHERE username='YOUR_USERNAME';"`.

Remove it for SOGo: `docker compose exec -u sogo sogo-mailcow sogo-tool user-preferences set defaults user@example.com SOGoGoogleAuthenticatorEnabled '{"SOGoGoogleAuthenticatorEnabled":0}'`.

## Checked

2026-11-09. Confirmed on the reset page: mailcow-reset-admin.sh and the older-install location, stopping the stack, the skip-grant-tables MariaDB client, show databases, SELECT user, the pre-10.4 PASSWORD() update, the 10.4 and newer ALTER USER statements, the tfa table delete and the SOGo sogo-tool command. No changes needed.

Method: docs-checked 2026-11-09 against the full reset page (debug-reset_pw.en.md in mailcow-dockerized-docs).
