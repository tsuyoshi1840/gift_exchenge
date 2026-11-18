import math
import random

from PySide6.QtCore import QElapsedTimer, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


# ==================================
# クラッカー（紙吹雪）演出
# ==================================
# 画面の左下と右下からクラッカーを鳴らしたように紙吹雪を飛ばす。
# 画像素材は使わず、コードで描いているので拡大しても粗くならない。

# アプリの配色に合わせた紙吹雪の色
CONFETTI_COLORS = [
    "#B22222",  # 赤
    "#216D5E",  # 緑
    "#AD9065",  # 金
    "#E8B64C",  # 黄
    "#FFF8EC",  # クリーム
    "#D9534F",  # 明るい赤
]

# 1回のクラッカーで飛ばす紙吹雪の数（左右それぞれ）
PIECES_PER_SIDE = 90

# 紙吹雪が消えるまでの時間（秒）
LIFETIME_SECONDS = 3.2

# 重力の強さ（ピクセル/秒^2）
GRAVITY = 900

# 画面更新の間隔（ミリ秒）約60fps
FRAME_INTERVAL_MS = 16


class ConfettiPiece:

    def __init__(self, x, y, angle_deg, speed):

        angle = math.radians(angle_deg)

        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = -math.sin(angle) * speed

        self.width = random.uniform(10, 18)
        self.height = random.uniform(5, 10)
        self.rotation = random.uniform(0, 360)
        self.spin = random.uniform(-540, 540)
        self.color = QColor(random.choice(CONFETTI_COLORS))
        self.age = 0.0

    def step(self, dt):

        # 空気抵抗で少しずつ減速し、重力で落ちる
        drag = 1.0 - 1.1 * dt
        self.vx *= drag
        self.vy = self.vy * drag + GRAVITY * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rotation += self.spin * dt
        self.age += dt


class ConfettiOverlay(QWidget):
    """親ウィンドウ全体に重ねて表示する透明なレイヤー。クリックは下に通す。"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.pieces = []

        self.timer = QTimer(self)
        self.timer.setInterval(FRAME_INTERVAL_MS)
        self.timer.timeout.connect(self.advance)

        self.clock = QElapsedTimer()

        self.hide()

    def burst(self):
        """左下と右下からクラッカーを鳴らす"""

        self.setGeometry(self.parentWidget().rect())

        width = self.width()
        height = self.height()

        # 画面サイズに合わせて飛ばす強さを変える
        base_speed = max(height, 500) * 2.3

        for _ in range(PIECES_PER_SIDE):
            # 左下から右上へ
            self.pieces.append(
                ConfettiPiece(
                    0,
                    height,
                    random.uniform(45, 80),
                    base_speed * random.uniform(0.6, 1.1)
                )
            )
            # 右下から左上へ
            self.pieces.append(
                ConfettiPiece(
                    width,
                    height,
                    random.uniform(100, 135),
                    base_speed * random.uniform(0.6, 1.1)
                )
            )

        self.show()
        self.raise_()

        if not self.timer.isActive():
            self.clock.start()
            self.timer.start()

    def advance(self):

        dt = self.clock.restart() / 1000
        dt = min(dt, 0.05)

        for piece in self.pieces:
            piece.step(dt)

        # 時間切れ・画面外に落ちたものを消す
        self.pieces = [
            piece
            for piece in self.pieces
            if piece.age < LIFETIME_SECONDS and piece.y < self.height() + 40
        ]

        if not self.pieces:
            self.timer.stop()
            self.hide()

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        for piece in self.pieces:

            # 最後の0.8秒でフェードアウト
            remaining = LIFETIME_SECONDS - piece.age
            painter.setOpacity(max(0.0, min(1.0, remaining / 0.8)))

            painter.save()
            painter.translate(QPointF(piece.x, piece.y))
            painter.rotate(piece.rotation)

            # 回転しているように見せるため、幅を周期的に縮める
            flip = abs(math.cos(math.radians(piece.rotation * 2)))
            w = piece.width * max(flip, 0.2)

            painter.setBrush(piece.color)
            painter.drawRect(QRectF(-w / 2, -piece.height / 2, w, piece.height))
            painter.restore()
