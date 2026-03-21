const { ipcRenderer } = require('electron');

const widgetContainer = document.getElementById('widget-container');
const sphereCanvas = document.getElementById('sphere-canvas');
const chatContainer = document.getElementById('chat-container');
const minimizeBtn = document.getElementById('minimize-btn');
const closeBtn = document.getElementById('close-btn');
const sendBtn = document.getElementById('send-btn');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');

// Backend Python API URL
const API_URL = 'http://127.0.0.1:5000/api/chat';

let isExpanded = false;
let isDraggingWidget = false;
let suppressNextWidgetClick = false;
let widgetDragStart = {
    mouseX: 0,
    mouseY: 0,
    windowX: 0,
    windowY: 0
};

function initializeParticleSphere() {
    if (!sphereCanvas) {
        return;
    }

    const context = sphereCanvas.getContext('2d');
    if (!context) {
        return;
    }

    const pointCount = 220;
    const sphereRadius = 48;
    const focalLength = 180;
    const sphereSpinSpeedY = 0.0065;
    const sphereSpinSpeedX = 0.0006;
    const points = [];

    for (let index = 0; index < pointCount; index += 1) {
        const u = Math.random();
        const v = Math.random();
        const theta = 2 * Math.PI * u;
        const phi = Math.acos((2 * v) - 1);
        const sinPhi = Math.sin(phi);

        points.push({
            x: sphereRadius * sinPhi * Math.cos(theta),
            y: sphereRadius * sinPhi * Math.sin(theta),
            z: sphereRadius * Math.cos(phi)
        });
    }

    function resizeCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const rect = sphereCanvas.getBoundingClientRect();

        sphereCanvas.width = Math.max(1, Math.floor(rect.width * dpr));
        sphereCanvas.height = Math.max(1, Math.floor(rect.height * dpr));
        context.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    let rotationY = 0;
    let rotationX = 0.45;

    function renderFrame() {
        const width = sphereCanvas.clientWidth;
        const height = sphereCanvas.clientHeight;
        const centerX = width / 2;
        const centerY = height / 2;

        context.clearRect(0, 0, width, height);

        const glowGradient = context.createRadialGradient(
            centerX + 10,
            centerY - 8,
            8,
            centerX,
            centerY,
            sphereRadius + 30
        );
        glowGradient.addColorStop(0, 'rgba(120, 170, 255, 0.32)');
        glowGradient.addColorStop(0.62, 'rgba(40, 70, 120, 0.18)');
        glowGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

        context.fillStyle = glowGradient;
        context.beginPath();
        context.arc(centerX, centerY, sphereRadius + 30, 0, Math.PI * 2);
        context.fill();

        const coreGradient = context.createRadialGradient(
            centerX - 9,
            centerY - 11,
            1,
            centerX,
            centerY,
            sphereRadius + 6
        );
        coreGradient.addColorStop(0, 'rgba(50, 78, 140, 0.28)');
        coreGradient.addColorStop(0.42, 'rgba(16, 28, 56, 0.58)');
        coreGradient.addColorStop(1, 'rgba(4, 8, 18, 0.80)');

        context.beginPath();
        context.arc(centerX, centerY, sphereRadius + 1, 0, Math.PI * 2);
        context.fillStyle = coreGradient;
        context.fill();

        const cosY = Math.cos(rotationY);
        const sinY = Math.sin(rotationY);
        const cosX = Math.cos(rotationX);
        const sinX = Math.sin(rotationX);

        const projectedPoints = [];
        for (const point of points) {
            const rotatedX = point.x * cosY - point.z * sinY;
            const rotatedZAfterY = point.x * sinY + point.z * cosY;
            const rotatedY = point.y * cosX - rotatedZAfterY * sinX;
            const rotatedZ = point.y * sinX + rotatedZAfterY * cosX;

            const perspective = focalLength / (focalLength + rotatedZ + sphereRadius);
            const drawX = centerX + (rotatedX * perspective);
            const drawY = centerY + (rotatedY * perspective);

            const depthRatio = (rotatedZ + sphereRadius) / (sphereRadius * 2);
            projectedPoints.push({
                drawX,
                drawY,
                rotatedZ,
                alpha: 0.38 + (0.62 * depthRatio),
                size: 0.6 + (1.65 * perspective)
            });
        }

        projectedPoints.sort((left, right) => left.rotatedZ - right.rotatedZ);

        for (const point of projectedPoints) {
            context.beginPath();
            context.arc(point.drawX, point.drawY, point.size, 0, Math.PI * 2);
            context.fillStyle = `rgba(255, 255, 255, ${point.alpha.toFixed(3)})`;
            context.shadowColor = 'rgba(170, 210, 255, 0.55)';
            context.shadowBlur = 5;
            context.fill();
        }

        context.shadowBlur = 0;

        rotationY += sphereSpinSpeedY;
        rotationX += sphereSpinSpeedX;

        requestAnimationFrame(renderFrame);
    }

    renderFrame();
}

