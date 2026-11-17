---
id: computing-software.game-programming.godot.low-level-networking-udp-tcp-websocket
name: low-level-networking-udp-tcp-websocket
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, packetpeerudp, streampeertcp, websocketpeer, networking, game-programming]
level: practitioner
status: docs-checked
description: "Use Godot low-level networking: PacketPeerUDP and UDPServer, StreamPeerTCP and TCPServer, WebSocketPeer, polling loops, and when to bypass the high-level multiplayer API."
sources: ["https://docs.godotengine.org/en/stable/classes/class_packetpeerudp.html", "https://docs.godotengine.org/en/stable/classes/class_streampeertcp.html", "https://docs.godotengine.org/en/stable/tutorials/networking/websocket.html", "https://docs.godotengine.org/en/stable/classes/class_udpserver.html", "https://docs.godotengine.org/en/stable/classes/class_streampeersocket.html", "https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Low-level networking: UDP, TCP and WebSocket

**Goal:** talk to custom servers, LAN discovery or web backends without MultiplayerAPI.

## UDP (LAN discovery, custom protocols)
```gdscript
var udp := PacketPeerUDP.new()
func _ready() -> void:
    udp.set_broadcast_enabled(true)
    udp.bind(47000)                         # listen
    udp.set_dest_address("255.255.255.255", 47000)
    udp.put_packet("DISCOVER".to_utf8_buffer())
func _process(_d: float) -> void:
    while udp.get_available_packet_count() > 0:
        var pkt := udp.get_packet()
        print(udp.get_packet_ip(), ":", udp.get_packet_port(), " ", pkt.get_string_from_utf8())
```
`UDPServer` gives per-client `PacketPeerUDP` connections (`poll()`, `is_connection_available()`,
`take_connection()`).

## TCP
```gdscript
var tcp := StreamPeerTCP.new()
func connect_to(host: String, port: int) -> void: tcp.connect_to_host(host, port)
func _process(_d: float) -> void:
    tcp.poll()
    if tcp.get_status() == StreamPeerTCP.STATUS_CONNECTED and tcp.get_available_bytes() > 0:
        var data := tcp.get_data(tcp.get_available_bytes())   # [error, bytes]
```
TCP is a byte stream: frame messages yourself (length prefix with `put_u32`/`get_u32`, or
`put_var`/`get_var` which length-prefix Variants; never `get_var(true)` on untrusted data since it
allows objects). `StreamPeerTLS` wraps TCP for TLS. `TCPServer` accepts connections.

## WebSocket
```gdscript
var ws := WebSocketPeer.new()
func _ready() -> void: ws.connect_to_url("wss://example.com/socket")
func _process(_d: float) -> void:
    ws.poll()
    match ws.get_ready_state():
        WebSocketPeer.STATE_OPEN:
            while ws.get_available_packet_count(): print(ws.get_packet().get_string_from_utf8())
        WebSocketPeer.STATE_CLOSED: print("closed ", ws.get_close_code())
func send(msg: String) -> void: ws.send_text(msg)
```
Works as a client in web exports. Servers (native only): `TCPServer.take_connection()` stream passed to
`WebSocketPeer.accept_stream` (or a TLS stream from `StreamPeerTLS.accept_stream`).

## Rules
- Every peer object needs `poll()` each frame (or in a thread) or nothing moves.
- Web exports support only HTTP client, HTTP requests, WebSocket (client) and WebRTC: no raw UDP/TCP.
- In 4.7 `poll()` and the `STATUS_*` enum of `StreamPeerTCP` come from its base class `StreamPeerSocket`
  (the 4.7 class page for StreamPeerTCP lists only bind, connect_to_host and the port/host getters). On Android enable the INTERNET export permission.
- Validate all incoming data; treat sizes and strings as hostile.

## Verify
- [ ] Connection loss and reconnection handled; LAN discovery works across two machines and firewall prompts.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from PacketPeerUDP, UDPServer, StreamPeer, StreamPeerTCP, StreamPeerSocket, StreamPeerTLS, TCPServer and WebSocketPeer class pages, the WebSocket tutorial and the Exporting for the Web page: method names, STATUS_CONNECTED, put_u32/get_u32, get_var allow_objects, accept_stream, STATE_OPEN/CLOSED, web export network support. Added: 4.7 StreamPeerSocket base class, Android INTERNET permission note. Removed: unverified MultiplayerPeer plug-in sentence.
Method: documentation only; no commands were run.
