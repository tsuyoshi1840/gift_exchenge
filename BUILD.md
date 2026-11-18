# EXE とインストーラーの作り方メモ

Python のアプリ（このフォルダ）から、Windows 用の EXE とインストーラーを作って配布するまでの手順です。

```
Pythonのコード ──(PyInstaller)──▶ dist\GiftExchange\GiftExchange.exe
                                         │
                              (Inno Setup)│
                                         ▼
                          installer\GiftExchange_Setup.exe ──▶ GitHub Releases
```

コマンドはすべて **PowerShell で、このフォルダに移動してから** 実行します。

```powershell
cd C:\Users\hao2z\Documents\gift_exchenge
```

---

## 0. 準備（初回、または別の PC で GitHub から取ってきたとき）

### Python のライブラリ

```powershell
pip install pyside6 pyinstaller
```

入っているか確認するには `pyinstaller --version` を実行します。

### Inno Setup

インストーラーを作るときだけ必要です。公式サイト（https://jrsoftware.org/isdl.php）から **Inno Setup 6** をダウンロードしてインストールします。日本語の言語ファイルは最初から入っています。

### GitHub から取ってきた直後に無いもの

`.gitignore` で除外しているので、次のものは GitHub には入っていません。ビルドすると作られます。

| フォルダ・ファイル | 中身 | 作られるタイミング |
|---|---|---|
| `build\` | PyInstaller の作業用ファイル | 手順 2 |
| `dist\` | 完成した EXE | 手順 2 |
| `installer\` | 完成したインストーラー | 手順 3 |
| `participants.json` | 参加者データ（実際は `%APPDATA%\GiftExchange\` に保存） | アプリ起動時 |

---

## 1. バージョンを上げる

1. `main.py` の `APP_VERSION` を書き換える（数字4つ。例：`"1.26.11.3"`）
2. バージョン情報ファイルを作り直す

```powershell
python build.py
```

`version_info.txt` が更新されます。この番号が EXE のプロパティとインストーラーのバージョンに使われます。

---

## 2. EXE を作る（PyInstaller）

```powershell
pyinstaller GiftExchange.spec --clean --noconfirm
```

- `--clean`：前回の作業用ファイルを消してから作る
- `--noconfirm`：`dist` を上書きするときに確認を出さない

### できあがるもの

```
dist\GiftExchange\
 ├─ GiftExchange.exe   ← これをダブルクリックで起動
 └─ _internal\         ← Python本体・PySide6・style.qss・assets など
```

**EXE だけを取り出すと動きません。** `_internal` フォルダと必ずセットで使います。

### GiftExchange.spec の中身（触るときのメモ）

- `datas=[('style.qss', '.'), ('assets', 'assets')]`：EXE に同梱するファイル。画像やフォントを `assets` 以外に追加したらここに足す
- `console=False`：黒いコンソール画面を出さない
- `icon=...`：EXE のアイコン
- `version='version_info.txt'`：EXE のプロパティに出るバージョン

### 動作チェック

`dist\GiftExchange\GiftExchange.exe` を起動して、次を確認します。

- ウィンドウのアイコン、丸ゴシックのフォント、ボタンの背景画像、雪が表示される
- 抽選で紙吹雪が出る
- EXE を右クリック → プロパティ → 詳細 で、バージョンが正しい

---

## 3. インストーラーを作る（Inno Setup）

設定ファイルは `GiftExchange.iss` です。

### 作り方（どちらか）

**A. 画面で作る**
1. `GiftExchange.iss` をダブルクリック（Inno Setup Compiler が開く）
2. メニューの **Build → Compile**（または `Ctrl + F9`）

**B. コマンドで作る**

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" GiftExchange.iss
```

### できあがるもの

```
installer\GiftExchange_Setup.exe
```

### GiftExchange.iss のポイント

- **バージョンは自動**：`dist\GiftExchange\GiftExchange.exe` に埋め込まれた番号を読むので、`.iss` を書き換える必要はありません（必ず手順 2 の後に実行する）
- **管理者権限なし**でインストールできます（インストール先は `%LOCALAPPDATA%\Programs\GiftExchange`）
- **AppId は変えない**：同じ番号だと「上書きインストール」として扱われます。変えると別アプリ扱いになります
- **ファイル名にバージョンを入れていない**のは、GitHub のダウンロードリンクを固定するためです（手順 4）
- 参加者データ（`%APPDATA%\GiftExchange\participants.json`）は、アンインストールしても消えません

> メモ：以前の PC で作った `.iss` は Git に入っていなかったため、この `GiftExchange.iss` は新しく作り直したものです。元の `.iss` が見つかって設定を引き継ぎたい場合は、`AppId` を元のものに合わせると、前のバージョンへの上書きインストールになります。

---

## 4. GitHub Releases で配布する

EXE やインストーラーは Git にコミットせず、**Releases に添付**して配ります。

1. 変更をコミットして push しておく
2. GitHub のリポジトリページ → 右側の **Releases** → **Draft a new release**
3. **Choose a tag** に `v1.26.11.3` のようにバージョンを入力 → **Create new tag**
4. タイトル（例：`Gift Exchange v1.26.11.3`）と、変更点を書く
5. 下の **Attach binaries** に次のファイルをドラッグ
   - `installer\GiftExchange_Setup.exe`（インストーラー版）
   - 必要なら `dist\GiftExchange` フォルダを ZIP にしたもの（インストール不要版）
6. **Publish release**

### いつも最新版を指すダウンロードリンク

ポートフォリオなどにはこのリンクを貼ると、新しいリリースを出しても書き換え不要です。

```
https://github.com/tsuyoshi1840/gift_exchenge/releases/latest/download/GiftExchange_Setup.exe
```

リリースの一覧ページはこちらです。

```
https://github.com/tsuyoshi1840/gift_exchenge/releases/latest
```

※ リポジトリが **Public** でないと、ほかの人はダウンロードできません。

---

## 5. 署名なしアプリの警告について

コード署名（有料の証明書）をしていないため、配布先の PC で次のような警告が出ることがあります。

| 警告 | 出る場面 | 対処 |
|---|---|---|
| **Windows によって PC が保護されました**（SmartScreen） | ダウンロードしたインストーラーを初めて起動したとき | 「詳細情報」→「実行」で起動できる |
| ブラウザの「一般的にダウンロードされていません」 | ダウンロード時 | 「保持する」を選ぶ |
| **スマート アプリ コントロール**でブロック | Windows 11 で SAC がオンのとき | 署名なしアプリは個別に許可できない。SAC をオフにするしかない（一度オフにすると再びオンにはできない） |

配布ページには「署名なしのため警告が出ることがあります」と一言書いておくと親切です。

---

## まとめ：毎回のリリース手順

```powershell
cd C:\Users\hao2z\Documents\gift_exchenge
# 1. main.py の APP_VERSION を上げてから
python build.py
# 2. EXE
pyinstaller GiftExchange.spec --clean --noconfirm
# 3. インストーラー
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" GiftExchange.iss
# 4. installer\GiftExchange_Setup.exe を GitHub Releases に添付
```
