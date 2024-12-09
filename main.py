import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo-Liste")
        self.root.geometry("800x600")
        
        # Datenbankverbindung
        self.conn = sqlite3.connect('todo.db')
        self.create_table()
        
        # GUI-Elemente
        self.create_widgets()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'offen'
            )
        ''')
        self.conn.commit()
        
    def create_widgets(self):
        # Eingabebereich
        input_frame = ttk.LabelFrame(self.root, text="Neue Aufgabe", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Titel:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Priorität:").grid(row=0, column=2, padx=5, pady=5)
        self.priority_combo = ttk.Combobox(input_frame, values=["Hoch", "Mittel", "Niedrig"])
        self.priority_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Hinzufügen", command=self.add_task).grid(row=0, column=4, padx=5, pady=5)
        
        # Aufgabenliste
        list_frame = ttk.LabelFrame(self.root, text="Aufgaben", padding="10")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Buttons für Aktionen
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Status ändern", command=self.change_status).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Priorität ändern", command=self.change_priority).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Löschen", command=self.delete_task).pack(side="left", padx=5)
        
        columns = ("ID", "Titel", "Priorität", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True)
        
        # Status-Menü
        self.status_menu = tk.Menu(self.root, tearoff=0)
        self.status_menu.add_command(label="Offen", command=lambda: self.update_status("offen"))
        self.status_menu.add_command(label="In Bearbeitung", command=lambda: self.update_status("in bearbeitung"))
        self.status_menu.add_command(label="Erledigt", command=lambda: self.update_status("erledigt"))
        
        # Priorität-Menü
        self.priority_menu = tk.Menu(self.root, tearoff=0)
        self.priority_menu.add_command(label="Hoch", command=lambda: self.update_priority("Hoch"))
        self.priority_menu.add_command(label="Mittel", command=lambda: self.update_priority("Mittel"))
        self.priority_menu.add_command(label="Niedrig", command=lambda: self.update_priority("Niedrig"))
        
        # Rechtsklick-Menü
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_cascade(label="Status ändern", menu=self.status_menu)
        self.context_menu.add_cascade(label="Priorität ändern", menu=self.priority_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Löschen", command=self.delete_task)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Initial tasks laden
        self.load_tasks()
        
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
        
    def add_task(self):
        title = self.title_entry.get()
        priority = self.priority_combo.get()
        
        if title:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, priority, status)
                VALUES (?, ?, ?)
            ''', (title, priority, 'offen'))
            self.conn.commit()
            
            self.title_entry.delete(0, tk.END)
            self.priority_combo.set('')
            self.load_tasks()
            
    def change_status(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus.")
            return
        self.status_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        
    def change_priority(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus.")
            return
        self.priority_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        
    def update_status(self, new_status):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item)['values'][0]
            cursor = self.conn.cursor()
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
            self.conn.commit()
            self.load_tasks()
            
    def update_priority(self, new_priority):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item)['values'][0]
            cursor = self.conn.cursor()
            cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (new_priority, task_id))
            self.conn.commit()
            self.load_tasks()
            
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Aufgabe aus.")
            return
            
        if messagebox.askyesno("Löschen", "Möchten Sie diese Aufgabe wirklich löschen?"):
            task_id = self.tree.item(selected_item)['values'][0]
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            self.load_tasks()
    
    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        cursor = self.conn.cursor()
        # Sortiere nach Status (erledigt ans Ende) und Priorität (Hoch zuerst)
        cursor.execute('''
            SELECT id, title, priority, status 
            FROM tasks 
            ORDER BY 
                CASE 
                    WHEN status = 'erledigt' THEN 2 
                    ELSE 1 
                END,
                CASE 
                    WHEN priority = 'Hoch' THEN 1
                    WHEN priority = 'Mittel' THEN 2
                    WHEN priority = 'Niedrig' THEN 3
                    ELSE 4
                END,
                id DESC
        ''')
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop() 