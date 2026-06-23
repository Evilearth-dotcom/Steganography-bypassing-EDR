import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BinHexTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIN → 十六进制 转换工具")
        self.setGeometry(100, 100, 780, 600)
        self.init_ui()

    def init_ui(self):
        
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QWidget { background-color: #2b2b2b; color: #fff; }
            QLabel { color: #fff; font-size: 12px; }
            QLineEdit {
                background-color: #3a3a3a;
                border: 1px solid #555;
                padding: 6px;
                color: white;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ffaa;
                border: 1px solid #444;
                font-family: Consolas;
                font-size: 12px;
            }
            QPushButton {
                background-color: #444;
                color: white;
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton#action {
                background-color: #2E8B57;
            }
            QPushButton#action:hover {
                background-color: #3cb371;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # 标题
        title = QLabel("BIN → 十六进制 转换工具")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 路径选择
        path_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("选择 loader.bin 文件...")
        self.btn_browse = QPushButton("浏览文件")
        path_layout.addWidget(self.file_path)
        path_layout.addWidget(self.btn_browse)
        layout.addLayout(path_layout)

        # 功能按钮
        btn_layout = QHBoxLayout()
        self.btn_bin2hex = QPushButton("BIN 转 十六进制")
        self.btn_copy = QPushButton("复制内容")
        self.btn_save = QPushButton("保存到文件")
        self.btn_save.setObjectName("action")

        btn_layout.addWidget(self.btn_bin2hex)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        # 信息栏
        info_layout = QHBoxLayout()
        self.label_size = QLabel("大小：0 字节")
        info_layout.addWidget(self.label_size)
        layout.addLayout(info_layout)

        # 预览区域
        layout.addWidget(QLabel("十六进制内容："))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        # 绑定事件
        self.btn_browse.clicked.connect(self.select_file)
        self.btn_bin2hex.clicked.connect(self.bin_to_hex)
        self.btn_copy.clicked.connect(self.copy_content)
        self.btn_save.clicked.connect(self.save_content)

        self.current_data = None

   
    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择 BIN 文件", "", "二进制文件 (*.bin);;所有文件 (*.*)")
        if path:
            self.file_path.setText(path)
            self.preview.clear()
            self.label_size.setText("大小：0 字节")


    def bin_to_hex(self):
        path = self.file_path.text().strip()
        if not os.path.exists(path):
            QMessageBox.warning(self, "错误", "文件不存在")
            return

        try:
            with open(path, "rb") as f:
                data = f.read()

            hex_str = data.hex()
            self.preview.setPlainText(hex_str)
            self.label_size.setText(f"大小：{len(data)} 字节")
            self.current_data = hex_str
            self.log("✅ BIN → 十六进制 转换成功")

        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def copy_content(self):
        if self.current_data is None:
            QMessageBox.warning(self, "提示", "无内容可复制")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_data)
        self.log("📋 已复制到剪贴板")

    def save_content(self):
        if self.current_data is None:
            QMessageBox.warning(self, "提示", "无内容可保存")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "保存十六进制", "hex_output.txt", "文本文件 (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.current_data)
            self.log(f"💾 已保存：{os.path.basename(filename)}")

    # ------------------------------
    # 日志输出
    # ------------------------------
    def log(self, text):
        self.preview.append(f"\n{text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BinHexTool()
    win.show()
    sys.exit(app.exec_())