// Append a message to the chat UI
function appendMessage(sender, text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');

    if (type === 'user') {
        msgDiv.classList.add('msg-user');
    } else if (type === 'aura') {
        msgDiv.classList.add('msg-aura');
    } else if (type === 'system') {
        msgDiv.classList.add('msg-system');
    } else if (type === 'error') {
        msgDiv.classList.add('msg-error');
    }

    // Bold sender prefix
    const strong = document.createElement('strong');
    strong.innerText = `${sender}: `;

    const span = document.createElement('span');
    span.innerText = text;

    msgDiv.appendChild(strong);
    msgDiv.appendChild(span);

    chatHistory.appendChild(msgDiv);

    // Auto-scroll
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Toggle logic
function expandToChat() {
    isExpanded = true;
    widgetContainer.style.display = 'none';
    chatContainer.style.display = 'flex';
    ipcRenderer.send('toggle-mode', true);
    chatInput.focus();
}

function collapseToWidget() {
    isExpanded = false;
    chatContainer.style.display = 'none';
    widgetContainer.style.display = 'flex';

    // Resume particle sphere rendering by ensuring it knows it's visible
    // (Render frame is already looping, but visibility might have been an issue)

    // Re-enable mouse events immediately so the widget is clickable right away
    ipcRenderer.send('set-ignore-mouse-events', false);
    ipcRenderer.send('toggle-mode', false);
}

function toggleMode() {
    if (isExpanded) {
        collapseToWidget();
    } else {
        expandToChat();
    }
}

function onWidgetMouseDown(event) {
    if (isExpanded || event.button !== 0) {
        return;
    }

    isDraggingWidget = true;
    widgetContainer.classList.add('dragging');

    widgetDragStart = {
        mouseX: event.screenX,
        mouseY: event.screenY,
        windowX: window.screenX,
        windowY: window.screenY
    };

    document.addEventListener('mousemove', onWidgetMouseMove);
    document.addEventListener('mouseup', onWidgetMouseUp);
}

function onWidgetMouseMove(event) {
    if (!isDraggingWidget) {
        return;
    }

    const deltaX = event.screenX - widgetDragStart.mouseX;
    const deltaY = event.screenY - widgetDragStart.mouseY;

    if (Math.abs(deltaX) > 2 || Math.abs(deltaY) > 2) {
        suppressNextWidgetClick = true;
    }

    ipcRenderer.send(
        'set-window-position',
        widgetDragStart.windowX + deltaX,
        widgetDragStart.windowY + deltaY
    );
}

function onWidgetMouseUp() {
    isDraggingWidget = false;
    widgetContainer.classList.remove('dragging');
    document.removeEventListener('mousemove', onWidgetMouseMove);
    document.removeEventListener('mouseup', onWidgetMouseUp);
}

function onWidgetClick() {
    if (suppressNextWidgetClick) {
        suppressNextWidgetClick = false;
        return;
    }

    toggleMode();
}

// Ensure the widget container handles mouse events (overriding transparent ignore behavior from Main process)
widgetContainer.addEventListener('mouseenter', () => {
    ipcRenderer.send('set-ignore-mouse-events', false);
});

widgetContainer.addEventListener('mouseleave', () => {
    // Only go back to transparent mode if we aren't expanded
    if (!isExpanded) {
        ipcRenderer.send('set-ignore-mouse-events', true, { forward: true });
    }
});

// Click handlers
widgetContainer.addEventListener('mousedown', onWidgetMouseDown);
widgetContainer.addEventListener('click', onWidgetClick);
minimizeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    collapseToWidget();
});
if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        collapseToWidget();
    });
}
ipcRenderer.on('force-collapse', () => {
    collapseToWidget();
});

// Submit chat handlers
async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = '';
    appendMessage('You', text, 'user');

    if (text.toLowerCase() === 'exit' || text.toLowerCase() === 'quit') {
        appendMessage('Aura', 'Shutting down UI...', 'aura');
        setTimeout(() => ipcRenderer.send('quit-app'), 1500);
        return;
    }

    if (text.toLowerCase() === 'close' || text.toLowerCase() === 'minimize' || text.toLowerCase() === 'hide') {
        collapseToWidget();
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.response) {
            appendMessage('Aura', data.response, 'aura');
        }

        if (data.action_result) {
            appendMessage('System', data.action_result, 'system');
        }

    } catch (err) {
        appendMessage('Error', 'Failed to connect to Python backend: ' + err.message, 'error');
    }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Intro message
appendMessage('System', 'Aura UI online. Connecting to internal brain...', 'system');

initializeParticleSphere();
