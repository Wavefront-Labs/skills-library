---
id: computing-software.software-engineering.mobile-development.mobile-navigation-architecture
name: mobile-navigation-architecture
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ui, mobile-navigation, navigation-compose, navigationstack, deep-links, back-stack]
level: practitioner
status: draft
description: "Design mobile navigation: Navigation Compose type-safe routes and SwiftUI NavigationStack paths, tabs with separate back stacks, deep-link entry, state restoration and testing."
sources:
  - https://developer.android.com/guide/navigation
  - https://developer.android.com/guide/navigation/design/type-safety
  - https://developer.apple.com/documentation/swiftui/navigationstack
  - https://developer.android.com/guide/navigation/principles
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile navigation architecture

**Goal:** predictable back behaviour, deep links that build the right back stack, per-tab history, and navigation state that survives process death.

## 1. Principles (Android and iOS alike)
- A fixed start destination; Back/Up returns towards it.
- Deep links create a **synthetic back stack** (opening an order from a notification lands on Order with Orders list behind it).
- Navigation is driven by state/events from screens, not by screens holding references to each other.
- Pass IDs between screens, not large objects; the destination loads data by ID.

## 2. Android: Navigation Compose with type-safe routes (2.8+)
```kotlin
@Serializable object Orders
@Serializable data class OrderDetail(val orderId: String)

NavHost(navController, startDestination = Orders) {
    composable<Orders> { OrdersScreen(onOpen = { id -> navController.navigate(OrderDetail(id)) }) }
    composable<OrderDetail>(
        deepLinks = listOf(navDeepLink<OrderDetail>(basePath = "https://acme.com/orders"))
    ) { entry ->
        val route = entry.toRoute<OrderDetail>()
        OrderDetailScreen(route.orderId, onBack = navController::navigateUp)
    }
}
```
ViewModels read arguments via `SavedStateHandle.toRoute<OrderDetail>()`. Avoid duplicate destinations from double taps: `launchSingleTop = true`.

Bottom navigation with separate back stacks:
```kotlin
navController.navigate(tab.route) {
    popUpTo(navController.graph.findStartDestination().id) { saveState = true }
    launchSingleTop = true
    restoreState = true
}
```

## 3. iOS: NavigationStack with a path
```swift
enum Route: Hashable, Codable { case order(id: String), settings }

@Observable final class Router { var path = NavigationPath() }

struct RootView: View {
    @State private var router = Router()
    var body: some View {
        NavigationStack(path: $router.path) {
            OrdersView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .order(let id): OrderDetailView(id: id)
                    case .settings: SettingsView()
                    }
                }
        }
        .environment(router)
        .onOpenURL { url in if let id = parseOrderID(url) { router.path = NavigationPath([Route.order(id: id)]) } }
    }
}
```
`NavigationPath` with `Codable` routes can be saved (`path.codable`) to `@SceneStorage` for restoration. `TabView` with one `NavigationStack` per tab gives per-tab history. UIKit apps often use a coordinator pattern around `UINavigationController`.

## 4. Modals vs push
Push for drill-down within a flow; sheets/full-screen covers for self-contained tasks (compose, login) that return a result. Keep modal flows in their own stack.

## 5. Testing
- Android: `TestNavHostController` + Compose UI tests; assert `currentBackStackEntry`.
- iOS: unit-test the `Router` (path contents after events); UI tests launch with a deep link URL.

## Gotchas
- Navigating from a composable body (not an event callback) loops on recomposition.
- Passing objects via routes bloats saved state (TransactionTooLargeException on Android); pass IDs.
- Programmatic pops during animations can be dropped on iOS; drive from state, not imperative calls in sequence.
- Process death: test with "Don't keep activities" (Android) and simulated termination (iOS).

## Verify
- From a cold start, tapping a deep link opens the detail screen and Back goes to the list; switching tabs preserves each tab's stack; navigation state survives a process kill.
