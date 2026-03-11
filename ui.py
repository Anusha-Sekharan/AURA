import math
import customtkinter as ctk
import threading
from PIL import Image

# Use dark mode for a sleek look
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HologramWidget(ctk.CTkCanvas):
    def __init__(self, master, size=150, command=None, **kwargs):
        super().__init__(master, width=size, height=size, bg="black", highlightthickness=0, **kwargs)
        self.size = size
        self.command = command
        self.bind("<Button-1>", self._on_click)
        self.angle1 = 0.0
        self.angle2 = math.pi / 2
        self.angle3 = math.pi
        self.running = True
        self.animate()

    def _on_click(self, event):
        if self.command:
            self.command()
            
    def stop(self):
        self.running = False
        
    def _draw_orbit_half(self, cx, cy, rx, ry, rotation_angle, is_back):
        # Draw the back half (-pi to 0) or front half (0 to pi)
        # Using degrees for easier iteration
        start_deg = 180 if is_back else 0
        end_deg = 360 if is_back else 180
        
        # Calculate layers for a thick, glowing, misty orbit look
        layers = [
            (8, "#2d0b38"),
            (5, "#6b186d"),
            (2, "#b32eb0"),
            (1, "#f4a6f2")
        ]
        
        for width, color in layers:
            pts = []
            for deg in range(start_deg, end_deg + 1, 10):
                rad = math.radians(deg)
                
                # We calculate standard 2D ellipse coordinates
                x = rx * math.cos(rad)
                y = ry * math.sin(rad)
                
                # Then we rotate the ellipse on the z-axis
                rot_x = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
                rot_y = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
                
                pts.append(cx + rot_x)
                pts.append(cy + rot_y)
                
            if len(pts) >= 4:
                self.create_line(pts, fill=color, width=width, smooth=True)

    def _draw_particle(self, cx, cy, rx, ry, rotation_angle, orbital_progress):
        progress = orbital_progress % (2 * math.pi)
        
        x = rx * math.cos(progress)
        y = ry * math.sin(progress)
        
        rot_x = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
        rot_y = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
        
        px, py = cx + rot_x, cy + rot_y
        
        # Front vs back determines size and brightness to simulate 3D depth
        is_front = math.sin(progress) >= 0
        s = 2.5 if is_front else 1.0
        color = "#ffffff" if is_front else "#d194d6"
        
        self.create_oval(px - s, py - s, px + s, py + s, fill=color, outline="")
        if is_front:
            self.create_oval(px - s - 2, py - s - 2, px + s + 2, py + s + 2, fill="", outline="#f4a6f2", width=1)


    def animate(self):
        if not self.running:
            return
            
        self.delete("all")
        
        # Different speeds for different particles
        self.angle1 += 0.05
        self.angle2 += 0.03
        self.angle3 += 0.04
        
        cx, cy = self.size / 2, self.size / 2
        
        max_r = self.size / 2 - 10
        rx = max_r
        ry = max_r * 0.35
        
        # The 3 orbit rotations around the core
        orbit_angles = [
            math.radians(30),
            math.radians(90),
            math.radians(150)
        ]
        
        particle_angles = [self.angle1, self.angle2, self.angle3]
        
        # Draw BACK halves of the orbits
        for r_angle in orbit_angles:
            self._draw_orbit_half(cx, cy, rx, ry, r_angle, is_back=True)
            
        # Draw BACK particles (if their progress is in the back half)
        for idx, r_angle in enumerate(orbit_angles):
            if math.sin(particle_angles[idx] % (2 * math.pi)) < 0:
                self._draw_particle(cx, cy, rx, ry, r_angle, particle_angles[idx])
        
        # Draw the Pitch Black Core (it occludes everything behind it, simulating 3D space)
        core_r = max_r * 0.45
        
        # Extremely faint glow boundary
        self.create_oval(cx - core_r - 2, cy - core_r - 2, cx + core_r + 2, cy + core_r + 2, fill="", outline="#2d0b38", width=2)
        # Deep void black core
        self.create_oval(cx - core_r, cy - core_r, cx + core_r, cy + core_r, fill="#010003", outline="")
        
        # Draw FRONT halves of the orbits
        for r_angle in orbit_angles:
            self._draw_orbit_half(cx, cy, rx, ry, r_angle, is_back=False)
            
        # Draw FRONT particles (if their progress is in the front half)
        for idx, r_angle in enumerate(orbit_angles):
            if math.sin(particle_angles[idx] % (2 * math.pi)) >= 0:
                self._draw_particle(cx, cy, rx, ry, r_angle, particle_angles[idx])

        self.after(40, self.animate)


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
        self.hologram = None
        
        self._setup_expanded_ui()
        self.collapsed_frame = ctk.CTkFrame(self.root, fg_color="black")
        
        # Start in collapsed (widget) mode
        self.toggle_mode()

    def _setup_expanded_ui(self):
        self.expanded_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#1a1a2e")
        
        # Header
        self.header_frame = ctk.CTkFrame(self.expanded_frame, height=40, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="AURA ASSISTANT", font=ctk.CTkFont(size=16, weight="bold"), text_color="#d482ff")
        self.title_label.pack(side="left", padx=5)
        
        self.minimize_btn = ctk.CTkButton(self.header_frame, text="ー", width=30, height=30, 
                                        command=self.toggle_mode, fg_color="transparent", hover_color="#333333")
        self.minimize_btn.pack(side="right")
        
        # Chat History
        self.chat_history = ctk.CTkTextbox(self.expanded_frame, wrap="word", font=ctk.CTkFont(size=14))
        self.chat_history.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat_history.configure(state="disabled", text_color="#e0e0e0", fg_color="#0f0f1c")
        
        # Input Area
        self.input_frame = ctk.CTkFrame(self.expanded_frame, height=50, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_field = ctk.CTkEntry(self.input_frame, placeholder_text="Ask Aura to do something...", font=ctk.CTkFont(size=14))
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=60, command=self.send_message, fg_color="#7a28cc", hover_color="#9a3fd6")
        self.send_btn.pack(side="right")

    def toggle_mode(self):
        if self.is_expanded:
            # Switch to widget mode
            self.expanded_frame.pack_forget()
            
            # Dimensions for 0.75 inch diameter (~150px)
            widget_size = 150
            self.root.geometry(f"{widget_size}x{widget_size}")
            self.root.overrideredirect(True) # Remove OS window borders
            self.root.configure(bg="black")
            
            try:
                # Make black pixels fully transparent on Windows
                self.root.wm_attributes("-transparentcolor", "black")
            except Exception:
                pass
            
            # Position widget in bottom right
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = screen_width - widget_size - 20
            y = screen_height - widget_size - 100
            self.root.geometry(f"+{x}+{y}")
            
            self.collapsed_frame.pack(fill="both", expand=True)
            
            if not self.hologram:
                self.hologram = HologramWidget(self.collapsed_frame, size=widget_size, command=self.toggle_mode)
                self.hologram.pack(fill="both", expand=True)
            else:
                self.hologram.running = True
                self.hologram.animate()
                
            self.is_expanded = False
        else:
            # Switch to chat mode
            if self.hologram:
                self.hologram.stop()
                
            self.collapsed_frame.pack_forget()
            
            try:
                # Remove transparency
                self.root.wm_attributes("-transparentcolor", "")
            except Exception:
                pass
                
            self.root.overrideredirect(False) # Restore OS window borders
            
            # Re-apply window color for main UI
            self.root.configure(bg="#1a1a2e")
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
        self.chat_history.insert("end", f"{sender}: ", "sender")
        self.chat_history.insert("end", f"{message}\n\n")
        
        # Color specific roles
        if sender == "Aura" or sender == "System":
            self.chat_history.tag_config("sender", foreground="#9a3fd6")
        else:
            self.chat_history.tag_config("sender", foreground="#00d0ff")
            
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
