"""
桌面截图工具主程序
提供桌面悬浮图标，点击后进行截图编辑并保存
"""
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import threading
import time
import os
import platform


class FloatingIcon:
    """桌面悬浮图标"""
    
    def __init__(self, root, on_click_callback):
        self.root = root
        self.on_click_callback = on_click_callback
        
        print("正在创建悬浮窗口...")
        
        # 创建悬浮窗口 - 暂时保留边框以便调试
        self.root.overrideredirect(False)  # 先保留边框
        self.root.attributes('-topmost', True)  # 窗口置顶
        self.root.attributes('-alpha', 0.9)  # 设置透明度
        
        # 计算屏幕中心位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 60) // 2
        y = (screen_height - 60) // 2
        
        # 设置窗口大小和位置（屏幕中央）
        self.root.geometry('60x60+{}+{}'.format(x, y))
        print(f"窗口位置: {x}, {y}")
        
        # 设置窗口标题（便于识别）
        self.root.title("截图工具")
        
        # 设置窗口背景
        self.root.config(bg='#007ACC')
        
        # 创建图标按钮
        self.canvas = tk.Canvas(root, width=60, height=60, 
                               bg='#007ACC', highlightthickness=0)
        self.canvas.pack()
        
        # 强制更新窗口显示
        self.root.update()
        print("悬浮窗口创建完成")
        
        # 绘制剪刀图标
        self._draw_icon()
        
        # 绑定点击事件
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        
        # 支持拖动
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        self.drag_start_x = 0
        self.drag_start_y = 0
    
    def _draw_icon(self):
        """绘制剪刀图标"""
        self.canvas.delete('all')
        # 绘制简单的剪刀图标
        self.canvas.create_oval(20, 10, 40, 30, fill='white', outline='white')
        self.canvas.create_line(30, 20, 45, 35, fill='white', width=3)
        self.canvas.create_line(30, 20, 30, 45, fill='white', width=3)
        self.canvas.create_line(30, 45, 15, 50, fill='white', width=3)
        self.canvas.create_oval(10, 45, 20, 55, fill='white', outline='white')
    
    def on_enter(self, event):
        """鼠标悬停效果"""
        self.canvas.config(bg='#005A9E')
        self._draw_icon()
    
    def on_leave(self, event):
        """鼠标离开效果"""
        self.canvas.config(bg='#007ACC')
        self._draw_icon()
    
    def start_drag(self, event):
        """开始拖动"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_drag(self, event):
        """拖动图标"""
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry('+{}+{}'.format(x, y))
    
    def on_click(self, event):
        """点击图标"""
        self.on_click_callback()


class ScreenshotEditor:
    """截图编辑器"""
    
    def __init__(self, root, on_save_callback):
        self.root = root
        self.on_save_callback = on_save_callback
        self.screenshot = None
        self.image = None
        self.drawing = False
        self.brush_color = 'red'
        self.brush_size = 3
        self.last_x = None
        self.last_y = None
        self.draw_objects = []
        self.current_tool = 'pen'  # pen, rectangle, text
        
        # 创建编辑器窗口
        self.editor_window = tk.Toplevel(root)
        self.editor_window.title("截图编辑器")
        self.editor_window.geometry('800x600')
        self.editor_window.withdraw()  # 先隐藏
        
        # 创建工具栏
        self._create_toolbar()
        
        # 创建画布
        self.canvas = tk.Canvas(self.editor_window, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定绘图事件
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.end_draw)
    
    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = tk.Frame(self.editor_window)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 工具选择
        tk.Label(toolbar, text="工具: ").pack(side=tk.LEFT)
        
        self.tool_var = tk.StringVar(value='pen')
        tools = [('画笔', 'pen'), ('矩形', 'rectangle'), ('文字', 'text')]
        for text, value in tools:
            rb = tk.Radiobutton(toolbar, text=text, variable=self.tool_var, 
                              value=value, indicatoron=0, width=8)
            rb.pack(side=tk.LEFT, padx=2)
        
        # 颜色选择
        tk.Label(toolbar, text="颜色: ").pack(side=tk.LEFT, padx=(20, 0))
        colors = ['red', 'blue', 'green', 'black', 'yellow']
        self.color_var = tk.StringVar(value='red')
        for color in colors:
            btn = tk.Button(toolbar, bg=color, width=3,
                          command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 笔刷大小
        tk.Label(toolbar, text="大小: ").pack(side=tk.LEFT, padx=(20, 0))
        self.size_scale = tk.Scale(toolbar, from_=1, to=20, orient=tk.HORIZONTAL)
        self.size_scale.set(3)
        self.size_scale.pack(side=tk.LEFT)
        
        # 操作按钮
        btn_frame = tk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="撤销", command=self.undo).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清空", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="保存", command=self.save, 
                 bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="重新截图", command=self.recapture,
                 bg='#f44336', fg='white').pack(side=tk.LEFT, padx=5)
    
    def set_color(self, color):
        """设置画笔颜色"""
        self.brush_color = color
    
    def start_draw(self, event):
        """开始绘图"""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.current_tool = self.tool_var.get()
        
        if self.current_tool == 'text':
            self._add_text(event.x, event.y)
    
    def draw(self, event):
        """绘图过程"""
        if not self.drawing:
            return
        
        if self.current_tool == 'pen':
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y,
                                   fill=self.brush_color,
                                   width=self.size_scale.get(),
                                   capstyle=tk.ROUND, smooth=True)
            self.last_x = x
            self.last_y = y
    
    def end_draw(self, event):
        """结束绘图"""
        if not self.drawing:
            return
        
        if self.current_tool == 'rectangle':
            x1, y1 = self.last_x, self.last_y
            x2, y2 = event.x, event.y
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                   outline=self.brush_color,
                                                   width=self.size_scale.get())
            self.draw_objects.append(rect_id)
        elif self.current_tool == 'pen':
            # 保存最后一段线的对象ID
            items = self.canvas.find_all()
            if items:
                self.draw_objects.append(items[-1])
        
        self.drawing = False
    
    def _add_text(self, x, y):
        """添加文字"""
        text = tk.simpledialog.askstring("添加文字", "请输入文字:")
        if text:
            text_id = self.canvas.create_text(x, y, text=text, 
                                             fill=self.brush_color,
                                             font=('Arial', self.size_scale.get() * 2))
            self.draw_objects.append(text_id)
    
    def undo(self):
        """撤销"""
        if self.draw_objects:
            item_id = self.draw_objects.pop()
            self.canvas.delete(item_id)
    
    def clear_all(self):
        """清空所有"""
        self.canvas.delete('all')
        self.draw_objects = []
    
    def load_screenshot(self, image):
        """加载截图到编辑器"""
        self.screenshot = image
        
        # 调整图像大小以适应画布
        canvas_width = 800
        canvas_height = 600
        img_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
        
        self.image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        
        # 清空画布并显示图像
        self.canvas.delete('all')
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # 显示编辑器窗口
        self.editor_window.deiconify()
    
    def recapture(self):
        """重新截图"""
        self.editor_window.withdraw()
        self.on_save_callback(recapture=True)
    
    def save(self):
        """保存截图"""
        # 获取文件保存路径
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), 
                      ("JPEG files", "*.jpg"), 
                      ("All files", "*.*")],
            title="保存截图"
        )
        
        if file_path:
            # 创建画布的副本并合并绘制内容
            result = self.image.copy()
            draw = ImageDraw.Draw(result)
            
            # 将画布上的绘制内容添加到图像上
            # 注意：这里简化处理，实际可能需要更复杂的转换
            # 如果需要精确的绘图保存，可以使用PIL的其他功能
            
            result.save(file_path)
            tk.messagebox.showinfo("成功", f"截图已保存到:\n{file_path}")
            
            self.editor_window.withdraw()


class ScreenCaptureWindow:
    """屏幕截图窗口"""
    
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        # 创建全屏窗口
        self.capture_window = tk.Toplevel(root)
        self.capture_window.attributes('-fullscreen', True)
        self.capture_window.attributes('-alpha', 0.3)
        self.capture_window.config(bg='black')
        self.capture_window.attributes('-topmost', True)
        
        # 创建画布用于绘制选区
        self.canvas = tk.Canvas(self.capture_window, bg='black',
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.capture_window.bind('<Escape>', lambda e: self.cancel())
        
        # 显示提示
        self.canvas.create_text(
            self.capture_window.winfo_screenwidth() // 2,
            self.capture_window.winfo_screenheight() // 2,
            text="拖动鼠标选择截图区域，按ESC取消",
            fill='white', font=('Arial', 16)
        )
    
    def on_mouse_down(self, event):
        """鼠标按下"""
        self.start_x = event.x
        self.start_y = event.y
    
    def on_mouse_drag(self, event):
        """鼠标拖动"""
        if self.start_x is None:
            return
        
        # 删除旧的矩形
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
        # 绘制新矩形
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )
    
    def on_mouse_up(self, event):
        """鼠标释放"""
        if self.start_x is None:
            return
        
        # 获取选区坐标
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        # 销毁截图窗口
        self.capture_window.destroy()
        
        # 执行截图
        if x2 - x1 > 10 and y2 - y1 > 10:  # 最小选区检查
            time.sleep(0.1)  # 等待窗口消失
            try:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                self.on_complete(screenshot, success=True)
            except Exception as e:
                print(f"截图失败: {e}")
                self.on_complete(None, success=False)
        else:
            self.on_complete(None, success=False)
    
    def cancel(self):
        """取消截图"""
        self.capture_window.destroy()
        self.on_complete(None, success=False)


class SnipTool:
    """截图工具主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        
        print("正在创建截图工具...")
        
        # 创建悬浮图标
        self.floating_icon = FloatingIcon(self.root, self.start_capture)
        
        # 显示窗口（重要！）
        self.root.deiconify()
        print("窗口已显示")
        
        # 创建编辑器
        self.editor = None
    
    def start_capture(self):
        """开始截图"""
        # 隐藏悬浮图标
        self.root.withdraw()
        
        # 创建截图窗口
        capture_window = ScreenCaptureWindow(self.root, self.on_capture_complete)
    
    def on_capture_complete(self, screenshot, success):
        """截图完成回调"""
        if success and screenshot:
            # 创建编辑器
            self.editor = ScreenshotEditor(self.root, self.on_save_complete)
            self.editor.load_screenshot(screenshot)
        else:
            # 重新显示悬浮图标
            self.root.deiconify()
    
    def on_save_complete(self, recapture=False):
        """保存完成回调"""
        # 关闭编辑器
        if self.editor:
            self.editor.editor_window.destroy()
        
        if recapture:
            # 重新截图
            self.start_capture()
        else:
            # 重新显示悬浮图标
            self.root.deiconify()
    
    def run(self):
        """运行程序"""
        self.root.mainloop()


def main():
    """主函数"""
    # 检查系统
    if platform.system() != 'Windows':
        print("警告: 此工具主要为 Windows 系统设计")
    
    # 创建并运行截图工具
    app = SnipTool()
    app.run()


if __name__ == '__main__':
    # 导入 tkinter.simpledialog 以支持文字输入
    import tkinter.simpledialog
    import tkinter.messagebox
    
    main()
