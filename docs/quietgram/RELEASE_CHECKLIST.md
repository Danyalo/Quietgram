# Release and phone checks

## Before a release

- [ ] Exact upstream base and source commits recorded; source tree clean.
- [ ] Build succeeds with the recorded toolchain.
- [ ] APK has the Quietgram application ID and a higher final version code than the previous release.
- [ ] APK is signed with the private Quietgram release key, not the public upstream test key.
- [ ] Signing certificate matches the previous Quietgram release.
- [ ] No signing credentials or user secrets committed or included in CI logs.
- [ ] Inherited Forkgram publishing workflows cannot run in Quietgram.
- [ ] Source tag, APK SHA-256, and upstream provenance included in release notes.

## Android device

- [ ] Global Search button and search field are absent on the main chat list.
- [ ] Pulling or scrolling the main list cannot expose global Search.
- [ ] Downloads/search and restored-navigation paths cannot open global Search.
- [ ] Archive is absent with the server archive both pinned and hidden.
- [ ] Pull-down cannot expose or open Archive.
- [ ] Other Archive navigation paths and restored Archive screens are blocked.
- [ ] Archive settings and account switches do not restore Archive access.
- [ ] Pinned-chat drag reordering works with Archive present in server state.
- [ ] Contacts and local recipient selection work; recipient pickers cannot discover remote users/channels via global Search.
- [ ] Search within a conversation works.
- [ ] Direct messages, secret chats, forwarding, attachments, media, and calls work.
- [ ] Notifications arrive without Google services while the screen is off.
- [ ] Reboot and network changes do not break notifications.
- [ ] Links, notifications, forwards, and custom folders can still open individual chats: this is an accepted limitation.

## Obtainium

- [ ] Repository URL points to Quietgram, not Forkgram.
- [ ] APK filtering selects exactly one intended asset.
- [ ] Prereleases excluded from normal phone updates.
- [ ] A second signed release installs over the first and retains account/app data.

These are manual acceptance checks until they have actually been executed; a clean diff or successful compilation does not mark them complete.
