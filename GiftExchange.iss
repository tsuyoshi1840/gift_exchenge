; ==================================
; Gift Exchange インストーラー（Inno Setup 6 用）
; ==================================
; 使い方：BUILD.md の「3. インストーラーを作る」を参照
; 先に pyinstaller で dist\GiftExchange を作っておくこと。
;
; ・バージョンは EXE に埋め込まれた番号（main.py の APP_VERSION）を自動で読む
; ・管理者権限なしでインストールできる（ユーザーごとのインストール）
; ・できたインストーラーは installer\GiftExchange_Setup.exe

#define MyAppName "Gift Exchange"
#define MyAppExeName "GiftExchange.exe"
#define MyAppPublisher "Gift Exchange"
#define MyAppVersion GetVersionNumbersString("dist\GiftExchange\GiftExchange.exe")

[Setup]
; AppId はアプリを見分けるための番号。上書きインストール・アンインストールに使うので変更しないこと
AppId={{C90AC5CF-8457-4852-9828-D58779F536C8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
VersionInfoVersion={#MyAppVersion}

; インストール先（管理者権限なしの場合は %LOCALAPPDATA%\Programs\GiftExchange）
DefaultDirName={autopf}\GiftExchange
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 出力先とファイル名（GitHub Releases の latest/download リンクを固定するため、名前にバージョンを入れない）
OutputDir=installer
OutputBaseFilename=GiftExchange_Setup

SetupIconFile=assets\images\icon_image.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; dist\GiftExchange の中身（EXE と _internal フォルダ）を丸ごと入れる
Source: "dist\GiftExchange\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

; 参加者データ（%APPDATA%\GiftExchange\participants.json）はアンインストールしても残す
