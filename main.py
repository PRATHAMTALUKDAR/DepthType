# import sys
# from pathlib import Path

# import cv2
# import torch
# import numpy as np

# from PIL import Image, ImageDraw, ImageFont

# from PySide6.QtCore import (
#     Qt,
#     QRectF,
#     QPointF,
#     QTimer,
#     Signal,
#     QVariantAnimation,
#     QEasingCurve,
#     QDir,
#     QStandardPaths,
#     QSize,
#     QStorageInfo,
# )
# from PySide6.QtGui import (
#     QImage,
#     QPixmap,
#     QPainter,
#     QColor,
#     QPen,
#     QBrush,
#     QRadialGradient,
#     QLinearGradient,
#     QFontDatabase,
#     QFont,
#     QIcon,
#     QPainterPath,
#     QKeySequence,
#     QShortcut,
# )

# from PySide6.QtWidgets import (
#     QApplication,
#     QMainWindow,
#     QWidget,
#     QLabel,
#     QPushButton,
#     QVBoxLayout,
#     QHBoxLayout,
#     QLineEdit,
#     QSlider,
#     QDialog,
#     QMessageBox,
#     QFrame,
#     QGraphicsOpacityEffect,
#     QListWidget,
#     QListWidgetItem,
#     QFileSystemModel,
#     QTreeView,
#     QHeaderView,
#     QAbstractItemView,
#     QComboBox,
#     QSplitter,
# )

# from ultralytics.models.sam import SAM2Predictor


# BASE_DIR = Path(__file__).resolve().parent
# FONT_PATH = (
#     BASE_DIR
#     / "assets"
#     / "fonts"
#     / "SF-Pro-Display-Regular.ttf"
# )
# ICON_PATH = BASE_DIR / "assets" / "icon.ico"


# def load_font(size):
#     if not FONT_PATH.exists():
#         raise FileNotFoundError(
#             f"Apple SF Pro font not found:\n{FONT_PATH}"
#         )

#     return ImageFont.truetype(
#         str(FONT_PATH),
#         size=max(12, int(size))
#     )


# def pil_to_pixmap(image, dpr=1.0):
#     image = image.convert("RGBA")
#     data = image.tobytes("raw", "RGBA")

#     qimage = QImage(
#         data,
#         image.width,
#         image.height,
#         QImage.Format.Format_RGBA8888
#     )

#     pixmap = QPixmap.fromImage(qimage.copy())
#     pixmap.setDevicePixelRatio(dpr)
#     return pixmap


# def create_app_icon():
#     if ICON_PATH.exists():
#         return QIcon(str(ICON_PATH))

#     size = 128
#     pixmap = QPixmap(size, size)
#     pixmap.fill(Qt.GlobalColor.transparent)

#     painter = QPainter(pixmap)
#     painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#     bg_grad = QLinearGradient(0, 0, size, size)
#     bg_grad.setColorAt(0.0, QColor("#fbf9f5"))
#     bg_grad.setColorAt(1.0, QColor("#ede6d9"))
#     painter.setPen(QPen(QColor("#d6cfc3"), 3))
#     painter.setBrush(QBrush(bg_grad))
#     painter.drawRoundedRect(QRectF(6, 6, size - 12, size - 12), 28, 28)

#     font = QFont("SF Pro Display", 64, QFont.Weight.Bold)
#     painter.setFont(font)
#     painter.setPen(QColor("#2563eb"))
#     painter.drawText(QRectF(0, -2, size, size), Qt.AlignmentFlag.AlignCenter, "D")

#     painter.setPen(Qt.PenStyle.NoPen)
#     painter.setBrush(QColor("#1c1917"))
#     painter.drawEllipse(QPointF(size * 0.56, size * 0.43), 13, 13)
#     body_path = QPainterPath()
#     body_path.moveTo(size * 0.34, size * 0.80)
#     body_path.quadTo(size * 0.56, size * 0.54, size * 0.78, size * 0.80)
#     painter.drawPath(body_path)

#     painter.end()
#     return QIcon(pixmap)


# def create_vector_icon(kind, color="#292524", size=15):
#     pixmap = QPixmap(size * 2, size * 2)
#     pixmap.fill(Qt.GlobalColor.transparent)

#     painter = QPainter(pixmap)
#     painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#     pen = QPen(
#         QColor(color),
#         2.4,
#         Qt.PenStyle.SolidLine,
#         Qt.PenCapStyle.RoundCap,
#         Qt.PenJoinStyle.RoundJoin
#     )
#     painter.setPen(pen)

#     if kind == "folder":
#         painter.drawRoundedRect(QRectF(4, 7, 24, 18), 3.0, 3.0)
#         path = QPainterPath()
#         path.moveTo(4, 11)
#         path.lineTo(4, 6)
#         path.lineTo(13, 6)
#         path.lineTo(16, 9)
#         painter.drawPath(path)

#     elif kind == "export":
#         path = QPainterPath()
#         path.moveTo(10, 13)
#         path.lineTo(6, 13)
#         path.lineTo(6, 26)
#         path.lineTo(26, 26)
#         path.lineTo(26, 13)
#         path.lineTo(22, 13)
#         painter.drawPath(path)
#         painter.drawLine(16, 19, 16, 5)
#         painter.drawLine(11, 10, 16, 5)
#         painter.drawLine(21, 10, 16, 5)

#     elif kind == "person":
#         painter.drawEllipse(QPointF(16, 10), 4.5, 4.5)
#         path = QPainterPath()
#         path.moveTo(7, 26)
#         path.quadTo(16, 17, 25, 26)
#         painter.drawPath(path)

#     elif kind == "text":
#         painter.drawLine(7, 7, 25, 7)
#         painter.drawLine(16, 7, 16, 26)
#         painter.drawLine(12, 26, 20, 26)

#     elif kind == "eyedropper":
#         path = QPainterPath()
#         path.moveTo(6, 26)
#         path.lineTo(11, 25)
#         path.lineTo(23, 13)
#         path.lineTo(19, 9)
#         path.lineTo(7, 21)
#         path.closeSubpath()
#         painter.drawPath(path)
#         painter.drawLine(17, 7, 25, 15)

#     elif kind == "back":
#         painter.drawLine(21, 7, 11, 16)
#         painter.drawLine(11, 16, 21, 25)

#     elif kind == "forward":
#         painter.drawLine(11, 7, 21, 16)
#         painter.drawLine(21, 16, 11, 25)

#     elif kind == "up":
#         painter.drawLine(16, 25, 16, 7)
#         painter.drawLine(8, 15, 16, 7)
#         painter.drawLine(24, 15, 16, 7)

#     elif kind == "drive":
#         painter.drawRoundedRect(QRectF(4, 9, 24, 14), 3.5, 3.5)
#         painter.drawLine(4, 18, 28, 18)
#         painter.drawEllipse(QPointF(23, 20.5), 1.0, 1.0)

#     elif kind == "image":
#         painter.drawRoundedRect(QRectF(4, 6, 24, 20), 3.0, 3.0)
#         painter.drawEllipse(QPointF(11, 12), 2.0, 2.0)
#         path = QPainterPath()
#         path.moveTo(6, 24)
#         path.lineTo(13, 17)
#         path.lineTo(18, 22)
#         path.lineTo(22, 18)
#         path.lineTo(26, 24)
#         painter.drawPath(path)

#     elif kind == "new_folder":
#         painter.drawRoundedRect(QRectF(4, 7, 24, 18), 3.0, 3.0)
#         path = QPainterPath()
#         path.moveTo(4, 11)
#         path.lineTo(4, 6)
#         path.lineTo(13, 6)
#         path.lineTo(16, 9)
#         painter.drawPath(path)
#         painter.drawLine(16, 13, 16, 21)
#         painter.drawLine(12, 17, 20, 17)

#     painter.end()
#     pixmap.setDevicePixelRatio(2.0)
#     return QIcon(pixmap)


# class ModernFileBrowserDialog(QDialog):
#     """Modern warm-paper Finder/Explorer file browser for opening and saving across the entire PC."""

#     IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

#     def __init__(
#         self,
#         parent=None,
#         mode="open",  # "open" or "save"
#         default_filename="depthtype_result.png",
#         initial_dir=None,
#     ):
#         super().__init__(parent)
#         self.mode = mode
#         self.selected_path = ""
#         self._history = []
#         self._history_idx = -1
#         self._navigating_history = False

#         self.setWindowTitle("Open Image" if mode == "open" else "Export Image")
#         self.resize(880, 560)
#         self.setMinimumSize(720, 460)
#         self.setModal(True)

#         if initial_dir and Path(initial_dir).exists():
#             start_dir = str(Path(initial_dir).resolve())
#         else:
#             pics = QStandardPaths.writableLocation(
#                 QStandardPaths.StandardLocation.PicturesLocation
#             )
#             start_dir = pics if pics and Path(pics).exists() else str(Path.home())

#         self._build_ui(default_filename)
#         self._apply_theme()
#         self._populate_sidebar()
#         self.navigate_to(start_dir)

#     def _build_ui(self, default_filename):
#         root = QVBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)


#         top_bar = QWidget()
#         top_bar.setObjectName("BrowserTopBar")
#         top_bar.setFixedHeight(50)

#         top_lay = QHBoxLayout(top_bar)
#         top_lay.setContentsMargins(14, 8, 14, 8)
#         top_lay.setSpacing(8)

#         self.back_btn = QPushButton()
#         self.back_btn.setIcon(create_vector_icon("back", "#292524", 13))
#         self.back_btn.setObjectName("NavIconBtn")
#         self.back_btn.setFixedSize(30, 30)
#         self.back_btn.setToolTip("Back")
#         self.back_btn.clicked.connect(self.go_back)

#         self.fwd_btn = QPushButton()
#         self.fwd_btn.setIcon(create_vector_icon("forward", "#292524", 13))
#         self.fwd_btn.setObjectName("NavIconBtn")
#         self.fwd_btn.setFixedSize(30, 30)
#         self.fwd_btn.setToolTip("Forward")
#         self.fwd_btn.clicked.connect(self.go_forward)

#         self.up_btn = QPushButton()
#         self.up_btn.setIcon(create_vector_icon("up", "#292524", 13))
#         self.up_btn.setObjectName("NavIconBtn")
#         self.up_btn.setFixedSize(30, 30)
#         self.up_btn.setToolTip("Parent Folder")
#         self.up_btn.clicked.connect(self.go_up)

#         self.path_input = QLineEdit()
#         self.path_input.setObjectName("PathBar")
#         self.path_input.setPlaceholderText("Enter path (e.g. D:\\Photos or C:\\Users)...")
#         self.path_input.returnPressed.connect(self._on_path_entered)

#         self.search_input = QLineEdit()
#         self.search_input.setObjectName("SearchBar")
#         self.search_input.setPlaceholderText("Filter files...")
#         self.search_input.setFixedWidth(185)
#         self.search_input.textChanged.connect(self._on_filter_changed)

#         top_lay.addWidget(self.back_btn)
#         top_lay.addWidget(self.fwd_btn)
#         top_lay.addWidget(self.up_btn)
#         top_lay.addSpacing(4)
#         top_lay.addWidget(self.path_input, 1)
#         top_lay.addWidget(self.search_input)

#         root.addWidget(top_bar)

#         sep1 = QFrame()
#         sep1.setFrameShape(QFrame.Shape.HLine)
#         sep1.setObjectName("BrowserSep")
#         root.addWidget(sep1)



#         body_split = QSplitter(Qt.Orientation.Horizontal)
#         body_split.setHandleWidth(1)
#         body_split.setObjectName("BrowserSplit")

#         self.places_list = QListWidget()
#         self.places_list.setObjectName("PlacesSidebar")
#         self.places_list.setMinimumWidth(165)
#         self.places_list.setMaximumWidth(230)
#         self.places_list.setIconSize(QSize(15, 15))
#         self.places_list.itemClicked.connect(self._on_place_clicked)

#         self.fs_model = QFileSystemModel(self)
#         self.fs_model.setFilter(
#             QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
#         )
#         self.fs_model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"])
#         self.fs_model.setNameFilterDisables(False)

#         self.tree_view = QTreeView()
#         self.tree_view.setObjectName("FileTree")
#         self.tree_view.setModel(self.fs_model)
#         self.tree_view.setRootIsDecorated(False)
#         self.tree_view.setItemsExpandable(False)
#         self.tree_view.setSortingEnabled(True)
#         self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
#         self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
#         self.tree_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
#         self.tree_view.setAlternatingRowColors(True)
#         self.tree_view.setIconSize(QSize(16, 16))
#         self.tree_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

#         header = self.tree_view.header()
#         header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
#         header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
#         header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
#         header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

#         self.tree_view.selectionModel().currentChanged.connect(self._on_selection_changed)
#         self.tree_view.doubleClicked.connect(self._on_item_double_clicked)

#         preview_pane = QWidget()
#         preview_pane.setObjectName("PreviewPane")
#         preview_pane.setMinimumWidth(200)
#         preview_pane.setMaximumWidth(250)

#         prev_lay = QVBoxLayout(preview_pane)
#         prev_lay.setContentsMargins(16, 18, 16, 18)
#         prev_lay.setSpacing(10)

#         self.thumb_label = QLabel("No Preview")
#         self.thumb_label.setObjectName("ThumbBox")
#         self.thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.thumb_label.setFixedHeight(175)

#         self.meta_name = QLabel("Select a file")
#         self.meta_name.setObjectName("MetaTitle")
#         self.meta_name.setWordWrap(True)
#         self.meta_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         self.meta_details = QLabel("")
#         self.meta_details.setObjectName("MetaSub")
#         self.meta_details.setWordWrap(True)
#         self.meta_details.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         prev_lay.addWidget(self.thumb_label)
#         prev_lay.addWidget(self.meta_name)
#         prev_lay.addWidget(self.meta_details)
#         prev_lay.addStretch()

#         body_split.addWidget(self.places_list)
#         body_split.addWidget(self.tree_view)
#         body_split.addWidget(preview_pane)
#         body_split.setSizes([185, 480, 215])

#         root.addWidget(body_split, 1)

#         sep2 = QFrame()
#         sep2.setFrameShape(QFrame.Shape.HLine)
#         sep2.setObjectName("BrowserSep")
#         root.addWidget(sep2)

#         bottom_bar = QWidget()
#         bottom_bar.setObjectName("BrowserBottomBar")
#         bottom_bar.setFixedHeight(54)

#         bot_lay = QHBoxLayout(bottom_bar)
#         bot_lay.setContentsMargins(14, 8, 14, 8)
#         bot_lay.setSpacing(10)

#         if self.mode == "save":
#             self.new_folder_btn = QPushButton(" New Folder")
#             self.new_folder_btn.setIcon(create_vector_icon("new_folder", "#292524", 14))
#             self.new_folder_btn.setObjectName("SecondaryBtn")
#             self.new_folder_btn.clicked.connect(self._create_new_folder)
#             bot_lay.addWidget(self.new_folder_btn)

#             name_lbl = QLabel("Save As:")
#             name_lbl.setObjectName("FieldLabel")
#             bot_lay.addWidget(name_lbl)

#             self.filename_input = QLineEdit(default_filename)
#             self.filename_input.setObjectName("FilenameInput")
#             self.filename_input.returnPressed.connect(self._confirm_selection)
#             bot_lay.addWidget(self.filename_input, 1)
#         else:
#             self.filename_input = QLineEdit()
#             self.filename_input.setObjectName("FilenameInput")
#             self.filename_input.setReadOnly(True)
#             self.filename_input.setPlaceholderText("Select an image file to open...")
#             bot_lay.addWidget(self.filename_input, 1)

#         self.format_combo = QComboBox()
#         self.format_combo.setObjectName("FormatCombo")
#         if self.mode == "open":
#             self.format_combo.addItem("All Images (*.png, *.jpg, *.webp, *.bmp)", ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"])
#             self.format_combo.addItem("PNG Images (*.png)", ["*.png"])
#             self.format_combo.addItem("JPEG Images (*.jpg, *.jpeg)", ["*.jpg", "*.jpeg"])
#             self.format_combo.addItem("All Files (*.*)", ["*"])
#         else:
#             self.format_combo.addItem("PNG Image (*.png)", ["*.png"])
#         self.format_combo.currentIndexChanged.connect(self._on_format_changed)
#         bot_lay.addWidget(self.format_combo)

#         cancel_btn = QPushButton("Cancel")
#         cancel_btn.setObjectName("SecondaryBtn")
#         cancel_btn.clicked.connect(self.reject)

#         self.action_btn = QPushButton("Open" if self.mode == "open" else "Export PNG")
#         self.action_btn.setObjectName("PrimaryBtn")
#         self.action_btn.clicked.connect(self._confirm_selection)
#         if self.mode == "open":
#             self.action_btn.setEnabled(False)

#         bot_lay.addWidget(cancel_btn)
#         bot_lay.addWidget(self.action_btn)

#         root.addWidget(bottom_bar)

#     def _populate_sidebar(self):
#         self.places_list.clear()

#         def add_header(text):
#             item = QListWidgetItem(text)
#             item.setFlags(Qt.ItemFlag.NoItemFlags)
#             font = item.font()
#             font.setPointSize(8)
#             font.setWeight(QFont.Weight.Bold)
#             item.setFont(font)
#             item.setForeground(QColor("#78716c"))
#             self.places_list.addItem(item)

#         def add_place(label, path_str, icon_kind="folder"):
#             if not path_str or not Path(path_str).exists():
#                 return
#             item = QListWidgetItem(create_vector_icon(icon_kind, "#44403c", 14), f"  {label}")
#             item.setData(Qt.ItemDataRole.UserRole, str(Path(path_str).resolve()))
#             self.places_list.addItem(item)

#         add_header("FAVORITES")
#         add_place("Desktop", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation))
#         add_place("Documents", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
#         add_place("Downloads", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation))
#         add_place("Pictures", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation), "image")
#         add_place("Home", str(Path.home()))

#         spacer = QListWidgetItem("")
#         spacer.setFlags(Qt.ItemFlag.NoItemFlags)
#         spacer.setSizeHint(QSize(10, 10))
#         self.places_list.addItem(spacer)

#         add_header("THIS PC · DRIVES")
#         for vol in QStorageInfo.mountedVolumes():
#             if vol.isValid() and vol.isReady():
#                 root_path = vol.rootPath()
#                 name = vol.displayName()
#                 drive_letter = root_path.rstrip("/\\")
#                 label = f"{name} ({drive_letter})" if name and name != root_path else f"Local Disk ({drive_letter})"
#                 add_place(label, root_path, "drive")

#     def navigate_to(self, directory_path):
#         target = Path(directory_path)
#         if not target.exists() or not target.is_dir():
#             return

#         clean_path = str(target.resolve())
#         idx = self.fs_model.setRootPath(clean_path)
#         self.tree_view.setRootIndex(idx)
#         self.path_input.setText(clean_path)

#         if not self._navigating_history:
#             self._history = self._history[: self._history_idx + 1]
#             if not self._history or self._history[-1] != clean_path:
#                 self._history.append(clean_path)
#                 self._history_idx = len(self._history) - 1

#         self.back_btn.setEnabled(self._history_idx > 0)
#         self.fwd_btn.setEnabled(self._history_idx < len(self._history) - 1)
#         self.up_btn.setEnabled(target.parent != target)

#     def go_back(self):
#         if self._history_idx > 0:
#             self._history_idx -= 1
#             self._navigating_history = True
#             self.navigate_to(self._history[self._history_idx])
#             self._navigating_history = False

#     def go_forward(self):
#         if self._history_idx < len(self._history) - 1:
#             self._history_idx += 1
#             self._navigating_history = True
#             self.navigate_to(self._history[self._history_idx])
#             self._navigating_history = False

#     def go_up(self):
#         curr = Path(self.fs_model.rootPath())
#         if curr.parent != curr:
#             self.navigate_to(str(curr.parent))

#     def _on_path_entered(self):
#         typed = self.path_input.text().strip().strip('"')
#         p = Path(typed)
#         if p.is_dir():
#             self.navigate_to(str(p))
#         elif p.is_file():
#             self.navigate_to(str(p.parent))
#             self.filename_input.setText(p.name)
#             if self.mode == "open":
#                 self.action_btn.setEnabled(True)

