import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

class PDFFlattenerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Flattener")
        
        # Simple window setup
        self.root.geometry("400x200")
        
        # Basic label
        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack(pady=20)
        
        # Basic buttons
        tk.Button(self.root, text="Select PDF", command=self.select_file).pack(pady=10)
        tk.Button(self.root, text="Flatten PDF", command=self.flatten_pdf).pack(pady=10)
        
        self.input_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF to flatten",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.input_path = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def flatten_pdf(self):
        if not self.input_path:
            messagebox.showwarning("Warning", "Please select a PDF file first!")
            return

        try:
            # Create output filename
            output_path = self.input_path.replace('.pdf', '_flattened.pdf')

            # Open and process the PDF
            with open(self.input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()

                # Process each page
                for page in reader.pages:
                    writer.add_page(page)

                # Write the flattened PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

            messagebox.showinfo("Success", 
                f"PDF flattened successfully!\nSaved as: {os.path.basename(output_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    try:
        app = PDFFlattenerGUI()
        app.root.mainloop()
    except Exception as e:
        # In case of error, show a message box and print to console
        print(f"Error occurred: {str(e)}")
        messagebox.showerror("Error", f"Application error: {str(e)}")
        # Keep the error message visible
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 