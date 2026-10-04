# Upstream base and updates

- Repository: https://github.com/forkgram/TelegramAndroid
- Stable release: `12.10.7.0`
- Base commit: `c64d60d3fa9e95559ce343f275f7b70eb4761fa7`
- Release: https://github.com/forkgram/TelegramAndroid/releases/tag/12.10.7.0
- Verified: 2026-10-04
- Project: Quietgram

## Git layout

`upstream` points to Forkgram. `origin` points to Quietgram. `telegram` points to `https://github.com/DrKLO/Telegram.git` for comparison only. The initial `dev` branch is an unchanged upstream baseline; `quietgram` holds the project patch stack. Published release tags must never move.

Keep project setup, app identity, Search restrictions, and Archive restrictions in separate commits. Make changes in upstream files as small as practical. Do not merge official Telegram directly into the project patch branch: Forkgram owns that integration.

## Preparing an update

1. Fetch `upstream` with its tags and choose an actual stable release, not a moving development head.
2. Record the current patch tip and base commit. Create a candidate branch from the patch tip.
3. Run `git rebase --onto NEW_BASE OLD_BASE candidate`, substituting exact commits.
4. Review conflicts and use `git range-diff OLD_BASE..OLD_TIP NEW_BASE..candidate` to compare the patches.
5. Review new Search and Archive entry points even when there are no conflicts. Confirm inherited publishing jobs remain restricted to upstream.
6. Run build checks and the phone checklist. Update this document with the new base and commit the provenance change.
7. Publish a new immutable source tag and signed APK only after validation.

For steps 2–4, use the helper after fetching and verifying the chosen release:

```sh
bash scripts/quietgram-rebase.sh OLD_BASE NEW_BASE quietgram-update-VERSION
```

The helper refuses a dirty tree or an existing candidate branch, preserves the previous branch, and prints the patch range-diff. If a conflict occurs, resolve it on the candidate and run `git rebase --continue`, or return to the previous branch with `git rebase --abort`. It does not publish or update the provenance document automatically.

## Build baseline

Upstream requests Gradle 8.13, SDK 36, Build Tools 36.0.0, NDK 27.2.12479018, and CMake 3.22.1. Its current CI uses JDK 17. Native dependencies and all submodules are needed for an APK; Java configuration checks require at least the `TMessagesProj/lib/jlatexmath` and `TMessagesProj_Modules/media` submodules.

The checked-in upstream test keystore is public. It is suitable only for disposable build checks. It must not sign Quietgram phone releases. The final release needs its own application ID, icon, project-specific Telegram API credentials, and a backed-up private signing key. These remain checklist items until the baseline build is working.
