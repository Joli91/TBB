import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel
import run


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None


class MainWindow(QMainWindow):
    def __init__(self, data=pd.DataFrame()):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Pandas Table View")

        # Create the table view and set the model
        table_view = QTableView()
        table_view.setModel(PandasModel(data))

        # Set the table properties
        table_view.setSortingEnabled(True)
        table_view.horizontalHeader().setStretchLastSection(True)
        table_view.verticalHeader().setVisible(False)

        # Set the central widget
        self.setCentralWidget(table_view)


if __name__ == "__main__":
    # Create a sample dataframe
    data = run.df

    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow(data)

    # Show the main window
    window.show()

    # Run the event loop
    sys.exit(app.exec_())
