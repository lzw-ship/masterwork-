import os
import tkinter as tk
from tkinter import Canvas, PhotoImage, Listbox, StringVar, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import time
import random
import threading
import pygame
import ctypes
import webbrowser
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tkinter import ttk
import json
import chardet
from docutils.nodes import image


def open_options_window():
    global root
    # 创建新的窗口
    options_window = tk.Toplevel(root)
    options_window.iconbitmap('E:/Music-Player/star.ico')
    options_window.title("选项")
    # 计算 options_window 的位置
    root.update_idletasks()  # 确保所有布局更新完成
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # 设置 options_window 的宽度和高度
    options_window_width = 200
    options_window_height = 200

    # 计算 options_window 的 x 和 y 坐标
    options_window_x = root_x + root_width
    options_window_y = root_y

    # 设置 options_window 的位置
    options_window.geometry(f"{options_window_width}x{options_window_height}+{options_window_x}+{options_window_y}")
    # 定义列表中的选项
    options = ["声明", "快捷键", "会员", "帮助"]

    # 创建列表框
    listbox = tk.Listbox(options_window)
    for option in options:
        listbox.insert(tk.END, option)

    # 将列表框放置在窗口中
    listbox.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # 添加选择事件处理，例如显示所选项目
    def show_license_info(event):
        # 获取当前选中的选项
        try:
            selected_option = listbox.get(listbox.curselection())
            if selected_option == "声明":
                def show_license():
                    # 创建一个新的窗口来显示条款信息
                    license_win = tk.Tk()
                    license_win.iconbitmap('E:/Music-Player/star.ico')
                    license_win.geometry("800x600+500+200")
                    license_win.title("用户需知")
                    license_win.configure(bg="#F5F5F5")  # 设置背景色

                    # 添加标题
                    title_label = ttk.Label(license_win, text="用户需知", font=("Arial", 16, "bold"),
                                            background="#F5F5F5")
                    title_label.pack(pady=10)

                    # 添加文本框来显示条款内容，并添加滚动条
                    text_frame = ttk.Frame(license_win, padding=10)
                    text_frame.pack(expand=True, fill='both')

                    text = tk.Text(text_frame, wrap='word', state='disabled', bg="#FFFFFF", fg="#333333",
                                   font=("Arial", 12))
                    text.grid(row=0, column=0, sticky='nsew')

                    scrollbar = ttk.Scrollbar(text_frame, command=text.yview, style='Custom.Vertical.TScrollbar')
                    scrollbar.grid(row=0, column=1, sticky='ns')

                    text['yscrollcommand'] = scrollbar.set

                    # 插入条款内容
                    terms = """
                        版权声明:
                        -----------------------------------
                        -----------------------------------


                        许可协议:
                        -----------------------------------
                        -----------------------------------


                        免责声明:
                        -----------------------------------
                        -----------------------------------


                        隐私条款:
                        -----------------------------------
                        -----------------------------------
                        """
                    text.config(state='normal')
                    text.insert('1.0', terms)
                    text.config(state='disabled')

                    # 调整文本框的布局
                    text_frame.grid_rowconfigure(0, weight=1)
                    text_frame.grid_columnconfigure(0, weight=1)

                    # 自定义滚动条样式
                    style = ttk.Style()
                    style.theme_use('clam')
                    style.configure('Custom.Vertical.TScrollbar', troughcolor='#E0E0E0', bordercolor='#F5F5F5',
                                    background='#A0A0A0', darkcolor='#A0A0A0', lightcolor='#A0A0A0', arrowcolor='white')

                    # 运行主循环
                    license_win.mainloop()

                if __name__ == "__main__":
                    show_license()
            elif selected_option == "快捷键":
                class ShortcutApp:
                    def __init__(self, root):
                        self.root = root
                        self.root.iconbitmap('E:/Music-Player/star.ico')
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
                        self.main_frame = tk.Frame(root)
                        self.main_frame.pack(padx=10, pady=10)

                        self.shortcuts_listbox = tk.Listbox(self.main_frame, width=50, height=15)
                        self.shortcuts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical")
                        self.scrollbar.config(command=self.shortcuts_listbox.yview)
                        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                        self.shortcuts_listbox.config(yscrollcommand=self.scrollbar.set)

                        self.update_listbox()

                        # 编辑按钮
                        self.edit_button = tk.Button(root, text="Edit Shortcut", command=self.modify_shortcut)
                        self.edit_button.pack(pady=5)

                    def load_shortcuts(self):
                        try:
                            with open('E:/Music-Player/shortcuts.json', 'rb') as f:
                                result = chardet.detect(f.read())
                                encoding = result['encoding']
                            with open('E:/Music-Player/shortcuts.json', 'r', encoding=encoding) as f:
                                self.shortcuts = json.load(f)
                        except FileNotFoundError:
                            self.save_shortcuts()  # 如果文件不存在，保存预定义的快捷键
                        except json.JSONDecodeError:
                            messagebox.showerror("Error", "The shortcuts.json file is not a valid JSON file.")
                            self.shortcuts = {}  # 清空快捷键字典

                    def save_shortcuts(self):
                        with open('E:/Music-Player/shortcuts.json', 'w', encoding='utf-8') as f:
                            json.dump(self.shortcuts, f, ensure_ascii=False, indent=4)

                    def update_listbox(self):
                        self.shortcuts_listbox.delete(0, tk.END)
                        for shortcut in self.shortcuts:
                            self.shortcuts_listbox.insert(tk.END, f"{shortcut} - {self.shortcuts[shortcut]}")

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
                    root = tk.Tk()
                    root.title("Shortcut Manager")

                    app = ShortcutApp(root)

                    root.mainloop()
            elif selected_option == "帮助":
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
                    style = ttk.Style()
                    style.theme_use('clam')  # 使用不同的主题
                    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25,
                                    fieldbackground="#D3D3D3")
                    style.map('Treeview', background=[('selected', '#A9A9A9')])

                    tree = ttk.Treeview(parent, columns=("Question", "Answer"), show="headings", height=20)
                    tree.heading("Question", text="问题")
                    tree.heading("Answer", text="回答")
                    tree.column("Question", width=350)  # 调整列宽
                    tree.column("Answer", width=350)
                    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky='nsew')

                    parent.grid_rowconfigure(1, weight=1)
                    parent.grid_columnconfigure(0, weight=1)

                    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
                    tree.configure(yscrollcommand=scrollbar.set)
                    scrollbar.grid(row=1, column=2, sticky='ns')
                    return tree

                def open_help_window():
                    help_window = tk.Tk()
                    help_window.iconbitmap('E:/Music-Player/star.ico')
                    help_window.title("解疑答惑")
                    help_window.geometry("800x600")
                    help_window.configure(bg="#D3D3D3")  # 设置背景色为灰色

                    # 创建搜索框
                    search_entry = ttk.Entry(help_window, width=40, font=('Arial', 12))
                    search_entry.grid(row=0, column=0, padx=10, pady=20, sticky=tk.W)
                    search_entry.insert(0, "搜索问题")
                    search_entry.bind("<FocusIn>", lambda event: search_entry.delete(0,
                                                                                     tk.END) if search_entry.get() == "搜索问题" else None)
                    search_entry.bind("<Return>", lambda event: search_questions(search_entry, questions_tree))

                    # 创建搜索按钮
                    search_button = ttk.Button(help_window, text="搜索",
                                               command=lambda: search_questions(search_entry, questions_tree),
                                               style='TButton')
                    search_button.grid(row=0, column=1, padx=10, pady=20, sticky=tk.W)

                    # 创建问题列表
                    global questions_tree
                    questions_tree = create_questions_treeview(help_window)

                    # 初始化显示所有问题和答案
                    for question, answer in questions:
                        questions_tree.insert("", "end", values=(question, answer))

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

                open_help_window()
                tk.mainloop()

            elif selected_option == "会员":
                def create_top_bar(root):
                    top_bar = tk.Frame(root, bg="#333333", height=10)
                    top_bar.pack(fill=tk.X)

                    logo_label = tk.Label(top_bar, text="Masterwork Music", fg="white", bg="#333333",
                                          font=("Arial", 16))
                    logo_label.pack(side=tk.LEFT, padx=10)

                    search_entry = tk.Entry(top_bar, width=10)
                    search_entry.pack(side=tk.LEFT, padx=10)

                def create_welcome_section(content_frame):
                    welcome_frame = tk.Frame(content_frame, pady=10, bg="white")
                    welcome_frame.pack(fill=tk.X, padx=10)

                    welcome_label = tk.Label(welcome_frame, text="你好，masterwork音樂用户！欢迎来到会员中心",
                                             font=("Arial", 14), bg="white")
                    welcome_label.pack()

                def create_membership_details(content_frame):
                    tkinter1 = tk
                    details_frame = tkinter1.Frame(content_frame, pady=10, bg="white")
                    details_frame.pack(fill=tkinter1.X, padx=10)

                    title_label = tkinter1.Label(details_frame, text="会员计划", font=("Arial", 16, "bold"), bg="white")
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
                    grid_frame = tkinter1.Frame(details_frame, bg="white")
                    grid_frame.pack(fill=tkinter1.X, padx=10, pady=10)

                    for i, membership in enumerate(membership_types):
                        type_frame = tkinter1.Frame(grid_frame, borderwidth=1, relief=tkinter1.SOLID, padx=10, pady=10,
                                                    bg="white")
                        type_frame.grid(row=0, column=i, padx=10, pady=10)

                        name_label = tkinter1.Label(type_frame, text=membership["name"], font=("Arial", 14, "bold"),
                                                    bg="white")
                        name_label.pack(anchor=tkinter1.W)

                        price_label = tkinter1.Label(type_frame, text=membership["price"], font=("Arial", 12),
                                                     bg="white")
                        price_label.pack(anchor=tkinter1.W)

                        description_label = tkinter1.Label(type_frame, text=membership["description"],
                                                           font=("Arial", 12), bg="white")
                        description_label.pack(anchor=tkinter1.W)

                        privileges_label = tkinter1.Label(type_frame, text="会员特权", font=("Arial", 12, "bold"),
                                                          bg="white")
                        privileges_label.pack(anchor=tkinter1.W, pady=5)

                        for privilege in membership["privileges"]:
                            label = tkinter1.Label(type_frame, text=f"{privilege['icon']} {privilege['text']}",
                                                   font=("Arial", 12),
                                                   bg="white")
                            label.pack(anchor=tkinter1.W)

                        subscribe_button = tkinter1.Button(type_frame, text="立即订阅",
                                                           command=lambda m=membership: subscribe_membership(m))
                        subscribe_button.pack(pady=5)

                def create_support_section(content_frame):
                    tkinter1 = tk
                    support_frame = tkinter1.Frame(content_frame, bg="white", padx=10, pady=10)
                    support_frame.pack(fill=tkinter1.X, padx=10, pady=10)

                    support_label = tkinter1.Label(support_frame, text="遇到问题？请联系我们",
                                                   font=("Arial", 14, "bold"),
                                                   bg="white")
                    support_label.pack(anchor=tkinter1.W, pady=10)

                    contact_button = tkinter1.Button(support_frame, text="联系客服", command=open_contact)
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
                    root = tk.Tk()
                    root.iconbitmap('E:/Music-Player/star.ico')
                    root.title("masterwork音樂会员中心")
                    root.geometry("800x600")
                    root.config(bg="white")  # 设置背景颜色为白色

                    # 创建顶部导航栏
                    create_top_bar(root)

                    # 创建主内容区域
                    main_frame = tk.Frame(root, bg="white")
                    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    canvas = tk.Canvas(main_frame, bg="white")
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    scrollbar = tk.Scrollbar(main_frame, command=canvas.yview)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                    canvas.configure(yscrollcommand=scrollbar.set)
                    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    content_frame = tk.Frame(canvas, bg="white")
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

        except IndexError:
            # 如果没有选中任何项目，则忽略
            pass

    # 绑定选择事件
    listbox.bind('<<ListboxSelect>>', show_license_info)


