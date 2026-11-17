
from PySide6.QtCore import Qt, QTimer
import random

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

        # 2列で配置
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

            self.next_button.setText("次の抽選を開始")

            self.display_pair(self.current_pair_index, pair)

            self.current_pair_index = self.current_pair_index + 1

            if self.current_pair_index >= len(self.pairs):
                self.next_button.setText("抽選完了")
                self.next_button.setEnabled(False)

    def start_lottery(self):

        self.spin_count = 0
        self.spin_duration = self.duration_spinbox.value()

        self.timer.start()

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

        # 設定ボタン
        settings_button_layout = QHBoxLayout()
        settings_button_layout.addStretch()

        self.settings_button = QPushButton("⚙")
        settings_button_layout.addWidget(self.settings_button)

        main_layout.addLayout(settings_button_layout)

        # 抽選演出時間の設定
        self.settings_widget = QWidget()
        settings_layout = QHBoxLayout(self.settings_widget)

        duration_label = QLabel("抽選演出時間（秒）")

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

        main_layout.addWidget(self.result_label)

        # 抽選ボタン
        self.next_button = QPushButton("抽選開始")
        self.next_button.setObjectName("next_button")

        main_layout.addWidget(self.next_button)

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

        # 2列の幅を均等にする
        for column in range(2):
            self.pair_grid.setColumnStretch(column, 1)

        list_widget = QWidget()
        list_widget.setLayout(self.pair_grid)

        # スクロールエリア
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_widget)

        main_layout.addWidget(scroll_area)


# ファイルの役割
# lottery.py：ペアを決める
# random_generator.py：乱数を生成する
# result_form.py：名前のリール演出と結果表示を担当する
