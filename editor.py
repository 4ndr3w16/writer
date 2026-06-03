import random

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFrame,
)
from PyQt6.QtCore import Qt, QTimer

from state import AppState


class ChatBubble(QLabel):
    def __init__(self, text, user=False):
        super().__init__(text)
        self.setWordWrap(True)
        self.setMaximumWidth(650)

        if user:
            self.setStyleSheet("""
                QLabel {
                    background-color: #5b4cff;
                    color: white;
                    padding: 12px 14px;
                    border-radius: 14px;
                    margin: 6px;
                    font-size: 15px;
                    border: 1px solid rgba(255,255,255,0.08);
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    background-color: #24252d;
                    color: #e7e7e7;
                    padding: 12px 14px;
                    border-radius: 14px;
                    margin: 6px;
                    border: 1px solid rgba(255,255,255,0.05);
                    font-size: 15px;
                }
            """)


class ChatPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #181920;
            }
            QScrollArea::viewport {
                background-color: #181920;
            }
        """)

        self.container = QFrame()
        self.chat_layout = QVBoxLayout(self.container)
        self.chat_layout.setSpacing(10)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        self.chat_layout.addStretch()

        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

    def add_message(self, text, user=False):
        bubble = ChatBubble(text, user)
        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1, bubble
        )
        QTimer.singleShot(50, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        ))


class InputPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribe tu historia, escena o idea...")

        self.btn = QPushButton("Enviar")

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.btn)

    def set_styles(self):
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #20222a;
                border: 1px solid #2f3240;
                border-radius: 12px;
                padding: 12px;
                font-size: 15px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #6a5cff;
            }
        """)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #6a5cff;
                color: white;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7b6dff;
            }
        """)


class ChatUI(QWidget):
    def __init__(self, state: AppState):
        super().__init__()

        self.state = state

        self.setWindowTitle("Akafuyu Writer")
        self.resize(1400, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: #1b1c22;
                color: #e6e6e6;
                font-family: Segoe UI;
                font-size: 15px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.chat = ChatPanel()
        self.input_panel = InputPanel()
        self.input_panel.set_styles()

        self.layout.addWidget(self.chat)
        self.layout.addWidget(self.input_panel)

        self.input_panel.btn.clicked.connect(self.send_message)
        self.input_panel.input.returnPressed.connect(self.send_message)

        self._load_history()

    def _load_history(self):
        if self.state.messages:
            for msg in self.state.messages:
                self.chat.add_message(
                    msg["content"], user=(msg["role"] == "user")
                )
        else:
            msg = random.choice([
                "El dojo está abierto.",
                "Habla.",
                "El mundo espera tu historia."
            ])
            self.chat.add_message(msg)

    def send_message(self):
        text = self.input_panel.input.text().strip()
        if not text:
            return

        self.input_panel.input.clear()

        self.chat.add_message(text, user=True)
        self.state.add("user", text)

        response = self.state.ask_ai()

        self.chat.add_message(response)
        self.state.add("assistant", response)
