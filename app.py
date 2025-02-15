import os
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PDF Flattener</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .upload-form {
            border: 2px dashed #ccc;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        .button {
            background: #0066cc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background: #0052a3;
        }
    </style>
</head>
<body>
    <h1>PDF Flattener</h1>
    <div class="upload-form">
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf" accept=".pdf" required>
            <br><br>
            <input type="submit" value="Flatten PDF" class="button">
        </form>
    </div>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

def flatten_pdf(input_stream):
    try:
        # Read the input PDF
        pdf_reader = PdfReader(input_stream)
        pdf_writer = PdfWriter()

        # Process each page
        for page in pdf_reader.pages:
            # Add the page to the output
            pdf_writer.add_page(page)
            
            # Flatten form fields if they exist
            if '/Annots' in page:
                for annotation in page['/Annots']:
                    page['/Annots'].remove(annotation)

        # Save to memory stream
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        
        return output_stream.getvalue()
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return render_template_string(HTML_TEMPLATE, error="No file uploaded")
        
        file = request.files['pdf']
        if file.filename == '':
            return render_template_string(HTML_TEMPLATE, error="No file selected")
        
        if not file.filename.lower().endswith('.pdf'):
            return render_template_string(HTML_TEMPLATE, error="Please upload a PDF file")
        
        try:
            output_pdf = flatten_pdf(file)
            return send_file(
                io.BytesIO(output_pdf),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"flattened_{secure_filename(file.filename)}"
            )
        except Exception as e:
            error = str(e)
    
    return render_template_string(HTML_TEMPLATE, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 