#     def _on_place_clicked(self, item):
#         target = item.data(Qt.ItemDataRole.UserRole)
#         if target:
#             self.navigate_to(target)

#     def _on_filter_changed(self, text):
#         base_filters = self.format_combo.currentData() or ["*"]
#         query = text.strip()
#         if not query:
#             self.fs_model.setNameFilters(base_filters)
#             return

#         custom = []
#         for pat in base_filters:
#             if pat == "*":
#                 custom.append(f"*{query}*")
#             else:
#                 ext = pat.lstrip("*")
#                 custom.append(f"*{query}*{ext}")
#         self.fs_model.setNameFilters(custom)

#     def _on_format_changed(self, _):
#         self._on_filter_changed(self.search_input.text())

#     def _on_selection_changed(self, current, _previous):
#         if not current.isValid():
#             return

#         path = Path(self.fs_model.filePath(current))
#         if path.is_dir():
#             self.meta_name.setText(path.name)
#             self.meta_details.setText("Folder")
#             self.thumb_label.setPixmap(QPixmap())
#             self.thumb_label.setText("Folder")
#             if self.mode == "open":
#                 self.filename_input.clear()
#                 self.action_btn.setEnabled(False)
#             return

#         self.filename_input.setText(path.name)
#         if self.mode == "open":
#             self.action_btn.setEnabled(True)

#         size_kb = path.stat().st_size / 1024.0
#         size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024.0:.2f} MB"
#         self.meta_name.setText(path.name)

#         if path.suffix.lower() in self.IMAGE_EXTS:
#             reader = QPixmap(str(path))
#             if not reader.isNull():
#                 scaled = reader.scaled(
#                     180,
#                     160,
#                     Qt.AspectRatioMode.KeepAspectRatio,
#                     Qt.TransformationMode.SmoothTransformation,
#                 )
#                 self.thumb_label.setText("")
#                 self.thumb_label.setPixmap(scaled)
#                 self.meta_details.setText(f"{reader.width()} × {reader.height()} px\n{size_str}")
#                 return

#         self.thumb_label.setPixmap(QPixmap())
#         self.thumb_label.setText(path.suffix.upper().lstrip(".") or "FILE")
#         self.meta_details.setText(size_str)

#     def _on_item_double_clicked(self, index):
#         if not index.isValid():
#             return
#         path = Path(self.fs_model.filePath(index))
#         if path.is_dir():
#             self.navigate_to(str(path))
#         elif path.is_file():
#             self.filename_input.setText(path.name)
#             self._confirm_selection()

#     def _create_new_folder(self):
#         curr_dir = Path(self.fs_model.rootPath())
#         base_name = "New Folder"
#         candidate = curr_dir / base_name
#         counter = 2
#         while candidate.exists():
#             candidate = curr_dir / f"{base_name} ({counter})"
#             counter += 1
#         try:
#             candidate.mkdir(parents=False, exist_ok=False)
#         except Exception as exc:
#             QMessageBox.warning(self, "New Folder", str(exc))

#     def _confirm_selection(self):
#         curr_dir = Path(self.fs_model.rootPath())
#         name = self.filename_input.text().strip()
#         if not name:
#             return

#         candidate = Path(name) if Path(name).is_absolute() else (curr_dir / name)

#         if self.mode == "open":
#             if candidate.is_dir():
#                 self.navigate_to(str(candidate))
#                 return
#             if candidate.is_file():
#                 self.selected_path = str(candidate.resolve())
#                 self.accept()
#         else:
#             if not candidate.name.lower().endswith(".png"):
#                 candidate = candidate.with_name(candidate.name + ".png")
#             self.selected_path = str(candidate.resolve())
#             self.accept()

#     def _apply_theme(self):
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f8f5ef;
#                 color: #1c1917;
#             }
#             QWidget#BrowserTopBar, QWidget#BrowserBottomBar {
#                 background-color: #f8f5ef;
#             }
#             QWidget#PreviewPane {
#                 background-color: #f4efe6;
#             }
#             QFrame#BrowserSep {
#                 background-color: #e4ddd1;
#                 max-height: 1px;
#                 border: none;
#             }
#             QSplitter#BrowserSplit::handle {
#                 background-color: #e4ddd1;
#             }
#             QListWidget#PlacesSidebar {
#                 background-color: #f2ede4;
#                 color: #292524;
#                 border: none;
#                 padding: 8px 6px;
#                 outline: none;
#                 font-size: 12px;
#             }
#             QListWidget#PlacesSidebar::item {
#                 padding: 6px 8px;
#                 border-radius: 6px;
#                 margin-bottom: 2px;
#             }
#             QListWidget#PlacesSidebar::item:hover {
#                 background-color: #e6dfd3;
#             }
#             QListWidget#PlacesSidebar::item:selected {
#                 background-color: #e0d7c8;
#                 color: #1c1917;
#                 font-weight: 600;
#             }
#             QTreeView#FileTree {
#                 background-color: #fbf9f5;
#                 alternate-background-color: #f6f2ea;
#                 color: #1c1917;
#                 border: none;
#                 outline: none;
#                 font-size: 12px;
#             }
#             QTreeView#FileTree::item {
#                 padding: 5px 6px;
#             }
#             QTreeView#FileTree::item:hover {
#                 background-color: #efeae0;
#             }
#             QTreeView#FileTree::item:selected {
#                 background-color: #2563eb;
#                 color: #ffffff;
#             }
#             QHeaderView::section {
#                 background-color: #f4efe6;
#                 color: #57534e;
#                 border: none;
#                 border-bottom: 1px solid #e4ddd1;
#                 padding: 6px 8px;
#                 font-size: 11px;
#                 font-weight: 600;
#             }
#             QLabel#ThumbBox {
#                 background-color: #fbf9f5;
#                 border: 1px solid #ded7cb;
#                 border-radius: 10px;
#                 color: #78716c;
#                 font-size: 11px;
#             }
#             QLabel#MetaTitle {
#                 color: #1c1917;
#                 font-size: 12px;
#                 font-weight: 600;
#             }
#             QLabel#MetaSub, QLabel#FieldLabel {
#                 color: #78716c;
#                 font-size: 11px;
#             }
#             QLineEdit#PathBar, QLineEdit#SearchBar, QLineEdit#FilenameInput {
#                 background-color: #fbf9f5;
#                 color: #1c1917;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 7px;
#                 padding: 5px 10px;
#                 font-size: 12px;
#                 selection-background-color: #2563eb;
#                 selection-color: #ffffff;
#             }
#             QLineEdit#PathBar:focus, QLineEdit#SearchBar:focus, QLineEdit#FilenameInput:focus {
#                 background-color: #ffffff;
#                 border: 1.5px solid #2563eb;
#             }
#             QComboBox#FormatCombo {
#                 background-color: #fbf9f5;
#                 color: #292524;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 7px;
#                 padding: 5px 10px;
#                 font-size: 12px;
#             }
#             QComboBox#FormatCombo QAbstractItemView {
#                 background-color: #fbf9f5;
#                 color: #1c1917;
#                 border: 1px solid #d6cfc3;
#                 selection-background-color: #2563eb;
#                 selection-color: #ffffff;
#             }
#             QPushButton#NavIconBtn {
#                 background-color: #fbf9f5;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 7px;
#             }
#             QPushButton#NavIconBtn:hover {
#                 background-color: #efeae0;
#             }
#             QPushButton#NavIconBtn:disabled {
#                 opacity: 0.45;
#             }
#             QPushButton#SecondaryBtn {
#                 background-color: #fbf9f5;
#                 color: #292524;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 7px;
#                 padding: 6px 14px;
#                 font-size: 12px;
#                 font-weight: 500;
#             }
#             QPushButton#SecondaryBtn:hover {
#                 background-color: #efeae0;
#             }
#             QPushButton#PrimaryBtn {
#                 background-color: #2563eb;
#                 color: #ffffff;
#                 border: none;
#                 border-radius: 7px;
#                 padding: 6px 18px;
#                 font-size: 12px;
#                 font-weight: 600;
#             }
#             QPushButton#PrimaryBtn:hover {
#                 background-color: #1d4ed8;
#             }
#             QPushButton#PrimaryBtn:disabled {
#                 background-color: #e5dfd4;
#                 color: #a8a29e;
#             }
#         """)


# class AnimatedModeSwitch(QWidget):
#     """Warm paper segmented control with a smoothly sliding indicator pill."""

#     modeChanged = Signal(str)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(244, 34)
#         self._mode = "select"
#         self._pill_x = 3.0
#         self._pill_w = 122.0
#         self._hovered = None

#         self.anim = QVariantAnimation(self)
#         self.anim.setDuration(260)
#         self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
#         self.anim.valueChanged.connect(self._on_anim_step)

#         self.setMouseTracking(True)
#         self.setCursor(Qt.CursorShape.PointingHandCursor)

#     def _on_anim_step(self, val):
#         self._pill_x = float(val)
#         self.update()

#     def set_mode(self, mode, animate=True):
#         if mode not in ("select", "text"):
#             return
#         self._mode = mode
#         target_x = 3.0 if mode == "select" else (self.width() - self._pill_w - 3.0)

#         if animate and abs(self._pill_x - target_x) > 0.5:
#             self.anim.stop()
#             self.anim.setStartValue(self._pill_x)
#             self.anim.setEndValue(target_x)
#             self.anim.start()
#         else:
#             self.anim.stop()
#             self._pill_x = target_x
#             self.update()

#     def mouseMoveEvent(self, event):
#         hov = "select" if event.position().x() < self.width() / 2.0 else "text"
#         if hov != self._hovered:
#             self._hovered = hov
#             self.update()

#     def leaveEvent(self, event):
#         self._hovered = None
#         self.update()

#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             chosen = "select" if event.position().x() < self.width() / 2.0 else "text"
#             if chosen != self._mode:
#                 self.set_mode(chosen, animate=True)
#                 self.modeChanged.emit(chosen)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#         rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
#         painter.setPen(QPen(QColor("#ded7cb"), 1.0))
#         painter.setBrush(QColor("#ece6db"))
#         painter.drawRoundedRect(rect, 9.0, 9.0)

#         pill_rect = QRectF(self._pill_x, 3.0, self._pill_w, self.height() - 6.0)
#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.setBrush(QColor(28, 25, 23, 22))
#         painter.drawRoundedRect(pill_rect.adjusted(0, 1.5, 0, 1.5), 7.0, 7.0)

#         painter.setPen(QPen(QColor("#e5dfd4"), 1.0))
#         painter.setBrush(QColor("#fbf9f5"))
#         painter.drawRoundedRect(pill_rect, 7.0, 7.0)

#         font = QFont(self.font())
#         font.setPointSize(9)
#         font.setWeight(QFont.Weight.DemiBold)
#         painter.setFont(font)

#         left_rect = QRectF(3.0, 0.0, self._pill_w, self.height())
#         sel_active = self._mode == "select"
#         sel_color = "#1c1917" if sel_active else ("#44403c" if self._hovered == "select" else "#78716c")
#         icon_sel = create_vector_icon("person", sel_color, 13)
#         icon_sel.paint(painter, QRectF(left_rect.left() + 12, (self.height() - 13) / 2.0, 13, 13).toRect())
#         painter.setPen(QColor(sel_color))
#         painter.drawText(left_rect.adjusted(28, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Subject Mask")

#         right_rect = QRectF(self.width() - self._pill_w - 3.0, 0.0, self._pill_w, self.height())
#         txt_active = self._mode == "text"
#         txt_color = "#1c1917" if txt_active else ("#44403c" if self._hovered == "text" else "#78716c")
#         icon_txt = create_vector_icon("text", txt_color, 13)
#         icon_txt.paint(painter, QRectF(right_rect.left() + 16, (self.height() - 13) / 2.0, 13, 13).toRect())
#         painter.setPen(QColor(txt_color))
#         painter.drawText(right_rect.adjusted(32, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Typography")


# class OpacityPopover(QWidget):
#     """Elevated warm-paper pill popover with smooth fade + vertical glide animation."""

#     opacityChanged = Signal(int)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(226, 44)
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

#         self._opacity_effect = QGraphicsOpacityEffect(self)
#         self._opacity_effect.setOpacity(0.0)
#         self.setGraphicsEffect(self._opacity_effect)

#         self._fade_anim = QVariantAnimation(self)
#         self._fade_anim.setDuration(200)
#         self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
#         self._fade_anim.valueChanged.connect(self._on_fade_step)
#         self._fade_anim.finished.connect(self._on_fade_finished)

#         self._slide_anim = QVariantAnimation(self)
#         self._slide_anim.setDuration(220)
#         self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
#         self._slide_anim.valueChanged.connect(self._on_slide_step)

#         self._target_x = 0
#         self._hiding = False

#         layout = QHBoxLayout(self)
#         layout.setContentsMargins(16, 4, 16, 4)
#         layout.setSpacing(10)

#         title = QLabel("Opacity")
#         title.setObjectName("PopoverTitle")

#         self.slider = QSlider(Qt.Orientation.Horizontal)
#         self.slider.setRange(10, 100)
#         self.slider.setValue(100)
#         self.slider.setCursor(Qt.CursorShape.PointingHandCursor)

#         self.value_label = QLabel("100%")
#         self.value_label.setObjectName("PopoverValue")
#         self.value_label.setFixedWidth(36)
#         self.value_label.setAlignment(
#             Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
#         )

#         layout.addWidget(title)
#         layout.addWidget(self.slider, 1)
#         layout.addWidget(self.value_label)

#         self.slider.valueChanged.connect(self._on_value_changed)
#         self.hide()

#     def _on_value_changed(self, val):
#         self.value_label.setText(f"{val}%")
#         self.opacityChanged.emit(val)

#     def _on_fade_step(self, val):
#         self._opacity_effect.setOpacity(float(val))

#     def _on_slide_step(self, val):
#         self.move(self._target_x, int(val))

#     def _on_fade_finished(self):
#         if self._hiding:
#             super().hide()
#             self._hiding = False

#     def show_animated(self, target_x, target_y):
#         self._target_x = target_x
#         self._hiding = False

#         if not self.isVisible() or self._opacity_effect.opacity() < 0.05:
#             self.move(target_x, target_y + 8)
#             super().show()
#             self.raise_()

#             self._fade_anim.stop()
#             self._fade_anim.setStartValue(self._opacity_effect.opacity())
#             self._fade_anim.setEndValue(1.0)
#             self._fade_anim.start()

#             self._slide_anim.stop()
#             self._slide_anim.setStartValue(target_y + 8)
#             self._slide_anim.setEndValue(target_y)
#             self._slide_anim.start()
#         else:
#             self.move(target_x, target_y)
#             self.raise_()

#     def hide_animated(self):
#         if not self.isVisible() or self._hiding:
#             return
#         self._hiding = True
#         self._fade_anim.stop()
#         self._fade_anim.setStartValue(self._opacity_effect.opacity())
#         self._fade_anim.setEndValue(0.0)
#         self._fade_anim.start()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#         rect = QRectF(self.rect()).adjusted(2, 2, -2, -3)
#         radius = rect.height() / 2.0

#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.setBrush(QColor(28, 25, 23, 22))
#         painter.drawRoundedRect(rect.adjusted(0, 3, 0, 4), radius, radius)
#         painter.setBrush(QColor(28, 25, 23, 14))
#         painter.drawRoundedRect(rect.adjusted(-1, 1, 1, 2), radius, radius)

#         grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
#         grad.setColorAt(0.0, QColor("#fffdf9"))
#         grad.setColorAt(1.0, QColor("#f5f0e6"))

#         painter.setPen(QPen(QColor("#d6cfc3"), 1.0))
#         painter.setBrush(QBrush(grad))
#         painter.drawRoundedRect(rect, radius, radius)


# class WarmColorPickerDialog(QDialog):
#     """Clean, warm light-themed custom color picker with HSB spectrum + hex input."""

#     colorSelected = Signal(str)

#     def __init__(self, initial_hex="#ffffff", parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Text Color")
#         self.setFixedSize(290, 275)
#         self.setModal(True)

#         col = QColor(initial_hex)
#         if not col.isValid():
#             col = QColor("#ffffff")
#         h, s, v, _ = col.getHsvF()
#         self._hue = max(0.0, h) if h >= 0 else 0.0
#         self._sat = s
#         self._val = v

#         self._setup_ui()
#         self._sync_from_hsv()

#     def _setup_ui(self):
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f8f5ef;
#             }
#             QLabel {
#                 color: #292524;
#                 font-size: 12px;
#                 background: transparent;
#             }
#             QLineEdit {
#                 background-color: #fbf9f5;
#                 color: #1c1917;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 padding: 5px 8px;
#                 font-size: 12px;
#                 font-weight: 600;
#             }
#             QLineEdit:focus {
#                 border: 1.5px solid #2563eb;
#             }
#             QPushButton#CancelBtn {
#                 background-color: #fbf9f5;
#                 color: #292524;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 padding: 6px 14px;
#                 font-size: 12px;
#             }
#             QPushButton#CancelBtn:hover {
#                 background-color: #efeae0;
#             }
#             QPushButton#ApplyBtn {
#                 background-color: #2563eb;
#                 color: #ffffff;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 6px 16px;
#                 font-size: 12px;
#                 font-weight: 600;
#             }
#             QPushButton#ApplyBtn:hover {
#                 background-color: #1d4ed8;
#             }
#         """)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(16, 16, 16, 16)
#         layout.setSpacing(12)

#         self.sv_box = _SVSquare(self)
#         self.sv_box.svChanged.connect(self._on_sv_changed)
#         layout.addWidget(self.sv_box)

#         self.hue_bar = _HueSliderBar(self)
#         self.hue_bar.hueChanged.connect(self._on_hue_changed)
#         layout.addWidget(self.hue_bar)

#         hex_row = QHBoxLayout()
#         hex_row.setSpacing(10)

#         self.preview_swatch = QFrame()
#         self.preview_swatch.setFixedSize(28, 28)

#         self.hex_input = QLineEdit()
#         self.hex_input.setMaxLength(7)
#         self.hex_input.textEdited.connect(self._on_hex_edited)

#         hex_row.addWidget(self.preview_swatch)
#         hex_row.addWidget(QLabel("Hex"))
#         hex_row.addWidget(self.hex_input, 1)
#         layout.addLayout(hex_row)

#         btn_row = QHBoxLayout()
#         btn_row.addStretch()

#         cancel_btn = QPushButton("Cancel")
#         cancel_btn.setObjectName("CancelBtn")
#         cancel_btn.clicked.connect(self.reject)

#         apply_btn = QPushButton("Apply")
#         apply_btn.setObjectName("ApplyBtn")
#         apply_btn.clicked.connect(self._on_apply)

#         btn_row.addWidget(cancel_btn)
#         btn_row.addWidget(apply_btn)
#         layout.addLayout(btn_row)

#     def _current_color(self):
#         c = QColor()
#         c.setHsvF(self._hue, self._sat, self._val, 1.0)
#         return c

#     def _sync_from_hsv(self):
#         self.sv_box.set_hsv(self._hue, self._sat, self._val)
#         self.hue_bar.set_hue(self._hue)
#         c = self._current_color()
#         self.preview_swatch.setStyleSheet(
#             f"background-color: {c.name()}; border-radius: 6px; border: 1px solid #d6cfc3;"
#         )
#         if not self.hex_input.hasFocus():
#             self.hex_input.setText(c.name().upper())

#     def _on_sv_changed(self, s, v):
#         self._sat = s
#         self._val = v
#         self._sync_from_hsv()

#     def _on_hue_changed(self, h):
#         self._hue = h
#         self._sync_from_hsv()

#     def _on_hex_edited(self, text):
#         if len(text) == 7 and text.startswith("#"):
#             c = QColor(text)
#             if c.isValid():
#                 h, s, v, _ = c.getHsvF()
#                 if h >= 0:
#                     self._hue = h
#                 self._sat = s
#                 self._val = v
#                 self.sv_box.set_hsv(self._hue, self._sat, self._val)
#                 self.hue_bar.set_hue(self._hue)
#                 self.preview_swatch.setStyleSheet(
#                     f"background-color: {c.name()}; border-radius: 6px; border: 1px solid #d6cfc3;"
#                 )

