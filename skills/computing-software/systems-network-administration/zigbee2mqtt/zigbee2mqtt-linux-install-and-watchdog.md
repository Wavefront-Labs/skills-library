---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-linux-install-and-watchdog
name: zigbee2mqtt-linux-install-and-watchdog
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, linux, nodejs, pnpm, systemd, watchdog, z2m-watchdog, onboarding]
level: practitioner
status: docs-checked
description: "Install Zigbee2MQTT natively on Linux with Node.js and pnpm, and use Z2M_WATCHDOG retry delays to recover from soft failures such as an unplugged adapter."
sources: ["https://www.zigbee2mqtt.io/guide/installation/01_linux.html", "https://www.zigbee2mqtt.io/guide/installation/15_watchdog.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT native Linux install and watchdog

The docs recommend Docker over a native install, but the native steps are:

```bash
sudo apt-get install -y curl
sudo curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs git make g++ gcc libsystemd-dev
corepack enable
node --version        # V20.x or V22.x
sudo mkdir /opt/zigbee2mqtt && sudo chown -R ${USER}: /opt/zigbee2mqtt
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
cd /opt/zigbee2mqtt && pnpm install --frozen-lockfile
pnpm start
```

An MQTT broker (Mosquitto recommended) must already exist. On first start the onboarding page opens on port 8080; once finished the log shows the coordinator firmware and "Connected to MQTT server". Ctrl+C stops it. To run in the background use a systemd unit (the page provides one). On Ubuntu Node.js can come from Snap with `--classic`.

Watchdog: set the environment variable `Z2M_WATCHDOG` to restart Zigbee2MQTT after soft failures it can handle itself (for example the adapter disconnecting).
- `Z2M_WATCHDOG=default` retries after 1, 5, 15, 30 then 60 minutes, and exits on the sixth failed start. A successful start resets the sequence.
- `Z2M_WATCHDOG=5,10,30` uses your own delays in minutes (decimals allowed, `0.5` is 30 s); the number of delays is the number of retries. Any other format prevents startup.
- It acts only after an initial successful start, ignores settings errors, and ignores manual stops.
- Hard Node.js crashes still need an OS supervisor (systemd) or the container restart policy.

## Checked

2026-11-03. Confirmed against the Linux install and Watchdog pages: install commands, Docker recommendation, Mosquitto recommendation, onboarding on port 8080, Snap --classic, systemd daemon option, Z2M_WATCHDOG default and custom delays, sixth-failure exit, behaviours that bypass the watchdog, OS watchdog for Node.js crashes. Fixed: Node.js version line now matches the page (V20.x, V22.x).
Method: documentation only; no commands were run.
