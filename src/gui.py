import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QSizePolicy,
                             QLabel, QScrollArea, QGroupBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from src.style_conf import *
from src.bailian import *


class SubButtonWidget(QWidget):
    """自定义二级按钮控件，包含功能按钮、控制按钮和状态标签"""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.parent_window = parent  # 保存主窗口引用

        # 设置固定高度
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(15)

        # 功能按钮
        self.func_btn = QPushButton(title)
        self.func_btn.setFixedHeight(50)
        self.func_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.func_btn.setStyleSheet(func_btn_style)

        # 控制按钮
        self.ctrl_btn = QPushButton("Start")
        self.ctrl_btn.setFixedSize(80, 40)
        self.ctrl_btn.setStyleSheet(ctrl_btn_style)

        # 状态标签
        self.status_label = QLabel("Pending")
        self.status_label.setFixedSize(100, 40)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(status_label_style)

        # 添加部件到布局
        layout.addWidget(self.func_btn, 70)  # 设置功能按钮的拉伸因子
        layout.addWidget(self.ctrl_btn, 15)  # 设置控制按钮的拉伸因子
        layout.addWidget(self.status_label, 15)  # 设置状态标签的拉伸因子

        # 连接控制按钮的点击事件
        self.ctrl_btn.clicked.connect(self.handle_ctrl_click)

        # 任务相关属性
        self.task_timer = QTimer()
        self.task_timer.timeout.connect(self.task_completed)
        self.is_running = False

    def handle_ctrl_click(self):
        """处理控制按钮点击事件"""
        # 检查主窗口是否有其他任务正在运行
        if self.parent_window and self.parent_window.is_any_task_running():
            # 如果已有任务运行，显示提示并返回
            self.parent_window.show_status_message("⚠️ 已有任务正在运行，请等待完成")
            return

        if self.is_running:
            # 如果任务正在运行，则停止任务
            self.stop_task()
        else:
            # 如果任务未运行，则启动任务
            self.start_task()

    def start_task(self):
        """启动任务"""
        # 通知主窗口任务开始
        if self.parent_window:
            self.parent_window.set_current_running_task(self)

        self.is_running = True
        self.ctrl_btn.setText("Stop")
        self.ctrl_btn.setStyleSheet(ctrl_btn_style2)
        self.status_label.setText("Running")
        self.status_label.setStyleSheet(status_label_style2)

        # 禁用功能按钮
        self.func_btn.setEnabled(False)

        # 启动任务计时器（10秒）
        self.task_timer.start(10000)

        # 通知主窗口更新状态
        if self.parent_window:
            self.parent_window.show_status_message(f"✅ 任务 '{self.func_btn.text()}' 已开始")

    def stop_task(self):
        """停止任务（手动停止）"""
        # 停止计时器
        self.task_timer.stop()

        # 更新UI
        self.task_completed(manual_stop=True)

    def task_completed(self, manual_stop=False):
        """任务完成处理"""
        self.is_running = False

        # 通知主窗口任务结束
        if self.parent_window:
            self.parent_window.clear_current_running_task()

        # 更新控制按钮
        self.ctrl_btn.setText("Start")
        self.ctrl_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                background-color: #2ECC71;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)

        # 更新状态标签
        self.status_label.setText("Completed")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                background-color: #27AE60;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
        """)

        # 启用功能按钮
        self.func_btn.setEnabled(True)

        # 通知主窗口更新状态
        if self.parent_window:
            stop_type = "手动停止" if manual_stop else "自动完成"
            self.parent_window.show_status_message(f"⏹️ 任务 '{self.func_btn.text()}' {stop_type}")

        # 3秒后恢复为"Pending"状态
        QTimer.singleShot(3000, self.reset_status)

    def reset_status(self):
        """重置状态为Pending"""
        if not self.is_running:
            self.status_label.setText("Pending")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    background-color: #BDC3C7;
                    color: #2C3E50;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)

            # 通知主窗口状态重置
            if self.parent_window:
                self.parent_window.show_status_message(f"🆗 任务 '{self.func_btn.text()}' 已重置")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("百炼英雄脚本助手v1.0")
        self.setGeometry(100, 100, 600, 650)  # 增大高度以容纳状态栏

        # 任务管理相关属性
        self.current_running_task = None  # 当前正在运行的任务
        self.all_sub_button_widgets = []  # 所有二级按钮控件的列表

        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(15)

        # 左侧主按钮区域
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)
        left_frame.setStyleSheet("background-color: #2C3E50; border-radius: 10px;")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(10, 20, 10, 20)
        left_layout.setSpacing(20)

        # 添加标题
        title_label = QLabel("功能菜单")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ECF0F1;
                padding: 10px;
                text-align: center;
            }
        """)
        left_layout.addWidget(title_label)

        # 创建主按钮
        self.main_buttons = []
        main_btn_titles = ["日常", "资源", "刷图"]
        for title in main_btn_titles:
            btn = QPushButton(title)
            btn.setFixedHeight(60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    background-color: #3498DB;
                    color: white;
                    border-radius: 8px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
                QPushButton:pressed {
                    background-color: #1B4F72;
                }
            """)
            btn.clicked.connect(lambda checked, t=title: self.show_sub_buttons(t))
            left_layout.addWidget(btn)
            self.main_buttons.append(btn)

        # 添加弹簧使按钮靠上
        left_layout.addStretch()

        # 右侧区域 - 使用滚动区域确保内容固定
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setFrameShape(QFrame.NoFrame)

        # 创建右侧内容容器
        self.right_content = QWidget()
        self.right_content.setStyleSheet("background-color: #ECF0F1;")
        self.right_layout = QVBoxLayout(self.right_content)
        self.right_layout.setContentsMargins(20, 20, 20, 20)
        self.right_layout.setSpacing(25)

        # 添加右侧标题
        self.right_title = QLabel("请选择功能")
        self.right_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2C3E50;
                padding-bottom: 15px;
                border-bottom: 2px solid #BDC3C7;
            }
        """)
        self.right_layout.addWidget(self.right_title)

        # 添加占位符
        self.placeholder = QLabel("请从左侧菜单中选择一个功能类别")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                color: #7F8C8D;
                padding: 50px;
            }
        """)
        self.right_layout.addWidget(self.placeholder)
        self.right_layout.addStretch()

        # 设置滚动区域的内容
        self.right_scroll.setWidget(self.right_content)

        # 将左右区域添加到内容布局
        content_layout.addWidget(left_frame, 1)
        content_layout.addWidget(self.right_scroll, 3)

        # 将内容区域添加到主布局
        main_layout.addWidget(content_widget, 9)  # 90%高度

        # 状态栏区域
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #2C3E50;")
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(15, 8, 15, 8)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ECF0F1;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.status_label)

        # 任务状态指示器
        self.task_indicator = QLabel()
        self.task_indicator.setFixedSize(20, 20)
        self.task_indicator.setStyleSheet("""
            QLabel {
                background-color: #27AE60;
                border-radius: 10px;
            }
        """)
        status_layout.addWidget(self.task_indicator)

        # 添加弹簧使内容靠左
        status_layout.addStretch()

        # 将状态栏添加到主布局
        main_layout.addWidget(status_frame, 1)  # 10%高度

        self.setCentralWidget(main_widget)

        # 存储二级按钮配置
        self.sub_buttons_config = {
            "日常": ["每日领取", "自动PK", "自动抽卡"],
            "资源": ["木头", "蓝矿"],
            "刷图": ["1-1", "2-2"]
        }

    def clear_right_frame(self):
        """清除右侧区域内容（保留标题）"""
        # 删除除标题之外的所有控件
        while self.right_layout.count() > 1:
            item = self.right_layout.takeAt(1)
            if item.widget():
                widget = item.widget()
                # 从所有任务列表中移除
                if isinstance(widget, SubButtonWidget):
                    try:
                        self.all_sub_button_widgets.remove(widget)
                    except ValueError:
                        pass
                widget.deleteLater()

    def show_sub_buttons(self, main_btn):
        """显示对应主按钮的二级按钮"""
        # 清除右侧区域（保留标题）
        self.clear_right_frame()

        # 更新标题
        self.right_title.setText(f"{main_btn}功能")

        # 获取对应主按钮的二级按钮列表
        sub_titles = self.sub_buttons_config.get(main_btn, [])

        # 添加固定位置的分组框
        button_group = QGroupBox(f"{main_btn}功能")
        button_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
                border: 2px solid #BDC3C7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        group_layout = QVBoxLayout(button_group)
        group_layout.setContentsMargins(15, 25, 15, 15)
        group_layout.setSpacing(15)

        # 添加二级按钮控件
        for title in sub_titles:
            sub_widget = SubButtonWidget(title, self)  # 传递self作为父窗口
            group_layout.addWidget(sub_widget)
            # 添加到全局列表
            self.all_sub_button_widgets.append(sub_widget)

        # 添加分组到右侧布局
        self.right_layout.addWidget(button_group)

        # 添加弹簧使内容保持顶部对齐
        self.right_layout.addStretch()

        # 更新状态栏
        self.show_status_message(f"已显示 '{main_btn}' 功能")

    # 任务管理方法
    def is_any_task_running(self):
        """检查是否有任务正在运行"""
        return self.current_running_task is not None

    def set_current_running_task(self, task):
        """设置当前运行的任务"""
        self.current_running_task = task
        self.update_task_indicator()

        # 禁用所有其他按钮
        for widget in self.all_sub_button_widgets:
            if widget != task:
                widget.ctrl_btn.setEnabled(False)

    def clear_current_running_task(self):
        """清除当前运行的任务"""
        self.current_running_task = None
        self.update_task_indicator()

        # 启用所有按钮
        for widget in self.all_sub_button_widgets:
            widget.ctrl_btn.setEnabled(True)

    def update_task_indicator(self):
        """更新任务状态指示器"""
        if self.current_running_task:
            self.task_indicator.setStyleSheet("""
                QLabel {
                    background-color: #E74C3C;
                    border-radius: 10px;
                }
            """)
        else:
            self.task_indicator.setStyleSheet("""
                QLabel {
                    background-color: #27AE60;
                    border-radius: 10px;
                }
            """)

    def show_status_message(self, message):
        """在状态栏显示消息"""
        self.status_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置应用字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())