# 搜索功能
def open_search():
    # 从免费代理服务获取代理列表
    def fetch_proxies():
        try:
            response = requests.get('https://free-proxy-list.net/')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            proxies = []
            for row in soup.find('table', id='proxylisttable').find_all('tr')[1:]:
                cols = row.find_all('td')
                if cols:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    protocol = 'http' if cols[6].text.strip() == 'no' else 'https'
                    proxies.append(f'{protocol}://{ip}:{port}')
            return proxies
        except requests.exceptions.RequestException as e:
            print(f"获取代理列表失败: {e}")
            return []

    # 验证代理有效性
    def validate_proxy(proxy):
        try:
            response = requests.get('https://www.baidu.com/', proxies={'http': proxy, 'https': proxy}, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def search_baidu():
        key_word = entry.get()
        base_url = 'https://www.baidu.com/s'
        params = {'wd': key_word}

        url = base_url + '?' + urllib.parse.urlencode(params)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        max_retries = 3
        proxies = fetch_proxies()
        if not proxies:
            print("无法获取有效代理，尝试直接请求...")
            proxies = [None]  # 如果没有有效代理，直接请求

        for attempt in range(max_retries):
            proxy = random.choice(proxies) if proxies else None

            if proxy and not validate_proxy(proxy):
                print(f"代理 {proxy} 无效，尝试下一个代理...")
                continue

            try:
                response = requests.get(url, headers=headers,
                                        proxies={'http': proxy, 'https': proxy} if proxy else None)
                response.raise_for_status()

                # 模拟人类行为，增加请求间隔
                time.sleep(random.uniform(1, 3))

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
                        if href and (href.startswith('http') or href.startswith('https')):
                            links.append(href)

                # 在主线程中更新文本框内容
                update_text_result()
                break  # 请求成功，退出重试循环

            except requests.exceptions.RequestException as e:
                print(f"请求错误: {e}")
                if attempt < max_retries - 1:
                    print(f"尝试重新请求，剩余尝试次数: {max_retries - attempt - 1}")
            except Exception as e:
                print(f"未知错误: {e}")
                break

    def update_text_result():
        # 清空显示区域并显示搜索结果链接
        text_result.config(state=tk.NORMAL)  # 设置为可写入状态
        text_result.delete('1.0', tk.END)
        for idx, link in enumerate(links, start=1):
            text_result.insert(tk.END, f"{idx}. {link}\n")
        text_result.config(state=tk.DISABLED)  # 设置为不可写入状态

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
    root = tk.Tk()
    root.iconbitmap('E:/Music-Player/star.ico')
    root.title("百度搜索")

    # 创建输入框和按钮
    label = tk.Label(root, text="请输入搜索关键词：")
    label.pack(pady=10)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)

    button_search = tk.Button(root, text="搜索", command=search_baidu)
    button_search.pack(pady=10)

    # 创建显示结果的文本框，设置为只读状态
    text_result = tk.Text(root, height=15, width=80)
    text_result.pack(padx=10, pady=10)
    text_result.config(state=tk.DISABLED)

    # 创建选择链接的输入框和按钮
    label_select = tk.Label(root, text="请输入链接编号：")
    label_select.pack(pady=10)

    entry_select = tk.Entry(root, width=10)
    entry_select.pack(pady=5)

    button_open = tk.Button(root, text="打开链接", command=open_selected_link)
    button_open.pack(pady=5)

    # 运行主程序
    root.mainloop()


