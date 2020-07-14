# encoding:utf-8
from PIL import ImageGrab
import tkinter as tk
import os, time
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkfont
from shutil import copyfile
from shutil import rmtree
from shutil import copy
from webbrowser import open_new_tab

win = tk.Tk()

# 从配置文件读取数据

desk_path = os.path.join(os.path.expanduser('~'), "Desktop")

if not os.path.exists('笔记'):
    os.makedirs('笔记')

if not os.path.exists('笔记\\Config.cfg'):
    set_file = open('笔记\\Config.cfg', 'a+')
    setting_module = {

        "position": {
            "win": {
                'x': 200, 'y': 200
            },
        },

        "items": ["语文", "数学", "英语",
                  "物理", "化学", "生物",
                  "其他"],
        "checkbutton": {
            "cb1": 1,
            "cb2": 0,
            "cb3": 1,
        },
        "lastchoice": [0],
        "sleep": '0',
        "filetype": ".png",
        "transit": "0.0"
    }
    print(setting_module, file=set_file)
    set_file.close()
set_file = open('笔记\\Config.cfg')
file_info = set_file.read()
set_file.close()
try:
    set_info = eval(file_info)  # set_info ：配置文件内容
except SyntaxError:
    # os.remove(desk_path + '\\笔记\\noteshoter.ini')
    tk.messagebox.showerror('错误', '配置文件内容被更改，请尝试重新运行程序')
    os._exit(1)

# 全局变量
small_shot = 0
setting_win = 0
manage_win = 0
old_dir = ''
new_dir = ''

if not os.path.exists('笔记'):
    os.makedirs('笔记')


# 主要函数
def center(win_name, ww, wh):
    sw = win_name.winfo_screenwidth()
    sh = win_name.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (ww, wh, (sw - ww) / 2, (sh - wh) / 2)
    win_name.geometry(alignstr)
    win_name.resizable(0, 0)  # 可选，窗口大小不可变
    return


def beside(win_name, oldwin_name, old_w, new_w, new_h):
    """

    :param win_name: 新的窗口
    :param oldwin_name: 父窗口
    :param old_w: 父窗口宽
    :param new_w: 新窗口宽
    :param new_h: 新窗口高
    :return: 无返回值
    """
    sw = win_name.winfo_screenwidth()
    oldwin_x = oldwin_name.winfo_x()
    oldwin_y = oldwin_name.winfo_y()

    if (sw - (oldwin_x + old_w)) < new_w:
        size = '%sx%s+%s+%s' % (new_w, new_h, oldwin_x - new_w - 20, oldwin_y)
        win_name.geometry(size)
    if (sw - (oldwin_x + old_w)) > new_w:
        size = '%sx%s+%s+%s' % (new_w, new_h, oldwin_x + old_w + 20, oldwin_y)
        win_name.geometry(size)

    win_name.resizable(0, 0)  # 可选，窗口大小不可变
    return


def exit_fun():
    global set_info
    """保存关闭时的信息"""
    new_set_file = open('笔记\\Config.cfg', 'w')
    # 多选按钮
    set_info['checkbutton']['cb1'] = hidden_v.get()
    set_info['checkbutton']['cb2'] = tip_v.get()
    set_info['checkbutton']['cb3'] = top_v.get()
    # 延迟时间
    set_info['sleep'] = sleep_value.get()
    # win位置记录
    set_info['position']['win']['x'] = win.winfo_x()
    set_info['position']['win']['y'] = win.winfo_y()
    # 上次选择项目记录
    choice_item = str(subject_com.get())
    # 选择的文件格式记录
    set_info['filetype'] = ftype_value.get()
    # 过渡延迟记录
    set_info['transit'] = transit_value.get()
    try:
        choice_index = set_info['items'].index(choice_item)
        set_info['lastchoice'][0] = choice_index
        print(set_info, file=new_set_file)
        new_set_file.close()
    except ValueError:
        set_info['lastchoice'][0] = 0
        print(set_info, file=new_set_file)
        new_set_file.close()
    os._exit(1)


