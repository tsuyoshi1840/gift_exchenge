
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
import random

from confetti import ConfettiOverlay
from image_button import ImageButton
from snow import SnowBackground

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QScrollArea,
    QWidget,
    QSpinBox
)


# 抽選演出の設定
# 基準値：3秒
SPIN_DURATION_SECONDS = 3

# 名前切り替えの間隔：250ms（0.25秒）
SPIN_INTERVAL_MS = 250


class ResultForm(QDialog):

    def display_pair(self, index, pair):

        # 組番号とペアを1つのラベルにまとめる
        pair_label = QLabel(
            f"{index + 1}組目\n"
            f"{pair[0]} × {pair[1]}"
        )

        pair_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pair_label.setWordWrap(True)
        pair_label.setObjectName("pair_name")

        # 横2列で配置
        # 1組目の下に3組目、2組目の下に4組目
        row = index // 2
        column = index % 2

        self.pair_grid.addWidget(pair_label, row, column)

    def change_names(self):

        # 抽選演出中のランダム表示
        left_name, right_name = random.sample(self.participants, 2)

        self.result_label.setText(
            f"{left_name} × {right_name}"
        )

        self.spin_count = self.spin_count + 1

        if self.spin_count >= self.spin_duration * 1000 / SPIN_INTERVAL_MS:

            self.timer.stop()

            # 確定したペアを表示
            pair = self.pairs[self.current_pair_index]

            self.result_label.setText(
                f"{pair[0]} × {pair[1]}"
            )

            self.display_pair(self.current_pair_index, pair)

            self.current_pair_index = self.current_pair_index + 1

            # 確定した瞬間にクラッカー演出
            self.confetti.burst()

            if self.current_pair_index >= len(self.pairs):
                self.next_button.setText("抽選完了")
                self.next_button.setEnabled(False)
            else:
                self.next_button.setText("次の抽選を開始")
                self.next_button.setEnabled(True)

    def start_lottery(self):

        # 演出中はもう一度押されても無視する
        if self.timer.isActive():
            return

        self.spin_count = 0
        self.spin_duration = self.duration_spinbox.value()

        # 演出が終わるまでボタンを押せないようにする
        self.next_button.setEnabled(False)
        self.next_button.setText("抽選中…")

        self.timer.start()

    # ==================================
    # 全画面表示（プロジェクター用）
    # ==================================
    def toggle_fullscreen(self):

        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_button.setText("⛶ 全画面")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("⛶ 元に戻す")

    def keyPressEvent(self, event):

        # 全画面中のEscは「閉じる」ではなく「全画面を解除」にする
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggle_fullscreen()
            return

        super().keyPressEvent(event)

    def resizeEvent(self, event):

        super().resizeEvent(event)

        # 紙吹雪のレイヤーをウィンドウ全体に合わせる
        self.confetti.setGeometry(self.rect())

    def __init__(self, pairs, parent=None):

        super().__init__(parent)

        self.pairs = pairs

        # 抽選の進行状況
        self.current_pair_index = 0
        self.spin_count = 0

        self.participants = [
            name
            for pair in pairs
            for name in pair
        ]

        # 名前切り替え用タイマー
        self.timer = QTimer(self)
        self.timer.setInterval(SPIN_INTERVAL_MS)
        self.timer.timeout.connect(self.change_names)

        # Formの初期サイズ
        self.resize(900, 650)

        # メインレイアウト
        main_layout = QVBoxLayout(self)

        # ウィンドウタイトル
        self.setWindowTitle("Gift Exchange - 抽選結果")

        # 全画面ボタン・設定ボタン
        settings_button_layout = QHBoxLayout()
        settings_button_layout.addStretch()

        self.fullscreen_button = QPushButton("⛶ 全画面")
        self.fullscreen_button.setObjectName("tool_button")
        self.fullscreen_button.setToolTip("全画面表示（F11）")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        settings_button_layout.addWidget(self.fullscreen_button)

        self.settings_button = QPushButton("⚙")
        self.settings_button.setObjectName("tool_button")
        self.settings_button.setToolTip("抽選演出の設定")
        settings_button_layout.addWidget(self.settings_button)

        # F11キーでも全画面を切り替える
        QShortcut(QKeySequence("F11"), self, self.toggle_fullscreen)

        main_layout.addLayout(settings_button_layout)

        # 抽選演出時間の設定
        self.settings_widget = QWidget()
        self.settings_widget.setObjectName("settings_area")
        settings_layout = QHBoxLayout(self.settings_widget)

        duration_label = QLabel("抽選演出時間（秒）")
        duration_label.setObjectName("settings_label")

        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 10)
        self.duration_spinbox.setValue(SPIN_DURATION_SECONDS)

        settings_layout.addWidget(duration_label)
        settings_layout.addWidget(self.duration_spinbox)

        main_layout.addWidget(self.settings_widget)

        # 初期状態は非表示
        self.settings_widget.hide()

        # ボタンで表示・非表示を切り替える
        self.settings_button.clicked.connect(
            lambda: self.settings_widget.setVisible(
                not self.settings_widget.isVisible()
            )
        )

        # 抽選結果表示エリア
        self.result_label = QLabel("抽選を開始してください")
        self.result_label.setObjectName("result_label")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.result_label,1)

        # 抽選ボタン
        # 背景画像：assets/images/buttons/result_button.png（または .gif）
        self.next_button = ImageButton("抽選開始", "result_button")
        self.next_button.setObjectName("next_button")

        main_layout.addWidget(
            self.next_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # 抽選演出開始
        self.next_button.clicked.connect(self.start_lottery)

        # ペア一覧タイトル
        list_title = QLabel("ペア一覧")
        list_title.setObjectName("pair_list_title")

        main_layout.addWidget(list_title)

        # ペア一覧
        self.pair_grid = QGridLayout()
        self.pair_grid.setHorizontalSpacing(0)
        self.pair_grid.setVerticalSpacing(0)

        # ペアが少ないときも上から詰めて並べる
        self.pair_grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 2列の幅を均等にする
        for column in range(2):
            self.pair_grid.setColumnStretch(column, 1)

        list_widget = QWidget()
        list_widget.setObjectName("pair_list")
        list_widget.setLayout(self.pair_grid)

        # スクロールエリア
        scroll_area = QScrollArea()
        scroll_area.setObjectName("pair_scroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_widget)

        main_layout.addWidget(scroll_area,3)

        # 背景に雪を降らせる（いちばん後ろに表示される）
        self.snow = SnowBackground(self)

        # クラッカー（紙吹雪）演出のレイヤー
        # 一番最後に作って、すべての部品の上に重ねる
        self.confetti = ConfettiOverlay(self)


# ファイルの役割
# lottery.py：ペアを決める
# random_generator.py：乱数を生成する
# result_form.py：名前のリール演出と結果表示を担当する

