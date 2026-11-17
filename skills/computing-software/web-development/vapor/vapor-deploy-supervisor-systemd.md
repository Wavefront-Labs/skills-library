---
id: computing-software.web-development.vapor.vapor-deploy-supervisor-systemd
name: vapor-deploy-supervisor-systemd
category: computing-software
field: web-development
product: vapor
tags: [vapor, supervisor, systemd, process-manager, deployment, linux, environment]
level: practitioner
status: docs-checked
description: "Run a Vapor app as a managed Linux service with Supervisor or systemd: config files, environment variables and start commands."
sources:
  - https://docs.vapor.codes/deploy/supervisor/
  - https://docs.vapor.codes/deploy/systemd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: start, stop and restart a built Vapor app as a service. Give each app its own config file. Both examples assume project `Hello` under user `vapor`; point the directory at the folder containing Package.swift. `--env production` disables verbose logging.

## Supervisor
Install: `sudo apt-get update && sudo apt-get install supervisor` (Ubuntu), `sudo yum install supervisor` (CentOS, Amazon Linux), `sudo dnf install supervisor` (Fedora).

`/etc/supervisor/conf.d/hello.conf`:

```sh
[program:hello]
command=/path/to/vapor-home/hello/.build/release/App serve --env production
directory=/path/to/vapor-home/hello/
user=vapor
stdout_logfile=/var/log/supervisor/%(program_name)s-stdout.log
stderr_logfile=/var/log/supervisor/%(program_name)s-stderr.log
```

Environment: put all values on one line; values with non-alphanumeric characters should be quoted.

```sh
environment=PORT=8123,ANOTHERVALUE="/something/else"
```

Start:

```sh
supervisorctl reread
supervisorctl add hello
supervisorctl start hello
```

`add` may already have started the app.

## systemd
Usually preinstalled on supported Swift distributions. `/etc/systemd/system/hello.service`:

```sh
[Unit]
Description=Hello
Requires=network.target
After=network.target

[Service]
Type=simple
User=vapor
Group=vapor
Restart=always
RestartSec=3
WorkingDirectory=/path/to/vapor-home/hello
ExecStart=/path/to/vapor-home/hello/.build/release/App serve --env production
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=vapor-hello

[Install]
WantedBy=multi-user.target
```

Environment, either files or inline entries in the service section:

```sh
EnvironmentFile=/path/to/environment/file1
Environment="PORT=8123"
Environment="ANOTHERVALUE=/something/else"
```

Run as root:

```sh
systemctl daemon-reload
systemctl enable hello
systemctl start hello
systemctl stop hello
systemctl restart hello
```

## Reading variables in Vapor
`let port = Environment.get("PORT")`

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/supervisor, deploy/systemd, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