# 初始化 pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Pygame and Mixer initialized in main thread")

# 高像素
root = tk.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor / 80)

# 窗口设置
root.attributes('-alpha', 1)
root.title('masterwork音樂播放機')
root.iconbitmap('E:/Music-Player/star.ico')
root.geometry('920x1200+550+100')
root.resizable(False, False)

# 设置背景图片
canvas = tk.Canvas(root, width=920, height=1200, bd=0, highlightthickness=0)
imgpath = 'E:/Music-Player/4.jpeg'
img = Image.open(imgpath)
img = img.resize((920, 1200), Image.LANCZOS)  # 使用 LANCZOS 进行抗锯齿处理
photo = ImageTk.PhotoImage(img)
canvas.create_image(460, 600, image=photo)  # 调整背景图片的位置，使其居中
canvas.pack()

folder = 'E:/Music-Player/music'
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
        # 支持多种格式的音乐文件
        supported_formats = ('.mp3', '.wav', '.ogg', '.flac')
        musics = [os.path.join(folder, music) for music in os.listdir(folder) if
                  music.lower().endswith(supported_formats)]
        if not musics:
            print("沒有找到支持的音乐文件")
            return
        res = musics
        ret = [os.path.basename(music)[:-4] for music in musics]
        var2.set(ret)
        if lb:
            lb.destroy()  # 如果列表框已经存在，先销毁它
        lb = tk.Listbox(root, listvariable=var2, background='Linen', font=('Microsoft JhengHei', 16))
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
    lb.selection_clear(0, tk.END)  # 清除当前选中的项目
    if filtered_res:
        lb.selection_set(0)  # 选中第一个搜索结果
        original_indices = {i: res.index(filtered_res[i]) for i in range(len(filtered_res))}  # 更新映射


