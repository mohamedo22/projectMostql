# imageditor/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TextForm
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64 , os
import tempfile  
def home(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 11)]
            image_path = 'image_editor/images/ce_5t.jpeg'
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            positions = [(10, 10 + 20 * i) for i in range(10)]
            for text, position in zip(texts, positions):
                draw.text(position, text, (255, 255, 255), font=font)
            response_image = BytesIO()
            image.save(response_image, 'JPEG')
            response_image.seek(0)
            image_base64 = base64.b64encode(response_image.getvalue()).decode('utf-8')
            request.session['image'] = image_base64
            return render(request, 'pdf_template.html', {'image': image_base64})
    else:
        form = TextForm()
    return render(request, 'upload_image.html', {'form': form})

def download_pdf(request):
    image_base64 = request.session.get('image')
    if not image_base64:
        return HttpResponse('No image to download', status=400)
    image_data = base64.b64decode(image_base64)
    
    # Save the image data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(image_data)
        tmp_file.flush()
        tmp_file.close()
        image_path = tmp_file.name
    
    try:
        # Open the image from the temporary file path
        image = Image.open(image_path)
        
        # Generate the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # Open the image and get its dimensions
        img = ImageReader(image_path)
        img_width, img_height = img.getSize()
        # Calculate scaling factors
        scaling_factor_width = letter[0] / img_width
        scaling_factor_height = letter[1] / img_height
        scaling_factor = min(scaling_factor_width, scaling_factor_height)
        # Calculate scaled dimensions
        new_width = img_width * scaling_factor * 0.9  # Adjust scale factor as needed (0.9 for 90% of original size)
        new_height = img_height * scaling_factor * 0.9  # Adjust scale factor as needed (0.9 for 90% of original size)
        # Create a canvas with the image dimensions
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=(600, 400))
        # Draw the image at the top-left corner
        p.drawImage(img, 0, 0, width=img_width*scaling_factor, height=img_height*scaling_factor, preserveAspectRatio=True, mask='auto')
        
        # Save the canvas
        p.showPage()
        p.save()

        # Get PDF data from buffer and close the buffer
        pdf = buffer.getvalue()
        buffer.close()

        # Write the PDF data to the response
        response.write(pdf)
        return response
    finally:
        pass