#     def _on_apply(self):
#         self.colorSelected.emit(self._current_color().name())
#         self.accept()


# class _SVSquare(QWidget):
#     svChanged = Signal(float, float)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedHeight(136)
#         self.setCursor(Qt.CursorShape.CrossCursor)
#         self._hue = 0.0
#         self._sat = 0.0
#         self._val = 1.0

#     def set_hsv(self, h, s, v):
#         self._hue = h
#         self._sat = s
#         self._val = v
#         self.update()

#     def _pick(self, pos):
#         s = max(0.0, min(1.0, pos.x() / max(1, self.width())))
#         v = max(0.0, min(1.0, 1.0 - pos.y() / max(1, self.height())))
#         self.svChanged.emit(s, v)

#     def mousePressEvent(self, e):
#         if e.button() == Qt.MouseButton.LeftButton:
#             self._pick(e.position())

#     def mouseMoveEvent(self, e):
#         if e.buttons() & Qt.MouseButton.LeftButton:
#             self._pick(e.position())

#     def paintEvent(self, e):
#         p = QPainter(self)
#         p.setRenderHint(QPainter.RenderHint.Antialiasing)
#         r = QRectF(self.rect())

#         path = QPainterPath()
#         path.addRoundedRect(r, 8, 8)
#         p.setClipPath(path)

#         pure = QColor()
#         pure.setHsvF(self._hue, 1.0, 1.0)
#         g_sat = QLinearGradient(0, 0, r.width(), 0)
#         g_sat.setColorAt(0.0, QColor("#ffffff"))
#         g_sat.setColorAt(1.0, pure)
#         p.fillRect(r, g_sat)

#         g_val = QLinearGradient(0, 0, 0, r.height())
#         g_val.setColorAt(0.0, QColor(0, 0, 0, 0))
#         g_val.setColorAt(1.0, QColor(0, 0, 0, 255))
#         p.fillRect(r, g_val)

#         cx = self._sat * r.width()
#         cy = (1.0 - self._val) * r.height()
#         p.setPen(QPen(QColor("#ffffff"), 2.0))
#         p.setBrush(Qt.BrushStyle.NoBrush)
#         p.drawEllipse(QPointF(cx, cy), 6, 6)
#         p.setPen(QPen(QColor("#1c1917"), 1.0))
#         p.drawEllipse(QPointF(cx, cy), 7, 7)


# class _HueSliderBar(QWidget):
#     hueChanged = Signal(float)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedHeight(16)
#         self.setCursor(Qt.CursorShape.PointingHandCursor)
#         self._hue = 0.0

#     def set_hue(self, h):
#         self._hue = h
#         self.update()

#     def _pick(self, pos):
#         h = max(0.0, min(0.999, pos.x() / max(1, self.width())))
#         self.hueChanged.emit(h)

#     def mousePressEvent(self, e):
#         if e.button() == Qt.MouseButton.LeftButton:
#             self._pick(e.position())

#     def mouseMoveEvent(self, e):
#         if e.buttons() & Qt.MouseButton.LeftButton:
#             self._pick(e.position())

#     def paintEvent(self, e):
#         p = QPainter(self)
#         p.setRenderHint(QPainter.RenderHint.Antialiasing)
#         r = QRectF(self.rect()).adjusted(0, 2, 0, -2)

#         grad = QLinearGradient(0, 0, r.width(), 0)
#         for i in range(7):
#             c = QColor()
#             c.setHsvF(min(0.999, i / 6.0), 1.0, 1.0)
#             grad.setColorAt(i / 6.0, c)

#         p.setPen(Qt.PenStyle.NoPen)
#         p.setBrush(grad)
#         p.drawRoundedRect(r, 6, 6)

#         kx = self._hue * r.width()
#         p.setPen(QPen(QColor("#1c1917"), 1.5))
#         p.setBrush(QColor("#ffffff"))
#         p.drawEllipse(QPointF(kx, self.height() / 2.0), 6.5, 6.5)


# class ImageCanvas(QWidget):

#     def __init__(self, editor):
#         super().__init__()
#         self.editor = editor

#         self.setMinimumSize(640, 480)
#         self.setMouseTracking(True)
#         self.setAcceptDrops(True)

#         self.pixmap = QPixmap()
#         self.image_size = None

#         self.points = []
#         self.mode = "select"

#         self.dragging_text = False
#         self.resizing_corner = None
#         self.resize_anchor = (0.0, 0.0)
#         self.resize_start_dist = 1.0
#         self.resize_start_font = 130
#         self.resize_start_pos = (0, 0)
#         self.resize_start_size = (1, 1)

#         self.text_selected = False
#         self.hovering_text = False
#         self.hover_corner = None
#         self.hovering_dropzone = False
#         self.eyedropper_active = False
#         self.drag_offset = (0, 0)
#         self.press_pos = QPointF()

#         self.opacity_popover = OpacityPopover(self)
#         self.opacity_popover.opacityChanged.connect(
#             self.editor.on_opacity_changed
#         )

#         self.cutout_anim_progress = 0.0
#         self.cutout_anim_active = False
#         self.cutout_contour_pixmap = None
#         self.cutout_subject_pixmap = None
#         self.anim_timer = QTimer(self)
#         self.anim_timer.setInterval(16)
#         self.anim_timer.timeout.connect(self._step_cutout_animation)

#     def start_cutout_animation(self, original_pil, mask):
#         if original_pil is None or mask is None:
#             return

#         dpr = self.devicePixelRatioF()
#         w, h = original_pil.size

#         mask_u8 = (mask * 255).astype(np.uint8)
#         edges = cv2.Canny(mask_u8, 60, 160)
#         edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
#         edges_blur = cv2.GaussianBlur(edges, (0, 0), 1.4)

#         contour_rgba = np.zeros((h, w, 4), dtype=np.uint8)
#         contour_rgba[:, :, 0] = 37
#         contour_rgba[:, :, 1] = 99
#         contour_rgba[:, :, 2] = 235
#         contour_rgba[:, :, 3] = np.clip(edges_blur.astype(np.int32) * 2, 0, 220).astype(np.uint8)

#         c_qimg = QImage(contour_rgba.data, w, h, QImage.Format.Format_RGBA8888)
#         self.cutout_contour_pixmap = QPixmap.fromImage(c_qimg.copy())
#         self.cutout_contour_pixmap.setDevicePixelRatio(dpr)

#         subj_pil = original_pil.convert("RGBA")
#         subj_pil.putalpha(Image.fromarray(mask_u8, mode="L"))
#         self.cutout_subject_pixmap = pil_to_pixmap(subj_pil, dpr=dpr)

#         self.cutout_anim_progress = 0.0
#         self.cutout_anim_active = True
#         self.anim_timer.start()

#     def _step_cutout_animation(self):
#         self.cutout_anim_progress += 0.032
#         if self.cutout_anim_progress >= 1.0:
#             self.cutout_anim_progress = 1.0
#             self.cutout_anim_active = False
#             self.cutout_contour_pixmap = None
#             self.cutout_subject_pixmap = None
#             self.anim_timer.stop()
#         self.update()

#     def set_preview(self, pixmap):
#         self.pixmap = pixmap
#         self.position_opacity_popover()
#         self.update()

#     def dropzone_rect(self):
#         card_w, card_h = 340, 190
#         return QRectF(
#             (self.width() - card_w) / 2,
#             (self.height() - card_h) / 2,
#             card_w,
#             card_h
#         )

#     def image_rect(self):
#         if self.pixmap.isNull() or not self.image_size:
#             return QRectF()

#         margin = 28
#         area = self.rect().adjusted(margin, margin, -margin, -margin)
#         if area.width() <= 0 or area.height() <= 0:
#             return QRectF()

#         img_w, img_h = self.image_size
#         scale = min(area.width() / img_w, area.height() / img_h)

#         draw_w = img_w * scale
#         draw_h = img_h * scale

#         x = (self.width() - draw_w) / 2.0
#         y = (self.height() - draw_h) / 2.0

#         return QRectF(x, y, draw_w, draw_h)

#     def image_to_widget_rect(self, img_rect):
#         target = self.image_rect()
#         if target.isNull() or not self.image_size:
#             return QRectF()

#         bx, by, bw, bh = img_rect
#         sx = target.width() / self.image_size[0]
#         sy = target.height() / self.image_size[1]

#         return QRectF(
#             target.x() + bx * sx,
#             target.y() + by * sy,
#             bw * sx,
#             bh * sy
#         )

#     def widget_to_image(self, position, clamp=True):
#         rect = self.image_rect()
#         if rect.isNull() or not self.image_size:
#             return None

#         if clamp and not rect.contains(position):
#             return None

#         nx = (position.x() - rect.x()) / rect.width()
#         ny = (position.y() - rect.y()) / rect.height()

#         x = int(nx * self.image_size[0])
#         y = int(ny * self.image_size[1])

#         if clamp:
#             return (
#                 max(0, min(x, self.image_size[0] - 1)),
#                 max(0, min(y, self.image_size[1] - 1))
#             )
#         return (x, y)

#     def get_widget_text_box(self):
#         bounds = self.editor.get_text_bounds()
#         if bounds is None:
#             return QRectF()
#         return self.image_to_widget_rect(bounds).adjusted(-6, -4, 6, 4)

#     def get_corner_rects(self, box):
#         r = 10.0
#         return {
#             "tl": QRectF(box.left() - r, box.top() - r, r * 2, r * 2),
#             "tr": QRectF(box.right() - r, box.top() - r, r * 2, r * 2),
#             "bl": QRectF(box.left() - r, box.bottom() - r, r * 2, r * 2),
#             "br": QRectF(box.right() - r, box.bottom() - r, r * 2, r * 2),
#         }

#     def hit_test_corner(self, pos):
#         if self.mode != "text" or self.image_size is None:
#             return None
#         box = self.get_widget_text_box()
#         if box.isNull():
#             return None
#         for key, rect in self.get_corner_rects(box).items():
#             if rect.contains(pos):
#                 return key
#         return None

#     def position_opacity_popover(self):
#         if (
#             not self.text_selected
#             or self.mode != "text"
#             or self.image_size is None
#             or not self.editor.text_input.text().strip()
#         ):
#             self.opacity_popover.hide_animated()
#             return

#         box = self.get_widget_text_box()
#         if box.isNull():
#             self.opacity_popover.hide_animated()
#             return

#         pw = self.opacity_popover.width()
#         ph = self.opacity_popover.height()

#         px = int(box.center().x() - pw / 2)
#         py = int(box.top() - ph - 12)

#         if py < 12:
#             py = int(box.bottom() + 12)

#         px = max(12, min(px, self.width() - pw - 12))
#         py = max(12, min(py, self.height() - ph - 12))

#         self.opacity_popover.show_animated(px, py)

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self.position_opacity_popover()

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             urls = event.mimeData().urls()
#             if urls and urls[0].toLocalFile().lower().endswith(
#                 (".png", ".jpg", ".jpeg", ".webp", ".bmp")
#             ):
#                 self.hovering_dropzone = True
#                 self.update()
#                 event.acceptProposedAction()

#     def dragLeaveEvent(self, event):
#         self.hovering_dropzone = False
#         self.update()

#     def dropEvent(self, event):
#         self.hovering_dropzone = False
#         urls = event.mimeData().urls()
#         if urls:
#             path = urls[0].toLocalFile()
#             self.editor.load_image_from_path(path)

#     def mousePressEvent(self, event):
#         if self.image_size is None:
#             if (
#                 event.button() == Qt.MouseButton.LeftButton
#                 and self.dropzone_rect().contains(event.position())
#             ):
#                 self.editor.open_image()
#             return

#         if self.eyedropper_active and event.button() == Qt.MouseButton.LeftButton:
#             point = self.widget_to_image(event.position())
#             if point is not None:
#                 self.editor.sample_color_from_image(point[0], point[1])
#             else:
#                 self.editor.set_eyedropper_mode(False)
#             return

#         if event.button() != Qt.MouseButton.LeftButton:
#             if (
#                 self.mode == "select"
#                 and event.button() == Qt.MouseButton.RightButton
#             ):
#                 point = self.widget_to_image(event.position())
#                 if point:
#                     self.points.append((point[0], point[1], 0))
#                     self.editor.add_selection_point(point[0], point[1], 0)
#             return

#         self.press_pos = event.position()

#         if self.mode == "select":
#             point = self.widget_to_image(event.position())
#             if point is not None:
#                 x, y = point
#                 self.points.append((x, y, 1))
#                 self.editor.add_selection_point(x, y, 1)
#             return

#         if self.mode == "text":
#             corner = self.hit_test_corner(event.position())
#             if corner is not None:
#                 bounds = self.editor.get_text_bounds()
#                 if bounds is not None:
#                     bx, by, bw, bh = bounds
#                     self.resizing_corner = corner
#                     self.resize_start_font = self.editor.font_size
#                     self.resize_start_pos = (bx, by)
#                     self.resize_start_size = (max(1, bw), max(1, bh))

#                     anchors = {
#                         "tl": (bx + bw, by + bh),
#                         "tr": (bx, by + bh),
#                         "bl": (bx + bw, by),
#                         "br": (bx, by),
#                     }
#                     self.resize_anchor = anchors[corner]

#                     img_pt = self.widget_to_image(event.position(), clamp=False)
#                     if img_pt is not None:
#                         dx = img_pt[0] - self.resize_anchor[0]
#                         dy = img_pt[1] - self.resize_anchor[1]
#                         self.resize_start_dist = max(10.0, np.hypot(dx, dy))

#                     self.text_selected = True
#                     self.opacity_popover.hide_animated()
#                     self.update()
#                     return

#             box = self.get_widget_text_box()
#             if not box.isNull() and box.contains(event.position()):
#                 bounds = self.editor.get_text_bounds()
#                 point = self.widget_to_image(event.position(), clamp=False)
#                 if bounds is not None and point is not None:
#                     bx, by, _, _ = bounds
#                     self.dragging_text = True
#                     self.drag_offset = (point[0] - bx, point[1] - by)
#                     self.text_selected = True
#                     self.setCursor(Qt.CursorShape.ClosedHandCursor)
#                     self.position_opacity_popover()
#                     self.update()
#                     return

#             self.text_selected = False
#             self.opacity_popover.hide_animated()
#             self.update()

#     def mouseMoveEvent(self, event):
#         if self.image_size is None:
#             hovered = self.dropzone_rect().contains(event.position())
#             if hovered != self.hovering_dropzone:
#                 self.hovering_dropzone = hovered
#                 self.setCursor(
#                     Qt.CursorShape.PointingHandCursor
#                     if hovered else Qt.CursorShape.ArrowCursor
#                 )
#                 self.update()
#             return

#         if self.eyedropper_active:
#             point = self.widget_to_image(event.position())
#             self.setCursor(
#                 Qt.CursorShape.CrossCursor
#                 if point is not None else Qt.CursorShape.ArrowCursor
#             )
#             return

#         if self.mode == "select":
#             point = self.widget_to_image(event.position())
#             self.setCursor(
#                 Qt.CursorShape.PointingHandCursor
#                 if point is not None else Qt.CursorShape.ArrowCursor
#             )
#             return

#         if self.resizing_corner is not None:
#             img_pt = self.widget_to_image(event.position(), clamp=False)
#             if img_pt is not None:
#                 ax, ay = self.resize_anchor
#                 dx = img_pt[0] - ax
#                 dy = img_pt[1] - ay
#                 curr_dist = max(10.0, np.hypot(dx, dy))
#                 scale = curr_dist / self.resize_start_dist

#                 new_font = int(
#                     np.clip(round(self.resize_start_font * scale), 16, 650)
#                 )
#                 self.editor.set_font_size(new_font)

#                 new_bounds = self.editor.get_text_bounds()
#                 if new_bounds is not None:
#                     _, _, nw, nh = new_bounds
#                     if self.resizing_corner == "tl":
#                         nx, ny = ax - nw, ay - nh
#                     elif self.resizing_corner == "tr":
#                         nx, ny = ax, ay - nh
#                     elif self.resizing_corner == "bl":
#                         nx, ny = ax - nw, ay
#                     else:
#                         nx, ny = ax, ay

#                     self.editor.place_text(int(nx), int(ny))
#             return

#         if self.dragging_text and self.mode == "text":
#             point = self.widget_to_image(event.position(), clamp=False)
#             if point is not None:
#                 x = point[0] - self.drag_offset[0]
#                 y = point[1] - self.drag_offset[1]
#                 self.editor.place_text(x, y)
#             return

#         if self.mode == "text":
#             corner = self.hit_test_corner(event.position())
#             if corner != self.hover_corner:
#                 self.hover_corner = corner
#                 self.update()

#             if corner in ("tl", "br"):
#                 self.setCursor(Qt.CursorShape.SizeFDiagCursor)
#                 return
#             elif corner in ("tr", "bl"):
#                 self.setCursor(Qt.CursorShape.SizeBDiagCursor)
#                 return

#             box = self.get_widget_text_box()
#             is_over = not box.isNull() and box.contains(event.position())
#             if is_over != self.hovering_text:
#                 self.hovering_text = is_over
#                 self.update()

#             self.setCursor(
#                 Qt.CursorShape.OpenHandCursor
#                 if is_over else Qt.CursorShape.ArrowCursor
#             )
#         else:
#             self.setCursor(Qt.CursorShape.ArrowCursor)

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             if self.resizing_corner is not None:
#                 self.resizing_corner = None
#                 self.position_opacity_popover()
#                 self.update()
#                 return

#             if self.dragging_text:
#                 self.dragging_text = False
#                 self.setCursor(Qt.CursorShape.OpenHandCursor)
#                 self.position_opacity_popover()
#                 self.update()

#     def _paint_warm_prism_background(self, painter):
#         w = float(self.width())
#         h = float(self.height())

#         painter.fillRect(self.rect(), QColor("#f2ede4"))

#         orbs = [
#             (w * 0.20, h * 0.24, max(w, h) * 0.52, QColor(225, 29, 72, 22)),
#             (w * 0.80, h * 0.22, max(w, h) * 0.54, QColor(124, 58, 237, 22)),
#             (w * 0.75, h * 0.80, max(w, h) * 0.50, QColor(8, 145, 178, 20)),
#             (w * 0.24, h * 0.82, max(w, h) * 0.48, QColor(217, 119, 6, 22)),
#         ]
#         for cx, cy, radius, color in orbs:
#             grad = QRadialGradient(cx, cy, radius)
#             grad.setColorAt(0.0, color)
#             grad.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
#             painter.fillRect(self.rect(), QBrush(grad))

#         grid_step = 44
#         painter.setPen(QPen(QColor(68, 64, 60, 13), 1))
#         for gx in range(0, int(w), grid_step):
#             painter.drawLine(gx, 0, gx, int(h))
#         for gy in range(0, int(h), grid_step):
#             painter.drawLine(0, gy, int(w), gy)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

#         self._paint_warm_prism_background(painter)

#         if self.pixmap.isNull():
#             card = self.dropzone_rect()

#             bg_color = (
#                 QColor(251, 249, 245, 245)
#                 if self.hovering_dropzone else QColor(248, 245, 239, 225)
#             )
#             border_color = (
#                 QColor("#2563eb")
#                 if self.hovering_dropzone else QColor("#d6cfc3")
#             )

#             painter.setPen(QPen(border_color, 1.4, Qt.PenStyle.DashLine))
#             painter.setBrush(bg_color)
#             painter.drawRoundedRect(card, 14, 14)

#             icon_rect = QRectF(
#                 card.center().x() - 16, card.top() + 44, 32, 32
#             )
#             icon = create_vector_icon("folder", "#57534e", 22)
#             icon.paint(
#                 painter, icon_rect.toRect(), Qt.AlignmentFlag.AlignCenter
#             )

#             title_font = QFont(self.font())
#             title_font.setPointSize(13)
#             title_font.setWeight(QFont.Weight.DemiBold)
#             painter.setFont(title_font)
#             painter.setPen(QColor("#1c1917"))
#             painter.drawText(
#                 QRectF(card.left(), card.top() + 88, card.width(), 22),
#                 Qt.AlignmentFlag.AlignCenter,
#                 "Drop an Image Here"
#             )

