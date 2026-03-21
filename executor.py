import subprocess
import os
import platform

class Executor:
    def __init__(self, speaker=None):
        self.speaker = speaker
        from memory_handler import MemoryHandler
        from clipboard_manager import ClipboardManager
        self.memory = MemoryHandler()
        self.clipboard = ClipboardManager()

    def execute(self, action, parameter=None):
        """
        Executes a local system command based on the action and parameter.
        """
        if action == "open_app":
            return self.open_application(parameter)
        elif action == "close_app":
            return self.close_application(parameter)
        elif action == "send_email":
            return self.send_email(parameter)
        elif action == "whatsapp_msg":
            return self.send_whatsapp(parameter)
        elif action == "whatsapp_call":
            return self.send_whatsapp_call(parameter)
        elif action == "play_music":
            return self.play_music(parameter)
        elif action == "news":
            return self.get_news(parameter)
        elif action == "create_folder":
            return self.create_folder(parameter)
        elif action == "delete_folder":
            return self.delete_folder(parameter)
        elif action == "volume_control":
            return self.volume_control(parameter)
        elif action == "power_control":
            return self.power_control(parameter)
        elif action == "screenshot":
            return self.take_screenshot()
        elif action == "google_search":
            return self.google_search(parameter)
        elif action == "youtube_play":
            return self.youtube_play(parameter)
        elif action == "weather":
            return self.get_weather(parameter)
        elif action == "definition":
            return self.get_definition(parameter)
        elif action == "translate":
            return self.translate_text(parameter)
        elif action == "system_info":
            return self.get_system_info()
        elif action == "remember":
            return self.remember(parameter)
        elif action == "clipboard":
            return self.get_clipboard_history()
        elif action == "timer":
            return self.set_timer(parameter)
        elif action == "calendar":
            return self.manage_calendar(parameter)
        else:
            return f"Unknown action: {action}"

    # ... (open_application and close_application methods) ...

    def get_clipboard_history(self):
        history = self.clipboard.get_history()
        if not history:
            return "Your clipboard history is empty."
            
        res = "Recent Clipboard History:\n"
        for i, item in enumerate(history, 1):
            # Truncate very long items
            display_item = item if len(item) < 100 else item[:97] + "..."
            res += f"{i}. {display_item}\n"
        return res

    def set_timer(self, details):
        import threading
        import time
        from plyer import notification
        
        if not details or not isinstance(details, dict):
            return "Invalid timer parameters."
            
        duration = details.get("duration_minutes", 0)
        message = details.get("message", "Timer is up!")
        
        try:
            duration = float(duration)
        except Exception:
            return "Invalid duration for timer."
            
        if duration <= 0:
            return "Duration must be positive."
            
        def alarm_thread(mins, msg):
            time.sleep(mins * 60)
            try:
                notification.notify(
                    title="Aura Alarm",
                    message=msg,
                    app_name="Aura Assistant",
                    timeout=10
                )
            except Exception:
                pass # plyer might fail on some windows configurations without correct libraries
                
            if self.speaker:
                self.speaker.speak(f"Alarm! {msg}")

        threading.Thread(target=alarm_thread, args=(duration, message), daemon=True).start()
        msg_str = f"Timer set for {duration} minute(s): {message}"
        print(msg_str)
        return msg_str

    def manage_calendar(self, details):
        import os.path
        import datetime
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        import dateparser
        import tzlocal
        
        if not details or not isinstance(details, dict):
            return "Invalid calendar parameters."
            
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    return f"Failed to refresh calendar credentials: {e}"
            else:
                if not os.path.exists('credentials.json'):
                    return ("Google Calendar 'credentials.json' is missing. "
                            "Please download it from Google Cloud Console and place it in the project directory.")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    # Increased wait time so user has enough time to click through accounts
                    creds = flow.run_local_server(port=0, timeout_seconds=300, success_message="Authentication successful! Please close this browser window and return to Aura.")
                except Exception as e:
                    return f"Authentication flow failed: {e}"
            # Save the credentials for the next run
            try:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except:
                pass

        try:
            service = build('calendar', 'v3', credentials=creds)
            action = details.get("action", "read")
            
            if action == "read":
                # Call the Calendar API
                now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                events_result = service.events().list(calendarId='primary', timeMin=now,
                                                      maxResults=3, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])

                if not events:
                    return "You have no upcoming meetings or events."
                
                result_str = "Upcoming Events:\n"
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    # clean up the ISO format string for simple reading
                    if 'T' in start:
                        dt = dateparser.parse(start)
                        readable_time = dt.strftime("%B %d at %I:%M %p") if dt else start
                    else:
                        readable_time = start
                    result_str += f"- {readable_time}: {event.get('summary', 'Busy')}\n"
                return result_str.strip()
                
            elif action == "create":
                time_str = details.get("time")
                summary = details.get("summary", "Aura Reminder")
                
                if not time_str:
                    return "I need a time to schedule the meeting/reminder."
                    
                parsed_date = dateparser.parse(time_str)
                if not parsed_date:
                    return f"Could not understand the time format: {time_str}"
                    
                sys_tz = tzlocal.get_localzone()
                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=sys_tz)
                    
                end_date = parsed_date + datetime.timedelta(minutes=30)
                
                event_body = {
                  'summary': summary,
                  'start': {
                    'dateTime': parsed_date.isoformat(),
                    'timeZone': str(sys_tz),
                  },
                  'end': {
                    'dateTime': end_date.isoformat(),
                    'timeZone': str(sys_tz),
                  },
                }

                event = service.events().insert(calendarId='primary', body=event_body).execute()
                return f"Scheduled '{summary}' for {parsed_date.strftime('%I:%M %p on %b %d')}."

        except HttpError as error:
            return f"An error occurred with Google Calendar API: {error}"
        except Exception as e:
            return f"Failed to manage calendar: {e}"

    
    def remember(self, details):
        if not details or not isinstance(details, dict):
            return "Invalid memory parameters."
        
        key = details.get("key")
        value = details.get("value")
        
        if not key or not value:
            return "I need a key and value to remember something."
            
        print(f"Executing: Remembering {key} = {value}")
        return self.memory.save_memory(key, value)
    
    def send_email(self, details):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import config

        recipient = details.get("recipient")
        subject = details.get("subject")
        body = details.get("body")

        if not recipient or not body:
            return "Missing recipient or body for email."

        sender_email = config.EMAIL_SENDER
        password = config.EMAIL_PASSWORD
        
        if "your_email" in sender_email:
            return "Email credentials not configured in config.py."

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
            
            return f"Email sent to {recipient}."
        except Exception as e:
            return f"Failed to send email: {e}"

    def send_whatsapp_call(self, details):
        import pyautogui
        import time
        
        contact = details.get("contact")
        
        if not contact:
            return "Missing contact name."
            
        msg = f"Executing: WhatsApp Call to {contact}"
        print(msg)
        if self.speaker: print(msg)
        
        # 1. Open WhatsApp
        self.open_application("whatsapp")
        
        # 2. Wait for it to open and focus
        time.sleep(2.0)
        
        try:
            # 3. Search for contact
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1.0)
            
            # Type name
            pyautogui.write(contact)
            time.sleep(2.0) # Wait for search to populate
            
            # Select first result (Down arrow + Enter is more reliable than just Enter)
            pyautogui.press('down')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2.5) # Wait longer for chat to load
            
            # 4. Initiate Call (Ctrl + Shift + C for Voice Call)
            print("Initiating call...")
            pyautogui.hotkey('ctrl', 'shift', 'c')
            
            return f"Calling {contact} on WhatsApp..."
            
        except Exception as e:
            return f"Call automation failed: {e}"

    def send_whatsapp(self, details):
        import pyautogui
        import time
        
        contact = details.get("contact")
        message = details.get("message")
        
        if not contact or not message:
            return "Missing contact or message."
            
        msg = f"Executing: WhatsApp Message to {contact}"
        print(msg)
        if self.speaker: print(msg)
        
        # 1. Open WhatsApp
        self.open_application("whatsapp")
        
        # 2. Wait for it to open and focus
        time.sleep(2.0) 
        
        try:
            # 3. Search for contact
            # Ctrl+F usually focuses search in WhatsApp Desktop
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Type name
            pyautogui.write(contact)
            time.sleep(2.0) # Wait for search results
            
            # Select first result
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # 4. Type and Send Message
            pyautogui.write(message)
            pyautogui.press('enter')
            
            return f"Message sent to {contact} (assuming name match)."
            
        except Exception as e:
            return f"Automation failed: {e}"

    def play_music(self, details):
        import pyautogui
        import time
        from urllib.parse import quote
        
        song = details.get("song")
        
        if not song:
            return "No song specified."
            
        msg = f"Executing: Playing '{song}' on Spotify"
        print(msg)
        if self.speaker: print(msg)
        
        # 1. Use Spotify Protocol to search
        # Encodes the query (e.g. "popular songs" -> "popular%20songs")
        try:
            query = quote(song)
            # Use 'track:' operator to ensure we find songs, not albums/playlists
            uri = f"spotify:search:track:{query}"
            
            print(f"Launching URI: {uri}")
            os.startfile(uri)
            
            # 2. Wait for Spotify to Open/Focus and Search to Load
            time.sleep(4.0)
            
            # 3. Play the first result
            # Focus is often in the search bar. 
            # Tab 1: Moves to 'Songs' filter chip.
            # Tab 2: Moves to the Top Result (The Song).
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.press('enter')
            
            return f"Playing {song} on Spotify..."
            
        except Exception as e:
            return f"Failed to play music: {e}"

    def get_news(self, details):
        import xml.etree.ElementTree as ET
        from urllib.request import urlopen
        from urllib.parse import quote
        
        category = details.get("category", "top stories").lower()
        limit = details.get("limit", 3)
        try:
            limit = int(limit)
        except:
            limit = 3
        
        # Free Google News RSS URLs
        url = "https://news.google.com/rss" # Default Top Stories
        
        if category in ["tech", "technology"]:
            url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY"
        elif category in ["sport", "sports"]:
            url = "https://news.google.com/rss/headlines/section/topic/SPORTS"
        elif category in ["world"]:
            url = "https://news.google.com/rss/headlines/section/topic/WORLD"
        elif category and category != "top stories":
            # General Search logic
            q = quote(category)
            url = f"https://news.google.com/rss/search?q={q}"
            
        msg = f"Executing: Fetching top {limit} news for '{category}'..."
        print(msg)
        if self.speaker: print(msg)
        
        try:
            with urlopen(url) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                headlines = []
                count = 0
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    # Clean source suffix: "Title - Source" -> "Title"
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    
                    headlines.append(title)
                    count += 1
                    if count >= limit:
                        break
                
                result = f"Here are the top {limit} {category} headlines:\n"
                
                # Speak them clearly
                if self.speaker:
                    print(f"Headlines fetched.")
                
                for i, h in enumerate(headlines, 1):
                    result += f"{i}. {h}\n"
                    if self.speaker:
                        print(h)
                        
                return result.strip()
                
        except Exception as e:
            return f"Failed to fetch news: {e}"

    def get_system_info(self):
        return f"System: {platform.system()} {platform.release()}"

    def open_application(self, app_name):
        if not app_name:
            return "No application specified."
        
        app_name = app_name.lower().strip()
        msg = f"Executing: Opening {app_name}"
        print(msg)
        if self.speaker: print(msg)

        # 1. URL Handlers
        if "http" in app_name or ".com" in app_name or ".org" in app_name:
            try:
                os.startfile(app_name)
                return f"Opening URL: {app_name}"
            except Exception as e:
                return f"Failed to open URL: {e}"

        # 2. Known Web Shortcuts (Keep only major utilities, remove specific sites)
        web_shortcuts = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com"
        }
        
        for key, url in web_shortcuts.items():
            if key in app_name:
                try:
                    os.startfile(url)
                    return f"Opening {key}..."
                except:
                    pass

        # 3. App Name Mappings (Common names to Executables or Protocols)
        app_map = {
            "edge": "msedge",
            "chrome": "chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "explorer": "explorer",
            "cmd": "cmd",
            "powershell": "powershell",
            "spotify": "spotify",
            "vscode": "code",
            "word": "winword",
            "excel": "excel",
            "whatsapp": "whatsapp:" 
        }

        # Check for direct mapping or substring match
        target = app_map.get(app_name)
        if not target:
            # Try to find a partial match in keys
            for key, val in app_map.items():
                if key in app_name:
                    target = val
                    break
        
        # 4. Execution
        try:
            if target:
                print(f"Launching mapped: {target}")
                # os.startfile handles both executables (via PATH/AppPaths) and Protocols
                os.startfile(target)
                return f"Opened {app_name} ({target})."
            else:
                # Fallback: Let Windows try to figure it out
                print(f"Launching fallback: {app_name}")
                os.startfile(app_name)
                return f"Attempted to open '{app_name}'."
                
        except Exception as e:
            # Final Fallback: Search in Browser or Open Domain
            print(f"Local open failed. Attempting domain guess for: {app_name}")
            import webbrowser
            
            # Heuristic: Try to open as a .com domain
            # "open unstop" -> unstop -> unstop.com
            # "open facebook" -> facebook -> facebook.com
            clean_name = app_name.replace(" ", "")
            url = f"https://www.{clean_name}.com"
            
            webbrowser.open(url)
            return f"Opening official website: {url}"


    def close_application(self, app_name):
        import psutil
        import difflib
        
        if not app_name:
            return "No application specified to close."
        
        app_name = app_name.lower().strip()
        msg = f"Executing: Closing {app_name}"
        print(msg)
        if self.speaker: print(msg)

        # Mapping for closing (process names)
        process_map = {
            "edge": ["msedge.exe"],
            "chrome": ["chrome.exe"],
            "notepad": ["notepad.exe"],
            "calculator": ["CalculatorApp.exe", "calc.exe"],
            "spotify": ["spotify.exe"],
            "vscode": ["Code.exe"],
            "word": ["WINWORD.EXE"],
            "excel": ["EXCEL.EXE"],
            "whatsapp": ["WhatsApp.exe", "WhatsApp.Root.exe"]
        }

        targets = process_map.get(app_name)
        
        # Fuzzy match if exact match fails
        if not targets:
            matches = difflib.get_close_matches(app_name, list(process_map.keys()), n=1, cutoff=0.6)
            if matches:
                matched_key = matches[0]
                print(f"Fuzzy match: '{app_name}' -> '{matched_key}'")
                targets = process_map[matched_key]

        if not targets:
             for key, val in process_map.items():
                if key in app_name:
                    targets = val
                    break
        
        # Fallback: try app_name itself
        if not targets:
            targets = [f"{app_name}.exe", app_name]

        found = False
        terminated_count = 0
        
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    pname = proc.info['name'].lower() if proc.info['name'] else ""
                    for target in targets:
                        if target.lower() == pname or (target.lower() in pname and len(target) > 3):
                            proc.terminate()
                            terminated_count += 1
                            found = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if found:
                return f"Closed {app_name} ({terminated_count} process instances)."
            else:
                return f"Could not find {app_name} running."
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Failed to close {app_name}: {e}"


    def create_folder(self, details):
        if not details or not isinstance(details, dict):
             return "Invalid parameters for folder creation."
        
        folder_name = details.get("name")
        path_hint = details.get("path", "desktop") # Default to desktop if not specified
        
        if not folder_name:
            return "I need a folder name to create it."

        # Clean folder name
        folder_name = folder_name.strip()
        
        # Resolve base path
        base_path = self._resolve_path(path_hint)
        full_path = os.path.join(base_path, folder_name)
        
        msg = f"Executing: Creating folder '{folder_name}' at {base_path}"
        print(msg)
        if self.speaker: print(msg)

        try:
            os.makedirs(full_path, exist_ok=True)
            return f"Folder '{folder_name}' created successfully at {base_path}."
        except Exception as e:
            return f"Failed to create folder: {e}"

    def delete_folder(self, details):
        import shutil
        
        if not details or not isinstance(details, dict):
             return "Invalid parameters for folder deletion."
        
        folder_name = details.get("name")
        path_hint = details.get("path", "desktop") # Default to desktop if not specified
        
        if not folder_name:
            return "I need a folder name to delete it."

        # Clean folder name
        folder_name = folder_name.strip()
        
        # Resolve base path
        base_path = self._resolve_path(path_hint)
        full_path = os.path.join(base_path, folder_name)
        
        msg = f"Executing: Deleting folder '{folder_name}' from {base_path}"
        print(msg)
        if self.speaker: print(msg)

        if not os.path.exists(full_path):
             return f"Folder '{folder_name}' does not exist at {base_path}."

        try:
            # Safety check: Prevent deleting entire desktop or user dir if name is empty (though checked above)
            # Also maybe check if it is a directory
            if not os.path.isdir(full_path):
                return f"Path '{full_path}' is not a folder."
            
            # Use send2trash for safety if available, otherwise shutil.rmtree
            # For now, explicit delete as requested, but maybe just rmtree
            shutil.rmtree(full_path)
            return f"Folder '{folder_name}' deleted successfully from {base_path}."
        except Exception as e:
            return f"Failed to delete folder: {e}"

    def _resolve_path(self, path_hint):
        user_path = os.path.expanduser("~")
        if not path_hint:
             return os.path.join(user_path, "Desktop")
             
        path_hint = path_hint.lower()
        
        if "desktop" in path_hint:
            return os.path.join(user_path, "Desktop")
        elif "document" in path_hint:
            return os.path.join(user_path, "Documents")
        elif "download" in path_hint:
            return os.path.join(user_path, "Downloads")
        elif "music" in path_hint:
            return os.path.join(user_path, "Music")
        elif "picture" in path_hint:
            return os.path.join(user_path, "Pictures")
        elif "video" in path_hint:
             return os.path.join(user_path, "Videos")
        else:
             # If user says a specific path like "C:/Users/...", try to use it if valid, else default to desktop
             if os.path.exists(path_hint):
                 return path_hint
             else:
                 # Check if it looks like an absolute path
                 if ":\\" in path_hint or ":/" in path_hint or path_hint.startswith("/"):
                     return path_hint
                 else:
                     return os.path.join(user_path, "Desktop") # Fallback

    def volume_control(self, details):
        from pycaw.utils import AudioUtilities
        
        if not details:
            return "Invalid volume parameters."
            
        action = details.get("action", "set")
        value = details.get("value")
        
        try:
            # Get default audio device
            devices = AudioUtilities.GetSpeakers()
            # New pycaw version exposes EndpointVolume property directly
            volume = devices.EndpointVolume
            
            if action == "mute":
                volume.SetMute(1, None)
                msg = "System muted."
            elif action == "unmute":
                volume.SetMute(0, None)
                msg = "System unmuted."
            elif action == "set":
                if value is None:
                    return "Volume value required."
                
                # Ensure value is int 0-100
                try:
                    vol_level = int(str(value).replace("%",""))
                    vol_level = max(0, min(100, vol_level))
                except:
                    return f"Invalid volume level: {value}"
                
                # Pycaw SetMasterVolumeLevelScalar takes 0.0 to 1.0
                scalar = vol_level / 100.0
                volume.SetMasterVolumeLevelScalar(scalar, None)
                msg = f"Volume set to {vol_level}%."
            else:
                return f"Unknown volume action: {action}"
                
            print(f"Executing: {msg}")
            if self.speaker: print(msg)
            return msg
            
        except Exception as e:
            return f"Failed to control volume: {e}"

    def power_control(self, details):
        action = details.get("action")
        if not action:
            return "No power action specified."
            
        action = action.lower()
        msg = ""
        cmd = ""
        
        if "shutdown" in action:
            msg = "Shutting down the system in 10 seconds."
            cmd = "shutdown /s /t 10"
        elif "restart" in action:
            msg = "Restarting the system in 10 seconds."
            cmd = "shutdown /r /t 10"
        elif "sleep" in action:
            msg = "Putting system to sleep."
            # Sleep command usually requires admin or specific config, but rundll32 works often
            cmd = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
        else:
             return f"Unknown power action: {action}"
             
        print(f"Executing: {msg}")
        if self.speaker: print(msg)
        
        try:
            os.system(cmd)
            return f"Command initiated: {msg}"
        except Exception as e:
            return f"Failed to execute power command: {e}"

    def take_screenshot(self):
        import pyautogui
        import datetime
        
        try:
            # User requested specific path: C:\Users\Anusha\OneDrive\Pictures\Screenshots
            user_home = os.path.expanduser("~")
            screens_path = os.path.join(user_home, "OneDrive", "Pictures", "Screenshots")
            
            if not os.path.exists(screens_path):
                os.makedirs(screens_path)
                
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Screenshot_{timestamp}.png"
            full_path = os.path.join(screens_path, filename)
            
            msg = "Taking screenshot..."
            print(msg)
            if self.speaker: print(msg)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(full_path)
            
            return f"Screenshot saved to {filename}."
            
        except Exception as e:
            return f"Failed to take screenshot: {e}"

    def google_search(self, details):
        import webbrowser
        from urllib.parse import quote
        
        query = details.get("query")
        if not query:
            return "No search query provided."
            
        msg = f"Executing: Searching Google for '{query}'"
        print(msg)
        if self.speaker: print(msg)
        
        try:
            url = f"https://www.google.com/search?q={quote(query)}"
            webbrowser.open(url)
            return f"Opened Google search for: {query}"
        except Exception as e:
            return f"Failed to search Google: {e}"

    def youtube_play(self, details):
        import webbrowser
        from urllib.parse import quote
        
        query = details.get("query")
        if not query:
            return "No video name provided."
            
        msg = f"Executing: Playing '{query}' on YouTube"
        print(msg)
        if self.speaker: print(msg)
        
        try:
            # Open search results. Auto-playing first video is complex/flaky without API or Selenium.
            # Best reliable method: Open search results.
            url = f"https://www.youtube.com/results?search_query={quote(query)}"
            webbrowser.open(url)
            return f"Opened YouTube results for: {query}"
        except Exception as e:
            return f"Failed to open YouTube: {e}"

    def get_weather(self, details):
        import requests
        
        location = details.get("location")
        msg = f"Executing: Checking weather for {location if location else 'your location'}..."
        print(msg)
        if self.speaker: print(msg)
        
        try:
            # wttr.in is a console-oriented weather service
            # format=3 gives concise "City: Condition Temp" output
            url = f"https://wttr.in/{location}?format=3" if location else "https://wttr.in/?format=3"
            
            response = requests.get(url)
            if response.status_code == 200:
                weather_info = response.text.strip()
                return f"Weather Report: {weather_info}"
            else:
                return "Failed to fetch weather data."
                
        except Exception as e:
            return f"Weather check failed: {e}"

    def get_definition(self, details):
        import wikipedia
        
        term = details.get("term")
        if not term:
             return "No term provided to define."
             
        msg = f"Executing: Defining '{term}'..."
        print(msg)
        if self.speaker: print(msg)
        
        try:
            # Get 1 sentence summary
            summary = wikipedia.summary(term, sentences=1)
            return f"{term}: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Term '{term}' is ambiguous. Options: {e.options[:3]}"
        except wikipedia.exceptions.PageError:
            return f"Could not find a definition for '{term}'."
        except Exception as e:
            return f"Definition failed: {e}"

    def translate_text(self, details):
        from deep_translator import GoogleTranslator
        
        text = details.get("text")
        target = details.get("target", "en")
        
        if not text:
            return "No text provided to translate."
            
        # Map common language names to codes if needed, but GoogleTranslator handles many
        # We can add a simple mapping for reliability
        msg = f"Executing: Translating to {target}..."
        print(msg)
        if self.speaker: print(msg)
        
        try:
            translator = GoogleTranslator(source='auto', target=target)
            translated = translator.translate(text)
            return f"Translation ({target}): {translated}"
        except Exception as e:
             return f"Translation failed: {e}"


if __name__ == "__main__":
    e = Executor()
    # e.execute("open_app", "notepad")
    # time.sleep(2)
    e.execute("close_app", "notepad")
