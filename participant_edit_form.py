    
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtCore import Qt, Signal


class ParticipantEditForm(QDialog):

    # 編集・削除の通知
    participant_updated = Signal(str)
    participant_deleted = Signal()

    def __init__(self, name, parent=None):
        super().__init__(parent)

        self.setWindowTitle("参加者編集")
        self.resize(350, 220)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # タイトル
        title = QLabel("参加者編集")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 名前入力欄
        self.name_input = QLineEdit()
        self.name_input.setText(name)

        # ボタン
        button_layout = QHBoxLayout()

        self.button_update = QPushButton("変更する")
        self.button_delete = QPushButton("削除する")

        button_layout.addWidget(self.button_update)
        button_layout.addWidget(self.button_delete)

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # ボタンのイベント接続
        self.button_update.clicked.connect(self.update_participant)
        self.button_delete.clicked.connect(self.delete_participant)

    # 名前変更の通知
    def update_participant(self):
        name = self.name_input.text().strip()

        if not name:
            return

        self.participant_updated.emit(name)
        self.accept()

    # 削除の通知
    def delete_participant(self):
        self.participant_deleted.emit()
        self.accept()
