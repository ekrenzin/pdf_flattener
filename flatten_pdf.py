from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def flatten_pdf(input_path, output_path):
    """
    Flatten a PDF file by merging all its layers into a single layer
    """
    try:
        # Open the PDF file
        with open(input_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            
            # Iterate through all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page.merge_page(page)
                pdf_writer.add_page(page)
            
            # Write the flattened PDF to the output file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Error flattening PDF: {str(e)}")
        return False

def select_files():
    files = filedialog.askopenfilenames(
        title="Select PDFs to flatten",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not files:
        return
        
    # Create output directory
    output_dir = os.path.join(os.path.dirname(files[0]), "flattened")
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    # Process each selected file
    for input_path in files:
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, f"flattened_{filename}")
        if flatten_pdf(input_path, output_path):
            success_count += 1
    
    messagebox.showinfo("Complete", 
        f"Successfully flattened {success_count} of {len(files)} PDFs.\n"
        f"Files saved in: {output_dir}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    select_files()
    
    root.destroy()

if __name__ == "__main__":
    main() 