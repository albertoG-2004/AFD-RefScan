import tkinter as tk
from tkinter import filedialog, messagebox
from automata import Automata
from readerPdf import read_pdf
from createReport import create_report

class AutomataInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("RefScan - Buscador de referencias")

        self.label = tk.Label(root, text="Selecciona un archivo PDF para buscar referencias:")
        self.label.pack(pady=10)

        self.file_button = tk.Button(root, text="Seleccionar PDF", command=self.load_pdf)
        self.file_button.pack(pady=10)

        self.automata = Automata()
        self.references = []

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                text = read_pdf(file_path)

                if not isinstance(text, str):
                    raise ValueError("El texto extraído no es una cadena.")
            
                self.references = self.automata.find_references(text)

                if self.references:
                    create_report(self.references, "Referencias_encontradas.csv")
                    messagebox.showinfo("Resultado", "Referencias encontradas:\n" + '\n'.join(
                        f"{ref['Referencia']} (línea {ref['Linea']}, Columna {ref['Columna']})" for ref in self.references
                    ))
                else:
                    messagebox.showinfo("Resultado", "No se encontraron referencias.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataInterfaz(root)
    root.mainloop()