def time_get():
    data = time.time()
    timeArray = time.localtime(data)
    timestr = time.strftime('%Y-%m-%d-%H-%M-%S', timeArray)
    # rename_time = timestr.replace(' ', '-').replace(':', '-')

    return timestr


def shorttime():
    data = time.time()
    timeArray = time.localtime(data)
    st_time = time.strftime('%Y%m%d%H%M%S', timeArray)
    return st_time


def path_fun():
    subject = str(subject_com.get())
    save_path = '笔记\\{0}'.format(subject)
    return save_path


def delete_old():
    if not old_dir:
        tk.messagebox.showerror('错误', '暂时还没有上一张图片')
        return
    del_info = '您确定要删除"{0}"吗？'.format(old_dir)
    res = tk.messagebox.askyesno('删除', del_info)

    if res:
        try:
            os.remove(old_dir)
        except FileNotFoundError:
            tk.messagebox.showerror('错误', '未找到指定文件，可能文件已经被删除了')
    return


def save_old_dir(new):
    global old_dir
    global new_dir

    old_dir = new_dir
    new_dir = new
    return


def screenshot():
    if hidden_v.get() == 1:
        win.withdraw()
    time.sleep(int(sleep_value.get()))
    time.sleep(float(transit_value.get()))
    im = ImageGrab.grab()
    time_now = time_get()
    s_dir = path_fun()
    file = os.path.exists(s_dir)
    if file:
        save_name = s_dir + '\\' + time_now + ftype_value.get()
    else:
        os.makedirs(s_dir)
        save_name = s_dir + '\\' + time_now + ftype_value.get()
    im.save(save_name)

    if not small_shot == 1:
        win.deiconify()

    if tip_v.get() == 1:
        tips = '截图已保存为:\n' + save_name
        tk.messagebox.showinfo('完成', tips)
    save_old_dir(save_name)
    return


def top():
    res = top_v.get()
    if res == 1:
        win.wm_attributes('-topmost', 1)
    if res == 0:
        win.wm_attributes('-topmost', 0)
    return


def clip_save():
    cimage = ImageGrab.grabclipboard()  # 获取剪贴板文件
    s_dir = path_fun()
    time_now = shorttime()
    file = os.path.exists(s_dir)
    if file:
        save_name = s_dir + '\\' + "PrtScr" + time_now + ftype_value.get()
    else:
        os.makedirs(s_dir)
        save_name = s_dir + '\\' + "PrtScr" + time_now + ftype_value.get()

    try:
        cimage.save(save_name)
        save_old_dir(save_name)
    except AttributeError:
        tk.messagebox.showerror('错误', '剪切板没有图片可以粘贴。')
    return