#             sub_font = QFont(self.font())
#             sub_font.setPointSize(11)
#             painter.setFont(sub_font)
#             painter.setPen(QColor("#78716c"))
#             painter.drawText(
#                 QRectF(card.left(), card.top() + 112, card.width(), 20),
#                 Qt.AlignmentFlag.AlignCenter,
#                 "or click to browse PNG, JPG, or WebP"
#             )
#             return

#         target = self.image_rect()

#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.setBrush(QColor(28, 25, 23, 28))
#         painter.drawRoundedRect(target.adjusted(-2, 4, 2, 8), 6, 6)

#         painter.drawPixmap(
#             target,
#             self.pixmap,
#             QRectF(self.pixmap.rect())
#         )

#         if self.cutout_anim_active and self.cutout_contour_pixmap is not None:
#             t = self.cutout_anim_progress
#             pulse = np.sin(t * np.pi)

#             if self.cutout_subject_pixmap is not None:
#                 lift_scale = 1.0 + 0.016 * pulse
#                 lifted_w = target.width() * lift_scale
#                 lifted_h = target.height() * lift_scale
#                 lifted_rect = QRectF(
#                     target.center().x() - lifted_w / 2.0,
#                     target.center().y() - lifted_h / 2.0 - (3.5 * pulse),
#                     lifted_w,
#                     lifted_h
#                 )
#                 painter.save()
#                 painter.setOpacity(0.92 * pulse)
#                 painter.drawPixmap(
#                     lifted_rect,
#                     self.cutout_subject_pixmap,
#                     QRectF(self.cutout_subject_pixmap.rect())
#                 )
#                 painter.restore()

#             painter.save()
#             painter.setOpacity(min(1.0, 1.1 * pulse))
#             painter.drawPixmap(
#                 target,
#                 self.cutout_contour_pixmap,
#                 QRectF(self.cutout_contour_pixmap.rect())
#             )
#             painter.restore()

#         if (
#             self.image_size
#             and self.mode == "text"
#             and (
#                 self.text_selected
#                 or self.hovering_text
#                 or self.dragging_text
#                 or self.resizing_corner is not None
#                 or self.hover_corner is not None
#             )
#         ):
#             box = self.get_widget_text_box()
#             if not box.isNull():
#                 painter.setPen(QPen(QColor("#2563eb"), 1.5))
#                 painter.setBrush(Qt.BrushStyle.NoBrush)
#                 painter.drawRect(box)

#                 corners = {
#                     "tl": box.topLeft(),
#                     "tr": box.topRight(),
#                     "bl": box.bottomLeft(),
#                     "br": box.bottomRight(),
#                 }
#                 for key, pt in corners.items():
#                     active = (
#                         self.hover_corner == key
#                         or self.resizing_corner == key
#                     )
#                     radius = 5.0 if active else 4.0
#                     painter.setPen(QPen(QColor("#2563eb"), 1.8))
#                     painter.setBrush(QColor("#fbf9f5"))
#                     painter.drawEllipse(pt, radius, radius)


# class DepthType(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("DepthType")
#         self.setWindowIcon(create_app_icon())
#         self.resize(1280, 720)
#         self.center_on_screen()

#         self.original = None
#         self.image_bgr = None
#         self.last_directory = None

#         self.mask = None
#         self.predictor = None
#         self.is_generating = False

#         self.text_color = "#ffffff"
#         self.text_opacity = 100
#         self.font_size = 130
#         self.text_position = (100, 100)

#         self.canvas = ImageCanvas(self)

#         esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
#         esc_shortcut.activated.connect(self.handle_escape)

#         self.setup_typography()
#         self.create_interface()
#         self.apply_stylesheet()

#     def handle_escape(self):
#         if self.canvas.eyedropper_active:
#             self.set_eyedropper_mode(False)
#             return
#         if self.isFullScreen():
#             self.showNormal()
#             self.resize(1280, 720)
#             self.center_on_screen()
#         else:
#             self.showFullScreen()

#     def center_on_screen(self):
#         screen = QApplication.primaryScreen()
#         if screen is not None:
#             geo = screen.availableGeometry()
#             x = geo.x() + (geo.width() - self.width()) // 2
#             y = geo.y() + (geo.height() - self.height()) // 2
#             self.move(x, y)

#     def setup_typography(self):
#         if FONT_PATH.exists():
#             font_id = QFontDatabase.addApplicationFont(str(FONT_PATH))
#             if font_id != -1:
#                 families = QFontDatabase.applicationFontFamilies(font_id)
#                 if families:
#                     QApplication.setFont(QFont(families[0], 13))
#                     return

#         QApplication.setFont(QFont("Segoe UI", 10))

#     def create_divider(self):
#         line = QFrame()
#         line.setFrameShape(QFrame.Shape.HLine)
#         line.setObjectName("Divider")
#         return line

#     def create_section_header(self, title):
#         lbl = QLabel(title.upper())
#         lbl.setObjectName("SectionHeader")
#         return lbl

#     def create_interface(self):
#         toolbar = QWidget()
#         toolbar.setObjectName("TopBar")
#         toolbar.setFixedHeight(50)

#         tb_layout = QHBoxLayout(toolbar)
#         tb_layout.setContentsMargins(16, 6, 16, 6)
#         tb_layout.setSpacing(10)

#         brand_label = QLabel("DepthType")
#         brand_label.setObjectName("BrandTitle")

#         self.open_button = QPushButton(" Open Image")
#         self.open_button.setIcon(create_vector_icon("folder", "#292524", 14))
#         self.open_button.setObjectName("SecondaryButton")
#         self.open_button.clicked.connect(self.open_image)

#         self.mode_switch = AnimatedModeSwitch(self)
#         self.mode_switch.modeChanged.connect(self.set_mode)

#         self.gpu_status = QLabel(self.get_gpu_status())
#         self.gpu_status.setObjectName("GpuLabel")

#         self.export_button = QPushButton(" Export PNG")
#         self.export_button.setIcon(create_vector_icon("export", "#ffffff", 14))
#         self.export_button.setObjectName("PrimaryButton")
#         self.export_button.clicked.connect(self.export_image)
#         self.export_button.setEnabled(False)

#         tb_layout.addWidget(brand_label)
#         tb_layout.addSpacing(8)
#         tb_layout.addWidget(self.open_button)
#         tb_layout.addStretch()
#         tb_layout.addWidget(self.mode_switch)
#         tb_layout.addStretch()
#         tb_layout.addWidget(self.gpu_status)
#         tb_layout.addSpacing(6)
#         tb_layout.addWidget(self.export_button)

#         # =========================================================
#         # 2. WARM LIGHT RIGHT SIDEBAR
#         # =========================================================
#         inspector = QWidget()
#         inspector.setObjectName("Sidebar")
#         inspector.setFixedWidth(268)

#         insp_layout = QVBoxLayout(inspector)
#         insp_layout.setContentsMargins(16, 16, 16, 16)
#         insp_layout.setSpacing(12)

#         insp_layout.addWidget(self.create_section_header("Subject Isolation"))

#         hint_lbl = QLabel(
#             "Click subject to auto-detect cutout\n"
#             "Right-click background to exclude"
#         )
#         hint_lbl.setObjectName("HintText")
#         insp_layout.addWidget(hint_lbl)

#         insp_layout.addWidget(self.create_divider())

#         insp_layout.addWidget(self.create_section_header("Typography"))

#         self.text_input = QLineEdit("DEPTH")
#         self.text_input.setPlaceholderText("Enter text…")
#         self.text_input.textChanged.connect(self.update_preview)
#         insp_layout.addWidget(self.text_input)

#         font_row = QHBoxLayout()
#         lbl_font = QLabel("Font")
#         lbl_font.setObjectName("KeyLabel")
#         val_font = QLabel("SF Pro Display")
#         val_font.setObjectName("ValueLabel")
#         font_row.addWidget(lbl_font)
#         font_row.addStretch()
#         font_row.addWidget(val_font)
#         insp_layout.addLayout(font_row)

#         canvas_tip = QLabel(
#             "Drag corner handles to resize.\n"
#             "Click text to adjust opacity."
#         )
#         canvas_tip.setObjectName("HintText")
#         insp_layout.addWidget(canvas_tip)

#         insp_layout.addWidget(self.create_divider())

#         insp_layout.addWidget(self.create_section_header("Color"))

#         swatch_row = QHBoxLayout()
#         swatch_row.setSpacing(8)
#         preset_colors = [
#             "#ffffff",
#             "#1c1917",
#             "#eab308",
#             "#f97316",
#             "#ef4444",
#             "#2563eb",
#         ]
#         for hex_col in preset_colors:
#             btn = QPushButton()
#             btn.setFixedSize(22, 22)
#             btn.setCursor(Qt.CursorShape.PointingHandCursor)
#             btn.setStyleSheet(
#                 f"background-color: {hex_col}; "
#                 f"border-radius: 11px; "
#                 f"border: 1px solid #d6cfc3;"
#             )
#             btn.clicked.connect(
#                 lambda checked=False, c=hex_col: self.set_text_color(c)
#             )
#             swatch_row.addWidget(btn)

#         swatch_row.addStretch()
#         insp_layout.addLayout(swatch_row)

#         color_tools_row = QHBoxLayout()
#         color_tools_row.setSpacing(8)

#         self.color_swatch = QFrame()
#         self.color_swatch.setFixedSize(14, 14)

#         self.color_label = QLabel("#FFFFFF")
#         self.color_label.setObjectName("ValueLabel")

#         self.color_button = QPushButton()
#         self.color_button.setObjectName("ColorPickerButton")
#         self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
#         self.color_button.clicked.connect(self.choose_color)

#         color_btn_layout = QHBoxLayout(self.color_button)
#         color_btn_layout.setContentsMargins(8, 0, 8, 0)
#         color_btn_layout.setSpacing(6)
#         color_btn_layout.addWidget(self.color_swatch)
#         color_btn_layout.addWidget(self.color_label)
#         color_btn_layout.addStretch()

#         self.eyedropper_button = QPushButton(" Pick")
#         self.eyedropper_button.setIcon(create_vector_icon("eyedropper", "#292524", 13))
#         self.eyedropper_button.setObjectName("SecondaryButton")
#         self.eyedropper_button.setCursor(Qt.CursorShape.PointingHandCursor)
#         self.eyedropper_button.setToolTip("Pick color directly from image")
#         self.eyedropper_button.clicked.connect(
#             lambda: self.set_eyedropper_mode(True)
#         )

#         color_tools_row.addWidget(self.color_button, 1)
#         color_tools_row.addWidget(self.eyedropper_button)
#         insp_layout.addLayout(color_tools_row)

#         self.update_color_swatch()
#         insp_layout.addStretch()

#         # =========================================================
#         # 3. ASSEMBLE MAIN WINDOW
#         # =========================================================
#         root = QWidget()
#         root_layout = QVBoxLayout(root)
#         root_layout.setContentsMargins(0, 0, 0, 0)
#         root_layout.setSpacing(0)

#         root_layout.addWidget(toolbar)
#         root_layout.addWidget(self.create_divider())

#         workspace = QHBoxLayout()
#         workspace.setContentsMargins(0, 0, 0, 0)
#         workspace.setSpacing(0)

#         workspace.addWidget(self.canvas, 1)

#         v_divider = QFrame()
#         v_divider.setFrameShape(QFrame.Shape.VLine)
#         v_divider.setObjectName("VerticalDivider")
#         workspace.addWidget(v_divider)

#         workspace.addWidget(inspector)
#         root_layout.addLayout(workspace, 1)

#         self.setCentralWidget(root)

#         self.status = QLabel("Ready")
#         self.status.setObjectName("StatusText")
#         self.statusBar().setSizeGripEnabled(False)
#         self.statusBar().addWidget(self.status)

#         self.set_mode("select", animate=False)

#     def apply_stylesheet(self):
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #f2ede4;
#             }

#             QWidget#TopBar {
#                 background-color: #f8f5ef;
#             }

#             QWidget#Sidebar {
#                 background-color: #f8f5ef;
#             }

#             QLabel {
#                 color: #1c1917;
#                 background: transparent;
#             }

#             QLabel#BrandTitle {
#                 font-size: 14px;
#                 font-weight: 700;
#                 color: #1c1917;
#             }

#             QLabel#SectionHeader {
#                 font-size: 10px;
#                 font-weight: 700;
#                 letter-spacing: 0.6px;
#                 color: #78716c;
#             }

#             QLabel#KeyLabel {
#                 font-size: 12px;
#                 color: #44403c;
#             }

#             QLabel#ValueLabel {
#                 font-size: 12px;
#                 color: #78716c;
#             }

#             QLabel#HintText {
#                 font-size: 11px;
#                 color: #78716c;
#                 line-height: 1.4;
#             }

#             QLabel#GpuLabel {
#                 font-size: 11px;
#                 color: #78716c;
#             }

#             QFrame#Divider {
#                 background-color: #e4ddd1;
#                 max-height: 1px;
#                 border: none;
#             }

#             QFrame#VerticalDivider {
#                 background-color: #e4ddd1;
#                 max-width: 1px;
#                 border: none;
#             }

#             QLabel#PopoverTitle {
#                 font-size: 11px;
#                 font-weight: 600;
#                 color: #292524;
#             }

#             QLabel#PopoverValue {
#                 font-size: 11px;
#                 font-weight: 600;
#                 color: #2563eb;
#             }

#             QPushButton#PrimaryButton {
#                 background-color: #2563eb;
#                 color: #ffffff;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 7px 14px;
#                 font-size: 12px;
#                 font-weight: 600;
#             }

#             QPushButton#PrimaryButton:hover {
#                 background-color: #1d4ed8;
#             }

#             QPushButton#PrimaryButton:pressed {
#                 background-color: #1e40af;
#             }

#             QPushButton#PrimaryButton:disabled {
#                 background-color: #e5dfd4;
#                 color: #a8a29e;
#             }

#             QPushButton#SecondaryButton {
#                 background-color: #fbf9f5;
#                 color: #292524;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 padding: 6px 12px;
#                 font-size: 12px;
#                 font-weight: 500;
#             }

#             QPushButton#SecondaryButton:hover {
#                 background-color: #f0ece3;
#             }

#             QPushButton#SecondaryButton:pressed {
#                 background-color: #e5dfd4;
#             }

#             QLineEdit {
#                 background-color: #fbf9f5;
#                 color: #1c1917;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 padding: 7px 10px;
#                 font-size: 13px;
#                 selection-background-color: #2563eb;
#                 selection-color: #ffffff;
#             }

#             QLineEdit:focus {
#                 background-color: #ffffff;
#                 border: 1.5px solid #2563eb;
#             }

#             QSlider::groove:horizontal {
#                 height: 3px;
#                 background: #d6cfc3;
#                 border-radius: 1.5px;
#             }

#             QSlider::sub-page:horizontal {
#                 background: #2563eb;
#                 border-radius: 1.5px;
#             }

#             QSlider::handle:horizontal {
#                 background: #fbf9f5;
#                 border: 1.5px solid #2563eb;
#                 width: 12px;
#                 height: 12px;
#                 margin: -5px 0;
#                 border-radius: 6px;
#             }

#             QPushButton#ColorPickerButton {
#                 background-color: #fbf9f5;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 min-height: 28px;
#             }

#             QPushButton#ColorPickerButton:hover {
#                 border-color: #a8a29e;
#                 background-color: #f0ece3;
#             }

#             QStatusBar {
#                 background-color: #f8f5ef;
#                 border-top: 1px solid #e4ddd1;
#                 color: #78716c;
#                 font-size: 11px;
#                 padding: 2px 12px;
#             }

#             QLabel#StatusText {
#                 color: #78716c;
#                 font-size: 11px;
#             }
#         """)

#     def set_font_size(self, size):
#         self.font_size = max(16, min(650, int(size)))

#     def set_text_color(self, hex_color):
#         self.text_color = hex_color
#         self.update_color_swatch()
#         self.update_preview()

#     def update_color_swatch(self):
#         self.color_swatch.setStyleSheet(
#             f"background-color: {self.text_color}; "
#             f"border-radius: 3px; "
#             f"border: 1px solid #d6cfc3;"
#         )
#         self.color_label.setText(self.text_color.upper())

#     def on_opacity_changed(self, value):
#         self.text_opacity = value
#         self.update_preview()

#     def get_gpu_status(self):
#         if torch.cuda.is_available():
#             return f"GPU: {torch.cuda.get_device_name(0)}"
#         if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
#             return "GPU: Apple Silicon MPS"
#         return "CPU"

#     def set_eyedropper_mode(self, active):
#         if active and self.original is None:
#             return
#         self.canvas.eyedropper_active = active
#         if active:
#             self.eyedropper_button.hide()
#             self.status.setText("Click anywhere on the image to pick color (Esc to cancel)")
#         else:
#             self.eyedropper_button.show()
#             if self.canvas.mode == "text":
#                 self.status.setText("Typography — Click text for opacity, drag corners to resize")

#     def sample_color_from_image(self, x, y):
#         if self.original is not None:
#             r, g, b = self.original.getpixel((x, y))
#             hex_col = f"#{r:02x}{g:02x}{b:02x}"
#             self.set_text_color(hex_col)
#         self.set_eyedropper_mode(False)

#     def set_mode(self, mode, animate=True):
#         if self.canvas.eyedropper_active:
#             self.set_eyedropper_mode(False)

#         self.canvas.mode = mode
#         self.mode_switch.set_mode(mode, animate=animate)

#         if mode != "text":
#             self.canvas.text_selected = False
#             self.canvas.opacity_popover.hide_animated()
#         else:
#             self.canvas.position_opacity_popover()

#         self.canvas.update()

#         if mode == "select":
#             self.status.setText(
#                 "Subject Mask — Click subject to auto-detect cutout"
#             )
#         else:
#             self.status.setText(
#                 "Typography — Click text for opacity, drag corners to resize"
#             )

#     def open_image(self):
#         browser = ModernFileBrowserDialog(
#             parent=self,
#             mode="open",
#             initial_dir=self.last_directory,
#         )
#         if browser.exec() and browser.selected_path:
#             self.load_image_from_path(browser.selected_path)

#     def load_image_from_path(self, path):
#         try:
#             p = Path(path)
#             self.last_directory = str(p.parent)
#             self.original = Image.open(p).convert("RGB")
#             self.image_bgr = cv2.cvtColor(
#                 np.array(self.original),
#                 cv2.COLOR_RGB2BGR
#             )

#             self.mask = None
#             self.predictor = None

#             self.canvas.points.clear()
#             self.canvas.text_selected = False
#             self.canvas.opacity_popover.hide()
#             self.canvas.image_size = self.original.size
#             self.canvas.set_preview(
#                 pil_to_pixmap(self.original, dpr=self.devicePixelRatioF())
#             )

#             self.font_size = max(48, self.original.width // 6)
#             self.text_position = (
#                 self.original.width // 4,
#                 self.original.height // 3
#             )

#             self.export_button.setEnabled(True)
#             self.set_mode("select", animate=False)
#             self.update_preview()

#             self.status.setText(
#                 f"{p.name} ({self.original.width} × {self.original.height})"
#             )

#         except Exception as error:
#             self._show_light_message("Image Error", str(error), is_error=True)

#     def add_selection_point(self, x, y, label):
#         if any(p[2] == 1 for p in self.canvas.points):
#             self.generate_mask()
#         else:
#             self.mask = None
#             self.status.setText(f"Excluded area at ({x}, {y}) — Click subject to cut out")
#             self.update_preview()

#     def generate_mask(self):
#         if self.original is None or self.is_generating:
#             return

#         if not any(p[2] == 1 for p in self.canvas.points):
#             return

#         self.is_generating = True
#         self.status.setText("Detecting subject…")
#         QApplication.processEvents()

#         try:
#             if torch.cuda.is_available():
#                 device = 0
#             elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
#                 device = "mps"
#             else:
#                 device = "cpu"

