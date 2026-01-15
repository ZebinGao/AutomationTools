class PomodoroTimer {
    constructor() {
        // 默认时间设置（毫秒）
        this.workTime = 25 * 60 * 1000; // 25分钟
        this.shortBreakTime = 5 * 60 * 1000; // 5分钟
        this.longBreakTime = 15 * 60 * 1000; // 15分钟
        
        // 当前状态
        this.currentTime = this.workTime;
        this.isRunning = false;
        this.currentMode = 'work'; // 'work', 'shortBreak', 'longBreak'
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
        
        // 初始化事件监听器
        this.initEventListeners();
        
        // 初始化显示
        this.updateDisplay();
    }
    
    initEventListeners() {
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        this.workModeBtn.addEventListener('click', () => this.setMode('work'));
        this.shortBreakModeBtn.addEventListener('click', () => this.setMode('shortBreak'));
        this.longBreakModeBtn.addEventListener('click', () => this.setMode('longBreak'));
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        
        const startTime = Date.now() - (this.workTime - this.currentTime);
        
        this.timer = setInterval(() => {
            this.currentTime = this.workTime - (Date.now() - startTime);
            
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
        
        switch (this.currentMode) {
            case 'work':
                this.currentTime = this.workTime;
                break;
            case 'shortBreak':
                this.currentTime = this.shortBreakTime;
                break;
            case 'longBreak':
                this.currentTime = this.longBreakTime;
                break;
        }
        
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
}

// 页面加载完成后初始化番茄钟
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
