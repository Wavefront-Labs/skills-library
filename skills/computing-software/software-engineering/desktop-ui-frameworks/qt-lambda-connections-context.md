---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-lambda-connections-context
name: qt-lambda-connections-context
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-lambda-connections-context, qt-signals-slots, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Connect signals to lambdas with a context object so the connection dies with the receiver and avoids dangling captures."
sources:
  - https://doc.qt.io/qt-6/signalsandslots.html
  - https://doc.qt.io/qt-6/qobject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt lambda connections with context object

**Goal:** safe lambda slots.

```cpp
// good: context 'this' ties lifetime and selects the thread
connect(sender, &Sender::done, this, [this] { handle(); });
// bad: no context, not disconnected when 'this' is destroyed
connect(sender, &Sender::done, [this] { handle(); });
```

**Gotcha:** Without a context object the connection is only dropped when the sender is destroyed, so a lambda capturing this or local state can run after the owner is gone; the functor's captured objects must also stay alive.

## Checked
2026-11-03. Confirmed in the Signals and Slots and QObject pages: the connect() overload with a context object, automatic disconnect when sender or context is destroyed, the functor is placed in the context's event loop, the context-less overload is error prone. Replaced: the QNetworkReply example with a generic Sender.

Method: documentation only; no commands were run.

## Verify
- Delete the owner mid-request in a test and confirm no crash and no late callback.
