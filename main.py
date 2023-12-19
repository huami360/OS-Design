import sys
import psutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QHBoxLayout, QPushButton, QWidget) # 导入需要的模块
from PyQt5.QtCore import QTimer

class ProcessManager(QMainWindow):

    def __init__(self, app):
        super().__init__()
        
        self.setWindowTitle("任务管理器")  
        self.resize(800, 600)
        
        self.table = QTableWidget(self) 
        self.table.setRowCount(10)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["进程名", "PID", "CPU%", "内存%"]) 
        
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 100) 
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        
        for i in range(10):
            self.table.setRowHeight(i, 40)
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setStyleSheet("font:bold 16px")  
        self.table.setStyleSheet("font: 14px")
        
        self.table.setGeometry(50, 50, 700, 500)
        
        self.processes = sorted(psutil.process_iter(), key=lambda p: p.cpu_percent(), reverse=True)
       
        menu_bar = self.menuBar()
        
        file_menu = QMenu('文件', self)
        menu_bar.addMenu(file_menu)
        
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.show_processes)
        file_menu.addAction(refresh_action)
        
        view_menu = QMenu('查看', self)
        menu_bar.addMenu(view_menu)  
        
        columns_action = QAction('选择列', self)
        view_menu.addAction(columns_action)
        
        # 创建一个横向布局，并添加两个按钮，分别用来翻页
        self.layout = QHBoxLayout()
        self.prev_button = QPushButton('上一页', self)
        self.next_button = QPushButton('下一页', self)
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.next_button)
        
        # 将按钮的信号槽函数连接到相应的方法
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        
        # 创建一个小部件，用来容纳布局，并将其放在表格的下方
        self.widget = QWidget(self)
        self.widget.setLayout(self.layout)
        self.widget.setGeometry(50, 550, 700, 50)
        
        self.timer = app.timer
        self.timer.timeout.connect(self.show_processes)
        self.timer.start(1000)
        
        # 定义一个属性，用来存储当前的页码，初始值为0
        self.page = 0

    def show_processes(self):
        # 根据当前的页码和每页显示的行数，计算出要显示的进程的索引范围
        start = self.page * 10
        end = start + 10
        
        # 用切片操作获取相应的进程列表
        processes = self.processes[start:end]
        
        for i in range(10):
            process = processes[i]
            name = process.name()
            pid = process.pid  
            cpu = process.cpu_percent()
            memory = process.memory_percent()
            
            item_name = QTableWidgetItem(name)
            item_pid = QTableWidgetItem(str(pid))
            item_cpu = QTableWidgetItem(f"{cpu:.2f}%")
            item_memory = QTableWidgetItem(f"{memory:.2f}%")
            
            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_pid)
            self.table.setItem(i, 2, item_cpu)
            self.table.setItem(i, 3, item_memory)
            
    # 定义一个信号槽函数，用来处理上一页的动作
    def prev_page(self):
        # 判断是否可以翻到上一页，即当前页码是否大于0
        if self.page > 0:
            # 如果可以，就将页码减1，并重新显示数据
            self.page -= 1
            self.show_processes()
    
    # 定义一个信号槽函数，用来处理下一页的动作
    def next_page(self):
        # 判断是否可以翻到下一页，即当前页码是否小于进程列表的长度除以每页的行数
        if self.page < len(self.processes) // 10:
            # 如果可以，就将页码加1，并重新显示数据
            self.page += 1
            self.show_processes()
            
if __name__ == '__main__':

    app = QApplication(sys.argv)       
    app.timer = QTimer() 
    process_manager = ProcessManager(app)
    process_manager.show()
    
    sys.exit(app.exec_())
