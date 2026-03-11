const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
    const primaryDisplay = screen.getPrimaryDisplay();
    const { width, height } = primaryDisplay.workAreaSize;

    const widgetSize = 150;

    mainWindow = new BrowserWindow({
        width: widgetSize,
        height: widgetSize,
        x: width - widgetSize - 20,
        y: height - widgetSize - 20,
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
            // Expanded chat mode
            mainWindow.setSize(400, 500);
            mainWindow.setPosition(width - 420, height - 520);
            mainWindow.setIgnoreMouseEvents(false);

            // Temporarily remove alwaysOnTop when expanded so the user can use other apps normally
            mainWindow.setAlwaysOnTop(false);
        } else {
            // Small widget mode
            mainWindow.setSize(widgetSize, widgetSize);
            mainWindow.setPosition(width - widgetSize - 20, height - widgetSize - 20);
            mainWindow.setIgnoreMouseEvents(true, { forward: true });
            mainWindow.setAlwaysOnTop(true);
        }
    });

    // IPC to handle drag area clicks (so the widget itself can receive clicks despite being mostly ignore-mouse)
    ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
        mainWindow.setIgnoreMouseEvents(ignore, options);
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
