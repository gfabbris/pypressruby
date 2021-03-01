"""
 Copyright (c) 2018-2021, UChicago Argonne, LLC
 See LICENSE file.
"""

import sys
from pypressruby.main_widget import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
