import sys
from dotenv import load_dotenv

load_dotenv()

from PyQt6.QtWidgets import QApplication
from editor import ChatUI
from state import AppState

app = QApplication(sys.argv)

state = AppState()

window = ChatUI(state)
window.show()

sys.exit(app.exec())
