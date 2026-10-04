# Quietgram APK builds

The supported phone target is ARM64 (`afatFd_v8aRelease`). Packaging overrides live in `quietgram.gradle` and `quietgram/AndroidManifest.xml`; the upstream app build file has one extra apply statement. The launcher label is Quietgram, its default icon is a green conversation bubble, and it uses a distinct application ID. Source namespaces remain unchanged.

The release manifest retains the upstream SDK23 overlay's capabilities. When updating upstream, compare that overlay with `quietgram/AndroidManifest.xml` as well as reviewing the two UI patches.

## Candidate pipeline

`.github/workflows/quietgram-apk.yml` runs only on pushes to this repository's `quietgram` branch or a manual dispatch. It has read-only repository permissions and does not run on external pull requests. It fetches pinned submodules, builds native dependencies from source, then assembles an unsigned APK. The workflow uses JDK 21, SDK 36, Build Tools 36.0.0, NDK 27.2.12479018 and CMake 3.22.1. Other native host tools and the Rust stable toolchain currently come from the runner; byte-for-byte reproducibility is not yet claimed.

`APP_ID` and `APP_HASH` are read from repository Actions secrets. Values are validated without printing them and passed as command-line project properties, so upstream's zero placeholders cannot override them. CI does not modify committed credentials. The candidate artifact includes the unsigned APK, its checksum, packaging information, and source commit. It is retained for 14 days and is not an installable phone release.

`CHECK_UPDATES=0` keeps Forkgram's update mechanism off; Obtainium will handle published GitHub Releases.

## Versioning and signing

Pass `-PQUIETGRAM_VERSION_CODE=N` when preparing a release. This is the final Android versionCode without upstream's ABI multipliers. The initial candidate uses 1. Increase this value for every published APK, including rebuilds of the same upstream version. Its versionName combines the upstream version with `-quietgram.N`. Record published codes in release notes; do not derive them solely from a workflow run number.

Unsigned builds are the default. The public upstream test signing key is explicitly removed from Quietgram's release configuration. A real signed build must supply `RELEASE_KEYSTORE_FILE`, `RELEASE_STORE_PASSWORD`, `RELEASE_KEY_PASSWORD`, and `RELEASE_KEY_ALIAS` as Gradle project properties. The private signing key must remain consistent across phone updates and must have a secure backup before the first release.

## Local packaging check

This checks the manifest and resources without compiling native dependencies or using API secrets:

```sh
./gradlew --no-daemon \
  :TMessagesProj_App:processAfatFd_v8aReleaseManifest \
  :TMessagesProj_App:processAfatFd_v8aReleaseResources \
  -Parm64-v8a -PQUIETGRAM_VERSION_CODE=1 -x buildNativeDeps
```

A full APK additionally requires all native submodules and the host tools listed in upstream BUILDING.md. CI deliberately builds only ARM64 with `ABIS=arm64-v8a`, then disables the redundant Gradle `buildNativeDeps` task after prebuilding the required libraries.
