from PySide6.QtGui import QFontDatabase, QIcon
from pathlib import Path
from lottery import create_pairs
from random_generator import create_generator
from result_form import ResultForm
import sys
import json
import secrets
from pathlib import Path
from participant_edit_form import ParticipantEditForm
from image_button import ImageButton
from app_paths import resource_path
from snow import SnowBackground

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QMessageBox
)
from PySide6.QtCore import Qt

# from register_form import RegistrationForm
from participant_list_form import ParticipantListForm

import os
from pathlib import Path

APP_NAME = "Gift Exchange"
APP_VERSION = "1.26.11.2"
# =================================
# データ保存先の設定
# =================================

# Windowsのユーザーデータ保存先を取得
app_data = Path(os.environ["APPDATA"])

# GiftExchange専用フォルダ
data_dir = app_data / "GiftExchange"

# JSONファイルの保存先
json_path = data_dir / "participants.json"

# フォルダがなければ作成
data_dir.mkdir(parents=True, exist_ok=True)

# JSONファイルがなければ初期データを作成
if not json_path.exists():
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            {"participants": []},
            file,
            ensure_ascii=False,
            indent=4
        )
# Listで形を設計した,CSSっぽいスタイル操作、UI表示を意識,ライブラリ使用によりコード書き換え,
# 名前入力Formを追加,json形式によるデータの保持,json表示,変更箇所を上部に整理,更新削除機能追加,
# 微修正,ユーザーデータディレクトリ方式(%APPDATA%\GiftExchange\participants.json)
# Inno Setup：その時点のアプリ一式をインストーラーに詰め直す

# C:\
#  └─ Users\
#      └─ ユーザー名\
#          └─ AppData\
#              └─ Roaming\
#                  └─ GiftExchange\
#                      └─ participants.json

# ==================================
# 参加者データ管理
# ==================================

# 	GIFの目安
# 画面上部の装飾	320 × 120 px
# 抽選結果の演出	240 × 240 px
# 小さな装飾アイコン	96 × 96 px
# 画面背景	600 × 650 px

# 参加者データを格納するリスト
participants = []

# JSON保存先
data_path = Path(__file__).parent / "participants.json"


# JSON読み込み
def load_participants():

    participants.clear()

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    participants.extend(data.get("participants", []))

# JSON保存
def save_participants():

    data = {
        "participants": participants
    }

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

def update_participant(index, new_name):
    participants[index] = new_name

    save_participants()
    update_participant_display()
    participant_form.update_participants(participants)


def delete_participant(index):
    participants.pop(index)

    save_participants()
    update_participant_display()
    participant_form.update_participants(participants)

def open_participant_edit_form(index):
    name = participants[index]

    edit_form = ParticipantEditForm(name, window)

    edit_form.participant_updated.connect(
        lambda new_name: update_participant(index, new_name)
    )

    edit_form.participant_deleted.connect(
        lambda: delete_participant(index)
    )

    edit_form.exec()
# ==================================
# アプリ起動
# ==================================
# 素材の場所は app_paths.py の resource_path() で解決する
# （EXEのときは sys._MEIPASS、Pythonで動かすときはこのフォルダ）
app = QApplication(sys.argv)

icon_path = resource_path("assets", "images", "icon_image.ico")
app.setWindowIcon(QIcon(str(icon_path)))

# フォント読み込み（Regular / Medium / Bold）
for font_file in [
    "MPLUSRounded1c-Regular.ttf",
    "MPLUSRounded1c-Medium.ttf",
    "MPLUSRounded1c-Bold.ttf",
]:
    font_path = resource_path("assets", "fonts", font_file)
    font_id = QFontDatabase.addApplicationFont(str(font_path))

    if font_id == -1:
        print("フォントの読み込みに失敗しました:", font_file)
# font-family: "Rounded Mplus 1c";名前を解決するときに使った
# else:
#     print(QFontDatabase.applicationFontFamilies(font_id))

# QSS読み込み
qss_path = resource_path("style.qss")

with open(qss_path, "r", encoding="utf-8") as file:
    app.setStyleSheet(file.read())



