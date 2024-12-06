import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QPushButton, QWidget, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

class TeacherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher CRUD Application")
        self.setGeometry(100, 100, 800, 600)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('teachers.db')

        if not self.db.open():
            print("Error: Unable to connect to database")
            return

        self.create_table()

        self.model = QSqlTableModel(self)
        self.model.setTable('Teacher')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)

        self.add_button = QPushButton("Add Teacher", self)
        self.add_button.clicked.connect(self.add_teacher)

        self.update_button = QPushButton("Update Teacher", self)
        self.update_button.clicked.connect(self.update_teacher)

        self.delete_button = QPushButton("Delete Teacher", self)
        self.delete_button.clicked.connect(self.delete_teacher)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_table(self):
        query = QSqlQuery()
        query.exec_('''CREATE TABLE IF NOT EXISTS Teacher (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        age INTEGER)''')

    def add_teacher(self):
        name = "John Doe"
        subject = "Math"
        age = 30
        query = QSqlQuery()
        query.prepare("INSERT INTO Teacher (name, subject, age) VALUES (?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(subject)
        query.addBindValue(age)
        query.exec_()

        self.model.select()

    def update_teacher(self):
        index = self.table_view.selectedIndexes()
        if index:
            row = index[0].row()
            self.model.setData(self.model.index(row, 1), "Updated Name")
            self.model.setData(self.model.index(row, 2), "Updated Subject")
            self.model.setData(self.model.index(row, 3), 35)
            self.model.submitAll()

    def delete_teacher(self):
        index = self.table_view.selectedIndexes()
        if index:
            row = index[0].row()
            self.model.removeRow(row)
            self.model.submitAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherApp()
    window.show()
    sys.exit(app.exec_())
