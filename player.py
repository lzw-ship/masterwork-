import os
import tkinter
from tkinter import Canvas, PhotoImage, Listbox, StringVar, messagebox,simpledialog, filedialog
from PIL import Image, ImageTk
import time
import sys
import random
import threading
import pygame
import ctypes
from math import sin, cos, pi, log
import webbrowser
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tkinter import ttk
import json
import chardet


def open_options_window():
    global root
    root.iconbitmap('star.ico')
    # 创建新的窗口
    options_window = tkinter.Toplevel(root)
    options_window.title("音乐选项")

    # 定义列表中的选项
    options = ["声明", "快捷键", "会员", "宗旨","帮助"]

    # 创建列表框
    listbox = tkinter.Listbox(options_window)
    for option in options:
        listbox.insert(tkinter.END, option)

    # 将列表框放置在窗口中
    listbox.pack(padx=20, pady=20, fill=tkinter.BOTH, expand=True)

    # 添加选择事件处理，例如显示所选项目
    def show_license_info(event):
        # 获取当前选中的选项
        try:
            selected_option = listbox.get(listbox.curselection())
            if selected_option == "声明":
                def show_license():
                    # 创建一个新的窗口来显示条款信息
                    license_win = tkinter.Tk()
                    license_win.iconbitmap('star.ico')
                    license_win.geometry("800x600+500+200")
                    license_win.title("用户需知")

                    # 添加文本框来显示条款内容，并添加滚动条
                    text_frame = tkinter.Frame(license_win)
                    text_frame.pack(expand=True, fill='both')

                    text = tkinter.Text(text_frame, wrap='word', state='disabled')
                    text.grid(row=0, column=0, sticky='nsew')

                    scrollbar = tkinter.Scrollbar(text_frame, command=text.yview)
                    scrollbar.grid(row=0, column=1, sticky='ns')

                    text['yscrollcommand'] = scrollbar.set

                    # 插入条款内容
                    terms = """
                        版权声明:
                        本软件由masterwork开发，受国际版权法保护。未经书面许可，任何单位和个人不得复制、发行或以其他方式使用本软件。

                        许可协议:
                        使用本软件即表示您同意遵守本许可协议中的所有条款。如果您不同意，请勿使用本软件。

                        免责声明:
                        本软件按“原样”提供，没有任何明示或暗示的保证，包括但不限于对适销性、特定用途适用性和非侵权的保证。

                        隐私条款:
                        我们尊重并保护所有用户的个人隐私。我们不会收集、使用或泄露您的个人信息，除非获得您的明确同意或法律要求。
                        """
                    text.config(state='normal')
                    text.insert('1.0', terms)
                    text.config(state='disabled')

                    # 调整文本框的布局
                    text_frame.grid_rowconfigure(0, weight=1)
                    text_frame.grid_columnconfigure(0, weight=1)

                    # 运行主循环
                    license_win.mainloop()

                if __name__ == "__main__":
                    show_license()
            elif selected_option == "快捷键":
                class ShortcutApp:
                    def __init__(self, root):
                        self.root = root
                        self.root.iconbitmap('star.ico')
                        self.shortcuts = {
                            "新建项目": "Ctrl + N",
                            "打开项目": "Ctrl + O",
                            "保存项目": "Ctrl + S",
                            "导出项目": "Ctrl + E",
                            "撤销操作": "Ctrl + Z",
                            "重做操作": "Ctrl + Y",
                            "剪切选择": "Ctrl + X",
                            "复制选择": "Ctrl + C",
                            "粘贴": "Ctrl + V",
                            "删除选择": "Delete",
                            "全选": "Ctrl + A",
                            "放大": "Ctrl + +",
                            "缩小": "Ctrl + -"
                        }

                        self.load_shortcuts()

                        # 主窗口控件
                        self.main_frame = tkinter.Frame(root)
                        self.main_frame.pack(padx=10, pady=10)

                        self.shortcuts_listbox = tkinter.Listbox(self.main_frame, width=50, height=15)
                        self.shortcuts_listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

                        self.scrollbar = tkinter.Scrollbar(self.main_frame, orient="vertical")
                        self.scrollbar.config(command=self.shortcuts_listbox.yview)
                        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

                        self.shortcuts_listbox.config(yscrollcommand=self.scrollbar.set)

                        self.update_listbox()

                        # 编辑按钮
                        self.edit_button = tkinter.Button(root, text="Edit Shortcut", command=self.modify_shortcut)
                        self.edit_button.pack(pady=5)

                    def load_shortcuts(self):
                        try:
                            with open('shortcuts.json', 'rb') as f:
                                result = chardet.detect(f.read())
                                encoding = result['encoding']
                            with open('shortcuts.json', 'r', encoding=encoding) as f:
                                self.shortcuts = json.load(f)
                        except FileNotFoundError:
                            self.save_shortcuts()  # 如果文件不存在，保存预定义的快捷键
                        except json.JSONDecodeError:
                            messagebox.showerror("Error", "The shortcuts.json file is not a valid JSON file.")
                            self.shortcuts = {}  # 清空快捷键字典

                    def save_shortcuts(self):
                        with open('shortcuts.json', 'w', encoding='utf-8') as f:
                            json.dump(self.shortcuts, f, ensure_ascii=False, indent=4)

                    def update_listbox(self):
                        self.shortcuts_listbox.delete(0, tkinter.END)
                        for shortcut in self.shortcuts:
                            self.shortcuts_listbox.insert(tkinter.END, f"{shortcut} - {self.shortcuts[shortcut]}")

                    def modify_shortcut(self):
                        shortcut = simpledialog.askstring("输入", "请输入要修改的快捷键:", parent=self.root)
                        if shortcut and shortcut in self.shortcuts:
                            new_value = simpledialog.askstring("输入", f"请输入新的快捷键值({shortcut}):",
                                                               parent=self.root)
                            if new_value is not None:
                                self.shortcuts[shortcut] = new_value
                                self.save_shortcuts()
                                messagebox.showinfo("提示", f"快捷键 {shortcut} 已更新为 {new_value}")
                                self.update_listbox()
                        elif not shortcut:
                            messagebox.showwarning("警告", "输入为空，请重新输入！")
                        else:
                            messagebox.showwarning("警告", "输入的快捷键不存在！")

                if __name__ == "__main__":
                    root = tkinter.Tk()
                    root.title("Shortcut Manager")

                    app = ShortcutApp(root)

                    root.mainloop()
            elif selected_option == "帮助":
                # 问题列表
                questions = [
                    ("连续包月会员可以退费吗？", "连续包月会员可以在一定条件下申请退费。"),
                    ("iOS充值如何退款？", "iOS充值退款请通过App Store客服处理。"),
                    ("为什么没有听歌领VIP的活动了？", "该活动已结束，敬请期待新的活动。"),
                    ("masterwork音樂的会员可以在酷狗概念版...?", "masterwork音樂会员可以在多个版本中使用。"),
                    ("为什么我是新用户领取不了vip？", "请检查您的账户是否符合领取条件。"),
                    ("是否可以在拼多多渠道购买会员？", "目前暂不支持在拼多多渠道购买会员。"),
                    ("领不到每日VIP怎么办？", "请尝试重新登录或联系客服。"),
                    ("学生会员取消了可以再订阅吗？", "学生会员取消后可以再次订阅。"),
                    ("如何下载歌曲到手机？", "在歌曲页面点击下载图标，选择音质后即可下载。"),
                    ("如何创建个人歌单？", "进入我的音乐，点击新建歌单，输入名称后保存。"),
                    ("如何删除歌单中的歌曲？", "在歌单页面长按歌曲，选择删除选项。"),
                    ("如何更改账户密码？", "进入设置，找到账户安全选项，按照提示操作。"),
                    ("如何找回忘记的密码？", "点击登录界面的忘记密码，按照指引操作。"),
                    ("如何使用一起听功能？", "打开一起听，邀请好友加入房间即可。"),
                    ("如何参加音乐直播？", "关注喜欢的主播，直播开始时进入直播间。"),
                    ("如何在masterwork音樂上发表评论？", "播放歌曲后，在评论区输入内容并发送。"),
                    ("如何开启夜间模式？", "进入设置，找到外观选项，选择夜间模式。"),
                    ("如何关闭广告？", "成为VIP会员后，大部分广告将自动关闭。"),
                    ("如何同步我的播放记录？", "登录账户后，播放记录会自动同步。"),
                    ("如何分享歌曲给朋友？", "在歌曲页面点击分享图标，选择分享方式。"),
                    ("如何使用masterwork音樂的K歌功能？", "打开K歌，选择喜欢的歌曲开始演唱。"),
                    ("如何获取更多的金币？", "完成日常任务或观看广告可获得金币。"),
                    ("如何使用金币？", "金币可用于购买虚拟物品或特权服务。"),
                    ("如何查看我的收藏？", "进入我的音乐，点击我的收藏查看。"),
                    ("如何设置默认播放音质？", "进入设置，找到播放选项，选择音质。"),
                    ("如何使用听歌识曲功能？", "打开听歌识曲，对准声源，等待识别结果。"),
                    ("如何添加歌曲到现有歌单？", "在歌曲页面点击添加到，选择目标歌单。"),
                    ("如何使用音乐闹钟？", "设置闹钟，选择音乐作为铃声。"),
                    ("如何下载离线歌词？", "在歌曲页面点击下载歌词，选择离线模式。"),
                    ("如何管理我的账户信息？", "进入设置，找到账户管理进行操作。"),
                    ("如何使用音乐搜索功能？", "在搜索栏输入关键词，如歌手名或歌曲名。"),
                    ("如何联系masterwork音樂客服？", "进入设置，找到帮助与反馈，点击在线客服。"),
                ]

                def search_questions(search_entry, questions_tree):
                    query = search_entry.get().strip()
                    if not query:
                        return

                    for item in questions_tree.get_children():
                        questions_tree.delete(item)

                    filtered_questions = [q for q in questions if query.lower() in q[0].lower()]
                    for question, answer in filtered_questions:
                        questions_tree.insert("", "end", values=(question, answer))

                def create_questions_treeview(parent):
                    tree = ttk.Treeview(parent, columns=("Question", "Answer"), show="headings")
                    tree.heading("Question", text="问题")
                    tree.heading("Answer", text="回答")
                    tree.column("Question", width=500)  # 增加问题列的宽度
                    tree.column("Answer", width=500)  # 增加回答列的宽度
                    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=80, sticky='nsew')

                    # 增加 Treeview 的高度
                    parent.grid_rowconfigure(1, weight=1)
                    parent.grid_columnconfigure(0, weight=1)

                    scrollbar = ttk.Scrollbar(parent, orient=tkinter.VERTICAL, command=tree.yview)
                    tree.configure(yscrollcommand=scrollbar.set)
                    scrollbar.grid(row=1, column=2, sticky='ns')
                    return tree

                def open_help_window():
                    help_window = tkinter.Tk()
                    help_window.title("解疑答惑")
                    help_window.geometry("800x600")

                    # 创建搜索框
                    search_entry = ttk.Entry(help_window, width=40)
                    search_entry.grid(row=0, column=0, padx=10, pady=50, sticky=tkinter.W)
                    search_entry.insert(0, "搜索问题")
                    search_entry.bind("<FocusIn>",
                                      lambda event: search_entry.delete(0,
                                                                        tkinter.END) if search_entry.get() == "搜索问题" else None)
                    search_entry.bind("<Return>", lambda event: search_questions(search_entry, questions_tree))

                    # 创建搜索按钮
                    search_button = ttk.Button(help_window, text="搜索",
                                               command=lambda: search_questions(search_entry, questions_tree))
                    search_button.grid(row=0, column=1, padx=10, pady=50, sticky=tkinter.W)

                    # 创建问题列表
                    global questions_tree
                    questions_tree = create_questions_treeview(help_window)

                    # 初始化显示所有问题和答案
                    for question, answer in questions:
                        questions_tree.insert("", "end", values=(question, answer))

                # 直接调用打开帮助窗口的函数
                open_help_window()

                # 进入Tkinter的主循环
                tkinter.mainloop()

            elif selected_option == "会员":
                def create_top_bar(root):
                    top_bar = tkinter.Frame(root, bg="#333333", height=10)
                    top_bar.pack(fill=tkinter.X)

                    logo_label = tkinter.Label(top_bar, text="Masterwork Music", fg="white", bg="#333333", font=("Arial", 16))
                    logo_label.pack(side=tkinter.LEFT, padx=10)

                    search_entry = tkinter.Entry(top_bar, width=10)
                    search_entry.pack(side=tkinter.LEFT, padx=10)

                def create_welcome_section(content_frame):
                    welcome_frame = tkinter.Frame(content_frame, pady=10, bg="white")
                    welcome_frame.pack(fill=tkinter.X, padx=10)

                    welcome_label = tkinter.Label(welcome_frame, text="你好，masterwork音樂用户！欢迎来到会员中心",
                                                  font=("Arial", 14), bg="white")
                    welcome_label.pack()

                def create_membership_details(content_frame):
                    details_frame = tkinter.Frame(content_frame, pady=10, bg="white")
                    details_frame.pack(fill=tkinter.X, padx=10)

                    title_label = tkinter.Label(details_frame, text="会员计划", font=("Arial", 16, "bold"), bg="white")
                    title_label.pack(pady=10)

                    # 会员分类
                    membership_types = [
                        {
                            "name": "普通会员",
                            "price": "¥30/月",
                            "description": "享受基础会员特权",
                            "privileges": [
                                {"icon": "🔥", "text": "无广告播放"},
                                {"icon": "🎶", "text": "高品质音质"},
                                {"icon": "🎵", "text": "下载歌曲"}
                            ]
                        },
                        {
                            "name": "高级会员",
                            "price": "¥50/月",
                            "description": "享受高级会员特权",
                            "privileges": [
                                {"icon": "🔥", "text": "无广告播放"},
                                {"icon": "🎶", "text": "高品质音质"},
                                {"icon": "🎵", "text": "下载歌曲"},
                                {"icon": "🌟", "text": "独家内容"},
                                {"icon": "🚀", "text": "优先客服支持"}
                            ]
                        },
                        {
                            "name": "超级会员",
                            "price": "¥100/年",
                            "description": "享受所有会员特权",
                            "privileges": [
                                {"icon": "🔥", "text": "无广告播放"},
                                {"icon": "🎶", "text": "高品质音质"},
                                {"icon": "🎵", "text": "下载歌曲"},
                                {"icon": "🌟", "text": "独家内容"},
                                {"icon": "🚀", "text": "优先客服支持"},
                                {"icon": "🎁", "text": "每月赠品"}
                            ]
                        }
                    ]

                    # 创建一个单独的 Frame 用于 grid 布局
                    grid_frame = tkinter.Frame(details_frame, bg="white")
                    grid_frame.pack(fill=tkinter.X, padx=10, pady=10)

                    for i, membership in enumerate(membership_types):
                        type_frame = tkinter.Frame(grid_frame, borderwidth=1, relief=tkinter.SOLID, padx=10, pady=10,
                                                   bg="white")
                        type_frame.grid(row=0, column=i, padx=10, pady=10)

                        name_label = tkinter.Label(type_frame, text=membership["name"], font=("Arial", 14, "bold"),
                                                   bg="white")
                        name_label.pack(anchor=tkinter.W)

                        price_label = tkinter.Label(type_frame, text=membership["price"], font=("Arial", 12),
                                                    bg="white")
                        price_label.pack(anchor=tkinter.W)

                        description_label = tkinter.Label(type_frame, text=membership["description"],
                                                          font=("Arial", 12), bg="white")
                        description_label.pack(anchor=tkinter.W)

                        privileges_label = tkinter.Label(type_frame, text="会员特权", font=("Arial", 12, "bold"),
                                                         bg="white")
                        privileges_label.pack(anchor=tkinter.W, pady=5)

                        for privilege in membership["privileges"]:
                            label = tkinter.Label(type_frame, text=f"{privilege['icon']} {privilege['text']}",
                                                  font=("Arial", 12),
                                                  bg="white")
                            label.pack(anchor=tkinter.W)

                        subscribe_button = tkinter.Button(type_frame, text="立即订阅",
                                                          command=lambda m=membership: subscribe_membership(m))
                        subscribe_button.pack(pady=5)

                def create_support_section(content_frame):
                    support_frame = tkinter.Frame(content_frame, bg="white", padx=10, pady=10)
                    support_frame.pack(fill=tkinter.X, padx=10, pady=10)

                    support_label = tkinter.Label(support_frame, text="遇到问题？请联系我们", font=("Arial", 14, "bold"),
                                                  bg="white")
                    support_label.pack(anchor=tkinter.W, pady=10)

                    contact_button = tkinter.Button(support_frame, text="联系客服", command=open_contact)
                    contact_button.pack(pady=5)

                def renew_membership():
                    messagebox.showinfo("续费成功", "您的会员已成功续费！")

                def open_contact():
                    messagebox.showinfo("联系我们", "我们的客服电话：123-456-7890")

                def subscribe_membership(membership):
                    messagebox.showinfo("订阅成功", f"您已成功订阅{membership['name']}！")

                def on_mousewheel(event, canvas):
                    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

                def main():
                    root = tkinter.Tk()
                    root.iconbitmap('star.ico')
                    root.title("masterwork音樂会员中心")
                    root.geometry("800x600")
                    root.config(bg="white")  # 设置背景颜色为白色

                    # 创建顶部导航栏
                    create_top_bar(root)

                    # 创建主内容区域
                    main_frame = tkinter.Frame(root, bg="white")
                    main_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

                    canvas = tkinter.Canvas(main_frame, bg="white")
                    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

                    scrollbar = tkinter.Scrollbar(main_frame, command=canvas.yview)
                    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

                    canvas.configure(yscrollcommand=scrollbar.set)
                    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    content_frame = tkinter.Frame(canvas, bg="white")
                    canvas.create_window((0, 0), window=content_frame, anchor="nw")

                    # 创建内容部分
                    create_welcome_section(content_frame)
                    create_membership_details(content_frame)

                    # 创建客服功能部分
                    create_support_section(content_frame)

                    # 绑定鼠标滚轮事件
                    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                    root.mainloop()

                if __name__ == "__main__":
                    main()
            elif selected_option == "宗旨":
                def run_heart_animation():
                    CANVAS_WIDTH, CANVAS_HEIGHT = 640, 480
                    CANVAS_CENTER_X, CANVAS_CENTER_Y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2
                    IMAGE_ENLARGE = 11

                    def heart_function(t, shrink_ratio=IMAGE_ENLARGE):
                        x = 16 * (sin(t) ** 3)
                        y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
                        x *= shrink_ratio
                        y *= shrink_ratio
                        x += CANVAS_CENTER_X
                        y += CANVAS_CENTER_Y
                        return int(x), int(y)

                    def scatter_inside(x, y, beta=0.15):
                        ratio_x = - beta * log(random.random())
                        ratio_y = - beta * log(random.random())
                        dx = ratio_x * (x - CANVAS_CENTER_X)
                        dy = ratio_y * (y - CANVAS_CENTER_Y)
                        return x - dx, y - dy

                    def shrink(x, y, ratio):
                        force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
                        dx = ratio * force * (x - CANVAS_CENTER_X)
                        dy = ratio * force * (y - CANVAS_CENTER_Y)
                        return x - dx, y - dy

                    def curve(p):
                        return 2 * (2 * sin(4 * p)) / (2 * pi)

                    class Heart:
                        def __init__(self, generate_frame=20):
                            self._points = set()
                            self._edge_diffusion_points = set()
                            self._center_diffusion_points = set()
                            self.all_points = {}
                            self.build(2000)
                            self.random_halo = 1000
                            self.generate_frame = generate_frame
                            for frame in range(generate_frame):
                                self.calc(frame)

                        def build(self, number):
                            for _ in range(number):
                                t = random.uniform(0, 2 * pi)
                                x, y = heart_function(t)
                                self._points.add((x, y))
                            for _x, _y in list(self._points):
                                for _ in range(3):
                                    x, y = scatter_inside(_x, _y, 0.05)
                                    self._edge_diffusion_points.add((x, y))
                            point_list = list(self._points)
                            for _ in range(4000):
                                x, y = random.choice(point_list)
                                x, y = scatter_inside(x, y, 0.17)
                                self._center_diffusion_points.add((x, y))

                        @staticmethod
                        def calc_position(x, y, ratio):
                            force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
                            dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
                            dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
                            return x - dx, y - dy

                        def calc(self, generate_frame):
                            ratio = 10 * curve(generate_frame / 10 * pi)
                            halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
                            halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
                            all_points = []
                            heart_halo_point = set()
                            for _ in range(halo_number):
                                t = random.uniform(0, 2 * pi)
                                x, y = heart_function(t, shrink_ratio=11.6)
                                x, y = shrink(x, y, halo_radius)
                                if (x, y) not in heart_halo_point:
                                    heart_halo_point.add((x, y))
                                    x += random.randint(-14, 14)
                                    y += random.randint(-14, 14)
                                    size = random.choice((1, 2, 2))
                                    all_points.append((x, y, size))
                            for x, y in self._points:
                                x, y = self.calc_position(x, y, ratio)
                                size = random.randint(1, 3)
                                all_points.append((x, y, size))
                            for x, y in self._edge_diffusion_points:
                                x, y = self.calc_position(x, y, ratio)
                                size = random.randint(1, 2)
                                all_points.append((x, y, size))
                            for x, y in self._center_diffusion_points:
                                x, y = self.calc_position(x, y, ratio)
                                size = random.randint(1, 2)
                                all_points.append((x, y, size))
                            self.all_points[generate_frame] = all_points

                        def render(self, render_canvas, render_frame):
                            colors = ["#9400D3", "#FFFF00", "#FFC0CB", "#FF0000", "#FFA500", "#A52A2A"]
                            color_cycle_length = len(colors)
                            for x, y, size in self.all_points[render_frame % self.generate_frame]:
                                color_index = int((x / (CANVAS_WIDTH // color_cycle_length)) % color_cycle_length)
                                color = colors[color_index]
                                render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=color)

                    def draw_heart(frame=0):
                        canvas.delete('all')
                        heart.render(canvas, frame)
                        frame += 1
                        if frame < heart.generate_frame:
                            root.after(160, draw_heart, frame)
                        else:
                            root.after(160, draw_heart, 0)

                    root = tkinter.Tk()
                    root.iconbitmap('star.ico')
                    root.title("唤醒一颗五彩斑斓的心跳")
                    canvas = tkinter.Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
                    canvas.pack()
                    heart = Heart()
                    draw_heart()  # 直接调用draw_heart开始动画
                    root.mainloop()

                run_heart_animation()
        except IndexError:
            # 如果没有选中任何项目，则忽略
            pass

    # 绑定选择事件
    listbox.bind('<<ListboxSelect>>', show_license_info)


#搜索功能
def open_search():
    # 初始化搜索结果的链接列表
    links = []
    def search_baidu():
        key_word = entry.get()
        base_url = 'https://www.baidu.com/s'
        params = {'wd': key_word}

        url = base_url + '?' + urllib.parse.urlencode(params)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # 打印响应状态码和URL，确保请求成功
            print(f"请求成功，状态码: {response.status_code}, URL: {response.url}")

            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找搜索结果的所有链接
            global links
            links = []
            for result in soup.find_all('div', class_='c-container'):
                link_elem = result.find('a')
                if link_elem:
                    href = link_elem.get('href')
                    # 百度搜索结果中的链接可能需要处理成正确地跳转链接
                    if href and (href.startswith('http') or href.startswith('https')):
                        links.append(href)

            # 在主线程中更新文本框内容
            update_text_result()

        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

    def update_text_result():
        # 清空显示区域并显示搜索结果链接
        text_result.config(state=tkinter.NORMAL)  # 设置为可写入状态
        text_result.delete('1.0', tkinter.END)
        for idx, link in enumerate(links, start=1):
            text_result.insert(tkinter.END, f"{idx}. {link}\n")
        text_result.config(state=tkinter.DISABLED)  # 设置为不可写入状态

    def open_selected_link():
        # 获取用户输入的数字
        try:
            index = int(entry_select.get()) - 1
            if 0 <= index < len(links):
                webbrowser.open_new(links[index])
            else:
                print("无效的链接编号")
        except ValueError:
            print("请输入有效的数字")

    # 创建主窗口
    root = tkinter.Tk()
    root.iconbitmap('star.ico')
    root.title("百度搜索")

    # 创建输入框和按钮
    label = tkinter.Label(root, text="请输入搜索关键词：")
    label.pack(pady=10)

    entry = tkinter.Entry(root, width=50)
    entry.pack(pady=5)

    button_search = tkinter.Button(root, text="搜索", command=search_baidu)
    button_search.pack(pady=10)

    # 创建显示结果的文本框，设置为只读状态
    text_result = tkinter.Text(root, height=15, width=80)
    text_result.pack(padx=10, pady=10)
    text_result.config(state=tkinter.DISABLED)

    # 创建选择链接的输入框和按钮
    label_select = tkinter.Label(root, text="请输入链接编号：")
    label_select.pack(pady=10)

    entry_select = tkinter.Entry(root, width=10)
    entry_select.pack(pady=5)

    button_open = tkinter.Button(root, text="打开链接", command=open_selected_link)
    button_open.pack(pady=5)

    # 运行主程序
    root.mainloop()


# 初始化 pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Pygame and Mixer initialized in main thread")

# 高像素
root = tkinter.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor / 80)

# 窗口设置
root.attributes('-alpha', 1)
root.title('masterwork音樂播放機')
root.iconbitmap('star.ico')
root.geometry('920x1200+550+100')
root.resizable(False, False)

# 设置背景图片
canvas = tkinter.Canvas(root, width=920, height=1200, bd=0, highlightthickness=0)
imgpath = '1.jpg'
img = Image.open(imgpath)
img = img.resize((920, 1200), Image.LANCZOS)  # 使用 LANCZOS 进行抗锯齿处理
photo = ImageTk.PhotoImage(img)
canvas.create_image(460, 600, image=photo)  # 调整背景图片的位置，使其居中
canvas.pack()

folder = 'E:/Python-MP3/mp3'
res = []
num = 0  # 初始化为0
playing = False
play_thread = None  # 用于存储播放线程
play_lock = threading.Lock()  # 用于线程同步

# 全局变量
var2 = StringVar()
lb = None  # 列表框的引用
filtered_res = []  # 存储过滤后的歌曲列表
original_indices = {}  # 存储过滤后的索引到原始索引的映射


# 确保 pygame 和 mixer 在每个线程中初始化
def ensure_pygame_initialized():
    if not pygame.get_init():
        pygame.init()
        print("Pygame initialized in thread")
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        print("Mixer initialized in thread")


# 功能函数
def buttonaddClick():
    global folder, res, num, lb
    if folder:
        musics = [os.path.join(folder, music) for music in os.listdir(folder) if music.endswith('.mp3')]
        if not musics:
            print("沒有找到MP3文件")
            return
        res = musics
        ret = [os.path.basename(music)[:-4] for music in musics]
        var2.set(ret)
        if lb:
            lb.destroy()  # 如果列表框已经存在，先销毁它
        lb = tkinter.Listbox(root, listvariable=var2, background='SkyBlue', font=('Microsoft JhengHei', 16))
        lb.place(x=160, y=280, width=600, height=600)
        lb.bind('<<ListboxSelect>>', on_select)  # 绑定选择事件
        buttonPlay['state'] = 'normal'
        buttonStop['state'] = 'normal'
        pause_resume.set('播放')
        num = random.randint(0, len(res) - 1)  # 重新初始化num
        print(f"初始化 num 为 {num}")
        print(f"歌单: {res}")  # 打印歌单


def play():
    global num, playing
    ensure_pygame_initialized()
    while playing:
        with play_lock:
            if not pygame.mixer.music.get_busy():
                if 0 <= num < len(res):
                    nextMusic = res[num]
                    print(f"播放 {nextMusic.split('/')[-1][:-4]}，索引 {num}")  # 打印当前播放的音乐名称
                    try:
                        pygame.mixer.music.load(nextMusic)
                        pygame.mixer.music.play(1)
                        num = (num + 1) % len(res)  # 循环播放
                        nextMusic = nextMusic.split('/')[-1][:-4]
                        musicName.set('正在播放：' + nextMusic + '   ')
                    except pygame.error as e:
                        print(f"Error loading or playing music: {e}")
                else:
                    num = 0  # 重置num
            else:
                time.sleep(0.1)


def buttonPlayClick():
    global pause_resume, playing, play_thread
    buttonPre['state'] = 'normal'
    buttonNext['state'] = 'normal'
    if pause_resume.get() == '播放':
        pause_resume.set('暫停')
        playing = True
        if play_thread is None or not play_thread.is_alive():
            play_thread = threading.Thread(target=play)
            play_thread.start()
    elif pause_resume.get() == '暫停':
        playing = False
        pygame.mixer.music.pause()
        pause_resume.set('繼續')
    elif pause_resume.get() == '繼續':
        playing = True
        pygame.mixer.music.unpause()
        pause_resume.set('暫停')


def buttonStopClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    buttonPre['state'] = 'disabled'
    buttonNext['state'] = 'disabled'
    pause_resume.set('播放')


def buttonPreClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if num == 0:
        num = len(res) - 2
    else:
        num -= 2
    playing = True

    # 增加一个线程播放音乐
    t = threading.Thread(target=play)  # play函数    num+1
    t.start()
    if pause_resume.get() == '繼續':
        pause_resume.set('暫停')
    # 更新当前播放的音乐名称
    nextMusic = res[num].split('/')[-1][:-4]
    musicName.set('正在播放：' + nextMusic + '   ')
    print(f"播放 {nextMusic}，索引 {num}")  # 打印当前播放的音乐名称


def buttonNextClick():
    global playing
    playing = False
    pygame.mixer.music.stop()

    global num
    if len(res) - 1 == num:
        num = -1
    playing = True

    # 增加一个线程播放音乐
    t = threading.Thread(target=play)  # play函数   num+1
    t.start()
    if pause_resume.get() == '繼續':
        pause_resume.set('暫停')
    # 更新当前播放的音乐名称
    nextMusic = res[num].split('/')[-1][:-4]
    musicName.set('正在播放：' + nextMusic + '   ')
    print(f"播放 {nextMusic}，索引 {num}")  # 打印当前播放的音乐名称


def on_select(event):
    global num, playing, play_thread
    if lb and event:
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if filtered_res:
                num = original_indices.get(index, index)  # 映射回原始索引，如果不存在则使用当前索引
            else:
                num = index
            print(f"选择的歌曲索引: {num}")  # 打印选择的歌曲索引
            ensure_pygame_initialized()
            playing = False
            pygame.mixer.music.stop()
            playing = True
            pygame.mixer.music.rewind()  # 重置音乐播放器
            if play_thread is None or not play_thread.is_alive():
                play_thread = threading.Thread(target=play)
                play_thread.start()
            else:
                print("線程已存在，不再啟動新線程")
            pause_resume.set('暫停')  # 將播放按钮变为暂停按钮
            buttonPre['state'] = 'normal'
            buttonNext['state'] = 'normal'


def search_music():
    global filtered_res, original_indices
    query = search_var.get().lower()
    if not query:
        return
    filtered_res = [music for music in res if query in os.path.basename(music).lower()]
    if not filtered_res:
        print("没有找到匹配的歌曲")
        return
    ret = [os.path.basename(music)[:-4] for music in filtered_res]
    var2.set(ret)
    lb.selection_clear(0, tkinter.END)  # 清除当前选中的项目
    if filtered_res:
        lb.selection_set(0)  # 选中第一个搜索结果
        original_indices = {i: res.index(filtered_res[i]) for i in range(len(filtered_res))}  # 更新映射


def return_to_full_list():
    global filtered_res, original_indices
    var2.set([os.path.basename(music)[:-4] for music in res])
    lb.selection_clear(0, tkinter.END)  # 清除当前选中的项目
    num = random.randint(0, len(res) - 1)  # 重新初始化num
    filtered_res = []
    original_indices = {}


def END():
    try:
        if pygame.mixer.get_init():  # 检查 mixer 是否已经初始化
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    except Exception as e:
        print(f"Error stopping music: {e}")
    finally:
        # 确保无论如何都会关闭窗口
        root2.destroy()
        root.destroy()


def closeWindow():
    global root2
    root2 = tkinter.Toplevel(root)  # 使用 Toplevel 而不是 Tk
    root2.iconbitmap('star.ico')
    root2.title('masterwork音樂退出介面')
    root2.geometry('500x600+660+150')

    # 设置背景图片
    imgpath2 = '2.jpg'
    if not os.path.exists(imgpath2):
        print(f"图像文件 {imgpath2} 不存在")
        return

    img2 = Image.open(imgpath2)
    # 计算保持宽高比的尺寸
    img_width, img_height = img2.size
    aspect_ratio = img_width / img_height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    if new_height > 600:
        new_height = 600
        new_width = int(new_height * aspect_ratio)
    img2 = img2.resize((new_width, new_height), Image.LANCZOS)  # 使用 LANCZOS 进行抗锯齿处理
    photo2 = ImageTk.PhotoImage(img2)
    root2.photo2 = photo2  # 保持对图像的引用

    # 创建带有图片的画布
    canvas2 = tkinter.Canvas(root2, width=500, height=600, bd=0, highlightthickness=0)
    canvas2.create_image(250, 300, image=root2.photo2)  # 调整背景图片的位置，使其居中
    canvas2.pack()

    buttonStop = tkinter.Button(root2, text='關閉音樂', fg="white", bg="orange", command=END,
                                font=('Microsoft JhengHei', 16))
    buttonStop.place(x=175, y=450, width=150, height=70)

    root2.mainloop()


def contorlVoice(value):
    value = float(value)  # 将字符串转换为浮点数
    pygame.mixer.music.set_volume(value / 100)


# 搜索功能
search_var = tkinter.StringVar()
search_entry = tkinter.Entry(root, textvariable=search_var, font=('Microsoft JhengHei', 16))
search_entry.place(x=160, y=240, width=600, height=40)

# 搜索按钮
buttonSearch = tkinter.Button(root, text='搜索', command=search_music, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonSearch.place(x=770, y=240, width=100, height=40)


# 返回功能
def return_to_full_list():
    var2.set([os.path.basename(music)[:-4] for music in res])
    lb.selection_clear(0, tkinter.END)  # 清除当前选中的项目
    num = random.randint(0, len(res) - 1)  # 重新初始化num


#列表按钮
buttonNext = tkinter.Button(root, text='列表', command=open_options_window, bg='SkyBlue',
                            font=('Microsoft JhengHei', 16))
buttonNext.place(x=750, y=20, width=100, height=40)

# 返回按钮
buttonReturn = tkinter.Button(root, text='返回', command=return_to_full_list, bg='SkyBlue',
                              font=('Microsoft JhengHei', 16))
buttonReturn.place(x=160, y=900, width=100, height=40)

# 资源按钮
buttonReturn = tkinter.Button(root, text='资源', command=open_search, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonReturn.place(x=620, y=900, width=100, height=40)


# 关闭窗口
root.protocol('WM_DELETE_WINDOW', closeWindow)

# 添加歌单按钮
buttonadd = tkinter.Button(root, text='歌單', command=buttonaddClick, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonadd.place(x=160, y=20, width=100, height=40)

# 播放/暂停按钮
pause_resume = tkinter.StringVar(root, value='播放')
buttonPlay = tkinter.Button(root, textvariable=pause_resume, command=buttonPlayClick, bg='SkyBlue',
                            font=('Microsoft JhengHei', 16))
buttonPlay.place(x=280, y=20, width=100, height=40)
buttonPlay['state'] = 'disabled'

# 停止按钮
buttonStop = tkinter.Button(root, text='停止', command=buttonStopClick, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonStop.place(x=380, y=20, width=100, height=40)
buttonStop['state'] = 'disabled'

# 下一首按钮
buttonNext = tkinter.Button(root, text='下一首', command=buttonNextClick, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonNext.place(x=520, y=20, width=100, height=40)
buttonNext['state'] = 'disabled'

# 上一首按钮
buttonPre = tkinter.Button(root, text='上一首', command=buttonPreClick, bg='SkyBlue', font=('Microsoft JhengHei', 16))
buttonPre.place(x=620, y=20, width=100, height=40)
buttonPre['state'] = 'disabled'

# 当前播放的音乐名称
musicName = tkinter.StringVar(root, value="暫時沒有播放音樂...")
labelName = tkinter.Label(root, textvariable=musicName, fg="SeaGreen", bg='FloralWhite',
                          font=('Microsoft JhengHei', 16))
labelName.place(x=160, y=66, width=600, height=40)

# 音量控制滑块
s = tkinter.Scale(root, label='', bg='FloralWhite', fg="DeepSkyBlue", from_=0, to_=100, orient=tkinter.HORIZONTAL,
                  length=580, showvalue=0, tickinterval=25, resolution=0.1, command=contorlVoice,
                  font=('Microsoft JhengHei', 16))
s.place(x=160, y=104, width=600)

root.mainloop()