# 返回功能
def return_to_full_list():
    var2.set([os.path.basename(music)[:-4] for music in res])
    lb.selection_clear(0, tk.END)  # 清除当前选中的项目
    num = random.randint(0, len(res) - 1)  # 重新初始化num


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
    root2 = tk.Toplevel(root)  # 使用 Toplevel 而不是 Tk
    root2.iconbitmap('E:/Music-Player/star.ico')
    root2.title('masterwork音樂退出介面')
    root2.geometry('500x600+660+150')

    # 设置背景图片
    imgpath2 = 'E:/Music-Player/3.jpeg'
    if not os.path.exists(imgpath2):
        print(f"图像文件 {imgpath2} 不存在")
        return
    canvas2 = tk.Canvas(root2, width=500, height=600, bd=0, highlightthickness=0)
    img2 = Image.open(imgpath2)
    img2 = img2.resize((500, 600), Image.LANCZOS)  # 使用 LANCZOS 进行抗锯齿处理
    photo2 = ImageTk.PhotoImage(img2)
    canvas2.create_image(250, 300, image=photo2)  # 调整背景图片的位置，使其居中
    canvas2.pack()
    # 创建标签并放置在 Canvas 上
    label = tk.Label(root2, text="你确定要退出吗?", font=('宋体', 30), bg='Dark Slate Gray', fg='white')
    canvas2.create_window(250, 300, window=label)  # 将标签放置在 Canvas 的中央

    buttonStop = tk.Button(root2, text='關閉音樂', fg="white", bg="brown", command=END,
                           font=('Microsoft JhengHei', 16))
    buttonStop.place(x=175, y=450, width=110, height=45)

    root2.mainloop()


