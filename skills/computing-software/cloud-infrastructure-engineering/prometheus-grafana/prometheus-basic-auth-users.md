---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-basic-auth-users
name: prometheus-basic-auth-users
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, basic-auth-users, htpasswd-bcrypt, web-config, bcrypt, grafana-datasource, alertmanager]
level: practitioner
status: gated
description: "Protect Prometheus, Alertmanager and exporters with web.yml basic_auth_users: generate bcrypt hashes, update every client, and avoid bcrypt CPU cost traps."
sources: ["https://prometheus.io/docs/guides/basic-auth/", "https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic_auth_users

## 1. Generate a bcrypt hash
```bash
htpasswd -nBC 10 "" | tr -d ':\n'; echo                 # prompts for password, prints $2y$10$... (command from the exporter-toolkit docs; Apache htpasswd is not installed here, not run)
python3 -c 'import bcrypt,getpass;print(bcrypt.hashpw(getpass.getpass().encode(),bcrypt.gensalt(10)).decode())'
```
Only bcrypt is accepted: a plaintext value fails `promtool check web-config` with `crypto/bcrypt: hashedSecret too short to be a bcrypted password` (run). The Python `bcrypt` hash (`$2b$10$...`) was accepted by the server (run). Cost 10 is the docs' example; see CPU note below.

## 2. web.yml
```yaml
basic_auth_users:
  prometheus: $2y$10$Z1Xc...          # self-scrape user
  grafana: $2y$10$Q9pL...             # data source user
  admin: $2y$10$hT4r...
tls_server_config:                    # basic auth over plain HTTP sends the password in clear text
  cert_file: tls.crt
  key_file: tls.key
```
`promtool check web-config web.yml` (prints `web.yml SUCCESS`), then start with `--web.config.file=web.yml`. The file is re-read live: changing `min_version` took effect on the next connection without a restart (run).

## 3. Update every client
- Self-scrape job: `basic_auth: {username: prometheus, password_file: /etc/prometheus/pw}`.
- Grafana data source: Basic auth toggle + user/password (stored in `secureJsonData` when provisioned).
- Alertmanager clients: Prometheus `alerting.alertmanagers[].basic_auth`; `amtool --http.config.file=<file>` (flag present in amtool 0.34.1 `--help`; the auth itself was not run).
- Health probes: `/-/healthy` and `/-/ready` are also protected (run: 401 without credentials). For Kubernetes probes use a `tcpSocket` or exec probe, or put auth in a proxy (gated: unconfirmed, source is paywalled or blocked; no cluster here, and whether an httpGet probe can carry an Authorization header via `httpHeaders` was not checked).

## CPU trap
The exporter-toolkit docs say the hash is computed on the first authenticated request and then cached, and that cost 10 takes about 70 ms on a typical machine while cost 18 can take seconds. Measured here with Python bcrypt `checkpw`: cost 10 = 0.047 s, 12 = 0.19 s, 14 = 0.77 s. Keep the cost at 10 and prefer mTLS or an auth proxy for heavy machine-to-machine traffic.

## Gotchas
- Usernames are case-sensitive (run: `Scraper:pw1` 401, `scraper:pw1` 200); there are no roles: the exporter-toolkit docs say listed users have full access to the web server.
- For SSO/RBAC put an authenticating reverse proxy (oauth2-proxy) in front instead.

## Verify
- [ ] `curl -s -o /dev/null -w '%{http_code}' https://host:9090/api/v1/query?query=up` returns 401.
- [ ] Same with `-u grafana:<pw>` returns 200.
- [ ] `up{job="prometheus"}` still 1 and Grafana data source test passes.

## Checked
Prometheus 3.15.1 and promtool (windows-amd64), OpenSSL 3.2.3, Python bcrypt, run locally: web.yml with basic_auth_users plus TLS (401 without credentials on /api and on /-/healthy, 200 with, `Scraper` 401 vs `scraper` 200, self-scrape with `basic_auth` worked), plaintext password rejected by `promtool check web-config`, `$2b$` hash accepted, bcrypt timings at cost 10/12/14, live re-read of web.yml. Docs read: exporter-toolkit docs/web-configuration.md (bcrypt, hash cached after first request, ~70 ms at cost 10). Not run: htpasswd, Kubernetes probes, Grafana data source, amtool authentication.
