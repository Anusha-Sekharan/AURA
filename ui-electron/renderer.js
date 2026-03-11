const { ipcRenderer } = require('electron');

const widgetContainer = document.getElementById('widget-container');
const chatContainer = document.getElementById('chat-container');
const minimizeBtn = document.getElementById('minimize-btn');
const sendBtn = document.getElementById('send-btn');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');

// Backend Python API URL
const API_URL = 'http://127.0.0.1:5000/api/chat';

let isExpanded = false;

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
function toggleMode() {
    isExpanded = !isExpanded;

    if (isExpanded) {
        widgetContainer.style.display = 'none';
        chatContainer.style.display = 'flex';
        ipcRenderer.send('toggle-mode', true);
        chatInput.focus();
    } else {
        chatContainer.style.display = 'none';
        widgetContainer.style.display = 'flex';
        ipcRenderer.send('toggle-mode', false);
    }
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
widgetContainer.addEventListener('click', toggleMode);
minimizeBtn.addEventListener('click', toggleMode);

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
