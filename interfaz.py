import tkinter as tk
from tkinter import messagebox
from automata import Automata

class AutomataInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("RefScan - Buscado rde referencias")

        self.label = tk.Label(root, text="Introduce el texto:")
        self.label.pack(pady=10)

        self.text_entry = tk.Text(root, height=15, width=45)
        self.text_entry.pack(pady=10)

        self.start_button = tk.Button(root, text="Iniciar busqueda", command=self.find_references)
        self.start_button.pack(pady=10)

        self.automata = Automata()
        self.references = []

    def find_references(self):
        text = self.text_entry.get("1.0", tk.END)

        self.references = self.automata.find_references(text)
    
        if self.references:
            messagebox.showinfo("Resultado", f"Referencias encontradas:{', '.join(self.references)}")
        else:
            messagebox.showinfo("Resultado", "No se encontraron referencias.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataInterfaz(root)
    root.mainloop()