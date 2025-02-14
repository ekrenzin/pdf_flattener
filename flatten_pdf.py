import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def flatten_pdf():
    # Create and hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    try:
        # Open file dialog for selecting input PDF
        input_path = filedialog.askopenfilename(
            title="Select PDF to flatten",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not input_path:  # User cancelled
            return

        # Automatically create output filename by adding '_flattened'
        output_path = input_path.replace('.pdf', '_flattened.pdf')

        # Open the PDF
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            # Process each page
            for page in reader.pages:
                writer.add_page(page)

            # Write the flattened PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

        messagebox.showinfo("Success", f"PDF flattened successfully!\nSaved as: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    flatten_pdf() 