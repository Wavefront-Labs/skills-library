---
id: computing-software.systems-network-administration.jellyfin.dlna-plugin
name: dlna-plugin
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, dlna, upnp, ssdp, port-1900, host-networking, plugin]
level: practitioner
status: draft
description: "Install and troubleshoot the Jellyfin DLNA plugin: SSDP on UDP 1900, host networking in Docker and debug logging."
sources: ["https://jellyfin.org/docs/general/post-install/networking/3_dlna/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# DLNA plugin

DLNA is no longer in a base Jellyfin install; it is a first-party plugin. In the admin dashboard open the Catalog, install the DLNA plugin, and restart the server.

**Requirements:** Docker host networking (if using Docker) and UDP port 1900.

DLNA is built on UPnP and uses its Service Discovery (SSDP) on UDP 1900, which cannot be configured. Open the port to your local network. Discovery sends a broadcast to the current subnet and waits for servers to answer, so clients in another subnet cannot find the server and using DLNA remotely is not possible. In Docker use host mode, otherwise the broadcast does not reach the bridged network.

**Troubleshooting**
- If binding fails, the log shows `Failed to bind to port 1900: "Address already in use". DLNA will be unavailable`.
- Setting `Alive message interval (seconds)` to 30 appears to help discovery for some clients.
- If a Base URL is set, try removing it and restarting.

**Debug logging.** Add this to `logging.default.json`:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Warning",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning",
        "Jellyfin.Plugin.Dlna": "Debug"
      }
    }
  }
}
```

Check: a DLNA client on the same subnet lists the server after the restart.