#             overrides = {
#                 "conf": 0.25,
#                 "task": "segment",
#                 "mode": "predict",
#                 "imgsz": 1024,
#                 "model": "sam2.1_b.pt",
#                 "device": device,
#                 "verbose": False
#             }

#             if self.predictor is None:
#                 self.predictor = SAM2Predictor(overrides=overrides)

#             points = [[p[0], p[1]] for p in self.canvas.points]
#             labels = [p[2] for p in self.canvas.points]

#             results = self.predictor(
#                 source=self.image_bgr,
#                 points=points,
#                 labels=labels
#             )

#             result = results[0]

#             if result.masks is None:
#                 raise RuntimeError("No subject detected. Try clicking another spot.")

#             masks = (
#                 result.masks.data
#                 .detach()
#                 .float()
#                 .cpu()
#                 .numpy()
#             )

#             if len(masks) == 0:
#                 raise RuntimeError("No subject mask found.")

#             if (
#                 result.boxes is not None
#                 and result.boxes.conf is not None
#                 and len(result.boxes.conf) == len(masks)
#             ):
#                 scores = result.boxes.conf.detach().cpu().numpy()
#                 index = int(np.argmax(scores))
#             else:
#                 index = int(np.argmax([np.sum(mask) for mask in masks]))

#             raw_mask = masks[index]
#             raw_mask = cv2.resize(
#                 raw_mask,
#                 self.original.size,
#                 interpolation=cv2.INTER_LINEAR
#             )
#             raw_mask = np.clip(raw_mask, 0, 1)
#             raw_mask = cv2.GaussianBlur(raw_mask, (0, 0), 1.0)
#             self.mask = np.clip(raw_mask, 0, 1)

#             self.export_button.setEnabled(True)
#             self.update_preview()
#             self.canvas.start_cutout_animation(self.original, self.mask)

#             self.set_mode("text", animate=True)
#             self.canvas.text_selected = True
#             self.canvas.position_opacity_popover()
#             self.status.setText("Subject isolated — Ready for typography")

#         except Exception as error:
#             self._show_light_message("SAM 2 Error", str(error), is_error=True)
#             self.status.setText("Subject detection failed")

#         finally:
#             self.is_generating = False

#     def choose_color(self):
#         if self.canvas.eyedropper_active:
#             self.set_eyedropper_mode(False)
#         dlg = WarmColorPickerDialog(self.text_color, self)
#         dlg.colorSelected.connect(self.set_text_color)
#         dlg.exec()

#     def get_text_bounds(self):
#         if self.original is None:
#             return None

#         text = self.text_input.text()
#         if not text:
#             return None

#         font = load_font(self.font_size)
#         draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
#         bbox = draw.textbbox((0, 0), text, font=font)

#         width = bbox[2] - bbox[0]
#         height = bbox[3] - bbox[1]
#         x, y = self.text_position

#         return (x, y, width, height)

#     def place_text(self, x, y):
#         if self.original is None:
#             return

#         bounds = self.get_text_bounds()
#         if bounds is not None:
#             _, _, width, height = bounds
#             x = max(0, min(x, self.original.width - width))
#             y = max(0, min(y, self.original.height - height))

#         self.text_position = (x, y)
#         self.update_preview()

#     def build_composite(self):
#         if self.original is None:
#             return None

#         base = self.original.convert("RGBA")
#         width, height = base.size

#         text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
#         draw = ImageDraw.Draw(text_layer)

#         text = self.text_input.text()
#         if text.strip():
#             font = load_font(self.font_size)
#             bbox = draw.textbbox((0, 0), text, font=font)
#             x, y = self.text_position

#             qcol = QColor(self.text_color)
#             alpha_val = int((self.text_opacity / 100.0) * 255)
#             rgba_fill = (qcol.red(), qcol.green(), qcol.blue(), alpha_val)

#             draw.text(
#                 (x - bbox[0], y - bbox[1]),
#                 text,
#                 font=font,
#                 fill=rgba_fill
#             )

#         composite = Image.alpha_composite(base, text_layer)

#         if self.mask is not None:
#             person = self.original.convert("RGBA")
#             alpha = Image.fromarray(
#                 (self.mask * 255).astype(np.uint8),
#                 mode="L"
#             )
#             person.putalpha(alpha)
#             composite = Image.alpha_composite(composite, person)

#         return composite

#     def update_preview(self, *_):
#         if self.original is None:
#             return

#         try:
#             result = self.build_composite()
#             self.canvas.set_preview(
#                 pil_to_pixmap(result, dpr=self.devicePixelRatioF())
#             )
#         except Exception as error:
#             self.status.setText(f"Preview error: {error}")

#     def _show_light_message(self, title, text, is_error=False):
#         box = QMessageBox(self)
#         box.setWindowTitle(title)
#         box.setText(text)
#         box.setIcon(QMessageBox.Icon.Critical if is_error else QMessageBox.Icon.Information)
#         box.setStyleSheet("""
#             QMessageBox {
#                 background-color: #f8f5ef;
#                 color: #1c1917;
#             }
#             QLabel {
#                 color: #1c1917;
#                 background: transparent;
#             }
#             QPushButton {
#                 background-color: #fbf9f5;
#                 color: #292524;
#                 border: 1px solid #d6cfc3;
#                 border-radius: 6px;
#                 padding: 6px 16px;
#                 font-size: 12px;
#             }
#             QPushButton:hover {
#                 background-color: #efeae0;
#             }
#         """)
#         box.exec()

#     def export_image(self):
#         if self.original is None:
#             return

#         browser = ModernFileBrowserDialog(
#             parent=self,
#             mode="save",
#             default_filename="depthtype_result.png",
#             initial_dir=self.last_directory,
#         )
#         if not browser.exec() or not browser.selected_path:
#             return

#         path = browser.selected_path
#         self.last_directory = str(Path(path).parent)

#         try:
#             result = self.build_composite()
#             result.save(path, "PNG")
#             self.status.setText(f"Exported {Path(path).name}")

#             self._show_light_message(
#                 "Export Complete",
#                 f"Saved successfully:\n{path}"
#             )

#         except Exception as error:
#             self._show_light_message("Export Error", str(error), is_error=True)

# if __name__ == "__main__":
#     if sys.platform == "win32":
#         import ctypes
#         ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
#             "DepthTypeStudio.DepthType.App.1"
#         )

#     app = QApplication(sys.argv)
#     app.setApplicationName("DepthType")

#     icon = create_app_icon()
#     app.setWindowIcon(icon)

#     window = DepthType()
#     window.setWindowIcon(icon)
#     window.show()

#     sys.exit(app.exec())
import os
import sys
from pathlib import Path

import cv2
import torch
import numpy as np

from PIL import Image, ImageDraw, ImageFont

from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    QTimer,
    Signal,
    QVariantAnimation,
    QEasingCurve,
    QDir,
    QStandardPaths,
    QSize,
    QStorageInfo,
)
from PySide6.QtGui import (
    QImage,
    QPixmap,
    QPainter,
    QColor,
    QPen,
    QBrush,
    QRadialGradient,
    QLinearGradient,
    QFontDatabase,
    QFont,
    QIcon,
    QPainterPath,
    QKeySequence,
    QShortcut,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSlider,
    QDialog,
    QMessageBox,
    QFrame,
    QGraphicsOpacityEffect,
    QListWidget,
    QListWidgetItem,
    QFileSystemModel,
    QTreeView,
    QHeaderView,
    QAbstractItemView,
    QComboBox,
    QSplitter,
)

from ultralytics.models.sam import SAM2Predictor


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
    APP_DATA_DIR = Path.home() / ".depthtype"
else:
    BASE_DIR = Path(__file__).resolve().parent
    APP_DATA_DIR = BASE_DIR

APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
FONT_PATH = BASE_DIR / "assets" / "fonts" / "SF-Pro-Display-Regular.ttf"
ICON_PATH = BASE_DIR / "assets" / "icon.ico"

BUNDLED_MODEL = BASE_DIR / "assets" / "sam2.1_b.pt"
MODEL_PATH = BUNDLED_MODEL if BUNDLED_MODEL.exists() else (APP_DATA_DIR / "sam2.1_b.pt")


def load_font(size):
    if not FONT_PATH.exists():
        raise FileNotFoundError(
            f"Apple SF Pro font not found:\n{FONT_PATH}"
        )

    return ImageFont.truetype(
        str(FONT_PATH),
        size=max(12, int(size))
    )


def pil_to_pixmap(image, dpr=1.0):
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")

    qimage = QImage(
        data,
        image.width,
        image.height,
        QImage.Format.Format_RGBA8888
    )

    pixmap = QPixmap.fromImage(qimage.copy())
    pixmap.setDevicePixelRatio(dpr)
    return pixmap


