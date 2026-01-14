// 全局变量
let sessionId = null;
let currentElementId = null;

// DOM 元素
const appPathInput = document.getElementById('appPath');
const startSessionBtn = document.getElementById('startSessionBtn');
const stopSessionBtn = document.getElementById('stopSessionBtn');
const refreshScreenshotBtn = document.getElementById('refreshScreenshotBtn');
const refreshSourceBtn = document.getElementById('refreshSourceBtn');
const elementStrategySelect = document.getElementById('elementStrategy');
const elementLocatorInput = document.getElementById('elementLocator');
const findElementBtn = document.getElementById('findElementBtn');
const clickElementBtn = document.getElementById('clickElementBtn');
const textInput = document.getElementById('textInput');
const sendTextBtn = document.getElementById('sendTextBtn');
const screenshotImg = document.getElementById('screenshot');
const loadingIndicator = document.getElementById('loadingIndicator');
const sourceTreeDiv = document.getElementById('sourceTree');

// 事件监听器
document.addEventListener('DOMContentLoaded', function() {
    startSessionBtn.addEventListener('click', startSession);
    stopSessionBtn.addEventListener('click', stopSession);
    refreshScreenshotBtn.addEventListener('click', refreshScreenshot);
    refreshSourceBtn.addEventListener('click', refreshSource);
    findElementBtn.addEventListener('click', findElement);
    clickElementBtn.addEventListener('click', clickElement);
    sendTextBtn.addEventListener('click', sendText);
});

// 启动会话
async function startSession() {
    const appPath = appPathInput.value.trim();
    
    if (!appPath) {
        alert('请输入应用程序路径');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ appPath: appPath })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            sessionId = data.sessionId;
            updateSessionControls(true);
            alert('会话启动成功');
            // 自动刷新截图和控件树
            await refreshScreenshot();
            await refreshSource();
        } else {
            throw new Error(data.error || '启动会话失败');
        }
    } catch (error) {
        console.error('启动会话失败:', error);
        alert('启动会话失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 停止会话
async function stopSession() {
    if (!sessionId) {
        alert('没有活动的会话');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            sessionId = null;
            currentElementId = null;
            updateSessionControls(false);
            clearScreenshot();
            clearSourceTree();
            alert('会话已停止');
        } else {
            throw new Error(data.error || '停止会话失败');
        }
    } catch (error) {
        console.error('停止会话失败:', error);
        alert('停止会话失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 刷新截图
async function refreshScreenshot() {
    if (!sessionId) {
        alert('请先启动会话');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}/screenshot`);
        const data = await response.json();
        
        if (response.ok) {
            // 显示截图
            screenshotImg.src = `data:image/jpeg;base64,${data.screenshot}`;
        } else {
            throw new Error(data.error || '获取截图失败');
        }
    } catch (error) {
        console.error('获取截图失败:', error);
        alert('获取截图失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 刷新控件树
async function refreshSource() {
    if (!sessionId) {
        alert('请先启动会话');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}/source`);
        const data = await response.json();
        
        if (response.ok) {
            // 显示控件树sourceTreeDiv.innerHTML = `<pre>${formatXml(data.source)}</pre>`;
            const rawxml = data.source;
            const formattedXml = formatXml(rawxml);
            sourceTreeDiv.textContent = formattedXml;
        } else {
            throw new Error(data.error || '获取控件树失败');
        }
    } catch (error) {
        console.error('获取控件树失败:', error);
        alert('获取控件树失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 查找元素
async function findElement() {
    if (!sessionId) {
        alert('请先启动会话');
        return;
    }
    
    const strategy = elementStrategySelect.value;
    const locator = elementLocatorInput.value.trim();
    
    if (!locator) {
        alert('请输入定位器');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}/element`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                strategy: strategy,
                locator: locator
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentElementId = data.elementId;
            updateElementControls(true);
            alert(`元素查找成功，ID: ${currentElementId}`);
        } else {
            throw new Error(data.error || '查找元素失败');
        }
    } catch (error) {
        console.error('查找元素失败:', error);
        alert('查找元素失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 点击元素
async function clickElement() {
    if (!sessionId || !currentElementId) {
        alert('请先查找元素');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}/element/${currentElementId}/click`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('元素点击成功');
            // 刷新截图以显示变化
            await refreshScreenshot();
        } else {
            throw new Error(data.error || '点击元素失败');
        }
    } catch (error) {
        console.error('点击元素失败:', error);
        alert('点击元素失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 发送文本
async function sendText() {
    if (!sessionId || !currentElementId) {
        alert('请先查找元素');
        return;
    }
    
    const text = textInput.value;
    
    if (text === undefined) {
        alert('请输入要发送的文本');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/session/${sessionId}/element/${currentElementId}/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('文本发送成功');
            // 清空文本输入框
            textInput.value = '';
            // 刷新截图以显示变化
            await refreshScreenshot();
        } else {
            throw new Error(data.error || '发送文本失败');
        }
    } catch (error) {
        console.error('发送文本失败:', error);
        alert('发送文本失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 更新会话控制按钮状态
function updateSessionControls(active) {
    startSessionBtn.disabled = active;
    stopSessionBtn.disabled = !active;
    refreshScreenshotBtn.disabled = !active;
    refreshSourceBtn.disabled = !active;
    findElementBtn.disabled = !active;
}

// 更新元素控制按钮状态
function updateElementControls(enabled) {
    clickElementBtn.disabled = !enabled;
    sendTextBtn.disabled = !enabled;
}

// 显示/隐藏加载指示器
function showLoading(show) {
    if (show) {
        loadingIndicator.classList.remove('hidden');
    } else {
        loadingIndicator.classList.add('hidden');
    }
}

// 清除截图
function clearScreenshot() {
    screenshotImg.src = '';
}

// 清除控件树
function clearSourceTree() {
    sourceTreeDiv.innerHTML = '<p>尚未加载控件树</p>';
}

// 格式化 XML
function formatXml(xml) {
    try {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xml, "text/xml");
        // --- 新增：过滤属性的逻辑 ---
        const allowedAttrs = ['ClassName', 'RuntimeId', 'Name'];
        
        // 递归遍历所有节点
        const walk = (node) => {
            if (node.attributes) {
                // 将属性名转为数组进行遍历，因为直接删除属性会影响循环
                const attrs = Array.from(node.attributes);
                for (const attr of attrs) {
                    if (!allowedAttrs.includes(attr.name)) {
                        node.removeAttribute(attr.name);
                    }
                }
            }
            node.childNodes.forEach(walk);
        };
        walk(xmlDoc.documentElement);
        // -----------------------

        const serializer = new XMLSerializer();
        const formatted = serializer.serializeToString(xmlDoc);
        
        // 以下为你原有的缩进逻辑
        let indent = 0;
        let result = '';
        // 移除多余空白并分割标签
        const lines = formatted.replace(/>\s*</g, '><').split(/>(?=<)/);
        
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            if (!line.startsWith('<')) line = '<' + line;
            if (!line.endsWith('>')) line = line + '>';

            // 匹配闭合标签 </Tag>
            if (line.match(/^<\//)) {
                indent--;
            }
            
            result += '  '.repeat(Math.max(0, indent)) + line + '\n';
            
            // 匹配起始标签 <Tag> 且不是自闭合标签 <Tag/>
            if (line.match(/^<[^/!][^>]*[^/]>$/)) {
                indent++;
            }
        }
        
        return result.trim();
    } catch (e) {
        // 如果格式化失败，返回原始 XML
        return xml;
    }
}
