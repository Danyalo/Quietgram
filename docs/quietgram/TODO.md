# Quietgram development checklist

## Scope

Hide global Search and Archive UI access while preserving direct messaging, contacts, local recipient selection, in-conversation search, and upstream notification behavior. Individual chats may still open through links, notifications, forwarded messages, or custom folders.

## Source and upstream updates

- Pin a stable upstream release by its full commit SHA.
- Keep UI changes, packaging, and build infrastructure in separate commits.
- Keep patches to upstream files small and review new UI entry points on every update.
- Rebase onto a new pinned upstream base on a separate candidate branch.
- Compare the patch stack and run build and acceptance checks before publication.

## Build and release

- Use the documented SDK, NDK, JDK, and build-tool versions.
- Keep the application identity distinct from upstream without renaming source namespaces.
- Supply project-specific Telegram API credentials through build secrets.
- Build unsigned ARM64 candidates and inspect package, label, version, and ABI.
- Sign with a consistent private release key and retain a secure backup.
- Verify the signing certificate, checksums, and native/ZIP alignment.
- Increase the final Android version code for every published APK.
- Publish immutable source tags, provenance, checksums, and signed release assets.

## Acceptance checks

- Verify Search and Archive restrictions, including gestures and restored navigation.
- Check pinned-chat reordering, recipient selection, forwarding, and in-chat search.
- Check messaging, media, calls, and background notification delivery.
- Confirm an Obtainium update retains app and account data.

Use RELEASE_CHECKLIST.md for per-release acceptance checks, BUILD.md for packaging and signing, and UPSTREAM.md for the update procedure.