def render_icon_pixmap(size=256):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    bg_grad = QLinearGradient(0, 0, size, size)
    bg_grad.setColorAt(0.0, QColor("#fbf9f5"))
    bg_grad.setColorAt(1.0, QColor("#ede6d9"))
    painter.setPen(QPen(QColor("#d6cfc3"), max(2, size // 42)))
    painter.setBrush(QBrush(bg_grad))
    r = size * 0.22
    pad = size * 0.05
    painter.drawRoundedRect(QRectF(pad, pad, size - pad * 2, size - pad * 2), r, r)

    font = QFont("SF Pro Display", int(size * 0.50), QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#2563eb"))
    painter.drawText(QRectF(0, -size * 0.015, size, size), Qt.AlignmentFlag.AlignCenter, "D")

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#1c1917"))
    painter.drawEllipse(QPointF(size * 0.56, size * 0.43), size * 0.10, size * 0.10)
    body_path = QPainterPath()
    body_path.moveTo(size * 0.34, size * 0.80)
    body_path.quadTo(size * 0.56, size * 0.54, size * 0.78, size * 0.80)
    painter.drawPath(body_path)

    painter.end()
    return pixmap


def export_multires_ico(output_path: Path):
    """Generates a true multi-resolution Windows .ico file for Task Manager & Explorer."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pm = render_icon_pixmap(256)
    qimg = pm.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
    ptr = qimg.constBits()
    arr = np.frombuffer(ptr, dtype=np.uint8).reshape((256, 256, 4)).copy()
    pil_icon = Image.fromarray(arr, mode="RGBA")
    pil_icon.save(
        str(output_path),
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )


def create_app_icon():
    if ICON_PATH.exists():
        return QIcon(str(ICON_PATH))

    icon = QIcon()
    for sz in (16, 24, 32, 48, 64, 128, 256):
        icon.addPixmap(render_icon_pixmap(sz))
    return icon


def create_vector_icon(kind, color="#292524", size=15):
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    pen = QPen(
        QColor(color),
        2.4,
        Qt.PenStyle.SolidLine,
        Qt.PenCapStyle.RoundCap,
        Qt.PenJoinStyle.RoundJoin
    )
    painter.setPen(pen)

    if kind == "folder":
        painter.drawRoundedRect(QRectF(4, 7, 24, 18), 3.0, 3.0)
        path = QPainterPath()
        path.moveTo(4, 11)
        path.lineTo(4, 6)
        path.lineTo(13, 6)
        path.lineTo(16, 9)
        painter.drawPath(path)

    elif kind == "export":
        path = QPainterPath()
        path.moveTo(10, 13)
        path.lineTo(6, 13)
        path.lineTo(6, 26)
        path.lineTo(26, 26)
        path.lineTo(26, 13)
        path.lineTo(22, 13)
        painter.drawPath(path)
        painter.drawLine(16, 19, 16, 5)
        painter.drawLine(11, 10, 16, 5)
        painter.drawLine(21, 10, 16, 5)

    elif kind == "person":
        painter.drawEllipse(QPointF(16, 10), 4.5, 4.5)
        path = QPainterPath()
        path.moveTo(7, 26)
        path.quadTo(16, 17, 25, 26)
        painter.drawPath(path)

    elif kind == "text":
        painter.drawLine(7, 7, 25, 7)
        painter.drawLine(16, 7, 16, 26)
        painter.drawLine(12, 26, 20, 26)

    elif kind == "eyedropper":
        path = QPainterPath()
        path.moveTo(6, 26)
        path.lineTo(11, 25)
        path.lineTo(23, 13)
        path.lineTo(19, 9)
        path.lineTo(7, 21)
        path.closeSubpath()
        painter.drawPath(path)
        painter.drawLine(17, 7, 25, 15)

    elif kind == "back":
        painter.drawLine(21, 7, 11, 16)
        painter.drawLine(11, 16, 21, 25)

    elif kind == "forward":
        painter.drawLine(11, 7, 21, 16)
        painter.drawLine(21, 16, 11, 25)

    elif kind == "up":
        painter.drawLine(16, 25, 16, 7)
        painter.drawLine(8, 15, 16, 7)
        painter.drawLine(24, 15, 16, 7)

    elif kind == "drive":
        painter.drawRoundedRect(QRectF(4, 9, 24, 14), 3.5, 3.5)
        painter.drawLine(4, 18, 28, 18)
        painter.drawEllipse(QPointF(23, 20.5), 1.0, 1.0)

    elif kind == "image":
        painter.drawRoundedRect(QRectF(4, 6, 24, 20), 3.0, 3.0)
        painter.drawEllipse(QPointF(11, 12), 2.0, 2.0)
        path = QPainterPath()
        path.moveTo(6, 24)
        path.lineTo(13, 17)
        path.lineTo(18, 22)
        path.lineTo(22, 18)
        path.lineTo(26, 24)
        painter.drawPath(path)

    elif kind == "new_folder":
        painter.drawRoundedRect(QRectF(4, 7, 24, 18), 3.0, 3.0)
        path = QPainterPath()
        path.moveTo(4, 11)
        path.lineTo(4, 6)
        path.lineTo(13, 6)
        path.lineTo(16, 9)
        painter.drawPath(path)
        painter.drawLine(16, 13, 16, 21)
        painter.drawLine(12, 17, 20, 17)

    painter.end()
    pixmap.setDevicePixelRatio(2.0)
    return QIcon(pixmap)


class ModernFileBrowserDialog(QDialog):
    """Modern warm-paper Finder/Explorer file browser for opening and saving across the entire PC."""

    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def __init__(
        self,
        parent=None,
        mode="open",
        default_filename="depthtype_result.png",
        initial_dir=None,
    ):
        super().__init__(parent)
        self.mode = mode
        self.selected_path = ""
        self._history = []
        self._history_idx = -1
        self._navigating_history = False

        self.setWindowTitle("Open Image" if mode == "open" else "Export Image")
        self.resize(880, 560)
        self.setMinimumSize(720, 460)
        self.setModal(True)

        if initial_dir and Path(initial_dir).exists():
            start_dir = str(Path(initial_dir).resolve())
        else:
            pics = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.PicturesLocation
            )
            start_dir = pics if pics and Path(pics).exists() else str(Path.home())

        self._build_ui(default_filename)
        self._apply_theme()
        self._populate_sidebar()
        self.navigate_to(start_dir)

    def _build_ui(self, default_filename):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top_bar = QWidget()
        top_bar.setObjectName("BrowserTopBar")
        top_bar.setFixedHeight(50)

        top_lay = QHBoxLayout(top_bar)
        top_lay.setContentsMargins(14, 8, 14, 8)
        top_lay.setSpacing(8)

        self.back_btn = QPushButton()
        self.back_btn.setIcon(create_vector_icon("back", "#292524", 13))
        self.back_btn.setObjectName("NavIconBtn")
        self.back_btn.setFixedSize(30, 30)
        self.back_btn.setToolTip("Back")
        self.back_btn.clicked.connect(self.go_back)

        self.fwd_btn = QPushButton()
        self.fwd_btn.setIcon(create_vector_icon("forward", "#292524", 13))
        self.fwd_btn.setObjectName("NavIconBtn")
        self.fwd_btn.setFixedSize(30, 30)
        self.fwd_btn.setToolTip("Forward")
        self.fwd_btn.clicked.connect(self.go_forward)

        self.up_btn = QPushButton()
        self.up_btn.setIcon(create_vector_icon("up", "#292524", 13))
        self.up_btn.setObjectName("NavIconBtn")
        self.up_btn.setFixedSize(30, 30)
        self.up_btn.setToolTip("Parent Folder")
        self.up_btn.clicked.connect(self.go_up)

        self.path_input = QLineEdit()
        self.path_input.setObjectName("PathBar")
        self.path_input.setPlaceholderText("Enter path (e.g. D:\\Photos or C:\\Users)...")
        self.path_input.returnPressed.connect(self._on_path_entered)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchBar")
        self.search_input.setPlaceholderText("Filter files...")
        self.search_input.setFixedWidth(185)
        self.search_input.textChanged.connect(self._on_filter_changed)

        top_lay.addWidget(self.back_btn)
        top_lay.addWidget(self.fwd_btn)
        top_lay.addWidget(self.up_btn)
        top_lay.addSpacing(4)
        top_lay.addWidget(self.path_input, 1)
        top_lay.addWidget(self.search_input)

        root.addWidget(top_bar)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setObjectName("BrowserSep")
        root.addWidget(sep1)

        body_split = QSplitter(Qt.Orientation.Horizontal)
        body_split.setHandleWidth(1)
        body_split.setObjectName("BrowserSplit")

        self.places_list = QListWidget()
        self.places_list.setObjectName("PlacesSidebar")
        self.places_list.setMinimumWidth(165)
        self.places_list.setMaximumWidth(230)
        self.places_list.setIconSize(QSize(15, 15))
        self.places_list.itemClicked.connect(self._on_place_clicked)

        self.fs_model = QFileSystemModel(self)
        self.fs_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )
        self.fs_model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"])
        self.fs_model.setNameFilterDisables(False)

        self.tree_view = QTreeView()
        self.tree_view.setObjectName("FileTree")
        self.tree_view.setModel(self.fs_model)
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setItemsExpandable(False)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setIconSize(QSize(16, 16))
        self.tree_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.tree_view.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.tree_view.selectionModel().currentChanged.connect(self._on_selection_changed)
        self.tree_view.doubleClicked.connect(self._on_item_double_clicked)

        preview_pane = QWidget()
        preview_pane.setObjectName("PreviewPane")
        preview_pane.setMinimumWidth(200)
        preview_pane.setMaximumWidth(250)

        prev_lay = QVBoxLayout(preview_pane)
        prev_lay.setContentsMargins(16, 18, 16, 18)
        prev_lay.setSpacing(10)

        self.thumb_label = QLabel("No Preview")
        self.thumb_label.setObjectName("ThumbBox")
        self.thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb_label.setFixedHeight(175)

        self.meta_name = QLabel("Select a file")
        self.meta_name.setObjectName("MetaTitle")
        self.meta_name.setWordWrap(True)
        self.meta_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.meta_details = QLabel("")
        self.meta_details.setObjectName("MetaSub")
        self.meta_details.setWordWrap(True)
        self.meta_details.setAlignment(Qt.AlignmentFlag.AlignCenter)

        prev_lay.addWidget(self.thumb_label)
        prev_lay.addWidget(self.meta_name)
        prev_lay.addWidget(self.meta_details)
        prev_lay.addStretch()

        body_split.addWidget(self.places_list)
        body_split.addWidget(self.tree_view)
        body_split.addWidget(preview_pane)
        body_split.setSizes([185, 480, 215])

        root.addWidget(body_split, 1)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setObjectName("BrowserSep")
        root.addWidget(sep2)

        bottom_bar = QWidget()
        bottom_bar.setObjectName("BrowserBottomBar")
        bottom_bar.setFixedHeight(54)

        bot_lay = QHBoxLayout(bottom_bar)
        bot_lay.setContentsMargins(14, 8, 14, 8)
        bot_lay.setSpacing(10)

        if self.mode == "save":
            self.new_folder_btn = QPushButton(" New Folder")
            self.new_folder_btn.setIcon(create_vector_icon("new_folder", "#292524", 14))
            self.new_folder_btn.setObjectName("SecondaryBtn")
            self.new_folder_btn.clicked.connect(self._create_new_folder)
            bot_lay.addWidget(self.new_folder_btn)

            name_lbl = QLabel("Save As:")
            name_lbl.setObjectName("FieldLabel")
            bot_lay.addWidget(name_lbl)

            self.filename_input = QLineEdit(default_filename)
            self.filename_input.setObjectName("FilenameInput")
            self.filename_input.returnPressed.connect(self._confirm_selection)
            bot_lay.addWidget(self.filename_input, 1)
        else:
            self.filename_input = QLineEdit()
            self.filename_input.setObjectName("FilenameInput")
            self.filename_input.setReadOnly(True)
            self.filename_input.setPlaceholderText("Select an image file to open...")
            bot_lay.addWidget(self.filename_input, 1)

        self.format_combo = QComboBox()
        self.format_combo.setObjectName("FormatCombo")
        if self.mode == "open":
            self.format_combo.addItem("All Images (*.png, *.jpg, *.webp, *.bmp)", ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"])
            self.format_combo.addItem("PNG Images (*.png)", ["*.png"])
            self.format_combo.addItem("JPEG Images (*.jpg, *.jpeg)", ["*.jpg", "*.jpeg"])
            self.format_combo.addItem("All Files (*.*)", ["*"])
        else:
            self.format_combo.addItem("PNG Image (*.png)", ["*.png"])
        self.format_combo.currentIndexChanged.connect(self._on_format_changed)
        bot_lay.addWidget(self.format_combo)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("SecondaryBtn")
        cancel_btn.clicked.connect(self.reject)

        self.action_btn = QPushButton("Open" if self.mode == "open" else "Export PNG")
        self.action_btn.setObjectName("PrimaryBtn")
        self.action_btn.clicked.connect(self._confirm_selection)
        if self.mode == "open":
            self.action_btn.setEnabled(False)

        bot_lay.addWidget(cancel_btn)
        bot_lay.addWidget(self.action_btn)

        root.addWidget(bottom_bar)

    def _populate_sidebar(self):
        self.places_list.clear()

        def add_header(text):
            item = QListWidgetItem(text)
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            font = item.font()
            font.setPointSize(8)
            font.setWeight(QFont.Weight.Bold)
            item.setFont(font)
            item.setForeground(QColor("#78716c"))
            self.places_list.addItem(item)

        def add_place(label, path_str, icon_kind="folder"):
            if not path_str or not Path(path_str).exists():
                return
            item = QListWidgetItem(create_vector_icon(icon_kind, "#44403c", 14), f"  {label}")
            item.setData(Qt.ItemDataRole.UserRole, str(Path(path_str).resolve()))
            self.places_list.addItem(item)

        add_header("FAVORITES")
        add_place("Desktop", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation))
        add_place("Documents", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
        add_place("Downloads", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation))
        add_place("Pictures", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation), "image")
        add_place("Home", str(Path.home()))

        spacer = QListWidgetItem("")
        spacer.setFlags(Qt.ItemFlag.NoItemFlags)
        spacer.setSizeHint(QSize(10, 10))
        self.places_list.addItem(spacer)

        add_header("THIS PC · DRIVES")
        for vol in QStorageInfo.mountedVolumes():
            if vol.isValid() and vol.isReady():
                root_path = vol.rootPath()
                name = vol.displayName()
                drive_letter = root_path.rstrip("/\\")
                label = f"{name} ({drive_letter})" if name and name != root_path else f"Local Disk ({drive_letter})"
                add_place(label, root_path, "drive")

    def navigate_to(self, directory_path):
        target = Path(directory_path)
        if not target.exists() or not target.is_dir():
            return

        clean_path = str(target.resolve())
        idx = self.fs_model.setRootPath(clean_path)
        self.tree_view.setRootIndex(idx)
        self.path_input.setText(clean_path)

        if not self._navigating_history:
            self._history = self._history[: self._history_idx + 1]
            if not self._history or self._history[-1] != clean_path:
                self._history.append(clean_path)
                self._history_idx = len(self._history) - 1

        self.back_btn.setEnabled(self._history_idx > 0)
        self.fwd_btn.setEnabled(self._history_idx < len(self._history) - 1)
        self.up_btn.setEnabled(target.parent != target)

    def go_back(self):
        if self._history_idx > 0:
            self._history_idx -= 1
            self._navigating_history = True
            self.navigate_to(self._history[self._history_idx])
            self._navigating_history = False

    def go_forward(self):
        if self._history_idx < len(self._history) - 1:
            self._history_idx += 1
            self._navigating_history = True
            self.navigate_to(self._history[self._history_idx])
            self._navigating_history = False

    def go_up(self):
        curr = Path(self.fs_model.rootPath())
        if curr.parent != curr:
            self.navigate_to(str(curr.parent))

    def _on_path_entered(self):
        typed = self.path_input.text().strip().strip('"')
        p = Path(typed)
        if p.is_dir():
            self.navigate_to(str(p))
        elif p.is_file():
            self.navigate_to(str(p.parent))
            self.filename_input.setText(p.name)
            if self.mode == "open":
                self.action_btn.setEnabled(True)

    def _on_place_clicked(self, item):
        target = item.data(Qt.ItemDataRole.UserRole)
        if target:
            self.navigate_to(target)

    def _on_filter_changed(self, text):
        base_filters = self.format_combo.currentData() or ["*"]
        query = text.strip()
        if not query:
            self.fs_model.setNameFilters(base_filters)
            return

        custom = []
        for pat in base_filters:
            if pat == "*":
                custom.append(f"*{query}*")
            else:
                ext = pat.lstrip("*")
                custom.append(f"*{query}*{ext}")
        self.fs_model.setNameFilters(custom)

    def _on_format_changed(self, _):
        self._on_filter_changed(self.search_input.text())

    def _on_selection_changed(self, current, _previous):
        if not current.isValid():
            return

        path = Path(self.fs_model.filePath(current))
        if path.is_dir():
            self.meta_name.setText(path.name)
            self.meta_details.setText("Folder")
            self.thumb_label.setPixmap(QPixmap())
            self.thumb_label.setText("Folder")
            if self.mode == "open":
                self.filename_input.clear()
                self.action_btn.setEnabled(False)
            return

        self.filename_input.setText(path.name)
        if self.mode == "open":
            self.action_btn.setEnabled(True)

        size_kb = path.stat().st_size / 1024.0
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024.0:.2f} MB"
        self.meta_name.setText(path.name)

        if path.suffix.lower() in self.IMAGE_EXTS:
            reader = QPixmap(str(path))
            if not reader.isNull():
                scaled = reader.scaled(
                    180,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.thumb_label.setText("")
                self.thumb_label.setPixmap(scaled)
                self.meta_details.setText(f"{reader.width()} × {reader.height()} px\n{size_str}")
                return

        self.thumb_label.setPixmap(QPixmap())
        self.thumb_label.setText(path.suffix.upper().lstrip(".") or "FILE")
        self.meta_details.setText(size_str)

    def _on_item_double_clicked(self, index):
        if not index.isValid():
            return
        path = Path(self.fs_model.filePath(index))
        if path.is_dir():
            self.navigate_to(str(path))
        elif path.is_file():
            self.filename_input.setText(path.name)
            self._confirm_selection()

    def _create_new_folder(self):
        curr_dir = Path(self.fs_model.rootPath())
        base_name = "New Folder"
        candidate = curr_dir / base_name
        counter = 2
        while candidate.exists():
            candidate = curr_dir / f"{base_name} ({counter})"
            counter += 1
        try:
            candidate.mkdir(parents=False, exist_ok=False)
        except Exception as exc:
            QMessageBox.warning(self, "New Folder", str(exc))

    def _confirm_selection(self):
        curr_dir = Path(self.fs_model.rootPath())
        name = self.filename_input.text().strip()
        if not name:
            return

        candidate = Path(name) if Path(name).is_absolute() else (curr_dir / name)

        if self.mode == "open":
            if candidate.is_dir():
                self.navigate_to(str(candidate))
                return
            if candidate.is_file():
                self.selected_path = str(candidate.resolve())
                self.accept()
        else:
            if not candidate.name.lower().endswith(".png"):
                candidate = candidate.with_name(candidate.name + ".png")
            self.selected_path = str(candidate.resolve())
            self.accept()

    def _apply_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ef;
                color: #1c1917;
            }
            QWidget#BrowserTopBar, QWidget#BrowserBottomBar {
                background-color: #f8f5ef;
            }
            QWidget#PreviewPane {
                background-color: #f4efe6;
            }
            QFrame#BrowserSep {
                background-color: #e4ddd1;
                max-height: 1px;
                border: none;
            }
            QSplitter#BrowserSplit::handle {
                background-color: #e4ddd1;
            }
            QListWidget#PlacesSidebar {
                background-color: #f2ede4;
                color: #292524;
                border: none;
                padding: 8px 6px;
                outline: none;
                font-size: 12px;
            }
            QListWidget#PlacesSidebar::item {
                padding: 6px 8px;
                border-radius: 6px;
                margin-bottom: 2px;
            }
            QListWidget#PlacesSidebar::item:hover {
                background-color: #e6dfd3;
            }
            QListWidget#PlacesSidebar::item:selected {
                background-color: #e0d7c8;
                color: #1c1917;
                font-weight: 600;
            }
            QTreeView#FileTree {
                background-color: #fbf9f5;
                alternate-background-color: #f6f2ea;
                color: #1c1917;
                border: none;
                outline: none;
                font-size: 12px;
            }
            QTreeView#FileTree::item {
                padding: 5px 6px;
            }
            QTreeView#FileTree::item:hover {
                background-color: #efeae0;
            }
            QTreeView#FileTree::item:selected {
                background-color: #2563eb;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f4efe6;
                color: #57534e;
                border: none;
                border-bottom: 1px solid #e4ddd1;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: 600;
            }
            QLabel#ThumbBox {
                background-color: #fbf9f5;
                border: 1px solid #ded7cb;
                border-radius: 10px;
                color: #78716c;
                font-size: 11px;
            }
            QLabel#MetaTitle {
                color: #1c1917;
                font-size: 12px;
                font-weight: 600;
            }
            QLabel#MetaSub, QLabel#FieldLabel {
                color: #78716c;
                font-size: 11px;
            }
            QLineEdit#PathBar, QLineEdit#SearchBar, QLineEdit#FilenameInput {
                background-color: #fbf9f5;
                color: #1c1917;
                border: 1px solid #d6cfc3;
                border-radius: 7px;
                padding: 5px 10px;
                font-size: 12px;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
            QLineEdit#PathBar:focus, QLineEdit#SearchBar:focus, QLineEdit#FilenameInput:focus {
                background-color: #ffffff;
                border: 1.5px solid #2563eb;
            }
            QComboBox#FormatCombo {
                background-color: #fbf9f5;
                color: #292524;
                border: 1px solid #d6cfc3;
                border-radius: 7px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QComboBox#FormatCombo QAbstractItemView {
                background-color: #fbf9f5;
                color: #1c1917;
                border: 1px solid #d6cfc3;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
            QPushButton#NavIconBtn {
                background-color: #fbf9f5;
                border: 1px solid #d6cfc3;
                border-radius: 7px;
            }
            QPushButton#NavIconBtn:hover {
                background-color: #efeae0;
            }
            QPushButton#NavIconBtn:disabled {
                opacity: 0.45;
            }
            QPushButton#SecondaryBtn {
                background-color: #fbf9f5;
                color: #292524;
                border: 1px solid #d6cfc3;
                border-radius: 7px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton#SecondaryBtn:hover {
                background-color: #efeae0;
            }
            QPushButton#PrimaryBtn {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 7px;
                padding: 6px 18px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #1d4ed8;
            }
            QPushButton#PrimaryBtn:disabled {
                background-color: #e5dfd4;
                color: #a8a29e;
            }
        """)


class AnimatedModeSwitch(QWidget):
    """Warm paper segmented control with a smoothly sliding indicator pill."""

    modeChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(244, 34)
        self._mode = "select"
        self._pill_x = 3.0
        self._pill_w = 122.0
        self._hovered = None

        self.anim = QVariantAnimation(self)
        self.anim.setDuration(260)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(self._on_anim_step)

        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _on_anim_step(self, val):
        self._pill_x = float(val)
        self.update()

    def set_mode(self, mode, animate=True):
        if mode not in ("select", "text"):
            return
        self._mode = mode
        target_x = 3.0 if mode == "select" else (self.width() - self._pill_w - 3.0)

        if animate and abs(self._pill_x - target_x) > 0.5:
            self.anim.stop()
            self.anim.setStartValue(self._pill_x)
            self.anim.setEndValue(target_x)
            self.anim.start()
        else:
            self.anim.stop()
            self._pill_x = target_x
            self.update()

    def mouseMoveEvent(self, event):
        hov = "select" if event.position().x() < self.width() / 2.0 else "text"
        if hov != self._hovered:
            self._hovered = hov
            self.update()

    def leaveEvent(self, event):
        self._hovered = None
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            chosen = "select" if event.position().x() < self.width() / 2.0 else "text"
            if chosen != self._mode:
                self.set_mode(chosen, animate=True)
                self.modeChanged.emit(chosen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setPen(QPen(QColor("#ded7cb"), 1.0))
        painter.setBrush(QColor("#ece6db"))
        painter.drawRoundedRect(rect, 9.0, 9.0)

        pill_rect = QRectF(self._pill_x, 3.0, self._pill_w, self.height() - 6.0)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(28, 25, 23, 22))
        painter.drawRoundedRect(pill_rect.adjusted(0, 1.5, 0, 1.5), 7.0, 7.0)

        painter.setPen(QPen(QColor("#e5dfd4"), 1.0))
        painter.setBrush(QColor("#fbf9f5"))
        painter.drawRoundedRect(pill_rect, 7.0, 7.0)

        font = QFont(self.font())
        font.setPointSize(9)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)

        left_rect = QRectF(3.0, 0.0, self._pill_w, self.height())
        sel_active = self._mode == "select"
        sel_color = "#1c1917" if sel_active else ("#44403c" if self._hovered == "select" else "#78716c")
        icon_sel = create_vector_icon("person", sel_color, 13)
        icon_sel.paint(painter, QRectF(left_rect.left() + 12, (self.height() - 13) / 2.0, 13, 13).toRect())
        painter.setPen(QColor(sel_color))
        painter.drawText(left_rect.adjusted(28, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Subject Mask")

        right_rect = QRectF(self.width() - self._pill_w - 3.0, 0.0, self._pill_w, self.height())
        txt_active = self._mode == "text"
        txt_color = "#1c1917" if txt_active else ("#44403c" if self._hovered == "text" else "#78716c")
        icon_txt = create_vector_icon("text", txt_color, 13)
        icon_txt.paint(painter, QRectF(right_rect.left() + 16, (self.height() - 13) / 2.0, 13, 13).toRect())
        painter.setPen(QColor(txt_color))
        painter.drawText(right_rect.adjusted(32, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Typography")


class OpacityPopover(QWidget):
    """Elevated warm-paper pill popover with smooth fade + vertical glide animation."""

    opacityChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(226, 44)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QVariantAnimation(self)
        self._fade_anim.setDuration(200)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_anim.valueChanged.connect(self._on_fade_step)
        self._fade_anim.finished.connect(self._on_fade_finished)

        self._slide_anim = QVariantAnimation(self)
        self._slide_anim.setDuration(220)
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._slide_anim.valueChanged.connect(self._on_slide_step)

        self._target_x = 0
        self._hiding = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 4, 16, 4)
        layout.setSpacing(10)

        title = QLabel("Opacity")
        title.setObjectName("PopoverTitle")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(10, 100)
        self.slider.setValue(100)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)

        self.value_label = QLabel("100%")
        self.value_label.setObjectName("PopoverValue")
        self.value_label.setFixedWidth(36)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(title)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.value_label)

        self.slider.valueChanged.connect(self._on_value_changed)
        self.hide()

    def _on_value_changed(self, val):
        self.value_label.setText(f"{val}%")
        self.opacityChanged.emit(val)

    def _on_fade_step(self, val):
        self._opacity_effect.setOpacity(float(val))

    def _on_slide_step(self, val):
        self.move(self._target_x, int(val))

    def _on_fade_finished(self):
        if self._hiding:
            super().hide()
            self._hiding = False

    def show_animated(self, target_x, target_y):
        self._target_x = target_x
        self._hiding = False

        if not self.isVisible() or self._opacity_effect.opacity() < 0.05:
            self.move(target_x, target_y + 8)
            super().show()
            self.raise_()

            self._fade_anim.stop()
            self._fade_anim.setStartValue(self._opacity_effect.opacity())
            self._fade_anim.setEndValue(1.0)
            self._fade_anim.start()

            self._slide_anim.stop()
            self._slide_anim.setStartValue(target_y + 8)
            self._slide_anim.setEndValue(target_y)
            self._slide_anim.start()
        else:
            self.move(target_x, target_y)
            self.raise_()

    def hide_animated(self):
        if not self.isVisible() or self._hiding:
            return
        self._hiding = True
        self._fade_anim.stop()
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(2, 2, -2, -3)
        radius = rect.height() / 2.0

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(28, 25, 23, 22))
        painter.drawRoundedRect(rect.adjusted(0, 3, 0, 4), radius, radius)
        painter.setBrush(QColor(28, 25, 23, 14))
        painter.drawRoundedRect(rect.adjusted(-1, 1, 1, 2), radius, radius)

        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0.0, QColor("#fffdf9"))
        grad.setColorAt(1.0, QColor("#f5f0e6"))

        painter.setPen(QPen(QColor("#d6cfc3"), 1.0))
        painter.setBrush(QBrush(grad))
        painter.drawRoundedRect(rect, radius, radius)


class WarmColorPickerDialog(QDialog):
    """Clean, warm light-themed custom color picker with HSB spectrum + hex input."""

    colorSelected = Signal(str)

    def __init__(self, initial_hex="#ffffff", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Text Color")
        self.setFixedSize(290, 275)
        self.setModal(True)

        col = QColor(initial_hex)
        if not col.isValid():
            col = QColor("#ffffff")
        h, s, v, _ = col.getHsvF()
        self._hue = max(0.0, h) if h >= 0 else 0.0
        self._sat = s
        self._val = v

        self._setup_ui()
        self._sync_from_hsv()

    def _setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ef;
            }
            QLabel {
                color: #292524;
                font-size: 12px;
                background: transparent;
            }
            QLineEdit {
                background-color: #fbf9f5;
                color: #1c1917;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                padding: 5px 8px;
                font-size: 12px;
                font-weight: 600;
            }
            QLineEdit:focus {
                border: 1.5px solid #2563eb;
            }
            QPushButton#CancelBtn {
                background-color: #fbf9f5;
                color: #292524;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 12px;
            }
            QPushButton#CancelBtn:hover {
                background-color: #efeae0;
            }
            QPushButton#ApplyBtn {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton#ApplyBtn:hover {
                background-color: #1d4ed8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.sv_box = _SVSquare(self)
        self.sv_box.svChanged.connect(self._on_sv_changed)
        layout.addWidget(self.sv_box)

        self.hue_bar = _HueSliderBar(self)
        self.hue_bar.hueChanged.connect(self._on_hue_changed)
        layout.addWidget(self.hue_bar)

        hex_row = QHBoxLayout()
        hex_row.setSpacing(10)

        self.preview_swatch = QFrame()
        self.preview_swatch.setFixedSize(28, 28)

        self.hex_input = QLineEdit()
        self.hex_input.setMaxLength(7)
        self.hex_input.textEdited.connect(self._on_hex_edited)

        hex_row.addWidget(self.preview_swatch)
        hex_row.addWidget(QLabel("Hex"))
        hex_row.addWidget(self.hex_input, 1)
        layout.addLayout(hex_row)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("CancelBtn")
        cancel_btn.clicked.connect(self.reject)

        apply_btn = QPushButton("Apply")
        apply_btn.setObjectName("ApplyBtn")
        apply_btn.clicked.connect(self._on_apply)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(apply_btn)
        layout.addLayout(btn_row)

    def _current_color(self):
        c = QColor()
        c.setHsvF(self._hue, self._sat, self._val, 1.0)
        return c

    def _sync_from_hsv(self):
        self.sv_box.set_hsv(self._hue, self._sat, self._val)
        self.hue_bar.set_hue(self._hue)
        c = self._current_color()
        self.preview_swatch.setStyleSheet(
            f"background-color: {c.name()}; border-radius: 6px; border: 1px solid #d6cfc3;"
        )
        if not self.hex_input.hasFocus():
            self.hex_input.setText(c.name().upper())

    def _on_sv_changed(self, s, v):
        self._sat = s
        self._val = v
        self._sync_from_hsv()

    def _on_hue_changed(self, h):
        self._hue = h
        self._sync_from_hsv()

    def _on_hex_edited(self, text):
        if len(text) == 7 and text.startswith("#"):
            c = QColor(text)
            if c.isValid():
                h, s, v, _ = c.getHsvF()
                if h >= 0:
                    self._hue = h
                self._sat = s
                self._val = v
                self.sv_box.set_hsv(self._hue, self._sat, self._val)
                self.hue_bar.set_hue(self._hue)
                self.preview_swatch.setStyleSheet(
                    f"background-color: {c.name()}; border-radius: 6px; border: 1px solid #d6cfc3;"
                )

    def _on_apply(self):
        self.colorSelected.emit(self._current_color().name())
        self.accept()


