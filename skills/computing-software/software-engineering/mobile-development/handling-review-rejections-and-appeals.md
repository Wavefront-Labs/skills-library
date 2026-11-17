---
id: computing-software.software-engineering.mobile-development.handling-review-rejections-and-appeals
name: handling-review-rejections-and-appeals
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, app-rejection, app-review, play-policy, appeals, resolution-center, policy-compliance, app-store-connect]
level: practitioner
status: draft
description: "Respond to App Store rejections and Google Play policy actions: read the cited guideline, reply in Resolution Center, fix or clarify, appeal correctly, and avoid repeat strikes."
sources: ["https://developer.apple.com/distribute/app-review/", "https://developer.apple.com/app-store/review/guidelines/", "https://support.google.com/googleplay/android-developer/answer/9899234", "https://support.google.com/googleplay/android-developer/answer/2477981"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handling review rejections and appeals

**Goal:** get a rejected build or suspended app back into the store quickly, without escalating
risk to the developer account.

## Apple: read the rejection precisely
- The message in App Store Connect's **App Review** section (Resolution Center) cites guideline
  numbers (for example 2.1 App Completeness, 4.3 Spam, 5.1.1 Data Collection, 3.1.1 In-App
  Purchase, 4.2 Minimum Functionality, 2.3 Accurate Metadata) and often screenshots.
- Classify: a **bug or missing item** (crash, broken login, missing demo account, placeholder
  content), **metadata** issue (fix in App Store Connect, no new build needed), **policy
  disagreement** (reviewer misunderstood a feature), or **business model** issue (payments, IAP).

## Apple: responding
- Missing information (demo account, how to reach a feature, hardware needed): reply in the thread
  with exact steps and credentials, and fill **App Review Information** notes for future
  submissions. Provide a demo video link for hardware-dependent or hard-to-reach features.
- Bug: fix, increment build number, resubmit, and reply explaining what changed.
- Disagreement: reply calmly with facts mapped to the guideline text (what the feature does, why it
  complies). You can request a **phone call** with App Review from the thread.
- If the reply fails, submit an **appeal to the App Review Board** (contact form) - one clear
  argument, evidence, no repeated submissions of the same build hoping for a different reviewer.
- Bug-fix exception: for apps already live, Apple may let a bug-fix update through while you
  address a non-legal guideline issue in the next version - ask in the reply.
- Metadata rejections can often be resolved by editing metadata and replying, without a new binary.

## Google Play: policy enforcement types
| Action | Meaning |
|---|---|
| Update rejected | the new release is blocked; live version unaffected |
| App removed | app taken down; fix and resubmit |
| App suspended | a strike; repeated suspensions can terminate the account |
| Limited visibility / warnings | fix by a deadline |
- Details appear in the Play Console **Policy status** page and email, with the policy, the issue,
  and sometimes the offending screen or APK.
- Common causes: Data safety form mismatched with SDK behaviour, permissions without approved
  declaration (SMS/Call Log, `MANAGE_EXTERNAL_STORAGE`, background location, foreground service types,
  exact alarms), missing account deletion path, deceptive behaviour, metadata policy (keyword stuffing,
  misleading icons), target API level deadlines, ads policy issues from SDKs.

## Google Play: responding
- Fix the issue in a new release (increment versionCode), update declarations (Data safety, Permissions
  declarations, App content) to match, and submit.
- If you believe it is a mistake, use the **appeal** link in the policy notice within the stated
  window; explain with evidence (screenshots, code behaviour, documentation). Appeals for suspensions
  should be precise - vague appeals are rejected.
- Check **all tracks** (internal/closed tests, old APKs still in active tracks): Play reviews them too;
  deactivate artefacts containing the violating SDK or permission.
- Audit third-party SDKs: many policy violations come from ad/analytics SDK versions; update or remove.

## Prevention
- Pre-submission checklist: demo account, complete features, no placeholders, accurate screenshots,
  privacy policy URL, account deletion, privacy manifests/Data safety in sync, IAP for digital goods
  where required.
- Track guideline and policy updates (Apple's yearly WWDC changes, Play policy deadlines) on a
  release calendar.
- Use phased release/staged rollout so a rejected hotfix does not block an urgent fix path; keep a
  minimal-change branch ready.

## Verify
- [ ] Every rejection logged with guideline, root cause and prevention action.
- [ ] App Review Information/Play declarations updated alongside fixes.
- [ ] No outstanding policy warnings in Play Console Policy status.
