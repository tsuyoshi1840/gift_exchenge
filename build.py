import re
from pathlib import Path

main_path = Path(__file__).parent / "main.py"
version_file = Path(__file__).parent / "version_info.txt"

main_code = main_path.read_text(encoding="utf-8")

match = re.search(
    r'APP_VERSION\s*=\s*["\']([^"\']+)["\']',
    main_code
)

if match is None:
    raise ValueError("APP_VERSIONが見つかりません。")

version_text = match.group(1)
version = tuple(int(value) for value in version_text.split("."))

if len(version) != 4:
    raise ValueError("バージョンは4つの数字で指定してください。")

print("現在のバージョン:", version_text)
version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version},
    prodvers={version},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '041104B0',
        [
          StringStruct('CompanyName', 'Gift Exchange'),
          StringStruct('FileDescription', 'Gift Exchange'),
          StringStruct('FileVersion', '{version_text}'),
          StringStruct('InternalName', 'GiftExchange'),
          StringStruct('OriginalFilename', 'GiftExchange.exe'),
          StringStruct('ProductName', 'Gift Exchange'),
          StringStruct('ProductVersion', '{version_text}')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1041, 1200])])
  ]
)
"""

version_file.write_text(version_info.strip(), encoding="utf-8")

print("Windows用バージョン情報を生成しました。")