class _SVSquare(QWidget):
    svChanged = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(136)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self._hue = 0.0
        self._sat = 0.0
        self._val = 1.0

    def set_hsv(self, h, s, v):
        self._hue = h
        self._sat = s
        self._val = v
        self.update()

    def _pick(self, pos):
        s = max(0.0, min(1.0, pos.x() / max(1, self.width())))
        v = max(0.0, min(1.0, 1.0 - pos.y() / max(1, self.height())))
        self.svChanged.emit(s, v)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pick(e.position())

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.MouseButton.LeftButton:
            self._pick(e.position())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect())

        path = QPainterPath()
        path.addRoundedRect(r, 8, 8)
        p.setClipPath(path)

        pure = QColor()
        pure.setHsvF(self._hue, 1.0, 1.0)
        g_sat = QLinearGradient(0, 0, r.width(), 0)
        g_sat.setColorAt(0.0, QColor("#ffffff"))
        g_sat.setColorAt(1.0, pure)
        p.fillRect(r, g_sat)

        g_val = QLinearGradient(0, 0, 0, r.height())
        g_val.setColorAt(0.0, QColor(0, 0, 0, 0))
        g_val.setColorAt(1.0, QColor(0, 0, 0, 255))
        p.fillRect(r, g_val)

        cx = self._sat * r.width()
        cy = (1.0 - self._val) * r.height()
        p.setPen(QPen(QColor("#ffffff"), 2.0))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPointF(cx, cy), 6, 6)
        p.setPen(QPen(QColor("#1c1917"), 1.0))
        p.drawEllipse(QPointF(cx, cy), 7, 7)


class _HueSliderBar(QWidget):
    hueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(16)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._hue = 0.0

    def set_hue(self, h):
        self._hue = h
        self.update()

    def _pick(self, pos):
        h = max(0.0, min(0.999, pos.x() / max(1, self.width())))
        self.hueChanged.emit(h)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pick(e.position())

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.MouseButton.LeftButton:
            self._pick(e.position())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(0, 2, 0, -2)

        grad = QLinearGradient(0, 0, r.width(), 0)
        for i in range(7):
            c = QColor()
            c.setHsvF(min(0.999, i / 6.0), 1.0, 1.0)
            grad.setColorAt(i / 6.0, c)

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(grad)
        p.drawRoundedRect(r, 6, 6)

        kx = self._hue * r.width()
        p.setPen(QPen(QColor("#1c1917"), 1.5))
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(QPointF(kx, self.height() / 2.0), 6.5, 6.5)


class ImageCanvas(QWidget):

    def __init__(self, editor):
        super().__init__()
        self.editor = editor

        self.setMinimumSize(640, 480)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.pixmap = QPixmap()
        self.image_size = None

        self.points = []
        self.mode = "select"

        self.dragging_text = False
        self.resizing_corner = None
        self.resize_anchor = (0.0, 0.0)
        self.resize_start_dist = 1.0
        self.resize_start_font = 130
        self.resize_start_pos = (0, 0)
        self.resize_start_size = (1, 1)

        self.text_selected = False
        self.hovering_text = False
        self.hover_corner = None
        self.hovering_dropzone = False
        self.eyedropper_active = False
        self.drag_offset = (0, 0)
        self.press_pos = QPointF()

        self.opacity_popover = OpacityPopover(self)
        self.opacity_popover.opacityChanged.connect(
            self.editor.on_opacity_changed
        )

        self.cutout_anim_progress = 0.0
        self.cutout_anim_active = False
        self.cutout_contour_pixmap = None
        self.cutout_subject_pixmap = None
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16)
        self.anim_timer.timeout.connect(self._step_cutout_animation)

    def start_cutout_animation(self, original_pil, mask):
        if original_pil is None or mask is None:
            return

        dpr = self.devicePixelRatioF()
        w, h = original_pil.size

        mask_u8 = (mask * 255).astype(np.uint8)
        edges = cv2.Canny(mask_u8, 60, 160)
        edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
        edges_blur = cv2.GaussianBlur(edges, (0, 0), 1.4)

        contour_rgba = np.zeros((h, w, 4), dtype=np.uint8)
        contour_rgba[:, :, 0] = 37
        contour_rgba[:, :, 1] = 99
        contour_rgba[:, :, 2] = 235
        contour_rgba[:, :, 3] = np.clip(edges_blur.astype(np.int32) * 2, 0, 220).astype(np.uint8)

        c_qimg = QImage(contour_rgba.data, w, h, QImage.Format.Format_RGBA8888)
        self.cutout_contour_pixmap = QPixmap.fromImage(c_qimg.copy())
        self.cutout_contour_pixmap.setDevicePixelRatio(dpr)

        subj_pil = original_pil.convert("RGBA")
        subj_pil.putalpha(Image.fromarray(mask_u8, mode="L"))
        self.cutout_subject_pixmap = pil_to_pixmap(subj_pil, dpr=dpr)

        self.cutout_anim_progress = 0.0
        self.cutout_anim_active = True
        self.anim_timer.start()

    def _step_cutout_animation(self):
        self.cutout_anim_progress += 0.032
        if self.cutout_anim_progress >= 1.0:
            self.cutout_anim_progress = 1.0
            self.cutout_anim_active = False
            self.cutout_contour_pixmap = None
            self.cutout_subject_pixmap = None
            self.anim_timer.stop()
        self.update()

    def set_preview(self, pixmap):
        self.pixmap = pixmap
        self.position_opacity_popover()
        self.update()

    def dropzone_rect(self):
        card_w, card_h = 340, 190
        return QRectF(
            (self.width() - card_w) / 2,
            (self.height() - card_h) / 2,
            card_w,
            card_h
        )

    def image_rect(self):
        if self.pixmap.isNull() or not self.image_size:
            return QRectF()

        margin = 28
        area = self.rect().adjusted(margin, margin, -margin, -margin)
        if area.width() <= 0 or area.height() <= 0:
            return QRectF()

        img_w, img_h = self.image_size
        scale = min(area.width() / img_w, area.height() / img_h)

        draw_w = img_w * scale
        draw_h = img_h * scale

        x = (self.width() - draw_w) / 2.0
        y = (self.height() - draw_h) / 2.0

        return QRectF(x, y, draw_w, draw_h)

    def image_to_widget_rect(self, img_rect):
        target = self.image_rect()
        if target.isNull() or not self.image_size:
            return QRectF()

        bx, by, bw, bh = img_rect
        sx = target.width() / self.image_size[0]
        sy = target.height() / self.image_size[1]

        return QRectF(
            target.x() + bx * sx,
            target.y() + by * sy,
            bw * sx,
            bh * sy
        )

    def widget_to_image(self, position, clamp=True):
        rect = self.image_rect()
        if rect.isNull() or not self.image_size:
            return None

        if clamp and not rect.contains(position):
            return None

        nx = (position.x() - rect.x()) / rect.width()
        ny = (position.y() - rect.y()) / rect.height()

        x = int(nx * self.image_size[0])
        y = int(ny * self.image_size[1])

        if clamp:
            return (
                max(0, min(x, self.image_size[0] - 1)),
                max(0, min(y, self.image_size[1] - 1))
            )
        return (x, y)

    def get_widget_text_box(self):
        bounds = self.editor.get_text_bounds()
        if bounds is None:
            return QRectF()
        return self.image_to_widget_rect(bounds).adjusted(-6, -4, 6, 4)

    def get_corner_rects(self, box):
        r = 10.0
        return {
            "tl": QRectF(box.left() - r, box.top() - r, r * 2, r * 2),
            "tr": QRectF(box.right() - r, box.top() - r, r * 2, r * 2),
            "bl": QRectF(box.left() - r, box.bottom() - r, r * 2, r * 2),
            "br": QRectF(box.right() - r, box.bottom() - r, r * 2, r * 2),
        }

    def hit_test_corner(self, pos):
        if self.mode != "text" or self.image_size is None:
            return None
        box = self.get_widget_text_box()
        if box.isNull():
            return None
        for key, rect in self.get_corner_rects(box).items():
            if rect.contains(pos):
                return key
        return None

    def position_opacity_popover(self):
        if (
            not self.text_selected
            or self.mode != "text"
            or self.image_size is None
            or not self.editor.text_input.text().strip()
        ):
            self.opacity_popover.hide_animated()
            return

        box = self.get_widget_text_box()
        if box.isNull():
            self.opacity_popover.hide_animated()
            return

        pw = self.opacity_popover.width()
        ph = self.opacity_popover.height()

        px = int(box.center().x() - pw / 2)
        py = int(box.top() - ph - 12)

        if py < 12:
            py = int(box.bottom() + 12)

        px = max(12, min(px, self.width() - pw - 12))
        py = max(12, min(py, self.height() - ph - 12))

        self.opacity_popover.show_animated(px, py)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.position_opacity_popover()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp", ".bmp")
            ):
                self.hovering_dropzone = True
                self.update()
                event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.hovering_dropzone = False
        self.update()

    def dropEvent(self, event):
        self.hovering_dropzone = False
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.editor.load_image_from_path(path)

    def mousePressEvent(self, event):
        if self.image_size is None:
            if (
                event.button() == Qt.MouseButton.LeftButton
                and self.dropzone_rect().contains(event.position())
            ):
                self.editor.open_image()
            return

        if self.eyedropper_active and event.button() == Qt.MouseButton.LeftButton:
            point = self.widget_to_image(event.position())
            if point is not None:
                self.editor.sample_color_from_image(point[0], point[1])
            else:
                self.editor.set_eyedropper_mode(False)
            return

        if event.button() != Qt.MouseButton.LeftButton:
            if (
                self.mode == "select"
                and event.button() == Qt.MouseButton.RightButton
            ):
                point = self.widget_to_image(event.position())
                if point:
                    self.points.append((point[0], point[1], 0))
                    self.editor.add_selection_point(point[0], point[1], 0)
            return

        self.press_pos = event.position()

        if self.mode == "select":
            point = self.widget_to_image(event.position())
            if point is not None:
                x, y = point
                # Start fresh on normal left-click so clicking a new subject (e.g., a car)
                # doesn't mix with old points; hold Shift+Click to add extra points
                if not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                    self.points.clear()
                self.points.append((x, y, 1))
                self.editor.add_selection_point(x, y, 1)
            return

        if self.mode == "text":
            corner = self.hit_test_corner(event.position())
            if corner is not None:
                bounds = self.editor.get_text_bounds()
                if bounds is not None:
                    bx, by, bw, bh = bounds
                    self.resizing_corner = corner
                    self.resize_start_font = self.editor.font_size
                    self.resize_start_pos = (bx, by)
                    self.resize_start_size = (max(1, bw), max(1, bh))

                    anchors = {
                        "tl": (bx + bw, by + bh),
                        "tr": (bx, by + bh),
                        "bl": (bx + bw, by),
                        "br": (bx, by),
                    }
                    self.resize_anchor = anchors[corner]

                    img_pt = self.widget_to_image(event.position(), clamp=False)
                    if img_pt is not None:
                        dx = img_pt[0] - self.resize_anchor[0]
                        dy = img_pt[1] - self.resize_anchor[1]
                        self.resize_start_dist = max(10.0, np.hypot(dx, dy))

                    self.text_selected = True
                    self.opacity_popover.hide_animated()
                    self.update()
                    return

            box = self.get_widget_text_box()
            if not box.isNull() and box.contains(event.position()):
                bounds = self.editor.get_text_bounds()
                point = self.widget_to_image(event.position(), clamp=False)
                if bounds is not None and point is not None:
                    bx, by, _, _ = bounds
                    self.dragging_text = True
                    self.drag_offset = (point[0] - bx, point[1] - by)
                    self.text_selected = True
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                    self.position_opacity_popover()
                    self.update()
                    return

            self.text_selected = False
            self.opacity_popover.hide_animated()
            self.update()

    def mouseMoveEvent(self, event):
        if self.image_size is None:
            hovered = self.dropzone_rect().contains(event.position())
            if hovered != self.hovering_dropzone:
                self.hovering_dropzone = hovered
                self.setCursor(
                    Qt.CursorShape.PointingHandCursor
                    if hovered else Qt.CursorShape.ArrowCursor
                )
                self.update()
            return

        if self.eyedropper_active:
            point = self.widget_to_image(event.position())
            self.setCursor(
                Qt.CursorShape.CrossCursor
                if point is not None else Qt.CursorShape.ArrowCursor
            )
            return

        if self.mode == "select":
            point = self.widget_to_image(event.position())
            self.setCursor(
                Qt.CursorShape.PointingHandCursor
                if point is not None else Qt.CursorShape.ArrowCursor
            )
            return

        if self.resizing_corner is not None:
            img_pt = self.widget_to_image(event.position(), clamp=False)
            if img_pt is not None:
                ax, ay = self.resize_anchor
                dx = img_pt[0] - ax
                dy = img_pt[1] - ay
                curr_dist = max(10.0, np.hypot(dx, dy))
                scale = curr_dist / self.resize_start_dist

                new_font = int(
                    np.clip(round(self.resize_start_font * scale), 16, 650)
                )
                self.editor.set_font_size(new_font)

                new_bounds = self.editor.get_text_bounds()
                if new_bounds is not None:
                    _, _, nw, nh = new_bounds
                    if self.resizing_corner == "tl":
                        nx, ny = ax - nw, ay - nh
                    elif self.resizing_corner == "tr":
                        nx, ny = ax, ay - nh
                    elif self.resizing_corner == "bl":
                        nx, ny = ax - nw, ay
                    else:
                        nx, ny = ax, ay

                    self.editor.place_text(int(nx), int(ny))
            return

        if self.dragging_text and self.mode == "text":
            point = self.widget_to_image(event.position(), clamp=False)
            if point is not None:
                x = point[0] - self.drag_offset[0]
                y = point[1] - self.drag_offset[1]
                self.editor.place_text(x, y)
            return

        if self.mode == "text":
            corner = self.hit_test_corner(event.position())
            if corner != self.hover_corner:
                self.hover_corner = corner
                self.update()

            if corner in ("tl", "br"):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                return
            elif corner in ("tr", "bl"):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                return

            box = self.get_widget_text_box()
            is_over = not box.isNull() and box.contains(event.position())
            if is_over != self.hovering_text:
                self.hovering_text = is_over
                self.update()

            self.setCursor(
                Qt.CursorShape.OpenHandCursor
                if is_over else Qt.CursorShape.ArrowCursor
            )
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.resizing_corner is not None:
                self.resizing_corner = None
                self.position_opacity_popover()
                self.update()
                return

            if self.dragging_text:
                self.dragging_text = False
                self.setCursor(Qt.CursorShape.OpenHandCursor)
                self.position_opacity_popover()
                self.update()

    def _paint_warm_prism_background(self, painter):
        w = float(self.width())
        h = float(self.height())

        painter.fillRect(self.rect(), QColor("#f2ede4"))

        orbs = [
            (w * 0.20, h * 0.24, max(w, h) * 0.52, QColor(225, 29, 72, 22)),
            (w * 0.80, h * 0.22, max(w, h) * 0.54, QColor(124, 58, 237, 22)),
            (w * 0.75, h * 0.80, max(w, h) * 0.50, QColor(8, 145, 178, 20)),
            (w * 0.24, h * 0.82, max(w, h) * 0.48, QColor(217, 119, 6, 22)),
        ]
        for cx, cy, radius, color in orbs:
            grad = QRadialGradient(cx, cy, radius)
            grad.setColorAt(0.0, color)
            grad.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
            painter.fillRect(self.rect(), QBrush(grad))

        grid_step = 44
        painter.setPen(QPen(QColor(68, 64, 60, 13), 1))
        for gx in range(0, int(w), grid_step):
            painter.drawLine(gx, 0, gx, int(h))
        for gy in range(0, int(h), grid_step):
            painter.drawLine(0, gy, int(w), gy)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self._paint_warm_prism_background(painter)

        if self.pixmap.isNull():
            card = self.dropzone_rect()

            bg_color = (
                QColor(251, 249, 245, 245)
                if self.hovering_dropzone else QColor(248, 245, 239, 225)
            )
            border_color = (
                QColor("#2563eb")
                if self.hovering_dropzone else QColor("#d6cfc3")
            )

            painter.setPen(QPen(border_color, 1.4, Qt.PenStyle.DashLine))
            painter.setBrush(bg_color)
            painter.drawRoundedRect(card, 14, 14)

            icon_rect = QRectF(
                card.center().x() - 16, card.top() + 44, 32, 32
            )
            icon = create_vector_icon("folder", "#57534e", 22)
            icon.paint(
                painter, icon_rect.toRect(), Qt.AlignmentFlag.AlignCenter
            )

            title_font = QFont(self.font())
            title_font.setPointSize(13)
            title_font.setWeight(QFont.Weight.DemiBold)
            painter.setFont(title_font)
            painter.setPen(QColor("#1c1917"))
            painter.drawText(
                QRectF(card.left(), card.top() + 88, card.width(), 22),
                Qt.AlignmentFlag.AlignCenter,
                "Drop an Image Here"
            )

            sub_font = QFont(self.font())
            sub_font.setPointSize(11)
            painter.setFont(sub_font)
            painter.setPen(QColor("#78716c"))
            painter.drawText(
                QRectF(card.left(), card.top() + 112, card.width(), 20),
                Qt.AlignmentFlag.AlignCenter,
                "or click to browse PNG, JPG, or WebP"
            )
            return

        target = self.image_rect()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(28, 25, 23, 28))
        painter.drawRoundedRect(target.adjusted(-2, 4, 2, 8), 6, 6)

        painter.drawPixmap(
            target,
            self.pixmap,
            QRectF(self.pixmap.rect())
        )

        if self.cutout_anim_active and self.cutout_contour_pixmap is not None:
            t = self.cutout_anim_progress
            pulse = np.sin(t * np.pi)

            if self.cutout_subject_pixmap is not None:
                lift_scale = 1.0 + 0.016 * pulse
                lifted_w = target.width() * lift_scale
                lifted_h = target.height() * lift_scale
                lifted_rect = QRectF(
                    target.center().x() - lifted_w / 2.0,
                    target.center().y() - lifted_h / 2.0 - (3.5 * pulse),
                    lifted_w,
                    lifted_h
                )
                painter.save()
                painter.setOpacity(0.92 * pulse)
                painter.drawPixmap(
                    lifted_rect,
                    self.cutout_subject_pixmap,
                    QRectF(self.cutout_subject_pixmap.rect())
                )
                painter.restore()

            painter.save()
            painter.setOpacity(min(1.0, 1.1 * pulse))
            painter.drawPixmap(
                target,
                self.cutout_contour_pixmap,
                QRectF(self.cutout_contour_pixmap.rect())
            )
            painter.restore()

        if (
            self.image_size
            and self.mode == "text"
            and (
                self.text_selected
                or self.hovering_text
                or self.dragging_text
                or self.resizing_corner is not None
                or self.hover_corner is not None
            )
        ):
            box = self.get_widget_text_box()
            if not box.isNull():
                painter.setPen(QPen(QColor("#2563eb"), 1.5))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(box)

                corners = {
                    "tl": box.topLeft(),
                    "tr": box.topRight(),
                    "bl": box.bottomLeft(),
                    "br": box.bottomRight(),
                }
                for key, pt in corners.items():
                    active = (
                        self.hover_corner == key
                        or self.resizing_corner == key
                    )
                    radius = 5.0 if active else 4.0
                    painter.setPen(QPen(QColor("#2563eb"), 1.8))
                    painter.setBrush(QColor("#fbf9f5"))
                    painter.drawEllipse(pt, radius, radius)


