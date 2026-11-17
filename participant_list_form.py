
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QListWidget,
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton
)
from PySide6.QtCore import QSize, Signal


class ParticipantListForm(QDialog):

    participant_selected = Signal(int)
    participant_added = Signal(str)

    def __init__(self, participants, parent=None):
        super().__init__(parent)

        self.setWindowTitle("参加者管理")
        self.resize(700, 520)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        # タイトル
        title = QLabel("参加者管理")

        # 登録人数
        self.count_label = QLabel()

        # 名前入力欄と追加ボタン
        input_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("名前を入力してください")

        self.button_add = QPushButton("追加")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.button_add)

        # 参加者名簿
        self.participant_list = QListWidget()
        self.participant_list.setObjectName("participant_list")

        self.participant_list.setViewMode(
            QListView.ViewMode.IconMode
        )
        self.participant_list.setFlow(
            QListView.Flow.LeftToRight
        )
        self.participant_list.setWrapping(True)
        self.participant_list.setWordWrap(False)
        self.participant_list.setResizeMode(
            QListView.ResizeMode.Adjust
        )
        self.participant_list.setMovement(
            QListView.Movement.Static
        )
        self.participant_list.setGridSize(QSize(140, 50))
        self.participant_list.setSpacing(8)

        # スクロールバーを非表示
        self.participant_list.setVerticalScrollBarPolicy(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.participant_list.setHorizontalScrollBarPolicy(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # 名前クリック時の処理
        self.participant_list.itemClicked.connect(
            self.select_participant
        )

        # 画面に配置
        layout.addWidget(title)
        layout.addWidget(self.count_label)
        layout.addLayout(input_layout)
        layout.addWidget(self.participant_list)

        self.setLayout(layout)

        # 登録済み参加者を表示
        self.update_participants(participants)

        # 追加ボタン
        self.button_add.clicked.connect(
            self.add_participant
        )

        # Enterキーでも追加
        self.name_input.returnPressed.connect(
            self.add_participant
        )

    # 参加者一覧を更新
    def update_participants(self, participants):

        self.participant_list.clear()
        self.participant_list.addItems(participants)

        self.count_label.setText(
            f"登録人数：{len(participants)} 人"
        )

    # 参加者を追加
    def add_participant(self):

        name = self.name_input.text().strip()

        if not name:
            return

        self.participant_added.emit(name)

        self.name_input.clear()
        self.name_input.setFocus()

    # 参加者をクリックしたとき
    def select_participant(self, item):

        index = self.participant_list.row(item)
        self.participant_selected.emit(index)
