import os
from flask import Flask, request, send_file, render_template_string
import tempfile
from werkzeug.utils import secure_filename
import fitz
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
        output_stream = io.BytesIO()
        doc = fitz.open(stream=input_stream.read())
        output_doc = fitz.open()

        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            bw_img = img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')
            
            img_bytes = io.BytesIO()
            bw_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, stream=img_bytes.getvalue())

        output_doc.save(output_stream)
        output_doc.close()
        doc.close()
        
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