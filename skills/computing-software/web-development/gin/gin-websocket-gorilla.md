---
id: computing-software.web-development.gin.gin-websocket-gorilla
name: gin-websocket-gorilla
category: computing-software
field: web-development
product: gin
tags: [gin, websocket, gorilla-websocket, upgrader, checkorigin, ping-pong, setponghandler, broadcast]
level: practitioner
status: docs-checked
description: "Upgrade Gin routes to WebSocket with gorilla/websocket: echo and chat hub, Upgrader fields, ping/pong deadlines, single-writer rule and wscat testing."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/websocket.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin WebSocket with gorilla/websocket

Goal: upgrade a Gin route to a WebSocket connection. Gin has no built-in WebSocket implementation; use `github.com/gorilla/websocket`.

```bash
go get github.com/gorilla/websocket
```

## Echo handler
```go
var upgrader = websocket.Upgrader{
  // Allow all origins for development; restrict this in production.
  CheckOrigin: func(r *http.Request) bool { return true },
}

func handleWebSocket(c *gin.Context) {
  conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
  if err != nil {
    log.Printf("WebSocket upgrade error: %v", err)
    return
  }
  defer conn.Close()

  for {
    messageType, message, err := conn.ReadMessage()
    if err != nil { break }
    if err := conn.WriteMessage(messageType, message); err != nil { break }
  }
}
// router.GET("/ws", handleWebSocket)
```

## Upgrader fields
`ReadBufferSize` / `WriteBufferSize` (bytes; default 4096), `CheckOrigin` (by default rejects cross-origin requests), `Subprotocols` (server protocols in order of preference). Response headers go in the third argument of `Upgrade` as an `http.Header`.

## Chat broadcast
Keep a `Hub` with `sync.RWMutex` and `map[*websocket.Conn]bool`: add the connection after upgrade, `defer hub.removeClient(conn)`, and call `hub.broadcast(messageType, message)` in the read loop.

## Ping/pong
```go
const (
  pongWait   = 60 * time.Second
  pingPeriod = (pongWait * 9) / 10 // must be less than pongWait
)
conn.SetReadDeadline(time.Now().Add(pongWait))
conn.SetPongHandler(func(string) error {
  conn.SetReadDeadline(time.Now().Add(pongWait))
  return nil
})
// goroutine: ticker := time.NewTicker(pingPeriod); conn.WriteMessage(websocket.PingMessage, nil)
```

## Test
```bash
npm install -g wscat
wscat -c ws://localhost:8080/ws
```
Type a message and press Enter; the echo server sends it back.

## Gotchas
- `defer conn.Close()` right after a successful upgrade; remove connections from shared structures when the read loop exits; set read and write deadlines to avoid goroutine leaks.
- gorilla/websocket does not support concurrent writes to one connection: serialize with a `sync.Mutex` or a single channel feeding one writer goroutine (channel generally preferred).
- The page's broadcast example writes while holding a read lock; for production use a channel per client.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: server-config/websocket.md. Confirmed: gorilla/websocket install, the echo handler, the Hub broadcast example and its read-lock note, Upgrader fields (4096 default buffers, CheckOrigin default, Subprotocols), response headers argument, ping/pong constants, cleanup bullets, the no-concurrent-writes rule and wscat testing. Trimmed nothing. The linked gorilla chat example and curl WebSocket section were not used.

Method: documentation only; no commands were run.
