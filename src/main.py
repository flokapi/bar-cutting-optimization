
import sys
import pathlib


from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


import find_best


class InputTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__(100, 2)
        self.setHorizontalHeaderLabels(['Length (m)', 'Quantity'])

    def get_target(self):
        self.setCurrentCell(0, 1)
        self.setCurrentCell(0, 0)
        target = {}
        for row_nb in range(self.rowCount()):
            length = self.item(row_nb, 0)
            qty = self.item(row_nb, 1)

            if (length == None) != (qty == None):
                return f'Row number {row_nb+1} is incomplete'

            if length and qty:
                try:
                    length = float(length.text())
                    qty = float(qty.text())
                except:
                    return f'Row number {row_nb+1} is invalid'

                if length in target.keys():
                    return f'Length {length} is defined twice'

                target[length] = qty

        return target


class ResultText(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFontPointSize(20)

    def show_result(self, result):
        if type(result) == str:
            self.setTextColor(QtGui.QColor('red'))
            self.setText(result)
            return

        lines = []
        for bar in result:
            qty = result[bar]
            lines.append(f'{qty} x ' + bar)

        txt = '\n'.join(lines)
        self.setTextColor(QtGui.QColor())
        self.setText(txt)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__()
        self.setIconSize(QtCore.QSize(30, 30))

        self.parent = parent

        self.bar_length = QtWidgets.QLineEdit()
        self.bar_length.setMaximumWidth(60)

        self.act = {}

        self.add_act('Reset', 'reset.png', self.parent.reset)
        self.addSeparator()
        self.addWidget(QtWidgets.QLabel('Bar Length (m): '))
        self.addWidget(self.bar_length)
        self.addSeparator()
        self.add_act('Compute', 'calc.png', self.parent.calc)

    def get_icon_path(self, icon):
        return pathlib.Path(__file__).parent / f"icons/{icon}"

    def set_icon(self, act, icon):
        icon = QtGui.QIcon(str(self.get_icon_path(icon)))
        self.act[act].setIcon(icon)

    def add_act(self, name, icon, conn):
        icon = QtGui.QIcon(str(self.get_icon_path(icon)))
        act = QtWidgets.QAction(icon, name, self)
        act.triggered.connect(conn)
        self.act[name] = act
        self.addAction(act)

    def get_bar_length(self):
        try:
            return float(self.bar_length.text())
        except:
            return None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 500)
        self.setWindowTitle('Steel Bar Cutting Optimization')

        self.initGUI()
        self.show()

    def initGUI(self):
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)

        self.input_table = InputTable()
        self.result_text = ResultText()

        gui_layout = QtWidgets.QHBoxLayout()
        gui_layout.addWidget(self.input_table)
        gui_layout.addWidget(self.result_text)

        gui_layout.setStretch(0, 1)
        gui_layout.setStretch(1, 2)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

    def reset(self):
        self.input_table.clearContents()
        self.result_text.clear()

    def calc(self):
        target = self.input_table.get_target()
        if type(target) == str:
            self.result_text.show_result(target)
            return

        bar_length = self.tool_bar.get_bar_length()
        if bar_length == None:
            self.result_text.show_result('Invalid Bar Length')
            return

        result = find_best.calc_result(bar_length, target)
        self.result_text.show_result(result)

    def close(self, event):
        sys.exit()


class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])

        self.win = MainWindow()

        sys.exit(self.exec_())


if __name__ == '__main__':
    app = App()
