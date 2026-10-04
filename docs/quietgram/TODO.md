# Quietgram project checklist

Working name: Quietgram. GitHub account: Danyalo (verified through the GitHub connector on 2026-10-04).

## Agreed scope

A personal Forkgram fork for GrapheneOS. Hide global Search and Archive, including gestures and alternative UI entry points. Preserve direct messaging, contacts, in-conversation search, and Forkgram's notification behavior. Individual chats can still open through links, notifications, or forwarded messages. No chat blocklist, allowlist, server, or protocol changes.

## 1. Repository and baseline — Codex

- [x] Verify the connected GitHub account and repository access.
- [x] Create a public GitHub fork under Danyalo, with a distinct project name.
- [x] Clone upstream and pin a stable Forkgram release by full commit SHA.
- [x] Read repository instructions and audit inherited build/release workflows.
- [x] Record upstream provenance and a repeatable update procedure.

## 2. Build and app identity — Codex

- [x] Pass upstream Gradle configuration and patched Java/Kotlin compilation checks.
- [x] Prepare CI for Java compilation without private credentials or native linking.

- [ ] Establish a successful baseline build using pinned SDK/NDK/JDK versions.
- [ ] Set a separate application ID, app label, and icon without renaming upstream Java packages.
- [ ] Configure user-owned Telegram API credentials without committing them.
- [ ] Create a release signing key; arrange an encrypted backup.
- [ ] Establish monotonically increasing final APK version codes.
- [ ] Add unsigned candidate-build CI and a separately controlled signing/release workflow.

## 3. Small UI patch stack — Codex

- [x] Commit global Search visibility and entry-point restrictions separately.
- [x] Commit Archive row, pull-down, and screen navigation restrictions separately.
- [x] Preserve contact selection and search inside existing conversations.
- [x] Review the diff for unrelated formatting, dependency, notification, or protocol changes.

## 4. Verify on GrapheneOS — Codex + user

- [ ] Build the patched APK and verify its package, version, and signature.
- [ ] User: install alongside Forkgram and log into Telegram.
- [ ] User: check Search controls/gestures, Archive row/pull-down, and alternative Archive entry points.
- [ ] User: check direct messages, contacts, forwarding, in-chat search, media, and calls.
- [ ] User: check notifications with no Google services, screen off, after reboot, and across network changes.

## 5. Releases and Obtainium — Codex + user

- [ ] Publish a tagged signed APK with exact upstream/source SHAs and checksum.
- [ ] User: add the new repository to Obtainium and select the intended APK.
- [ ] Publish a second version and verify that Obtainium updates it without losing app data.
- [x] Save a concise release and phone-test checklist in the repository.

## 6. Upstream updates — Codex

- [ ] Add a repeatable command to replay only our commits onto a new stable Forkgram base.
- [ ] Rehearse one update and inspect the resulting patch stack.
- [ ] Require build checks and behavioral review before publishing updates.

## User input needed later

Codex handles source changes, repository setup where available, CI, packaging, documentation, and update preparation. The user supplies Telegram API credentials through an appropriate local/secret mechanism, keeps the signing-key backup, and performs tests on the physical phone. Never paste signing passwords or private keys into public files.

## Current status

Public fork: https://github.com/Danyalo/Quietgram. Connector write access and Git push authentication are verified. Local source is pinned to Forkgram 12.10.7.0, commit c64d60d3fa9e95559ce343f275f7b70eb4761fa7. No AGENTS.md or RTK.md was found in the searched workspace/ancestors or upstream checkout.

Search and Archive patches are separate commits. The behavioral patch changes only DialogsActivity and DialogsAdapter. Inherited publishing jobs are restricted to forkgram/TelegramAndroid; Quietgram has a separate Java compilation workflow. Upstream Gradle configuration and patched Java/Kotlin compilation succeeded locally with JDK 21. Native linking was deliberately excluded, so this is not an APK build. Final recompilation after the pinned-reordering adjustment also succeeded (138 tasks, 47 seconds).

Next: establish an APK build, give it its own application ID/label/icon, configure user-owned API credentials, create/back up its private release key, and test on GrapheneOS. No APK, release signing key, or phone release has been created.
