import PyPDF2
import os

def flatten_pdf(input_path, output_path):
    try:
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        print(f"✅ Successfully flattened: {os.path.basename(input_path)}")
        return True
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(input_path)}: {str(e)}")
        return False

def main():
    input_dir = 'pdf_files/input'
    output_dir = 'pdf_files/output'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"❌ Input directory '{input_dir}' does not exist!")
        return
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"⚠️ No PDF files found in {input_dir}")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    processed = 0
    failed = 0
    
    for filename in pdf_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"flattened_{filename}")
        
        if flatten_pdf(input_path, output_path):
            processed += 1
        else:
            failed += 1
    
    # Print summary
    print("\n📊 Summary:")
    print(f"✅ Successfully processed: {processed} files")
    print(f"❌ Failed: {failed} files")
    print(f"📂 Output directory: {output_dir}")

if __name__ == "__main__":
    main() 