class DepthType(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DepthType")
        self.setWindowIcon(create_app_icon())
        self.resize(1280, 720)
        self.center_on_screen()

        self.original = None
        self.image_bgr = None
        self.last_directory = None

        self.mask = None
        self.predictor = None
        self.is_generating = False

        self.text_color = "#ffffff"
        self.text_opacity = 100
        self.font_size = 130
        self.text_position = (100, 100)

        self.canvas = ImageCanvas(self)

        esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        esc_shortcut.activated.connect(self.handle_escape)

        self.setup_typography()
        self.create_interface()
        self.apply_stylesheet()

    def handle_escape(self):
        if self.canvas.eyedropper_active:
            self.set_eyedropper_mode(False)
            return
        if self.isFullScreen():
            self.showNormal()
            self.resize(1280, 720)
            self.center_on_screen()
        else:
            self.showFullScreen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen is not None:
            geo = screen.availableGeometry()
            x = geo.x() + (geo.width() - self.width()) // 2
            y = geo.y() + (geo.height() - self.height()) // 2
            self.move(x, y)

    def setup_typography(self):
        if FONT_PATH.exists():
            font_id = QFontDatabase.addApplicationFont(str(FONT_PATH))
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    QApplication.setFont(QFont(families[0], 13))
                    return

        QApplication.setFont(QFont("Segoe UI", 10))

    def create_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("Divider")
        return line

    def create_section_header(self, title):
        lbl = QLabel(title.upper())
        lbl.setObjectName("SectionHeader")
        return lbl

    def create_interface(self):
        toolbar = QWidget()
        toolbar.setObjectName("TopBar")
        toolbar.setFixedHeight(50)

        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(16, 6, 16, 6)
        tb_layout.setSpacing(10)

        brand_label = QLabel("DepthType")
        brand_label.setObjectName("BrandTitle")

        self.open_button = QPushButton(" Open Image")
        self.open_button.setIcon(create_vector_icon("folder", "#292524", 14))
        self.open_button.setObjectName("SecondaryButton")
        self.open_button.clicked.connect(self.open_image)

        self.mode_switch = AnimatedModeSwitch(self)
        self.mode_switch.modeChanged.connect(self.set_mode)

        self.gpu_status = QLabel(self.get_gpu_status())
        self.gpu_status.setObjectName("GpuLabel")

        self.export_button = QPushButton(" Export PNG")
        self.export_button.setIcon(create_vector_icon("export", "#ffffff", 14))
        self.export_button.setObjectName("PrimaryButton")
        self.export_button.clicked.connect(self.export_image)
        self.export_button.setEnabled(False)

        tb_layout.addWidget(brand_label)
        tb_layout.addSpacing(8)
        tb_layout.addWidget(self.open_button)
        tb_layout.addStretch()
        tb_layout.addWidget(self.mode_switch)
        tb_layout.addStretch()
        tb_layout.addWidget(self.gpu_status)
        tb_layout.addSpacing(6)
        tb_layout.addWidget(self.export_button)

        inspector = QWidget()
        inspector.setObjectName("Sidebar")
        inspector.setFixedWidth(268)

        insp_layout = QVBoxLayout(inspector)
        insp_layout.setContentsMargins(16, 16, 16, 16)
        insp_layout.setSpacing(12)

        insp_layout.addWidget(self.create_section_header("Subject Isolation"))

        hint_lbl = QLabel(
            "Click subject to auto-detect cutout\n"
            "Shift+Click to add · Right-click to exclude"
        )
        hint_lbl.setObjectName("HintText")
        insp_layout.addWidget(hint_lbl)

        insp_layout.addWidget(self.create_divider())

        insp_layout.addWidget(self.create_section_header("Typography"))

        self.text_input = QLineEdit("DEPTH")
        self.text_input.setPlaceholderText("Enter text…")
        self.text_input.textChanged.connect(self.update_preview)
        insp_layout.addWidget(self.text_input)

        font_row = QHBoxLayout()
        lbl_font = QLabel("Font")
        lbl_font.setObjectName("KeyLabel")
        val_font = QLabel("SF Pro Display")
        val_font.setObjectName("ValueLabel")
        font_row.addWidget(lbl_font)
        font_row.addStretch()
        font_row.addWidget(val_font)
        insp_layout.addLayout(font_row)

        canvas_tip = QLabel(
            "Drag corner handles to resize.\n"
            "Click text to adjust opacity."
        )
        canvas_tip.setObjectName("HintText")
        insp_layout.addWidget(canvas_tip)

        insp_layout.addWidget(self.create_divider())

        insp_layout.addWidget(self.create_section_header("Color"))

        swatch_row = QHBoxLayout()
        swatch_row.setSpacing(8)
        preset_colors = [
            "#ffffff",
            "#1c1917",
            "#eab308",
            "#f97316",
            "#ef4444",
            "#2563eb",
        ]
        for hex_col in preset_colors:
            btn = QPushButton()
            btn.setFixedSize(22, 22)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                f"background-color: {hex_col}; "
                f"border-radius: 11px; "
                f"border: 1px solid #d6cfc3;"
            )
            btn.clicked.connect(
                lambda checked=False, c=hex_col: self.set_text_color(c)
            )
            swatch_row.addWidget(btn)

        swatch_row.addStretch()
        insp_layout.addLayout(swatch_row)

        color_tools_row = QHBoxLayout()
        color_tools_row.setSpacing(8)

        self.color_swatch = QFrame()
        self.color_swatch.setFixedSize(14, 14)

        self.color_label = QLabel("#FFFFFF")
        self.color_label.setObjectName("ValueLabel")

        self.color_button = QPushButton()
        self.color_button.setObjectName("ColorPickerButton")
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_button.clicked.connect(self.choose_color)

        color_btn_layout = QHBoxLayout(self.color_button)
        color_btn_layout.setContentsMargins(8, 0, 8, 0)
        color_btn_layout.setSpacing(6)
        color_btn_layout.addWidget(self.color_swatch)
        color_btn_layout.addWidget(self.color_label)
        color_btn_layout.addStretch()

        self.eyedropper_button = QPushButton(" Pick")
        self.eyedropper_button.setIcon(create_vector_icon("eyedropper", "#292524", 13))
        self.eyedropper_button.setObjectName("SecondaryButton")
        self.eyedropper_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eyedropper_button.setToolTip("Pick color directly from image")
        self.eyedropper_button.clicked.connect(
            lambda: self.set_eyedropper_mode(True)
        )

        color_tools_row.addWidget(self.color_button, 1)
        color_tools_row.addWidget(self.eyedropper_button)
        insp_layout.addLayout(color_tools_row)

        self.update_color_swatch()
        insp_layout.addStretch()

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(toolbar)
        root_layout.addWidget(self.create_divider())

        workspace = QHBoxLayout()
        workspace.setContentsMargins(0, 0, 0, 0)
        workspace.setSpacing(0)

        workspace.addWidget(self.canvas, 1)

        v_divider = QFrame()
        v_divider.setFrameShape(QFrame.Shape.VLine)
        v_divider.setObjectName("VerticalDivider")
        workspace.addWidget(v_divider)

        workspace.addWidget(inspector)
        root_layout.addLayout(workspace, 1)

        self.setCentralWidget(root)

        self.status = QLabel("Ready")
        self.status.setObjectName("StatusText")
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().addWidget(self.status)

        self.set_mode("select", animate=False)

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2ede4;
            }

            QWidget#TopBar {
                background-color: #f8f5ef;
            }

            QWidget#Sidebar {
                background-color: #f8f5ef;
            }

            QLabel {
                color: #1c1917;
                background: transparent;
            }

            QLabel#BrandTitle {
                font-size: 14px;
                font-weight: 700;
                color: #1c1917;
            }

            QLabel#SectionHeader {
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.6px;
                color: #78716c;
            }

            QLabel#KeyLabel {
                font-size: 12px;
                color: #44403c;
            }

            QLabel#ValueLabel {
                font-size: 12px;
                color: #78716c;
            }

            QLabel#HintText {
                font-size: 11px;
                color: #78716c;
                line-height: 1.4;
            }

            QLabel#GpuLabel {
                font-size: 11px;
                color: #78716c;
            }

            QFrame#Divider {
                background-color: #e4ddd1;
                max-height: 1px;
                border: none;
            }

            QFrame#VerticalDivider {
                background-color: #e4ddd1;
                max-width: 1px;
                border: none;
            }

            QLabel#PopoverTitle {
                font-size: 11px;
                font-weight: 600;
                color: #292524;
            }

            QLabel#PopoverValue {
                font-size: 11px;
                font-weight: 600;
                color: #2563eb;
            }

            QPushButton#PrimaryButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#PrimaryButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#PrimaryButton:pressed {
                background-color: #1e40af;
            }

            QPushButton#PrimaryButton:disabled {
                background-color: #e5dfd4;
                color: #a8a29e;
            }

            QPushButton#SecondaryButton {
                background-color: #fbf9f5;
                color: #292524;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
            }

            QPushButton#SecondaryButton:hover {
                background-color: #f0ece3;
            }

            QPushButton#SecondaryButton:pressed {
                background-color: #e5dfd4;
            }

            QLineEdit {
                background-color: #fbf9f5;
                color: #1c1917;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 13px;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }

            QLineEdit:focus {
                background-color: #ffffff;
                border: 1.5px solid #2563eb;
            }

            QSlider::groove:horizontal {
                height: 3px;
                background: #d6cfc3;
                border-radius: 1.5px;
            }

            QSlider::sub-page:horizontal {
                background: #2563eb;
                border-radius: 1.5px;
            }

            QSlider::handle:horizontal {
                background: #fbf9f5;
                border: 1.5px solid #2563eb;
                width: 12px;
                height: 12px;
                margin: -5px 0;
                border-radius: 6px;
            }

            QPushButton#ColorPickerButton {
                background-color: #fbf9f5;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                min-height: 28px;
            }

            QPushButton#ColorPickerButton:hover {
                border-color: #a8a29e;
                background-color: #f0ece3;
            }

            QStatusBar {
                background-color: #f8f5ef;
                border-top: 1px solid #e4ddd1;
                color: #78716c;
                font-size: 11px;
                padding: 2px 12px;
            }

            QLabel#StatusText {
                color: #78716c;
                font-size: 11px;
            }
        """)

    def set_font_size(self, size):
        self.font_size = max(16, min(650, int(size)))

    def set_text_color(self, hex_color):
        self.text_color = hex_color
        self.update_color_swatch()
        self.update_preview()

    def update_color_swatch(self):
        self.color_swatch.setStyleSheet(
            f"background-color: {self.text_color}; "
            f"border-radius: 3px; "
            f"border: 1px solid #d6cfc3;"
        )
        self.color_label.setText(self.text_color.upper())

    def on_opacity_changed(self, value):
        self.text_opacity = value
        self.update_preview()

    def get_gpu_status(self):
        if torch.cuda.is_available():
            return f"GPU: {torch.cuda.get_device_name(0)}"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "GPU: Apple Silicon MPS"
        return "CPU"

    def set_eyedropper_mode(self, active):
        if active and self.original is None:
            return
        self.canvas.eyedropper_active = active
        if active:
            self.eyedropper_button.hide()
            self.status.setText("Click anywhere on the image to pick color (Esc to cancel)")
        else:
            self.eyedropper_button.show()
            if self.canvas.mode == "text":
                self.status.setText("Typography — Click text for opacity, drag corners to resize")

    def sample_color_from_image(self, x, y):
        if self.original is not None:
            r, g, b = self.original.getpixel((x, y))
            hex_col = f"#{r:02x}{g:02x}{b:02x}"
            self.set_text_color(hex_col)
        self.set_eyedropper_mode(False)

    def set_mode(self, mode, animate=True):
        if self.canvas.eyedropper_active:
            self.set_eyedropper_mode(False)

        self.canvas.mode = mode
        self.mode_switch.set_mode(mode, animate=animate)

        if mode != "text":
            self.canvas.text_selected = False
            self.canvas.opacity_popover.hide_animated()
        else:
            self.canvas.position_opacity_popover()

        self.canvas.update()

        if mode == "select":
            self.status.setText(
                "Subject Mask — Click subject to auto-detect cutout"
            )
        else:
            self.status.setText(
                "Typography — Click text for opacity, drag corners to resize"
            )

    def open_image(self):
        browser = ModernFileBrowserDialog(
            parent=self,
            mode="open",
            initial_dir=self.last_directory,
        )
        if browser.exec() and browser.selected_path:
            self.load_image_from_path(browser.selected_path)

    def load_image_from_path(self, path):
        try:
            p = Path(path)
            self.last_directory = str(p.parent)
            self.original = Image.open(p).convert("RGB")
            self.image_bgr = cv2.cvtColor(
                np.array(self.original),
                cv2.COLOR_RGB2BGR
            )

            self.mask = None
            self.predictor = None

            self.canvas.points.clear()
            self.canvas.text_selected = False
            self.canvas.opacity_popover.hide()
            self.canvas.image_size = self.original.size
            self.canvas.set_preview(
                pil_to_pixmap(self.original, dpr=self.devicePixelRatioF())
            )

            self.font_size = max(48, self.original.width // 6)
            self.text_position = (
                self.original.width // 4,
                self.original.height // 3
            )

            self.export_button.setEnabled(True)
            self.set_mode("select", animate=False)
            self.update_preview()

            self.status.setText(
                f"{p.name} ({self.original.width} × {self.original.height})"
            )

        except Exception as error:
            self._show_light_message("Image Error", str(error), is_error=True)

    def add_selection_point(self, x, y, label):
        if any(p[2] == 1 for p in self.canvas.points):
            self.generate_mask()
        else:
            self.mask = None
            self.status.setText(f"Excluded area at ({x}, {y}) — Click subject to cut out")
            self.update_preview()

    def generate_mask(self):
        if self.original is None or self.is_generating:
            return

        if not any(p[2] == 1 for p in self.canvas.points):
            return

        self.is_generating = True
        self.status.setText("Detecting subject…")
        QApplication.processEvents()

        try:
            if torch.cuda.is_available():
                device = 0
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"

            overrides = {
                "conf": 0.0,
                "task": "segment",
                "mode": "predict",
                "imgsz": 1024,
                "model": str(MODEL_PATH),
                "device": device,
                "verbose": False
            }

            if self.predictor is None:
                self.predictor = SAM2Predictor(overrides=overrides)

            points = [[p[0], p[1]] for p in self.canvas.points]
            labels = [p[2] for p in self.canvas.points]

            results = self.predictor(
                source=self.image_bgr,
                points=points,
                labels=labels,
                multimask_output=True,
            )

            result = results[0]

            if result.masks is None:
                raise RuntimeError("No subject detected. Try clicking another spot.")

            masks = (
                result.masks.data
                .detach()
                .float()
                .cpu()
                .numpy()
            )

            if len(masks) == 0:
                raise RuntimeError("No subject mask found.")

            # Pick the highest-confidence whole-object mask
            if (
                result.boxes is not None
                and result.boxes.conf is not None
                and len(result.boxes.conf) == len(masks)
            ):
                scores = result.boxes.conf.detach().cpu().numpy()
                index = int(np.argmax(scores))
            else:
                # Prefer full-subject mask (level 1/2) over tiny sub-part (level 0)
                areas = [float(np.sum(m > 0.5)) for m in masks]
                img_area = float(masks[0].shape[0] * masks[0].shape[1])
                valid = [i for i, a in enumerate(areas) if a < img_area * 0.88]
                if valid:
                    index = max(valid, key=lambda i: areas[i])
                else:
                    index = int(np.argmax(areas))

            raw_mask = masks[index]
            raw_mask = cv2.resize(
                raw_mask,
                self.original.size,
                interpolation=cv2.INTER_LINEAR
            )
            raw_mask = np.clip(raw_mask, 0, 1)
            raw_mask = cv2.GaussianBlur(raw_mask, (0, 0), 1.0)
            self.mask = np.clip(raw_mask, 0, 1)

            self.export_button.setEnabled(True)
            self.update_preview()
            self.canvas.start_cutout_animation(self.original, self.mask)

            self.set_mode("text", animate=True)
            self.canvas.text_selected = True
            self.canvas.position_opacity_popover()
            self.status.setText("Subject isolated — Ready for typography")

        except Exception as error:
            self._show_light_message("SAM 2 Error", str(error), is_error=True)
            self.status.setText("Subject detection failed")

        finally:
            self.is_generating = False

    def choose_color(self):
        if self.canvas.eyedropper_active:
            self.set_eyedropper_mode(False)
        dlg = WarmColorPickerDialog(self.text_color, self)
        dlg.colorSelected.connect(self.set_text_color)
        dlg.exec()

    def get_text_bounds(self):
        if self.original is None:
            return None

        text = self.text_input.text()
        if not text:
            return None

        font = load_font(self.font_size)
        draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        bbox = draw.textbbox((0, 0), text, font=font)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x, y = self.text_position

        return (x, y, width, height)

    def place_text(self, x, y):
        if self.original is None:
            return

        bounds = self.get_text_bounds()
        if bounds is not None:
            _, _, width, height = bounds
            x = max(0, min(x, self.original.width - width))
            y = max(0, min(y, self.original.height - height))

        self.text_position = (x, y)
        self.update_preview()

    def build_composite(self):
        if self.original is None:
            return None

        base = self.original.convert("RGBA")
        width, height = base.size

        text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        text = self.text_input.text()
        if text.strip():
            font = load_font(self.font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            x, y = self.text_position

            qcol = QColor(self.text_color)
            alpha_val = int((self.text_opacity / 100.0) * 255)
            rgba_fill = (qcol.red(), qcol.green(), qcol.blue(), alpha_val)

            draw.text(
                (x - bbox[0], y - bbox[1]),
                text,
                font=font,
                fill=rgba_fill
            )

        composite = Image.alpha_composite(base, text_layer)

        if self.mask is not None:
            person = self.original.convert("RGBA")
            alpha = Image.fromarray(
                (self.mask * 255).astype(np.uint8),
                mode="L"
            )
            person.putalpha(alpha)
            composite = Image.alpha_composite(composite, person)

        return composite

    def update_preview(self, *_):
        if self.original is None:
            return

        try:
            result = self.build_composite()
            self.canvas.set_preview(
                pil_to_pixmap(result, dpr=self.devicePixelRatioF())
            )
        except Exception as error:
            self.status.setText(f"Preview error: {error}")

    def _show_light_message(self, title, text, is_error=False):
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(QMessageBox.Icon.Critical if is_error else QMessageBox.Icon.Information)
        box.setStyleSheet("""
            QMessageBox {
                background-color: #f8f5ef;
                color: #1c1917;
            }
            QLabel {
                color: #1c1917;
                background: transparent;
            }
            QPushButton {
                background-color: #fbf9f5;
                color: #292524;
                border: 1px solid #d6cfc3;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #efeae0;
            }
        """)
        box.exec()

    def export_image(self):
        if self.original is None:
            return

        browser = ModernFileBrowserDialog(
            parent=self,
            mode="save",
            default_filename="depthtype_result.png",
            initial_dir=self.last_directory,
        )
        if not browser.exec() or not browser.selected_path:
            return

        path = browser.selected_path
        self.last_directory = str(Path(path).parent)

        try:
            result = self.build_composite()
            result.save(path, "PNG")
            self.status.setText(f"Exported {Path(path).name}")

            self._show_light_message(
                "Export Complete",
                f"Saved successfully:\n{path}"
            )

        except Exception as error:
            self._show_light_message("Export Error", str(error), is_error=True)


if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "DepthTypeStudio.DepthType.App.1"
        )

    app = QApplication(sys.argv)
    app.setApplicationName("DepthType")

    icon = create_app_icon()
    app.setWindowIcon(icon)

    window = DepthType()
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())