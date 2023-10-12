import os  # Import the os module here
from django.conf import settings
from django.http import HttpResponse
from docx import Document
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.staticfiles.finders import find
from masque_EME.forms import pre40
from pdfminer.high_level import extract_text
import re



def modify_docx(n_marche):
    # Open the template document
    doc = Document('static/Skoll/docx/PRE40.docx')
    
    # Go through each paragraph in the doc and replace {n_marche} with the actual value
    for paragraph in doc.paragraphs:
        if '{n_marche}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{n_marche}', n_marche)
            
    filename = f"modified_template_{n_marche}.docx"  # Unique filename based on n_marche
    modified_doc_path = os.path.join(settings.MEDIA_ROOT, filename)

    doc.save(modified_doc_path)

    # Return the file path, not the HttpResponse
    return modified_doc_path


def extract_information(text):
    info_dict = {}
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"\b\d{8,15}\b", text) # Adjusting the boundaries for a phone number to be 8-15 digits long


    # Regular expressions for each information to be captured
    info_dict["N° de Marché"] = re.search(r"N° marché : (\d+)", text).group(1) if re.search(r"N° marché : (\d+)", text) else "Not found"
    info_dict["N° du lot"] = re.search(r"N° du lot : (\d+)", text).group(1) if re.search(r"N° du lot : (\d+)", text) else "Not found"
    info_dict["N° de commande"] = re.search(r"N° commande :\n\n(\w+)", text).group(1) if re.search(r"N° commande :\n\n(\w+)", text) else "Not found"
    info_dict["Prestation réalisée du"] = re.search(r"Prestation du (\d{2}/\d{2}/\d{4})", text).group(1) if re.search(r"Prestation du (\d{2}/\d{2}/\d{4})", text) else "Not found"
    info_dict["Prestation réalisée au"] = re.search(r"au (\d{2}/\d{2}/\d{4})", text).group(1) if re.search(r"au (\d{2}/\d{2}/\d{4})", text) else "Not found"
        

    info_dict["Bénéficiaire > Prénom"] = re.search(r"Nom, prénom : \w+ (\w+)", text).group(1) if re.search(r"Nom, prénom : \w+ (\w+)", text) else "Not found"
    info_dict["Bénéficiaire > Identifiant"] = re.search(r"Identifiant N° : (\w+)", text).group(1) if re.search(r"Identifiant N° : (\w+)", text) else "Not found"
    info_dict["Bénéficiaire > tel"] = phones[0] if phones else "Not found"
    info_dict["Bénéficiaire > mail"] = emails[0] if emails else "Not found"
    
    organisme_nom_match = re.search(r"Nom : (.+?)\n\nIdentifiant N°", text, re.DOTALL)
    if organisme_nom_match:
        info_dict["Organisme > Nom"] = organisme_nom_match.group(1).strip()
    else:
        info_dict["Organisme > Nom"] = "Not found"

    lieu_realisation_match = re.search(r"Mél. :(.*?)Tél. :", text, re.DOTALL)
    if lieu_realisation_match:
        lieu_realisation = lieu_realisation_match.group(1).strip()
        # Removing any sequence of more than 5 digits
        lieu_realisation = re.sub(r"\d{5,}", "", lieu_realisation)
        # Removing email addresses
        lieu_realisation = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "", lieu_realisation)
        info_dict["Organisme > lieu de réalisation"] = lieu_realisation.strip()
    else:
        info_dict["Organisme > lieu de réalisation"] = "Not found"

    info_dict["Organisme > Tel"] = "Not found" # If there is a specific pattern to capture, add it here.
    info_dict["Organisme > Mail"] = emails[1] if len(emails) > 1 else "Not found"
    
    info_dict["Correspondant > Nom, prénom"] = re.search(r"Correspondant-e Pôle emploi\n\nNom, prénom :\n\n(\w+ \w+)", text).group(1) if re.search(r"Correspondant-e Pôle emploi\n\nNom, prénom :\n\n(\w+ \w+)", text) else "Not found"
    info_dict["Correspondant > Pole emploi de"] = re.search(r"Pôle emploi de : (\w+-\w+-\w+)", text).group(1) if re.search(r"Pôle emploi de : (\w+-\w+-\w+)", text) else "Not found"
    info_dict["Correspondant > Mail"] = "Not found" # If there is a specific pattern to capture, add it here.
    
    return info_dict


def index(request):
    file_url = None
    extracted_info = None
    extracted_text = None  
    modified_docx_url = None  # New variable to store the modified docx file's URL

    if request.method == "POST":
        form = pre40(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save()
            file_url = instance.pdf_file.url
            file_path = instance.pdf_file.path

            # Extract text from the uploaded PDF
            extracted_text = extract_text(file_path)
            
            # Extract specific information from the text
            extracted_info = extract_information(extracted_text)
            n_marche = extracted_info.get("N° de Marché", "")
            
            # Modify and save the docx file
            docx_path = modify_docx(n_marche)  # Updated the function call
            if docx_path:
                modified_docx_url = os.path.join(settings.MEDIA_URL, os.path.basename(docx_path))

            form = pre40()  # Reset the form after saving
            
    else:
        form = pre40()

    context = {
        "form": form,
        "file_url": file_url,
        "extracted_info": extracted_info,
        "raw_extracted_text": extracted_text,
        "modified_docx_url": modified_docx_url,  # Pass the URL to the template
    }

    return render(request, 'masque_EME/index.html', context)
