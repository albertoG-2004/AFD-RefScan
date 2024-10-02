import tkinter as tk
from tkinter import filedialog
from automata import Automata
from readerPdf import read_pdf
from readerDocx import read_docx
from createReport import create_report

class AutomataInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("RefScan - Buscador de referencias")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        self.title_label = tk.Label(
            root, text="RefScan", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        self.title_label.pack(pady=20)

        self.label = tk.Label(
            root, text="Selecciona un archivo PDF o DOCX para buscar referencias:",
            font=("Helvetica", 12), bg="#2c3e50", fg="#bdc3c7"
        )
        self.label.pack(pady=10)

        self.file_button = tk.Button(
            root, text="Seleccionar PDF", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=self.load_pdf
        )
        self.file_button.pack(pady=20)

        self.file_button = tk.Button(
            root, text="Seleccionar DOCX", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=self.load_docx
        )
        self.file_button.pack(pady=20)

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
                    self.show_success_popup()  
                    self.show_references_popup()  
                else:
                    self.show_no_references_popup()  
            except Exception as e:
                self.show_error_popup(f"No se pudo leer el archivo PDF: {e}")

    def load_docx(self):
        file_path = filedialog.askopenfilename(filetypes=[("DOCX Files", "*.docx")])
        if file_path:
            try:
                text = read_docx(file_path)

                if not isinstance(text, str):
                    raise ValueError("El texto extraído no es una cadena.")
                self.references = self.automata.find_references(text)

                if self.references:
                    create_report(self.references, "Referencias_encontradas.csv")
                    self.show_success_popup()  
                    self.show_references_popup()  
                else:
                    self.show_no_references_popup()  
            except Exception as e:
                self.show_error_popup(f"No se pudo leer el archivo DOCX: {e}")

    def show_references_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Referencias Encontradas")
        popup.geometry("400x300")
        popup.configure(bg="#2c3e50")

        title_label = tk.Label(
            popup, text="Referencias Encontradas", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        title_label.pack(pady=10)

        frame = tk.Frame(popup, bg="#34495e")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(frame, bg="#34495e")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        reference_frame = tk.Frame(canvas, bg="#34495e")
        canvas.create_window((0, 0), window=reference_frame, anchor="nw")

        for ref in self.references:
            ref_label = tk.Label(
                reference_frame,
                text=f"{ref['Referencia']} (línea {ref['Linea']}, columna {ref['Columna']})",
                font=("Helvetica", 12),
                bg="#34495e", fg="#ecf0f1", wraplength=350, anchor="w", justify="left"
            )
            ref_label.pack(anchor="w", padx=10, pady=5)

        close_button = tk.Button(
            popup, text="Cerrar", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=popup.destroy
        )
        close_button.pack(pady=10)

    def show_success_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Reporte Generado")
        popup.geometry("300x150")
        popup.configure(bg="#2c3e50")

        label = tk.Label(
            popup, text="¡Reporte generado con éxito!", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        label.pack(pady=20)

        close_button = tk.Button(
            popup, text="Cerrar", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=popup.destroy
        )
        close_button.pack(pady=10)

    def show_no_references_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Resultado")
        popup.geometry("300x150")
        popup.configure(bg="#2c3e50")

        label = tk.Label(
            popup, text="No se encontraron referencias.", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        label.pack(pady=20)

        close_button = tk.Button(
            popup, text="Cerrar", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=popup.destroy
        )
        close_button.pack(pady=10)

    def show_error_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Error")
        popup.geometry("300x150")
        popup.configure(bg="#2c3e50")

        label = tk.Label(
            popup, text=message, font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#e74c3c"
        )
        label.pack(pady=20)

        close_button = tk.Button(
            popup, text="Cerrar", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
            relief="flat", padx=10, pady=5, command=popup.destroy
        )
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataInterfaz(root)
    root.mainloop()