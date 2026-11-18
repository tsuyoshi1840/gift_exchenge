# Code signing policy

Free code signing provided by [SignPath.io](https://about.signpath.io/), certificate by [SignPath Foundation](https://signpath.org/).

> Status: the application to SignPath Foundation is pending. Until it is approved, release binaries are unsigned.
>
> 日本語の要約は下にあります。

## What is signed

Only the Windows release binaries of **Gift Exchange** are signed:

- `GiftExchange.exe` (the application)
- `GiftExchange_Setup.exe` (the Inno Setup installer)

All signed binaries are built from the source code in this repository by the public GitHub Actions workflow [`.github/workflows/release.yml`](.github/workflows/release.yml) on GitHub-hosted runners. Binaries built on a personal computer are never submitted for signing.

The signing key is held by SignPath in a hardware security module (HSM). This project never has access to the private key.

## Team roles

This is a single-maintainer project. All roles are held by the same person.

| Role | Member |
|---|---|
| Committers and reviewers | [@tsuyoshi1840](https://github.com/tsuyoshi1840) |
| Approvers | [@tsuyoshi1840](https://github.com/tsuyoshi1840) |

- Every change by a non-committer (for example, a pull request) is reviewed by a committer before it is merged.
- Every signing request is approved manually by an approver.
- All team members use multi-factor authentication for GitHub and SignPath.

## Privacy policy

This program will not transfer any information to other networked systems unless specifically requested by the user or the person installing or operating it.

Gift Exchange works completely offline. Participant names are stored only on the user's own computer, in `%APPDATA%\GiftExchange\participants.json`, and are never sent anywhere.

## Uninstallation

The installer registers an uninstaller. Use **Settings → Apps → Installed apps → Gift Exchange → Uninstall**. The participant data file in `%APPDATA%\GiftExchange\` is kept and can be deleted manually.

---

## 日本語の要約

- 署名には SignPath.io の無料コード署名と、SignPath Foundation の証明書を使っています。
- 署名するのは、このリポジトリのソースから GitHub Actions でビルドした `GiftExchange.exe` と `GiftExchange_Setup.exe` だけです。個人の PC でビルドしたものは署名しません。
- 秘密鍵は SignPath が管理しており、このプロジェクトは保持していません。
- メンテナーは 1 人（[@tsuyoshi1840](https://github.com/tsuyoshi1840)）で、すべての署名リクエストを手動で承認します。
- アプリはネットワーク通信をしません。参加者の名前は PC 内（`%APPDATA%\GiftExchange\participants.json`）にのみ保存されます。
