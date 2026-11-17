---
id: computing-software.software-engineering.mobile-development.home-screen-widgets-widgetkit-and-glance
name: home-screen-widgets-widgetkit-and-glance
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, widgetkit, glance-widgets, app-widgets, timeline-provider, app-intents, live-activities, jetpack-glance]
level: practitioner
status: draft
description: "Build home screen widgets with WidgetKit (timelines, App Groups, interactive App Intents) and Jetpack Glance (GlanceAppWidget, updates, actions) within refresh budgets."
sources: ["https://developer.apple.com/documentation/widgetkit", "https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date", "https://developer.android.com/develop/ui/compose/glance", "https://developer.android.com/develop/ui/views/appwidgets/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Home screen widgets (WidgetKit / Glance)

**Goal:** glanceable widgets that show fresh-enough data, update within platform budgets, and deep
link into the right screen.

## Shared principles
- Widgets run in a separate process/extension with strict memory and time limits; they display data
  the app already prepared. Do heavy work in the app or a background task and share results.
- Updates are budgeted by the system - design for "fresh enough", not real time.
- Tapping a widget should deep link to the specific content shown.

## iOS: WidgetKit
```swift
struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> Entry { .sample }
    func getSnapshot(in context: Context, completion: @escaping (Entry) -> Void) { completion(.sample) }
    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> Void) {
        let data = SharedStore.load()                         // App Group container
        let entries = (0..<4).map { i in Entry(date: .now.addingTimeInterval(Double(i) * 900), data: data) }
        completion(Timeline(entries: entries, policy: .atEnd))
    }
}
@main struct OrdersWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Orders", provider: Provider()) { entry in
            OrdersView(entry: entry).containerBackground(.fill.tertiary, for: .widget)
                .widgetURL(URL(string: "myapp://orders"))
        }
        .supportedFamilies([.systemSmall, .systemMedium, .accessoryRectangular])
    }
}
```
- Share data via an **App Group** (`UserDefaults(suiteName:)`, shared files, SwiftData/Core Data in the
  group container); Keychain sharing for tokens if the widget fetches.
- After the app changes data: `WidgetCenter.shared.reloadTimelines(ofKind: "Orders")`. System budget
  is roughly 40-70 refreshes per day for frequently viewed widgets; reloads triggered while the app
  is in the foreground do not count.
- Timeline entries for known future states (countdowns, schedules) avoid refreshes; `Text(date, style: .timer)`
  animates without updates.
- **Interactive widgets** (iOS 17): `Button(intent: ToggleTaskIntent(id:))` / `Toggle` running an
  `AppIntent` in the widget process; configuration via `AppIntentConfiguration`.
- Lock Screen / StandBy / watch accessory families; Live Activities (ActivityKit) for ongoing
  events updated by push.

## Android: Jetpack Glance
```kotlin
class OrdersWidget : GlanceAppWidget() {
    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val orders = OrdersRepository(context).latest()          // load before provideContent
        provideContent {
            GlanceTheme {
                Column(GlanceModifier.fillMaxSize().background(GlanceTheme.colors.surface).padding(12.dp)
                        .clickable(actionStartActivity<MainActivity>())) {
                    Text("Orders: ${orders.size}")
                    Button("Refresh", onClick = actionRunCallback<RefreshAction>())
                }
            }
        }
    }
}
class OrdersWidgetReceiver : GlanceAppWidgetReceiver() { override val glanceAppWidget = OrdersWidget() }
```
Manifest receiver with `APPWIDGET_UPDATE` intent filter and `appwidget-provider` XML (min sizes,
`targetCellWidth/Height`, `previewLayout`, `widgetCategory`, `updatePeriodMillis`).
- Glance is Compose-like but translates to RemoteViews: only Glance composables (no arbitrary
  Compose), limited layouts.
- Update from the app: `OrdersWidget().updateAll(context)` or `update(context, glanceId)`;
  schedule periodic refreshes with WorkManager (`updatePeriodMillis` minimum is 30 minutes and wakes
  the device - prefer WorkManager with constraints).
- Per-widget state with `PreferencesGlanceStateDefinition` and `updateAppWidgetState`.
- Provide generated previews (Android 15 `setWidgetPreview`) and responsive `SizeMode.Responsive`
  layouts for different sizes.

## Verify
- [ ] Widget shows correct data after app changes (reload/update called).
- [ ] Placeholder/preview renders without network.
- [ ] Taps deep link to the specific item; refresh frequency within budget (no excessive wakeups).
