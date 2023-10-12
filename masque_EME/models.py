from django.db import models

# Create your models here.

class Document(models.Model):
    pdf_file= models.FileField(upload_to='documents/')

    