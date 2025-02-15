import os
import sys

try:
    import fitz  # PyMuPDF
    from PIL import Image
    import io
except ImportError:
    print("❌ Missing required packages. Please install them using one of these methods:")
    print("\nMethod 1: Install from requirements.txt:")
    print("pip install -r requirements.txt")
    print("\nMethod 2: Install packages directly:")
    print("pip install PyMuPDF Pillow")
    sys.exit(1)

def flatten_pdf(input_path, output_path):
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(input_path)
        output_doc = fitz.open()

        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image with higher DPI for better quality
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x resolution for better quality
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to black and white (1-bit) with better threshold
            bw_img = img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')
            
            # Convert back to bytes
            img_bytes = io.BytesIO()
            bw_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Create new page with same dimensions
            new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insert B&W image
            new_page.insert_image(new_page.rect, stream=img_bytes.getvalue())

        # Save the output PDF
        output_doc.save(output_path)
        output_doc.close()
        doc.close()
        
        print(f"✅ Successfully flattened and converted to B&W: {os.path.basename(input_path)}")
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