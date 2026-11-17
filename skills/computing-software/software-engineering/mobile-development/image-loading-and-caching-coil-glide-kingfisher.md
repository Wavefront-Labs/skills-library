---
id: computing-software.software-engineering.mobile-development.image-loading-and-caching-coil-glide-kingfisher
name: image-loading-and-caching-coil-glide-kingfisher
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, image-loading, coil, glide, kingfisher, asyncimage, image-caching, downsampling, memory]
level: practitioner
status: draft
description: "Load remote images efficiently on mobile with Coil, Glide and Kingfisher: memory/disk caching, downsampling to view size, placeholders, list performance and OOM avoidance."
sources: ["https://coil-kt.github.io/coil/", "https://bumptech.github.io/glide/", "https://github.com/onevcat/Kingfisher", "https://developer.android.com/topic/performance/graphics/load-bitmap"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image loading and caching (Coil / Glide / Kingfisher)

**Goal:** images that appear fast, scroll smoothly in lists, survive offline via caches, and never
crash the app with out-of-memory errors.

## Why use a library
A loader handles request deduplication, cancellation when views are recycled, memory cache (decoded
bitmaps), disk cache (encoded bytes), **downsampling** to the target size, transformations, and
lifecycle awareness. Hand-rolled `BitmapFactory.decodeStream` or `Data(contentsOf:)` loaders get
these wrong.

## Android: Coil (Compose-first, Kotlin coroutines)
```kotlin
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)
        .data(user.avatarUrl)
        .crossfade(true)
        .build(),
    contentDescription = user.name,
    placeholder = painterResource(R.drawable.avatar_placeholder),
    error = painterResource(R.drawable.avatar_error),
    contentScale = ContentScale.Crop,
    modifier = Modifier.size(48.dp).clip(CircleShape),
)
```
- Coil 3 (`io.coil-kt.coil3`) is Kotlin Multiplatform; add a network fetcher artifact
  (`coil-network-okhttp` or `coil-network-ktor3`).
- Configure one `ImageLoader` app-wide (`SingletonImageLoader.Factory`) with memory cache percentage,
  disk cache size, and your shared OkHttp client.
- Size: AsyncImage resolves the size from constraints; give images a bounded size in layouts so the
  decoded bitmap is small.

## Android: Glide (Views, mature)
```kotlin
Glide.with(fragment).load(url).placeholder(R.drawable.ph).centerCrop().into(imageView)
```
Use `with(fragment)`/`with(view)` (lifecycle-bound), not application context, so requests cancel
on destroy. Glide downsamples to the ImageView size automatically.

## iOS: Kingfisher (or Nuke, SDWebImage)
```swift
KFImage(url)
    .placeholder { ProgressView() }
    .setProcessor(DownsamplingImageProcessor(size: CGSize(width: 96, height: 96)))
    .scaleFactor(UIScreen.main.scale)
    .cacheOriginalImage()
    .fade(duration: 0.2)
    .resizable().frame(width: 48, height: 48).clipShape(Circle())
// UIKit: imageView.kf.setImage(with: url, options: [.processor(DownsamplingImageProcessor(size: imageView.bounds.size)), .scaleFactor(UIScreen.main.scale)])
```
- SwiftUI's built-in `AsyncImage` has **no disk or memory cache beyond URLCache** and no
  downsampling - fine for a prototype, not for feeds.
- Decoding a 4000x3000 photo costs about 48 MB of memory regardless of JPEG file size; always
  downsample (ImageIO `CGImageSourceCreateThumbnailAtIndex` under the hood).

## Practices
- **Request appropriately sized images from the server/CDN** (`?w=96&dpr=3`, AVIF/WebP); the cheapest
  pixel is the one never downloaded.
- Stable cache keys: strip expiring signed-URL query params via a custom key, or caches never hit.
- Prefetch the next items in lists (Coil `imageLoader.enqueue`, Kingfisher `ImagePrefetcher`, list
  prefetch callbacks).
- Clear memory caches on `onTrimMemory`/memory warnings (libraries hook these by default).
- Set content descriptions / accessibility labels; decorative images null / `.accessibilityHidden(true)`.
- GIF/SVG/video frames need extra decoders (`coil-gif`, `coil-svg`, `coil-video`).

## Verify
- [ ] Memory profiler shows bitmap sizes close to on-screen size while scrolling a feed.
- [ ] Second launch offline shows cached images.
- [ ] No jank when flinging an image-heavy list on a low-end device.
