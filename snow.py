import math
import random

from PySide6.QtCore import QElapsedTimer, QEvent, QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


# ==================================
# 雪を降らせる背景
# ==================================
# 画面のいちばん後ろに透明なレイヤーを置いて、雪をコードで描く。
# ボタンや文字の後ろを雪が通るので、操作のじゃまにならない。
#
# 使い方：
#   SnowBackground(window)

# 雪の数（画面の広さ 100万ピクセルあたり）
FLAKES_PER_MEGAPIXEL = 220

# 雪の大きさ（半径・ピクセル）
FLAKE_RADIUS_MIN = 1.5
FLAKE_RADIUS_MAX = 4.5

# 落ちる速さ（ピクセル/秒）
FALL_SPEED_MIN = 25
FALL_SPEED_MAX = 70

# 雪の色（背景がクリーム色なので、白に薄い金色のふちを付けて見えるようにする）
FLAKE_COLOR = QColor(255, 255, 255, 235)
FLAKE_EDGE_COLOR = QColor(173, 144, 101, 110)

# 画面更新の間隔（ミリ秒）約30fps
FRAME_INTERVAL_MS = 33


class SnowFlake:

    def __init__(self, width, height, start_anywhere):

        self.radius = random.uniform(FLAKE_RADIUS_MIN, FLAKE_RADIUS_MAX)

        # 大きい雪ほど手前にある＝速く落ちるように見せる
        depth = (self.radius - FLAKE_RADIUS_MIN) / (FLAKE_RADIUS_MAX - FLAKE_RADIUS_MIN)
        self.speed = FALL_SPEED_MIN + (FALL_SPEED_MAX - FALL_SPEED_MIN) * depth

        self.base_x = random.uniform(0, width)
        self.y = random.uniform(-height, height) if start_anywhere else random.uniform(-40, -5)

        # 左右にゆらゆら揺れる
        self.sway_width = random.uniform(8, 25)
        self.sway_speed = random.uniform(0.6, 1.4)
        self.phase = random.uniform(0, math.tau)

    def step(self, dt):

        self.y += self.speed * dt
        self.phase += self.sway_speed * dt

    @property
    def x(self):
        return self.base_x + math.sin(self.phase) * self.sway_width


class SnowBackground(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setStyleSheet("background: transparent;")

        self.flakes = []

        # 親ウィンドウの大きさが変わったら追従する
        parent.installEventFilter(self)
        self.fit_to_parent()

        self.clock = QElapsedTimer()
        self.clock.start()

        self.timer = QTimer(self)
        self.timer.setInterval(FRAME_INTERVAL_MS)
        self.timer.timeout.connect(self.advance)
        self.timer.start()

        # いちばん後ろに置く
        self.lower()
        self.show()

    def eventFilter(self, watched, event):

        if watched is self.parentWidget() and event.type() == QEvent.Type.Resize:
            self.fit_to_parent()

        return False

    def target_count(self):
        area = self.width() * self.height()
        return max(20, int(area / 1_000_000 * FLAKES_PER_MEGAPIXEL))

    def fit_to_parent(self):

        self.setGeometry(self.parentWidget().rect())
        self.lower()

        # 画面が広くなったら雪を増やし、狭くなったら減らす
        count = self.target_count()

        while len(self.flakes) < count:
            self.flakes.append(SnowFlake(self.width(), self.height(), True))

        del self.flakes[count:]

    def advance(self):

        dt = min(self.clock.restart() / 1000, 0.1)

        for index, flake in enumerate(self.flakes):
            flake.step(dt)

            # 下まで落ちたら、上から降らせ直す
            if flake.y - flake.radius > self.height():
                self.flakes[index] = SnowFlake(self.width(), self.height(), False)

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(FLAKE_EDGE_COLOR, 1))
        painter.setBrush(FLAKE_COLOR)

        for flake in self.flakes:
            painter.drawEllipse(QPointF(flake.x, flake.y), flake.radius, flake.radius)
