---
id: computing-software.software-engineering.mobile-development.webview-security
name: webview-security
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, webview-security, android-webview, wkwebview, javascript-interface, custom-tabs, safari-view-controller, xss, url-allowlist]
level: advanced
status: draft
description: "Secure Android WebView and WKWebView: restrict navigation to allowlisted origins, safe JavaScript bridges, file access settings, and when to use Custom Tabs instead."
sources: ["https://developer.android.com/develop/ui/views/layout/webapps/webview", "https://developer.android.com/privacy-and-security/risks/unsafe-use-of-javascriptinterface", "https://developer.apple.com/documentation/webkit/wkwebview", "https://mas.owasp.org/MASTG/", "https://developer.chrome.com/docs/android/custom-tabs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebView security

**Goal:** embed web content without turning the app into a bridge that web attackers can use to
reach native APIs, local files or user sessions.

## First: should this be a WebView?
- Showing third-party or arbitrary web pages (links, help articles, OAuth login): use **Custom
  Tabs** (Android) or **SFSafariViewController / ASWebAuthenticationSession** (iOS). They run in the
  browser's process, share its security model, and the app cannot read the content.
- WebView only for **your own** trusted content that needs tight integration.

## Android WebView settings
```kotlin
webView.settings.apply {
    javaScriptEnabled = true               // only if needed
    allowFileAccess = false                // default false on API 30+; keep it false
    allowContentAccess = false
    allowFileAccessFromFileURLs = false    // deprecated, default false
    allowUniversalAccessFromFileURLs = false
    domStorageEnabled = true               // if the app needs it
    mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
    setSupportMultipleWindows(false)
}
WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)   // never true in release
```
- Load local assets via `WebViewAssetLoader` (`https://appassets.androidplatform.net/assets/...`)
  instead of `file://` URLs, so same-origin policy applies normally.
- Restrict navigation:
```kotlin
webView.webViewClient = object : WebViewClient() {
    override fun shouldOverrideUrlLoading(view: WebView, req: WebResourceRequest): Boolean {
        val uri = req.url
        val allowed = uri.scheme == "https" && uri.host in setOf("app.example.com", "cdn.example.com")
        if (!allowed) { openInBrowser(uri); return true }   // block in WebView
        return false
    }
    override fun onReceivedSslError(v: WebView, h: SslErrorHandler, e: SslError) { h.cancel() } // never proceed()
}
```
  Match hosts exactly (not `endsWith("example.com")`, which accepts `evilexample.com`); parse with
  `Uri`, never string prefix checks.

## JavaScript bridges
- `addJavascriptInterface(obj, "Native")` exposes every `@JavascriptInterface` method to **any page
  loaded in that WebView, including iframes**. Only add bridges when navigation is locked to your
  origins; expose minimal, validated methods; never expose file, shell, or token-returning methods.
- Prefer `WebViewCompat.addWebMessageListener(webView, "native", setOf("https://app.example.com"), listener)`
  (AndroidX WebKit): messages are accepted only from allowlisted origins and the listener sees the
  sender's origin.
- `evaluateJavascript` with data from untrusted sources: JSON-encode values, never concatenate
  strings into script.

## iOS WKWebView
- UIWebView is removed; use WKWebView (separate web content process).
- Navigation policy:
```swift
func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction) async -> WKNavigationActionPolicy {
    guard let url = action.request.url, url.scheme == "https", allowedHosts.contains(url.host() ?? "") else {
        if let url = action.request.url { await UIApplication.shared.open(url) }
        return .cancel
    }
    return .allow
}
```
- Script message handlers (`WKScriptMessageHandler`): check `message.frameInfo.isMainFrame` and
  `message.frameInfo.securityOrigin` before acting; validate the body. Use `WKContentWorld` to isolate
  your injected scripts from page scripts.
- `loadFileURL(_:allowingReadAccessTo:)` with the narrowest directory; never grant read access to the
  whole Documents directory.
- `isInspectable = false` in release (iOS 16.4+ defaults to non-inspectable).

## Sessions and data
- Do not inject long-lived auth tokens into page JavaScript; prefer short-lived tokens or cookies
  set for your domain only (`CookieManager`, `WKHTTPCookieStore`), and clear them on logout
  (`WebStorage.deleteAllData`, `WKWebsiteDataStore.removeData`).
- Content Security Policy on your pages limits XSS impact inside the WebView.

## Verify
- [ ] Navigating to a non-allowlisted URL opens the browser instead of loading in the WebView.
- [ ] Bridges reject messages from other origins/iframes (test with a malicious page).
- [ ] Release builds: debugging disabled, file access off, SSL errors cancelled.