def manage():
    global manage_win
    global set_info
    if manage_win == 1:
        tk.messagebox.showwarning('警告', '您已经打开了管理窗口，不可重复打开')
        return

    man_win = tk.Tk()
    # center(man_win, 300, 200)
    beside(man_win, win, 200, 300, 200)

    man_win.title('管理您的笔记截图')
    man_win.wm_attributes('-topmost', 1)
    if man_win:
        manage_win = 1

    tk.Label(man_win,
             text='截图列表：',
             fg='Indigo',
             font=('', 14)).place(x=20, y=0)

    tk.Label(man_win,
             text=subject_com.get(),
             fg='Green',
             font=('', 14)).place(x=150, y=0)
    # 获取截图列表
    subject = str(subject_com.get())
    walk_dir = '笔记\\{0}'.format(subject)
    note_tuple = os.walk(walk_dir)
    try:
        note_list = list(note_tuple)[0][2]
    except IndexError:
        tk.messagebox.showerror('错误', '未找到相应文件，文件可能还未被创建')
        man_win.destroy()
        return
    sb = Scrollbar(man_win)
    sb.pack(side=LEFT, ipady=100)
    lb = Listbox(man_win,
                 yscrollcommand=sb.set,
                 width=25)
    lb.place(x=20, y=20)
    sb.config(command=lb.yview)

    # 插入
    for i in range(0, len(note_list)):
        lb.insert(END, note_list[i])

    lb.see(END)

    # 函数
    def re_top():
        global manage_win
        manage_win = 0
        top()
        man_win.destroy()

    def delete():

        choice = str(lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        try:
            ask_tip = '您确定要删除{0}吗?'.format(lb.get(choice))
        except TclError:
            tk.messagebox.showerror('错误', '未选中任何项，不能删除')
            return
        res = tk.messagebox.askokcancel('删除？', ask_tip)

        if res is True:

            choice_abs_path = walk_dir + '\\' + lb.get(choice)
            try:
                os.remove(choice_abs_path)
            except FileNotFoundError:
                tk.messagebox.showerror('错误', '未找到指定文件，可能文件已经被删除了')
                lb.delete(choice)

            lb.delete(choice)
            # 判断是否删除成功
            if os.path.exists(choice_abs_path):
                tk.messagebox.showerror('错误', '删除失败')
            else:
                return
        man_win.mainloop()
        return

    def show(self):
        choice = str(lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        choice_abs_path = walk_dir + '\\' + lb.get(choice)
        try:
            f = open(choice_abs_path)
            f.close()
            os.system(choice_abs_path)

        except FileNotFoundError:
            tk.messagebox.showerror('错误', '未找到指定文件，可能文件已经被删除了')
            lb.delete(ACTIVE)

        return

    def open_file():
        cmd = 'start ' + walk_dir
        os.system(cmd)
        return

    def renew():
        nonlocal man_win
        global manage_win
        manage_win = 0
        man_win.destroy()
        manage()
        return

    def copy_pic():
        choice = str(lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        try:
            choice_abs_path = walk_dir + '\\' + lb.get(choice)
        except TclError:
            tk.messagebox.showerror('错误', '未选中任何项，不能另存为')
            return

        file = os.path.exists(choice_abs_path)
        if not file:
            tk.messagebox.showerror('错误', '未找到指定文件，可能文件已经被删除了')
            lb.delete(choice)
            return

        save_dir = filedialog.asksaveasfilename(title='保存位置以及图片名称',
                                                filetypes=[('图片', '')],
                                                initialdir=desk_path)
        if save_dir == '':
            tk.messagebox.showerror('错误', '没有选择保存位置或输入保存名称')
            return
        save_dir = save_dir + ftype_value.get()
        try:
            copyfile(choice_abs_path, save_dir)
            tk.messagebox.showinfo('笔记截图器', '保存成功')
            return
        except Exception:
            tk.messagebox.showerror('错误', '出现了未知的问题，导致截图未成功保存')
        return

    lb.bind('<Double-Button-1>', show)
    tk.Button(man_win,
              text='删   除',
              fg='Red',
              font=('', 11),
              width=10,
              command=delete,
              relief=RIDGE).place(x=204, y=20)
    tk.Button(man_win,
              text='打开文件夹',
              fg='Tomato',
              font=('', 11),
              width=10,
              command=open_file,
              relief=RIDGE).place(x=204, y=60)
    tk.Button(man_win,
              text='刷   新',
              fg='YellowGreen',
              font=('', 11),
              width=10,
              command=renew,
              relief=RIDGE).place(x=204, y=100)
    tk.Button(man_win,
              text='图片另存为',
              fg='DarkOrange',
              font=('', 11),
              width=10,
              command=copy_pic,
              relief=RIDGE).place(x=204, y=140)
    tk.Label(man_win,
             text='双击预览图片',
             fg='LightSkyBlue',
             font=('', 10)).place(x=207, y=180)

    man_win.protocol('WM_DELETE_WINDOW', re_top)
    man_win.mainloop()
    return


def setting():
    global setting_win
    if setting_win == 1:
        tk.messagebox.showwarning('警告', '您已经打开了设置窗口，不可重复打开')
        return
    set_win = tk.Tk()
    set_win.title('设置您的截图器')
    beside(set_win, win, 200, 320, 300)
    set_win.wm_attributes('-topmost', 1)
    if set_win:
        setting_win = 1

    def save_fun():

        global setting_win
        old_setting = eval(open('笔记\\Config.cfg').read())
        if old_setting != set_info:
            res = tk.messagebox.askokcancel('保存', '保存后重新启动程序，设置才会生效')
            if res:
                set_win.destroy()
                # print(setting_win, '保存了')
                exit_fun()

            else:
                return

        set_win.destroy()
        setting_win = 0
        return

    """科目的添加和删除"""
    sub_frame = Frame(set_win, width=20, height=50)
    sub_frame.place(x=5, y=5)

    tk.Label(sub_frame,
             text='项目设置',
             font=('', 15),
             fg='#006e54').pack(side=TOP)
    sub_sb = Scrollbar(sub_frame)
    sub_sb.pack(side=LEFT, ipady=70)
    sub_lb = Listbox(sub_frame,
                     yscrollcommand=sub_sb.set,
                     width=10)
    sub_lb.pack(side=RIGHT)
    sub_sb.config(command=sub_lb.yview)

    for i in range(0, len(set_info['items'])):
        sub_lb.insert(END, set_info['items'][i])

    def add_item():
        item = input_box.get()
        if not item:
            tk.messagebox.showwarning('警告', '要添加的项目名称不能为空')
            input_box.focus_force()
            return

        for index in range(0, len(set_info['items'])):
            if item == set_info['items'][index]:
                tk.messagebox.showwarning('警告', '新添加的项目名称不能与原有的项目名称相同')
                input_box.delete(0, 'end')
                return

        sub_lb.insert(END, item)
        set_info['items'].append(item)
        input_box.delete(0, 'end')
        sub_lb.see(END)
        return

    def delete_item():

        choice = str(sub_lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        try:
            ask_tip = '您确定要删除 "{0}" 吗?'.format(sub_lb.get(choice))
        except TclError:
            tk.messagebox.showerror('错误', '未选中任何项，不能删除')
            return
        res = tk.messagebox.askokcancel('删除？', ask_tip)
        if res:
            sub_lb.delete(choice)
            del set_info['items'][int(choice)]
            sub_lb.see(END)
        return

    my_item = StringVar()
    input_box = tk.Entry(set_win, textvariable=my_item, width=11)
    input_box.place(x=10, y=228)
    tk.Button(set_win,
              text='添加',
              fg='YellowGreen',
              relief=RIDGE,
              command=add_item).place(x=10, y=257)
    tk.Button(set_win,
              text='删除',
              fg='Red',
              relief=RIDGE,
              command=delete_item).place(x=55, y=257)

    """文件夹"""
    file_frame = Frame(set_win, width=10)
    file_frame.place(x=120, y=5)
    tk.Label(file_frame,
             text='文件夹',
             font=('', 15),
             fg='#2ca9e1').pack(side=TOP)

    # 获取文件夹内容
    walk_dir = '笔记'
    item_file = os.walk(walk_dir)

    try:
        item_list = list(item_file)[0][1]
        file_sb = Scrollbar(file_frame)
        file_sb.pack(side=LEFT, ipady=70)
        file_lb = Listbox(file_frame,
                          yscrollcommand=file_sb.set,
                          width=10)
        file_lb.pack(side=RIGHT)
        file_sb.config(command=file_lb.yview)

        for file_i in range(0, len(item_list)):
            file_lb.insert(END, item_list[file_i])

    except IndexError:
        tk.messagebox.showerror('错误', '未找到相应文件，文件可能还未被创建')

        setting_win = 0
        return

    def delete_file():
        choice = str(file_lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        try:
            ask_tip = '您确定要删除"{0}"文件夹以及其中的文件吗?'.format(file_lb.get(choice))
        except TclError:
            tk.messagebox.showerror('错误', '未选中任何项，不能删除')
            return
        res = tk.messagebox.askokcancel('删除？', ask_tip)
        if res:
            choice_file = walk_dir + '\\' + file_lb.get(choice)
            rmtree(choice_file)
            # print(choice_file)
            if os.path.exists(choice_file):
                tk.messagebox.showerror('错误', '文件夹未成功移除')

            file_lb.delete(choice)
        else:
            return
        return

    def open_file(self):
        choice = str(file_lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        choice_abs_path = walk_dir + '\\' + file_lb.get(choice)
        try:
            cmd = 'start ' + choice_abs_path
            os.system(cmd)

        except FileNotFoundError:
            tk.messagebox.showerror('错误', '未找到指定文件，可能文件已经被删除了')
            lb.delete(ACTIVE)
        return

    def file_save_as():
        coun = tk.messagebox.askokcancel('提醒', '此操作只会将所选文件夹中的文件另存为\n是否继续?')
        if not coun:
            return

        choice = str(file_lb.curselection())
        choice = ''.join([x for x in choice if x.isdigit()])
        try:
            choice_abs_path = walk_dir + '\\' + file_lb.get(choice)
        except TclError:
            tk.messagebox.showerror('错误', '没有选择文件，无法另存为')
            return
        new_save_dir = filedialog.askdirectory(title='保存位置',
                                               initialdir=desk_path)

        source_file_list = list(os.walk(choice_abs_path))[0][2]
        for pic_index in range(0, len(source_file_list)):
            pic_name = source_file_list[pic_index]
            source_path = choice_abs_path + '\\' + pic_name
            try:
                copy(source_path, new_save_dir)
            except FileNotFoundError:
                tk.messagebox.showerror('错误', '没有找到目标文件夹')
                return
        tk.messagebox.showinfo('完成', '成功另存为，共移动了{0}个文件'.format(len(source_file_list)))
        return

    tk.Button(set_win,
              text='删除文件夹',
              fg='Red',
              font=('', 11),
              relief=RIDGE,
              width=11,
              command=delete_file).place(x=215, y=50)
    tk.Button(set_win,
              text='文件夹另存为',
              fg='Orange',
              font=('', 11),
              relief=RIDGE,
              width=11,
              command=file_save_as).place(x=215, y=90)
    tk.Label(set_win,
             text='双击打开文件夹',
             fg='#007bbb').place(x=212, y=150)

    """缓存操作"""

    def clear_cache():
        if os.path.exists('笔记\\Config.cfg'):
            tk.messagebox.showwarning('警告', '缓存文件储存着您的一些设置以及您添加的项目，不推荐删除\n'
                                            '删除后程序的所有设置将恢复为缺省设置\n'
                                            '且下次运行程序时仍然会生成缓存文件')
            res = tk.messagebox.askokcancel('删除？', '您仍要删除吗？')
            if res:
                os.remove('笔记\\Config.cfg')
                tk.messagebox.showinfo('已删除', '删除成功，程序结束')
                os._exit(1)
        else:
            tk.messagebox.showerror('错误', '程序没有找到缓存文件,可能已经被删除了')
            os._exit(1)

        return

    cache_size = os.path.getsize('笔记\\Config.cfg') / 1024
    size_tip = '缓存占用了您的磁盘约{:.2f}KB的空间'.format(cache_size)
    tk.Label(set_win,
             text=size_tip,
             fg='#eb6101').place(x=100, y=228)
    tk.Button(set_win,
              text='清理缓存',
              fg='#4a488e',
              relief=RIDGE,
              command=clear_cache).place(x=170, y=257)
    file_lb.bind('<Double-Button-1>', open_file)

    set_win.protocol('WM_DELETE_WINDOW', save_fun)
    set_win.mainloop()
    return


def small():
    win.withdraw()
    mini = tk.Tk()
    mini.title('')
    bwin_x = win.winfo_x()
    bwin_y = win.winfo_y()
    if not bwin_x and not bwin_y:
        bwin_x = set_info['position']['win']['x']
        bwin_y = set_info['position']['win']['y']
    data = '180x35+%d+%d' % (bwin_x, bwin_y)
    mini.geometry(data)
    mini.resizable(0, 0)
    if top_v.get() == 1:
        mini.wm_attributes('-topmost', 1)
    else:
        mini.wm_attributes('-topmost', 0)
    ft = tkfont.Font(size=25, weight=tkfont.BOLD)

    def renormal():
        global small_shot
        small_shot = 0
        win.deiconify()
        sw = mini.winfo_screenwidth()
        winx = mini.winfo_x()
        winy = mini.winfo_y()
        if (winx + 150) > sw:
            re_data = '170x80+%s+%s' % ((sw - 200), winy)
        else:
            re_data = '170x80+%s+%s' % (winx, winy)
        win.geometry(re_data)
        mini.destroy()
        return

    def small_shot():
        if hidden_v.get() == 1:
            mini.withdraw()
        global small_shot
        small_shot = 1
        screenshot()
        mini.deiconify()
        return

    ttk.Button(mini,
               text='截图',
               width=10,
               command=small_shot).place(x=5, y=3)

    ttk.Button(mini,
               text='删除上一张',
               width=10,
               command=delete_old).place(x=95, y=3)

    mini.protocol('WM_DELETE_WINDOW', renormal)
    mini.mainloop()
    return


def error_exit():
    os.remove('笔记\\Config.cfg')
    tk.messagebox.showerror('错误', '配置文件内容被更改，请尝试重新运行程序')
    os._exit(1)
    return


def author():
    tk.messagebox.showinfo('关于作者', '作者的CSDN昵称：Temperature6\n\n'
                                   '作者的CSDN ID：qq_45413288')
    return


def open_web():
    open_new_tab('http://inews.gtimg.com/newsapp_ls/0/11592595688/0')
    return


def little_tip():
    """小提示"""
    """
    tk.messagebox.showinfo('提示', '(1)按下键盘上的PrintScreen键(也可能是PrtScr，依具体情况而定)\n'
                                 '可以在剪切板中存入一张全屏截图,'
                                 '使用"从剪切板粘贴"可以快速保存\n\n'
                                 '(2)保存为".bmp"文件时截图会更快\n\n'
                                 '(3)小窗口模式下的"Del Old"按键可删除上一张图片\n\n'
                                 '(4)此版本为Windows10 GUI适配版')
    """
    tip_win = tk.Tk()
    tip_win.title('小提示')
    center(tip_win, 800, 300)

    tk.Label(tip_win, text='(1)按下键盘上的PrintScreen键(也可能是PrtScr，依具体情况而定),'
                           '可以在剪切板中存入一张全屏截图,使用"从剪切板粘贴"可以快速保存').place(x=2, y=5)
    tk.Label(tip_win, text='(2)保存为".bmp"文件时截图会更快').place(x=2, y=35)
    tk.Label(tip_win, text='(3)小窗口模式下的"删除上一张"按钮或者"截图"菜单中的"删除上一张"'
                           '按钮可删除上一张图片').place(x=2, y=65)
    tk.Label(tip_win, text='(4)如果电脑系统在窗口消失时有过渡动画时间导致无法在截图时隐藏窗口,'
                           '可以适当在截图餐单-过渡延迟中适当调高过渡延迟').place(x=2, y=95)
    tk.Label(tip_win, text='(5)此版本为Windows10 GUI适配版').place(x=2, y=125)
    tip_win.mainloop()
    return


win.title('')
try:
    win_x = set_info['position']['win']['x']
    win_y = set_info['position']['win']['y']
    win_size = '%sx%s+%s+%s' % (170, 80, win_x, win_y)
    win.geometry(win_size)
    win.resizable(0, 0)
    tk.Label(win,
             text='项目:',
             font=('', 15),
             fg='YellowGreen').place(x=2, y=5)

    xVariable1 = tk.StringVar()
    subject_com = ttk.Combobox(win, textvariable=xVariable1, width=10)
    subject_com["value"] = set_info['items']
    subject_com.current(set_info['lastchoice'][0])
    subject_com.bind("<<ComboboxSelected>>")
    subject_com.place(x=60, y=5)

    menubar = tk.Menu(win)
    top_v = IntVar()
    top_v.set(int(set_info['checkbutton']['cb3']))
    programmenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="程序", menu=programmenu)
    programmenu.add_checkbutton(label='顶端显示', variable=top_v, onvalue=1, offvalue=0, command=top)
    programmenu.add_command(label="小窗口模式", command=small)
    programmenu.add_separator()
    programmenu.add_command(label="管理截图", command=manage)
    programmenu.add_command(label="设置", command=setting)
    programmenu.add_separator()
    programmenu.add_command(label="退出", command=exit_fun)
    shotmenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="截图", menu=shotmenu)
    shotmenu.add_command(label='从剪切板粘贴', command=clip_save)
    shotmenu.add_command(label='删除上一张', command=delete_old)
    shotmenu.add_separator()

    ftypemenu = tk.Menu(win, tearoff=False)
    ftype_value = StringVar()
    if set_info['filetype'] in ['.png', '.jpg', '.bmp']:
        ftype_value.set(set_info['filetype'])
    else:
        ftype_value.set(set_info['.png'])
    ftypemenu.add_radiobutton(label='jpg文件', variable=ftype_value, value=".jpg")
    ftypemenu.add_radiobutton(label='png文件', variable=ftype_value, value=".png")
    ftypemenu.add_radiobutton(label='bmp文件', variable=ftype_value, value=".bmp")
    shotmenu.add_cascade(label='文件格式', menu=ftypemenu)
    shotmenu.add_separator()
    sleepmenu = tk.Menu(win, tearoff=False)
    sleep_value = StringVar()
    if set_info['sleep'] in ['0', '1', '2', '3']:
        sleep_value.set(int(set_info['sleep']))
    else:
        sleep_value.set(0)
    sleepmenu.add_radiobutton(label='立刻截图', variable=sleep_value, value=0)
    sleepmenu.add_radiobutton(label='延迟1S截图', variable=sleep_value, value=1)
    sleepmenu.add_radiobutton(label='延迟2S截图', variable=sleep_value, value=2)
    sleepmenu.add_radiobutton(label='延迟3S截图', variable=sleep_value, value=3)
    shotmenu.add_cascade(label='截图延迟', menu=sleepmenu)
    transitmenu = tk.Menu(win, tearoff=False)
    transit_value = StringVar()
    if set_info['transit'] in ['0.0', '0.05', '0.1', '0.15', '0.2', '0.25', '0.3']:
        transit_value.set(set_info['transit'])
    else:
        transit_value.set("0.0")
    transitmenu.add_radiobutton(label='无过渡延迟', variable=transit_value, value='0.0')
    transitmenu.add_radiobutton(label='过渡延迟0.05秒', variable=transit_value, value='0.05')
    transitmenu.add_radiobutton(label='过渡延迟0.1秒', variable=transit_value, value='0.1')
    transitmenu.add_radiobutton(label='过渡延迟0.15秒', variable=transit_value, value='0.15')
    transitmenu.add_radiobutton(label='过渡延迟0.2秒', variable=transit_value, value='0.2')
    transitmenu.add_radiobutton(label='过渡延迟0.25秒', variable=transit_value, value='0.25')
    transitmenu.add_radiobutton(label='过渡延迟0.3秒', variable=transit_value, value='0.3')
    shotmenu.add_cascade(label="过渡延迟", menu=transitmenu)
    shotmenu.add_separator()
    tip_v = IntVar()
    if set_info['checkbutton']['cb2'] in [0, 1]:
        tip_v.set(set_info['checkbutton']['cb2'])
    shotmenu.add_checkbutton(label='总是提醒', variable=tip_v, onvalue=1, offvalue=0)
    hidden_v = IntVar()
    if set_info['checkbutton']['cb1'] in [0, 1]:
        hidden_v.set(set_info['checkbutton']['cb1'])
    shotmenu.add_checkbutton(label='截图时隐藏窗口', variable=hidden_v, onvalue=1, offvalue=0)
    aboutmenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="关于", menu=aboutmenu)
    aboutmenu.add_command(label='小技巧', command=little_tip)
    aboutmenu.add_command(label='作者', command=author)
    aboutmenu.add_command(label='支持作者', command=open_web)
    win.config(menu=menubar)

    ttk.Button(win,
               text='截     图',
               width=11,
               command=screenshot).place(x=40, y=40)

    # 判断是否顶端显示
    if top_v.get() == 1:
        win.wm_attributes('-topmost', 1)
    if top_v.get() == 0:
        win.wm_attributes('-topmost', 0)

except KeyError:
    # print('line759')
    error_exit()
except IndexError:
    # print('line762')
    error_exit()

win.protocol('WM_DELETE_WINDOW', exit_fun)

win.mainloop()
