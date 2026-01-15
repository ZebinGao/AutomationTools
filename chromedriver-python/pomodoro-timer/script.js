class PomodoroTimer {
    constructor() {
        // 默认时间设置（毫秒）
        this.defaultWorkTime = 25 * 60 * 1000; // 25分钟
        this.defaultShortBreakTime = 5 * 60 * 1000; // 5分钟
        this.defaultLongBreakTime = 15 * 60 * 1000; // 15分钟

        // 从localStorage加载或使用默认值
        this.workTime = parseInt(localStorage.getItem('pomodoroWorkTime')) * 60 * 1000 || this.defaultWorkTime;
        this.shortBreakTime = parseInt(localStorage.getItem('pomodoroShortBreakTime')) * 60 * 1000 || this.defaultShortBreakTime;
        this.longBreakTime = parseInt(localStorage.getItem('pomodoroLongBreakTime')) * 60 * 1000 || this.defaultLongBreakTime;
        
        // 当前状态
        this.currentMode = 'work'; // 'work', 'shortBreak', 'longBreak'
        this.currentTime = this.getModeTime(this.currentMode); // 初始化时使用当前模式的时间
        this.isRunning = false;
        this.sessionCount = 0;
        
        // 计时器变量
        this.timer = null;
        
        // DOM元素
        this.timeDisplay = document.getElementById('time');
        this.modeDisplay = document.getElementById('mode');
        this.startBtn = document.getElementById('start-btn');
        this.pauseBtn = document.getElementById('pause-btn');
        this.resetBtn = document.getElementById('reset-btn');
        this.countDisplay = document.getElementById('count');
        this.workModeBtn = document.getElementById('work-mode');
        this.shortBreakModeBtn = document.getElementById('short-break-mode');
        this.longBreakModeBtn = document.getElementById('long-break-mode');

        // 新增DOM元素
        this.themeToggleBtn = document.getElementById('theme-toggle');
        this.workTimeInput = document.getElementById('work-time');
        this.shortBreakTimeInput = document.getElementById('short-break-time');
        this.longBreakTimeInput = document.getElementById('long-break-time');
        this.saveSettingsBtn = document.getElementById('save-settings');
        
        // 初始化事件监听器
        this.initEventListeners();
        
        // 初始化显示
        this.loadSettings();
        this.updateDisplay();
        this.applyThemeFromLocalStorage();
    }
    
    initEventListeners() {
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        this.workModeBtn.addEventListener('click', () => this.setMode('work'));
        this.shortBreakModeBtn.addEventListener('click', () => this.setMode('shortBreak'));
        this.longBreakModeBtn.addEventListener('click', () => this.setMode('longBreak'));

        this.themeToggleBtn.addEventListener('click', () => this.toggleTheme());
        this.saveSettingsBtn.addEventListener('click', () => this.saveSettings());
    }

    getModeTime(mode) {
        switch (mode) {
            case 'work':
                return this.workTime;
            case 'shortBreak':
                return this.shortBreakTime;
            case 'longBreak':
                return this.longBreakTime;
            default:
                return this.workTime;
        }
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        
        const modeTime = this.getModeTime(this.currentMode);
        const startTime = Date.now() - (modeTime - this.currentTime);
        
        this.timer = setInterval(() => {
            this.currentTime = modeTime - (Date.now() - startTime);
            
            if (this.currentTime <= 0) {
                this.completeSession();
            } else {
                this.updateDisplay();
            }
        }, 1000);
    }
    
    pause() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        clearInterval(this.timer);
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
    }
    
    reset() {
        this.pause();
        this.currentTime = this.getModeTime(this.currentMode);
        this.updateDisplay();
    }
    
    setMode(mode) {
        this.pause();
        this.currentMode = mode;
        
        // 更新按钮状态
        this.workModeBtn.classList.remove('active');
        this.shortBreakModeBtn.classList.remove('active');
        this.longBreakModeBtn.classList.remove('active');
        
        switch (mode) {
            case 'work':
                this.currentTime = this.workTime;
                this.workModeBtn.classList.add('active');
                this.modeDisplay.textContent = '专注时间';
                this.modeDisplay.className = 'work-mode';
                break;
            case 'shortBreak':
                this.currentTime = this.shortBreakTime;
                this.shortBreakModeBtn.classList.add('active');
                this.modeDisplay.textContent = '短休息';
                this.modeDisplay.className = 'short-break-mode';
                break;
            case 'longBreak':
                this.currentTime = this.longBreakTime;
                this.longBreakModeBtn.classList.add('active');
                this.modeDisplay.textContent = '长休息';
                this.modeDisplay.className = 'long-break-mode';
                break;
        }
        
        this.updateDisplay();
    }
    
    completeSession() {
        this.pause();
        
        // 增加完成的番茄钟计数（仅在专注时间结束后）
        if (this.currentMode === 'work') {
            this.sessionCount++;
            this.countDisplay.textContent = this.sessionCount;
        }
        
        // 播放提示音
        this.playSound();
        
        // 显示通知
        this.showNotification();
        
        // 自动切换到下一个模式
        this.switchToNextMode();
    }
    
    switchToNextMode() {
        if (this.currentMode === 'work') {
            // 专注时间结束后，每4个番茄钟进行一次长休息，否则短休息
            if (this.sessionCount % 4 === 0) {
                this.setMode('longBreak');
            } else {
                this.setMode('shortBreak');
            }
        } else {
            // 休息时间结束后，回到专注时间
            this.setMode('work');
        }
        
        // 自动开始下一个计时
        setTimeout(() => this.start(), 2000);
    }
    
    playSound() {
        // 创建一个简单的提示音
        try {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = context.createOscillator();
            const gainNode = context.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(context.destination);
            
            oscillator.type = 'sine';
            oscillator.frequency.value = 800;
            gainNode.gain.value = 0.3;
            
            oscillator.start();
            
            setTimeout(() => {
                oscillator.stop();
            }, 1000);
        } catch (e) {
            console.log("无法播放提示音");
        }
    }
    
    showNotification() {
        if ("Notification" in window) {
            if (Notification.permission === "granted") {
                new Notification("番茄钟提醒", {
                    body: this.getNotificationMessage(),
                    icon: "favicon.ico"
                });
            } else if (Notification.permission !== "denied") {
                Notification.requestPermission().then(permission => {
                    if (permission === "granted") {
                        new Notification("番茄钟提醒", {
                            body: this.getNotificationMessage(),
                            icon: "favicon.ico"
                        });
                    }
                });
            }
        }
    }
    
    getNotificationMessage() {
        switch (this.currentMode) {
            case 'work':
                return "专注时间结束！该休息了。";
            case 'shortBreak':
                return "短休息结束！该开始新的专注时间了。";
            case 'longBreak':
                return "长休息结束！该开始新的专注时间了。";
            default:
                return "番茄钟时间结束！";
        }
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.currentTime / 60000);
        const seconds = Math.floor((this.currentTime % 60000) / 1000);
        
        // 格式化时间为 MM:SS
        const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        this.timeDisplay.textContent = formattedTime;
    }

    // 新增主题切换功能
    toggleTheme() {
        document.body.classList.toggle('dark-theme');
        const isDarkTheme = document.body.classList.contains('dark-theme');
        localStorage.setItem('pomodoroTheme', isDarkTheme ? 'dark' : 'light');
        this.themeToggleBtn.textContent = isDarkTheme ? '☀️' : '🌙';
    }

    applyThemeFromLocalStorage() {
        const savedTheme = localStorage.getItem('pomodoroTheme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            this.themeToggleBtn.textContent = '☀️';
        } else {
            document.body.classList.remove('dark-theme');
            this.themeToggleBtn.textContent = '🌙';
        }
    }

    // 新增时间设置功能
    loadSettings() {
        this.workTimeInput.value = this.workTime / 60000;
        this.shortBreakTimeInput.value = this.shortBreakTime / 60000;
        this.longBreakTimeInput.value = this.longBreakTime / 60000;
    }

    saveSettings() {
        const newWorkTime = parseInt(this.workTimeInput.value);
        const newShortBreakTime = parseInt(this.shortBreakTimeInput.value);
        const newLongBreakTime = parseInt(this.longBreakTimeInput.value);

        if (isNaN(newWorkTime) || newWorkTime <= 0 ||
            isNaN(newShortBreakTime) || newShortBreakTime <= 0 ||
            isNaN(newLongBreakTime) || newLongBreakTime <= 0) {
            alert("请输入有效的时间（大于0的整数）");
            return;
        }

        this.workTime = newWorkTime * 60 * 1000;
        this.shortBreakTime = newShortBreakTime * 60 * 1000;
        this.longBreakTime = newLongBreakTime * 60 * 1000;

        localStorage.setItem('pomodoroWorkTime', newWorkTime);
        localStorage.setItem('pomodoroShortBreakTime', newShortBreakTime);
        localStorage.setItem('pomodoroLongBreakTime', newLongBreakTime);

        alert("时间设置已保存！");
        this.reset(); // 保存设置后重置计时器
        this.setMode(this.currentMode); // 确保当前模式的时间更新
    }
}

// 页面加载完成后初始化番茄钟
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