def contorlVoice(value):
    value = float(value)  # 将字符串转换为浮点数
    pygame.mixer.music.set_volume(value / 100)


# 搜索功能
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, font=('Microsoft JhengHei', 16))
search_entry.place(x=160, y=240, width=600, height=40)

# 加载图片并调整大小
try:
    image8 = Image.open("E:/Music-Player/搜索.png")
    # 调整图片大小，例如调整为 32x32 像素
    image8 = image8.resize((32, 32), Image.LANCZOS)
    photo8 = ImageTk.PhotoImage(image8)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/搜索.png")
    photo8 = None
# 搜索按钮
buttonSearch = tk.Button(root, image=photo8, command=search_music, bg='Light Salmon', font=('Microsoft JhengHei', 16))
buttonSearch.place(x=770, y=240, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonSearch.image = photo8

# 加载图片并调整大小
try:
    image2 = Image.open("E:/Music-Player/列表.png")
    # 调整图片大小，例如调整为 32x32 像素
    image2 = image2.resize((32, 32), Image.LANCZOS)
    photo2 = ImageTk.PhotoImage(image2)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/列表.png")
    photo2 = None
# 列表按钮
buttonwin = tk.Button(root, image=photo2, command=open_options_window, bg='brown',
                      font=('Microsoft JhengHei', 16))
buttonwin.place(x=750, y=20, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonwin.image = photo2

# 加载图片并调整大小
try:
    image3 = Image.open("E:/Music-Player/返回.png")
    # 调整图片大小，例如调整为 32x32 像素
    image3 = image3.resize((32, 32), Image.LANCZOS)
    photo3 = ImageTk.PhotoImage(image3)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/返回.png")
    photo3 = None
# 返回按钮
buttonReturn = tk.Button(root, image=photo3, command=return_to_full_list, bg='Dark Slate Gray',
                         font=('Microsoft JhengHei', 16))
buttonReturn.place(x=160, y=900, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonReturn.image = photo3

# 加载图片并调整大小
try:
    image7 = Image.open("E:/Music-Player/资源.png")
    # 调整图片大小，例如调整为 32x32 像素
    image7 = image7.resize((32, 32), Image.LANCZOS)
    photo7 = ImageTk.PhotoImage(image7)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/资源.png")
    photo7 = None
# 资源按钮
buttonopen = tk.Button(root, image=photo7, command=open_search, bg='Dark Slate Gray', font=('Microsoft JhengHei', 16))
buttonopen.place(x=620, y=900, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonopen.image = photo7

# 关闭窗口
root.protocol('WM_DELETE_WINDOW', closeWindow)

# 加载图片并调整大小
try:
    image6 = Image.打开("E:/Music-Player/歌单.png")
    # 调整图片大小，例如调整为 32x32 像素
    image6 = image6.resize((32, 32), Image.LANCZOS)
    photo6 = ImageTk.PhotoImage(image6)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/歌单.png")
    photo6 = None
# 添加歌单按钮
buttonadd = tk.Button(root, image=photo6, command=buttonaddClick, bg='Dark Slate Gray', font=('Microsoft JhengHei', 16))
buttonadd.place(x=390, y=900, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonadd.image = photo6

# 播放/暂停按钮
pause_resume = tk.StringVar(root, value='播放')
buttonPlay = tk.Button(root, textvariable=pause_resume, command=buttonPlayClick, bg='brown',
                       font=('Microsoft JhengHei', 16))
buttonPlay.place(x=330, y=20, width=100, height=40)
buttonPlay['state'] = 'disabled'

# 加载图片并调整大小
try:
    image9 = Image.打开("E:/Music-Player/停止.png")
    # 调整图片大小，例如调整为 32x32 像素
    image9 = image9.resize((32, 32), Image.LANCZOS)
    photo9 = ImageTk.PhotoImage(image9)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/停止.png")
    photo9 = None
# 停止按钮
buttonStop = tk.Button(root, image=photo9, command=buttonStopClick, bg='brown', font=('Microsoft JhengHei', 16))
buttonStop.place(x=450, y=20, width=100, height=40)
buttonStop['state'] = 'disabled'
# 保持对图像的引用，防止垃圾回收
buttonadd.image = photo9

# 加载图片并调整大小
try:
    image4 = Image.打开("E:/Music-Player/下一首.png")
    # 调整图片大小，例如调整为 32x32 像素
    image4 = image4.resize((32, 32), Image.LANCZOS)
    photo4 = ImageTk.PhotoImage(image4)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/下一首.png")
    photo4 = None
# 下一首按钮
buttonNext = tk.Button(root, image=photo4, command=buttonNextClick, bg='brown', font=('Microsoft JhengHei', 16))
buttonNext.place(x=620, y=20, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonNext.image = photo4
buttonNext['state'] = 'disabled'

# 加载图片并调整大小
try:
    image5 = Image.打开("E:/Music-Player/上一首.png")
    # 调整图片大小，例如调整为 32x32 像素
    image5 = image5.resize((32, 32), Image.LANCZOS)
    photo5 = ImageTk.PhotoImage(image5)
except FileNotFoundError:
    print("文件未找到: E:/Music-Player/上一首.png")
    photo5 = None
# 上一首按钮
buttonPre = tk.Button(root, image=photo5, command=buttonPreClick, bg='brown', font=('Microsoft JhengHei', 16))
buttonPre.place(x=170, y=20, width=100, height=40)
# 保持对图像的引用，防止垃圾回收
buttonPre.image = photo5
buttonPre['state'] = 'disabled'

# 当前播放的音乐名称
musicName = tk.StringVar(root, value="暫時沒有播放音樂...")
labelName = tk.标签(root, textvariable=musicName, fg="Cornsilk", bg='Light Salmon',
                     font=('Microsoft JhengHei', 16))
labelName.place(x=160, y=66, width=600, height=40)

# 音量控制滑块
s = tk.Scale(root, label='', bg='FloralWhite', fg="DeepSkyBlue", from_=0, to_=100, orient=tk.HORIZONTAL,
             length=580, showvalue=0, tickinterval=25, resolution=0.1, command=contorlVoice,
             font=('Microsoft JhengHei', 16))
s.place(x=160, y=104, width=600)

root.mainloop()
