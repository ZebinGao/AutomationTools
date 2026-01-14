# WinAppDriver Web 控制台

这是一个基于 Flask 的 Web 应用程序，作为 WinAppDriver 的中间层，提供了一个直观的网页界面来控制 Windows 应用程序。

## 项目结构

``` 
web/
├── app.py                 # Flask 主应用
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── utils/                 # 工具函数
│   ├── __init__.py
│   ├── winappdriver.py    # WinAppDriver API 封装
│   └── image_utils.py     # 图像处理工具
├── static/                # 静态文件 (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/             # HTML 模板
```

## 功能特性

1. **会话管理**: 创建和销毁 WinAppDriver 会话
2. **截图功能**: 实时获取应用程序截图并压缩传输
3. **控件树查看**: 显示应用程序的 UI 控件树结构
4. **元素操作**: 查找、点击和输入文本到 UI 元素
5. **响应式界面**: 适配不同屏幕尺寸

## 安装和运行

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **配置 WinAppDriver**:
   - 确保 WinAppDriver 已安装并在默认端口 (4723) 运行
   - 或者修改 `config.py` 中的 `WINAPPDRIVER_URL` 设置

3. **运行应用**:
   ```bash
   python app.py
   ```

4. **访问界面**:
   - 打开浏览器访问 `http://localhost:5000`

## API 接口

### 会话管理
- `POST /api/session` - 创建新会话
- `DELETE /api/session/<session_id>` - 删除会话

### 屏幕操作
- `GET /api/session/<session_id>/screenshot` - 获取截图
- `GET /api/session/<session_id>/source` - 获取控件树

### 元素操作
- `POST /api/session/<session_id>/element` - 查找元素
- `POST /api/session/<session_id>/element/<element_id>/click` - 点击元素
- `POST /api/session/<session_id>/element/<element_id>/text` - 发送文本

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML, CSS, JavaScript
- **通信**: REST API
- **图像处理**: Pillow (Python Imaging Library)

## 开发指南

1. **修改配置**: 在 `config.py` 中调整应用设置
2. **扩展功能**: 在 `utils/winappdriver.py` 中添加新的 WinAppDriver 操作
3. **优化图像处理**: 在 `utils/image_utils.py` 中调整图像压缩算法
4. **更新界面**: 修改 `templates/index.html` 和 `static/css/style.css`

## 注意事项

1. 确保 WinAppDriver 服务正在运行
2. 应用程序路径需要是目标机器上的有效路径
3. 某些操作可能需要管理员权限
