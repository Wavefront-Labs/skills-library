---
id: computing-software.web-development.vapor.vapor-deploy-digitalocean
name: vapor-deploy-digitalocean
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-digitalocean, digitalocean, droplet, ufw, swiftly, deployment, ubuntu]
level: practitioner
status: docs-checked
description: "Deploy a Hello World Vapor app to a DigitalOcean Droplet: Ubuntu server, ufw firewall, non-root user, Swiftly, toolbox build, open port 8080, run."
sources:
  - https://docs.vapor.codes/deploy/digital-ocean/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a Vapor app on a DigitalOcean Droplet (needs an account with billing).

## Create the server
Create a Droplet on Ubuntu 22.04 LTS (any Linux version Swift supports works), choose a plan and region, add an SSH key, create, then copy its IP.

## Initial setup
```sh
ssh root@your_server_ip
ufw allow OpenSSH
ufw enable
adduser vapor
usermod -aG sudo vapor
rsync --archive --chown=vapor:vapor ~/.ssh /path/to/vapor-home
exit
ssh vapor@your_server_ip
```

The rsync step copies root's authorized keys to the new user.

## Install Swift
Install Swiftly following https://swiftlang.github.io/swiftly/, then:

```sh
swiftly install latest
swift --version
```

## Build the Vapor Toolbox
Build from source; pick the latest release from the toolbox GitHub releases (the page uses 18.6.0).

```sh
git clone https://github.com/vapor/toolbox.git
cd toolbox
git checkout 18.6.0
swift build -c release --disable-sandbox --enable-test-discovery
sudo mv .build/release/vapor /usr/local/bin
```

## Create and run a project
```sh
vapor new HelloWorld -n      # -n answers no to all prompts: bare bones template
cd HelloWorld
sudo ufw allow 8080
swift run App serve --hostname 0.0.0.0 --port 8080
```

Visiting `http://<server-ip>:8080` should show "It works!" and the server logs the request (`Server starting on http://0.0.0.0:8080`, `GET /`). Ctrl+C quits, which may take a second.

## Next
For automatic start on boot and restart on crash, use Supervisor; for performance, security and ease of use, proxy behind Nginx (see the Vapor Supervisor and Nginx pages).

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/digital-ocean, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
