---
id: computing-software.systems-network-administration.linux.http-basic-auth-htpasswd
name: http-basic-auth-htpasswd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, htpasswd, basic-auth, nginx-auth-basic, apache-authbasic, auth-basic-user-file, bcrypt, require-valid-user, satisfy-any, web-server, security, sysadmin]
level: practitioner
status: verified
description: "Protect nginx or Apache paths with HTTP basic auth: creating htpasswd files with bcrypt, auth_basic/AuthType config, IP-or-password access and testing with curl."
sources:
  - https://httpd.apache.org/docs/2.4/programs/htpasswd.html
  - https://httpd.apache.org/docs/2.4/howto/auth.html
  - https://nginx.org/en/docs/http/ngx_http_auth_basic_module.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HTTP basic auth with htpasswd

**Goal:** put a password in front of an admin page, staging site or metrics endpoint —
over TLS only — with hashes the server can actually verify.

## 1. Create the password file
```bash
# htpasswd ships with the Apache HTTP Server tools package of your distribution
htpasswd -c -B -C 12 /etc/nginx/.htpasswd alice    # -c creates the file (replacing an existing one), -B bcrypt, -C cost
htpasswd -B /etc/nginx/.htpasswd bob               # add/update without -c
htpasswd -D /etc/nginx/.htpasswd bob               # delete
htpasswd -v /etc/nginx/.htpasswd alice             # verify a password
chmod 640 /etc/nginx/.htpasswd      # readable by the web server's group only; set the group to match your server
```
Without `htpasswd`, nginx accepts `openssl passwd` output too (apr1 is the Apache MD5 variant, weaker than bcrypt).
nginx accepts passwords hashed with the system `crypt()` function, apr1, or `{scheme}data` forms; whether a bcrypt hash verifies depends on the platform `crypt()`, so test a login before rollout and use `-m` (apr1) if it fails (a `$2y$12` hash verified on Debian 13 with nginx 1.26.3). `-b` takes the password from the command line (visible in `ps`); without it htpasswd prompts, and `-B` alone uses cost 5.

## 2. nginx
```nginx
location /admin/ {
    auth_basic           "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://app;
}
# IP allowlist OR password:
location /metrics {
    satisfy any;
    allow 10.0.99.0/24;
    deny  all;
    auth_basic "metrics";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
location /healthz { auth_basic off; }     # exempt a sub-path
```

## 3. Apache
```apache
<Location "/admin">
    AuthType Basic
    AuthName "Restricted"
    AuthBasicProvider file
    AuthUserFile /etc/httpd/.htpasswd
    Require valid-user
</Location>
<Location "/metrics">
    <RequireAny>
        Require ip 10.0.99.0/24
        Require valid-user
    </RequireAny>
    AuthType Basic
    AuthName "metrics"
    AuthUserFile /etc/httpd/.htpasswd
</Location>
```
Groups: `AuthGroupFile` + `Require group admins`.

## 4. Test
```bash
nginx -t && systemctl reload nginx
curl -s -o /dev/null -w '%{http_code}\n' https://site/admin/            # 401
curl -s -o /dev/null -w '%{http_code}\n' -u alice https://site/admin/   # prompts; 200
```

## Gotchas
- Basic authentication sends the password from the client to the server unencrypted; use it only over HTTPS (Apache: mod_ssl).
- Keep the password file outside the document root.
- If the server cannot read the file, expect an error response rather than a 401 (a request with credentials got 500 and the error log showed `open() ... failed (13: Permission denied)`): check permissions and security labels.
- `return 200 ...` in the same location is evaluated before `auth_basic`, so that location answers without a password; use `proxy_pass`, `root` or `try_files` there.

## Verify
- [ ] Unauthenticated request returns 401 with `WWW-Authenticate: Basic`; correct credentials 200; wrong password 401.
- [ ] `ls -l` on the htpasswd file shows mode 640 and the web server's group.

## Checked

Documentation check. Checked 2026-10-27 against the Apache HTTP Server 2.4 htpasswd and authentication how-to pages (httpd.apache.org) and nginx's ngx_http_auth_basic_module and ngx_http_core_module pages (nginx.org): htpasswd `-c`, `-B`, `-C cost`, `-D`, `-v`, `-m`, bcrypt and crypt() hashing; nginx `auth_basic`, `auth_basic off`, `auth_basic_user_file`, the supported password types (crypt(), apr1, `{scheme}data`) and `satisfy any`; Apache `AuthType Basic`, `AuthBasicProvider file`, `AuthGroupFile`, `<RequireAny>` and the unencrypted-password warning. Removed the distro package names, the glibc/RHEL bcrypt statement, the SELinux label names, the proxy_set_header advice, the base64 remark and the rate-limit remark, which none of the checked pages state.
Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (apache2-utils htpasswd, nginx 1.26.3 on 127.0.0.1): htpasswd -c -B -C 12 ($2y$12), -B without -C ($2y$05), -m (apr1), -D, -v (exit 3 and `password verification failed` on a wrong password); nginx 401 without credentials, 200 with a bcrypt or apr1 user, 401 for a wrong password, satisfy any with a non-allowed address still needing the password, auth_basic off, 500 with an `open() ... Permission denied` error-log line when the file was unreadable. Not run: Apache configuration, allowed-IP path of satisfy any, the Apache group file.
