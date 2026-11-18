from PySide6.QtCore import QRectF
from PySide6.QtGui import QMovie, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QPushButton, QStyle, QStyleOptionButton

from app_paths import resource_path


# ==================================
# 背景画像つきボタン
# ==================================
# assets/images/buttons/ に「ボタン名.gif」または「ボタン名.png」を置くと、
# ボタンの背景に薄く表示される（GIFならアニメーションする）。
# ファイルが無いときは、今まで通りQSSの色だけで表示される。
#
# 表示の重なり順
#   1. QSSの背景色・枠線
#   2. 背景画像（opacityで透過）
#   3. ボタンの文字

BUTTON_IMAGE_DIR = ("assets", "images", "buttons")

# 背景画像の濃さ（0.0 = 見えない 〜 1.0 = そのまま）
DEFAULT_IMAGE_OPACITY = 0.35

# QSSの border-radius と合わせる（角の丸みで画像を切り抜く）
DEFAULT_CORNER_RADIUS = 10


class ImageButton(QPushButton):

    def __init__(
        self,
        text,
        image_name,
        opacity=DEFAULT_IMAGE_OPACITY,
        corner_radius=DEFAULT_CORNER_RADIUS,
        parent=None
    ):
        super().__init__(text, parent)

        self.image_opacity = opacity
        self.corner_radius = corner_radius

        self.pixmap = None
        self.movie = None

        self.load_image(image_name)

    def load_image(self, image_name):

        folder = resource_path(*BUTTON_IMAGE_DIR)

        gif_path = folder / f"{image_name}.gif"
        png_path = folder / f"{image_name}.png"

        if gif_path.exists():
            self.movie = QMovie(str(gif_path))
            self.movie.frameChanged.connect(self.update)
            self.movie.start()

        elif png_path.exists():
            self.pixmap = QPixmap(str(png_path))

    def current_image(self):

        if self.movie is not None:
            return self.movie.currentPixmap()

        return self.pixmap

    def paintEvent(self, event):

        image = self.current_image()

        # 画像が無ければ普通のボタンとして描く
        if image is None or image.isNull():
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        option = QStyleOptionButton()
        self.initStyleOption(option)

        # 1. 背景色・枠線（QSS）
        self.style().drawControl(
            QStyle.ControlElement.CE_PushButtonBevel,
            option,
            painter,
            self
        )

        # 2. 背景画像（角丸で切り抜いて、透過して描く）
        inner = QRectF(self.rect()).adjusted(2, 2, -2, -2)

        clip = QPainterPath()
        clip.addRoundedRect(inner, self.corner_radius, self.corner_radius)

        painter.save()
        painter.setClipPath(clip)
        painter.setOpacity(self.image_opacity)
        painter.drawPixmap(inner.toRect(), image)
        painter.restore()

        # 3. 文字
        self.style().drawControl(
            QStyle.ControlElement.CE_PushButtonLabel,
            option,
            painter,
            self
        )
