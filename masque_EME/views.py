from django.shortcuts import render
from masque_EME.forms import pre40
from io import StringIO
from pdfminer.high_level import extract_text

def index(request):
    file_url = None
    extracted_text = None

    if request.method == "POST":
        form = pre40(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save()
            file_url = instance.pdf_file.url
            file_path = instance.pdf_file.path

            # Extract text from the uploaded PDF
            extracted_text = extract_text(file_path)

            form = pre40()  # Reset the form after saving
    else:
        form = pre40()

    context = {
        "form": form,
        "file_url": file_url,
        "extracted_text": extracted_text,
    }

    return render(request, 'masque_EME/index.html', context)
