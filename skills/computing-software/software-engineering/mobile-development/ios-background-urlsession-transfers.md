---
id: computing-software.software-engineering.mobile-development.ios-background-urlsession-transfers
name: ios-background-urlsession-transfers
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, background-urlsession, urlsession, background-transfers, uploads, downloads, handleeventsforbackgroundurlsession]
level: advanced
status: draft
description: "Run uploads and downloads that survive app suspension with a background URLSession: configuration, delegate wiring, app relaunch handler, and upload-from-file rule."
sources: ["https://developer.apple.com/documentation/foundation/url_loading_system/downloading_files_in_the_background", "https://developer.apple.com/documentation/foundation/urlsessionconfiguration/1407496-background", "https://developer.apple.com/documentation/uikit/uiapplicationdelegate/1622941-application"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Background URLSession transfers

A background session hands transfers to a system daemon (`nsurlsessiond`) so they continue when the app is suspended or even terminated by the system.

```swift
final class Transfers: NSObject, URLSessionDownloadDelegate {
    static let shared = Transfers()
    var backgroundCompletion: (() -> Void)?

    lazy var session: URLSession = {
        let cfg = URLSessionConfiguration.background(withIdentifier: "com.example.app.transfers")
        cfg.sessionSendsLaunchEvents = true
        cfg.isDiscretionary = false          // true lets the system pick good conditions
        return URLSession(configuration: cfg, delegate: self, delegateQueue: nil)
    }()

    func download(_ url: URL) { session.downloadTask(with: url).resume() }

    func urlSession(_ s: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo tmp: URL) {
        // move the file NOW; tmp is deleted when this method returns
        try? FileManager.default.moveItem(at: tmp, to: destination(for: downloadTask))
    }
    func urlSessionDidFinishEvents(forBackgroundURLSession s: URLSession) {
        DispatchQueue.main.async { self.backgroundCompletion?(); self.backgroundCompletion = nil }
    }
}

// AppDelegate
func application(_ app: UIApplication, handleEventsForBackgroundURLSession id: String,
                 completionHandler: @escaping () -> Void) {
    Transfers.shared.backgroundCompletion = completionHandler
    _ = Transfers.shared.session       // recreate the session with the same identifier
}
```

## Rules and gotchas
- Use one session per identifier; recreate it on every launch so pending delegate callbacks are delivered.
- Background sessions support only download and upload tasks (not data tasks), and uploads must come from a file: `uploadTask(with:fromFile:)`, not from `Data` or a stream.
- Only delegates are supported, not completion-handler APIs.
- Force-quitting the app from the app switcher cancels background transfers.
- Call the system completion handler promptly, or the system penalises later background launches.
- SwiftUI apps use `.backgroundTask(.urlSession("id"))` instead of the app-delegate method (iOS 16+).

Verify: start a large download, background the app, toggle Wi-Fi off and on, and confirm the file completes; use `log stream --predicate 'subsystem == "com.apple.CFNetwork"'` or console logs to see relaunch events.
