---
id: computing-software.devops-ci-cd.jenkins.notifications-slack-email-and-post-conditions
name: notifications-slack-email-and-post-conditions
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, notifications, slack-notification, slack-plugin, slacksend, email-ext, emailext, mailer, mail-step, post-conditions, post-always, post-failure, post-fixed, post-regression, post-changed, post-unstable, culprits, requestor, developers-recipient, notify-on-change, teams-notification, office-365-connector, matrix-notifications, github-checks, commit-status, build-status-badge, alert-fatigue]
level: practitioner
status: docs-checked
description: "Notify from Jenkins without alert fatigue: post fixed/regression/changed conditions, slackSend threads, emailext recipient providers, Teams, commit status and Checks."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/#post", "https://plugins.jenkins.io/slack/", "https://plugins.jenkins.io/email-ext/", "https://plugins.jenkins.io/office-365-connector/", "https://plugins.jenkins.io/github-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notifications: Slack, email and post conditions

**Goal:** people hear about a build exactly when it changes state, with the commit, the
culprit and a link — and nothing else.

## 1. Post conditions — notify on *change*, not on every run
```groovy
post {
  success    { … }        // this build green
  unstable   { … }        // tests failed
  failure    { … }        // build broke
  aborted    { … }
  changed    { … }        // status differs from previous build (any direction)
  fixed      { … }        // previous failed/unstable, now success  ← the "good news" ping
  regression { … }        // previous success, now worse            ← the "bad news" ping
  always     { junit …; cleanWs() }
  cleanup    { … }        // after all other post blocks, regardless
}
```
The reference lists the conditions in the order `always, changed, fixed, regression, aborted,
failure, success, unstable, unsuccessful, cleanup` (`cleanup` runs after every other
condition has been evaluated). `regression` fires when the run is failure, unstable or
aborted and the previous run was successful. A pipeline that posts to Slack on `failure`
spams the channel every 10 minutes while main is red; `regression` + `fixed` (plus
`unstable` on PR jobs only) is the sane default. For PR jobs, prefer commit status/Checks
over chat.

Check `currentBuild.result` / `currentBuild.currentResult` semantics in the Pipeline
global-variable reference before relying on them for custom change detection.

## 2. Slack
Slack plugin with a **Slack app** bot token stored as a credential (see the plugin page for
the required scopes). JCasC:
```yaml
unclassified:
  slackNotifier:
    teamDomain: example
    tokenCredentialId: slack-bot
    botUser: true
```
```groovy
post {
  regression {
    slackSend channel: '#team-a-builds', color: 'danger',
      message: "FAILED ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
  }
  fixed {
    slackSend channel: '#team-a-builds', color: 'good', message: "FIXED ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
  }
}
```
- Threads: `def r = slackSend(message: 'Deploy started…'); slackSend(channel: r.threadId, message: 'done')`
  — keep a deploy's chatter in one thread (`slackResponse.threadId` requires `botUser: true`).
- `slackUploadFile` for logs/screenshots; `blocks:` for Block Kit (the attachments API is
  legacy and lacks blocks, file uploads and threads).
- Use a channel per team.
- Invite the Jenkins bot user into each channel you want notifications in.

## 3. Email
`mail` (Mailer, basic) vs `emailext` (Email Extension: templates, recipient providers,
attachments):
```groovy
post {
  regression {
    emailext subject: '[FAILED] ${JOB_NAME} #${BUILD_NUMBER}',
      body: 'See ${BUILD_URL}',        // content tokens and templates: see the Email Extension page
      recipientProviders: [culprits(), requestor(), developers()],
      to: 'team-a@example.com'
  }
}
```
Configure SMTP and the default user e-mail suffix in *Manage Jenkins → System* so Git
usernames map to addresses. Per the Email Extension page, the Culprits provider together
with Developers includes everyone who committed since the last successful build. The
recipient providers can also be used with Mailer via `emailextrecipients([...])`.

## 4. Microsoft Teams, Matrix, others
Teams: Office 365 Connector plugin (`office365ConnectorSend webhookUrl: …`; its page covers
both connector and Power Automate workflow webhooks). Generic: `httpRequest` to any webhook
with a JSON body. Keep webhook URLs in credentials.

## 5. Commit status and Checks instead of chat
Multibranch jobs with GitHub branch source send commit statuses through the Status API;
the GitHub Checks plugin publishes richer Checks. This is where PR authors look — chat
pings for PR failures are redundant. The Embeddable Build Status plugin provides README
badges.

## 6. Anti-patterns
- `post { always { slackSend … } }` — noise; nobody reads it after a week.
- Notifying `success` on main for every merge in a busy repo.
- Emailing `developers()` on `unstable` of a flaky suite — fix the flake instead.
- Putting the Slack token in the Jenkinsfile instead of a credential.
- Catching exceptions in `script {}` and swallowing them so `post { failure }` never fires;
  rethrow.

## Verify
- [ ] Breaking main yields exactly one Slack message (regression); the fix yields one (fixed); the next green build yields none.
- [ ] Email on regression lists changes and failed tests and goes to culprits.
- [ ] PR failures show as commit status/Checks in the SCM UI.
- [ ] No tokens/webhook URLs appear in Jenkinsfiles.

## Checked
2026-11-02. Confirmed against the Pipeline syntax post section, Slack, Email Extension and Office 365 Connector plugin pages: post condition list and definitions (changed, fixed, regression), slackSend blocks/threadId/slackUploadFile, botUser, teamDomain, tokenCredentialId, invite the bot, legacy attachments, Email Extension recipient providers and Culprits wording, emailextrecipients with Mailer, Office 365 workflow webhooks. Removed: evaluation-order claim including notBuilt, currentBuild.result behaviour, notifyCommitters, email token and attachment options, GitLab/Bitbucket plugin claims, badge URL, 2024 Teams date.
Method: documentation only; no commands were run.
