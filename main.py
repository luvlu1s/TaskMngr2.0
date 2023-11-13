import tkinter as tk
from tkinter import messagebox
import psutil


class KillAWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminate Task")

        self.create_widgets()

    def create_widgets(self):
        # Listbox to display processes
        self.process_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.process_listbox.pack(expand=True, fill=tk.BOTH)

        # Populate the listbox with process names
        self.refresh_process_list()

        # Bind right-click event to the listbox
        self.process_listbox.bind("<Button-3>", self.show_context_menu)

    def refresh_process_list(self):
        # Clear listbox
        self.process_listbox.delete(0, tk.END)
        processes = [p.info for p in psutil.process_iter(['pid', 'name',])]
        for process in processes:
            self.process_listbox.insert(tk.END, f"{process['name']} (PID: {process['pid']})")


    def show_context_menu(self, event):
        # Context Menu
        contex_menu = tk.Menu(self.root, tearoff=0)
        contex_menu.add_command(label="Kill Process", command=self.kill_selected_process)

        contex_menu.post(event.x_root, event.y_root)

    def kill_selected_process(self):
        # Get selected process from the listbox
        selected_index = self.process_listbox.curselection()
        if selected_index:
            selected_process = self.process_listbox.get(selected_index)
            pid = int(selected_process.split("(PID: ")[1].rstrip(")"))

            # Let the user Confirm before killing the process
            response = messagebox.askokcancel("Confirm Kill", f"Do you want to kill {selected_process}?")
            if response:
                try:
                    # Check if process exist
                    if psutil.pid_exists(pid):
                        # Attempt to kill the process
                        psutil.Process(pid).terminate()
                    else:
                        messagebox.showerror("ERROR", "Process not found")
                except psutil.AccessDenied:
                    messagebox.showerror("ERROR", "Access Denied. Insufficient  permissions")
                except Exception as e:
                    messagebox.showerror("ERROR", "Error while attempting to terminate: {str(e)}")

                # Refresh process list after termination
                self.refresh_process_list()



if __name__ == "__main__":
    root = tk.Tk()
    app = KillAWindowApp(root)
    root.mainloop()

