import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

class PDFFlattenerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Flattener")
        
        # Set minimum window size
        self.root.minsize(400, 200)
        
        # Center window on screen
        window_width = 400
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Selected file label
        self.file_label = ttk.Label(main_frame, text="No file selected", wraplength=350)
        self.file_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Buttons
        ttk.Button(main_frame, text="Select PDF", command=self.select_file).grid(
            row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Flatten PDF", command=self.flatten_pdf).grid(
            row=1, column=1, padx=5)

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
    app = PDFFlattenerGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main() 