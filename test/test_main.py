import unittest
import subprocess
import psutil
from tkinter import Tk, END, messagebox
from main import KillAWindowApp

class TestKillAWindowApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = KillAWindowApp(self.root)
        self.root.update_idletasks()
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_refresh_process_list(self):
        initial_process_count = self.app.process_listbox.size()
        self.assertEqual(initial_process_count, 0, "Initial process list should be empty")

        # Simulate adding processes
        processes = [{'pid': 123, 'name': 'process1'}, {'pid': 456, 'name': 'process2'}]
        self.app.process_listbox.delete(0, END)
        for process in processes:
            self.app.process_listbox.insert(END, f"{process['name']} (PID: {process['pid']})")
        updated_process_count = self.app.process_listbox.size()
        self.assertEqual(updated_process_count, len(processes), "Process list should be updated")

    def test_show_context_menu(self):
        event = subprocess.Popen(["xte", "mousemove", "50", "50"])
        self.app.show_context_menu(event)
        context_menu_exists = isinstance(self.app.context_menu, Tk.Menu)
        self.assertTrue(context_menu_exists, "Context menu should be created")

    def test_kill_selected_process(self):
        self.app.process_listbox.insert(END, "TestProcess (PID: 789)")
        self.app.process_listbox.selection_set(0)
        messagebox.askokcancel = lambda *args: True
        with self.assertLogs(level='ERROR') as cm:
            self.app.kill_selected_process()

        # Check if the process is terminated
        terminated_process_exists = psutil.pid_exists(789)
        self.assertFalse(terminated_process_exists, "Process should be terminated")
        self.assertIn("ERROR:", cm.output[0], "Error message should be logged")

if __name__ == "__main__":
    unittest.main()
