---
id: computing-software.software-engineering.mobile-development.release-automation-with-fastlane
name: release-automation-with-fastlane
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, fastlane, ci-cd, app-store-connect-api, match, supply]
level: practitioner
status: docs-checked
description: "Automate iOS and Android builds, signing, screenshots, metadata and store uploads with fastlane lanes, App Store Connect API keys and CI."
sources:
  - https://docs.fastlane.tools/
  - https://docs.fastlane.tools/app-store-connect-api/
  - https://docs.fastlane.tools/actions/match/
  - https://docs.fastlane.tools/actions/supply/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release automation with fastlane

**Goal:** one command (run by CI) builds, signs, versions and uploads both apps, so releases are routine and reproducible.

## 1. Setup
```bash
gem install bundler && bundle init && echo 'gem "fastlane"' >> Gemfile && bundle install
bundle exec fastlane init
```
Run fastlane through Bundler (`bundle exec`) so CI and developers use the same version (commit `Gemfile.lock`).

## 2. iOS lanes
```ruby
# fastlane/Fastfile
platform :ios do
  before_all do
    app_store_connect_api_key(key_id: ENV["ASC_KEY_ID"], issuer_id: ENV["ASC_ISSUER_ID"],
                              key_content: ENV["ASC_KEY_P8"])
  end

  lane :beta do
    setup_ci                                            # temporary keychain on CI
    match(type: "appstore", readonly: true)
    increment_build_number(build_number: ENV["CI_BUILD_NUMBER"])
    build_app(scheme: "App", export_method: "app-store")
    upload_to_testflight(skip_waiting_for_build_processing: true, changelog: changelog_from_git_commits(merge_commit_filtering: "exclude_merges"))
  end

  lane :release do
    build_app(scheme: "App")
    upload_to_app_store(submit_for_review: true, automatic_release: false, phased_release: true,
                        precheck_include_in_app_purchases: false, force: true)
  end
end
```
Authenticate with an App Store Connect API key via fastlane's `app_store_connect_api_key` action (key id, issuer id, key content or file path; the API uses JWT authorisation). `setup_ci` creates a temporary keychain for use with `match` on CI. `skip_waiting_for_build_processing: true` skips remaining processing (no external distribution); with a changelog it still waits until the build appears so the changelog can be set.

## 3. Android lanes
```ruby
platform :android do
  lane :internal do
    gradle(task: "bundle", build_type: "Release",
           properties: { "android.injected.version.code" => ENV["CI_BUILD_NUMBER"].to_i })
    upload_to_play_store(track: "internal", aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH],
                         json_key_data: ENV["PLAY_SERVICE_ACCOUNT_JSON"])
  end
  lane :promote do
    upload_to_play_store(track: "internal", track_promote_to: "production", rollout: "0.05",
                         skip_upload_aab: true, skip_upload_metadata: true, json_key_data: ENV["PLAY_SERVICE_ACCOUNT_JSON"])
  end
end
```
The Play service account needs release permissions for the app in Play Console.

## 4. Metadata and screenshots as code
- `fastlane deliver init` downloads existing App Store Connect metadata into `./fastlane/metadata` (also `screenshots`, `app-previews`); `supply init` does the same for Google Play. Keep the metadata (not the screenshots) in git, edit locally and push back with the release lanes.
- `snapshot` (iOS) and `screengrab` (Android) capture screenshots; `frameit` adds device frames.

## 5. CI
```yaml
- run: bundle exec fastlane ios beta
  env: { MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}, ASC_KEY_P8: ${{ secrets.ASC_KEY_P8 }}, ... }
```
`match` reads its encryption passphrase from the `MATCH_PASSWORD` environment variable.
## Gotchas
- fastlane actions wrap Apple/Google APIs that change; keep fastlane updated.
- `match` option `readonly` (default false) only fetches existing certificates and profiles when true; keep CI read-only so it does not generate new ones.
- Prefer passing build numbers as parameters rather than relying on project-file changes persisting on CI.

## Verify
- A tag push runs `fastlane ios beta` and `fastlane android internal` end to end on CI with no interactive prompts, and builds appear in TestFlight and the Play internal track.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against docs.fastlane.tools: home, App Store Connect API, match, supply, deliver (upload_to_app_store), upload_to_testflight, setup_ci, gradle, changelog_from_git_commits, snapshot, screengrab, frameit and increment_build_number. Removed: `is_key_content_base64`, `default_platform`, the Apple-ID-2FA claim, dependency-caching advice, and the claim that `readonly: false` can nuke certificates. The `rollout: "0.05"` and ENV variable names are illustrative values, not documented defaults.