# ==================================
# メインウィンドウ
# ==================================

window = QWidget()
window.setWindowTitle(f"{APP_NAME} Ver.{APP_VERSION}")
window.resize(700, 520)

# メインレイアウト
layout = QVBoxLayout()
layout.setContentsMargins(65, 45, 65, 35)
layout.setSpacing(20)


# ==================================
# 上部タイトル
# ==================================

title = QLabel("Gift抽選 だよ")
title.setObjectName("title")
title.setAlignment(Qt.AlignmentFlag.AlignCenter)

subtitle = QLabel("プレゼント交換のペアを決めよう")
subtitle.setObjectName("subtitle")
subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

layout.addWidget(title)
layout.addWidget(subtitle)


# ==================================
# 参加者表示
# ==================================

# 参加人数表示
# 背景画像：assets/images/buttons/participant_count.png（または .gif）
count = ImageButton("参加予定人数　0 人", "participant_count")
count.setObjectName("participant_count")


layout.addWidget(count, alignment=Qt.AlignmentFlag.AlignHCenter)
# ==================================
# ボタン
# ==================================

# button_register = QPushButton("参加者を登録する")
# button_register.setObjectName("register_button")
# button_lottery.setObjectName("lottery_button")
# 背景画像：assets/images/buttons/lottery_button.png（または .gif）
button_lottery = ImageButton("抽選をはじめる", "lottery_button")
button_lottery.setObjectName("next_button")


layout.addWidget(button_lottery, alignment=Qt.AlignmentFlag.AlignHCenter)



# ==================================
# 各Form
# ==================================

# 登録Form
# registration_form = RegistrationForm(window)

# 参加者一覧Form
participant_form = ParticipantListForm(participants, window)


# ==================================
# 画面更新処理
# ==================================

# 参加者一覧と人数表示を更新
def update_participant_display():


    count.setText(
        f"参加予定人数　{len(participants)} 人"
    )


# ==================================
# 参加者操作
# ==================================

# 参加者追加処理
def add_participant(name):

    participants.append(name)
    # 自動更新
    participant_form.update_participants(participants)
    save_participants()
    update_participant_display()



    print(participants)


# 登録Formを開く
# def open_registration_form():

#     registration_form.show()
#     registration_form.raise_()
#     registration_form.activateWindow()


# 参加者一覧Formを開く
def open_participant_form():

    participant_form.update_participants(participants)

    participant_form.show()
    participant_form.raise_()
    participant_form.activateWindow()

# 抽選結果Formを開く
def open_result_form():

    try:
        # 抽選のたびにランダムなシード値（32ビット）を作る
        seed = secrets.randbits(32)
        generator = create_generator(seed)
        pairs = create_pairs(participants, generator)

    except ValueError as error:
        # 人数が奇数・2人未満のときは画面にメッセージを出す
        QMessageBox.warning(
            window,
            "抽選できません",
            f"{error}\n（現在の登録人数：{len(participants)} 人）"
        )
        return

    result_form = ResultForm(pairs, window)
    result_form.exec()

# ==================================
# Signalの接続
# ==================================
participant_form.participant_selected.connect(
    open_participant_edit_form
)
# 登録Formと追加処理を接続
# registration_form.participant_added.connect(add_participant)
participant_form.participant_added.connect(add_participant)

# 登録ボタンとFormを接続
# button_register.clicked.connect(open_registration_form)

# 参加人数ボタンとFormを接続
count.clicked.connect(open_participant_form)

button_lottery.clicked.connect(open_result_form)


# ==================================
# 下部メッセージ
# ==================================

footer = QLabel("参加者を登録して、抽選を始めましょう")
footer.setObjectName("footer")
footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

layout.addStretch()
layout.addWidget(footer)


# ==================================
# 起動時のデータ読み込み
# ==================================

load_participants()
update_participant_display()


# ==================================
# 表示・実行
# ==================================

window.setLayout(layout)

# 背景に雪を降らせる（いちばん後ろに表示される）
snow = SnowBackground(window)

window.show()

sys.exit(app.exec())
