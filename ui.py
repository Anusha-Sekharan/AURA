import customtkinter as ctk
import threading
from PIL import Image

# Use dark mode for a sleek look
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AuraUI:
    def __init__(self, brain, executor, speaker):
        self.brain = brain
        self.executor = executor
        self.speaker = speaker
        
        self.root = ctk.CTk()
        self.root.title("Aura")
        self.root.geometry("400x500")
        
        # Make the window float on top
        self.root.attributes("-topmost", True)
        
        # State
        self.is_expanded = True
        
        self._setup_expanded_ui()
        self._setup_collapsed_ui()
        
        # Start in collapsed (widget) mode
        self.toggle_mode()

    def _setup_expanded_ui(self):
        self.expanded_frame = ctk.CTkFrame(self.root, corner_radius=15)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.expanded_frame, height=40, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Aura Assistant", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(side="left", padx=5)
        
        self.minimize_btn = ctk.CTkButton(self.header_frame, text="ー", width=30, height=30, 
                                        command=self.toggle_mode, fg_color="transparent", hover_color="#333333")
        self.minimize_btn.pack(side="right")
        
        # Chat History
        self.chat_history = ctk.CTkTextbox(self.expanded_frame, wrap="word", font=ctk.CTkFont(size=13))
        self.chat_history.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat_history.configure(state="disabled")
        
        # Input Area
        self.input_frame = ctk.CTkFrame(self.expanded_frame, height=50, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_field = ctk.CTkEntry(self.input_frame, placeholder_text="Ask Aura to do something...", font=ctk.CTkFont(size=13))
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=60, command=self.send_message)
        self.send_btn.pack(side="right")

    def _setup_collapsed_ui(self):
        self.collapsed_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # A simple circular/rounded button for the floating widget
        self.widget_btn = ctk.CTkButton(self.collapsed_frame, text="A", width=50, height=50, 
                                      corner_radius=25, font=ctk.CTkFont(size=20, weight="bold"),
                                      command=self.toggle_mode)
        self.widget_btn.pack(expand=True)

    def toggle_mode(self):
        if self.is_expanded:
            # Switch to widget mode
            self.expanded_frame.pack_forget()
            self.root.geometry("60x60")
            self.root.overrideredirect(True) # Remove OS window borders
            
            # Position widget in bottom right
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = screen_width - 80
            y = screen_height - 100
            self.root.geometry(f"+{x}+{y}")
            
            self.collapsed_frame.pack(fill="both", expand=True)
            self.is_expanded = False
        else:
            # Switch to chat mode
            self.collapsed_frame.pack_forget()
            self.root.overrideredirect(False) # Restore OS window borders
            self.root.geometry("400x500")
            
            # Position chat window
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = screen_width - 420
            y = screen_height - 540
            self.root.geometry(f"+{x}+{y}")
            
            self.expanded_frame.pack(fill="both", expand=True)
            self.is_expanded = True
            self.input_field.focus()

    def append_message(self, sender, message):
        self.chat_history.configure(state="normal")
        self.chat_history.insert("end", f"{sender}: {message}\n\n")
        self.chat_history.see("end")
        self.chat_history.configure(state="disabled")

    def process_command_thread(self, text):
        try:
            # Think
            command = self.brain.process(text)
            
            # Speak Response
            response_text = command.get("response", "")
            if response_text:
                self.root.after(0, self.append_message, "Aura", response_text)
                self.speaker.speak(response_text)
            
            # Act
            action = command.get("action")
            parameter = command.get("parameter")
            
            if action and action != "chat":
                result = self.executor.execute(action, parameter)
                if result:
                    self.root.after(0, self.append_message, "System", result)
                    self.speaker.speak(result)
                    
        except Exception as e:
            self.root.after(0, self.append_message, "Error", str(e))

    def send_message(self, event=None):
        text = self.input_field.get().strip()
        if not text:
            return
            
        self.input_field.delete(0, "end")
        self.append_message("You", text)
        
        if "exit" in text.lower() or "quit" in text.lower():
            self.append_message("Aura", "Shutting down...")
            self.speaker.speak("Shutting down.")
            self.root.after(2000, self.root.destroy)
            return

        # Run brain logic in a background thread to prevent UI freezing
        threading.Thread(target=self.process_command_thread, args=(text,), daemon=True).start()

    def run(self):
        self.append_message("System", "Aura online. Waiting for command.")
        self.root.mainloop()

if __name__ == "__main__":
    # Test UI independently
    class MockComponent:
        def process(self, *args): return {"response": "Mock thinking", "action": "none"}
        def execute(self, *args): return "Mock action executed"
        def speak(self, *args): pass
        
    app = AuraUI(MockComponent(), MockComponent(), MockComponent())
    app.run()
