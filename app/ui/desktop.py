import tkinter as tk
from tkinter import scrolledtext
import sys
import io
from app.core.kernel import NV001Kernel

class NV001DesktopApp:
    def __init__(self, root, kernel: NV001Kernel):
        self.root = root
        self.kernel = kernel
        
        self.root.title("NV001 Interface")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e1e1e")
        
        # Output Area
        self.output_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", 
            font=("Consolas", 11), insertbackground="white",
            padx=15, pady=15, borderwidth=0
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_area.config(state=tk.DISABLED)
        
        # Input Area
        self.input_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.input_box = tk.Entry(
            self.input_frame, font=("Consolas", 12), bg="#2d2d2d", 
            fg="white", insertbackground="white", borderwidth=0
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.input_box.bind("<Return>", self.handle_input)
        self.input_box.focus_set()
        
        self.send_button = tk.Button(
            self.input_frame, text="Execute", bg="#444", fg="white", 
            font=("Consolas", 10, "bold"), borderwidth=0, padx=15, pady=5,
            command=self.handle_input_button, activebackground="#666"
        )
        self.send_button.pack(side=tk.RIGHT)
        
        self.log("NV001 Kernel Initialized. System ready.")
        self.log("Type 'help' to see available commands or 'agent <goal>' for autonomous reasoning.\n")
        
    def log(self, message: str):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, message + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
        
    def handle_input_button(self):
        self.handle_input(None)

    def handle_input(self, event):
        command = self.input_box.get().strip()
        if not command:
            return
            
        self.input_box.delete(0, tk.END)
        self.log(f"\nUSER > {command}")
        
        if command.lower() == "exit":
            self.root.quit()
            return
            
        # Capture kernel's stdout prints seamlessly into the GUI
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        
        try:
            self.kernel.execute_command(command)
        except Exception as e:
            print(f"Error executing command: {e}")
            
        sys.stdout = old_stdout
        
        output = mystdout.getvalue()
        if output:
            self.log(output.strip("\n"))

def start_gui():
    kernel = NV001Kernel()
    kernel.start()
    
    root = tk.Tk()
    app = NV001DesktopApp(root, kernel)
    root.mainloop()
    
    kernel.stop()

if __name__ == "__main__":
    start_gui()
