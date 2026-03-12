const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');

let mainWindow;
let lastWidgetPosition;

function createWindow() {
    const primaryDisplay = screen.getPrimaryDisplay();
    const { width, height } = primaryDisplay.workAreaSize;

    const widgetSize = 150;
    const initialX = width - widgetSize - 20;
    const initialY = height - widgetSize - 20;

    lastWidgetPosition = { x: initialX, y: initialY };

    mainWindow = new BrowserWindow({
        width: widgetSize,
        height: widgetSize,
        x: initialX,
        y: initialY,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');

    // Make the window ignore mouse events where the pixel is transparent
    mainWindow.setIgnoreMouseEvents(true, { forward: true });

    // IPC to toggle window size for chat mode
    ipcMain.on('toggle-mode', (event, isExpanded) => {
        if (isExpanded) {
            const currentBounds = mainWindow.getBounds();
            lastWidgetPosition = { x: currentBounds.x, y: currentBounds.y };

            // Expanded chat mode
            mainWindow.setSize(360, 460);
            mainWindow.setPosition(width - 376, height - 480);
            mainWindow.setIgnoreMouseEvents(false);

            // Temporarily remove alwaysOnTop when expanded so the user can use other apps normally
            mainWindow.setAlwaysOnTop(false);
        } else {
            // Small widget mode
            mainWindow.setSize(widgetSize, widgetSize);
            const targetX = lastWidgetPosition?.x ?? initialX;
            const targetY = lastWidgetPosition?.y ?? initialY;
            mainWindow.setPosition(targetX, targetY);
            // Do NOT call setIgnoreMouseEvents here — renderer manages it
            // via mouseenter/mouseleave so the widget stays immediately clickable
            mainWindow.setAlwaysOnTop(true);
        }
    });

    // IPC to handle drag area clicks (so the widget itself can receive clicks despite being mostly ignore-mouse)
    ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
        mainWindow.setIgnoreMouseEvents(ignore, options);
    });

    // Move widget window from renderer drag events
    ipcMain.on('set-window-position', (event, x, y) => {
        if (!mainWindow || !Number.isFinite(x) || !Number.isFinite(y)) {
            return;
        }

        const nextX = Math.round(x);
        const nextY = Math.round(y);

        mainWindow.setPosition(nextX, nextY);
        lastWidgetPosition = { x: nextX, y: nextY };
    });

    // Handle app quitting from renderer
    ipcMain.on('quit-app', () => {
        app.quit();
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    app.quit();
});
