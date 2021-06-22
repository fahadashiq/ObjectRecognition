from django.shortcuts import render
from django.http import HttpResponse
from .models import PredictedImage
import pythoncom
import win32com.client as wincl
from django.conf import settings
from . import object_detection
from PIL import Image
import uuid
from django.core.files.storage import FileSystemStorage


# view for text to speech
def toSpeech(request, label):
    label = label.replace('_', ' ')
    label = label.replace('-', ' and ')
    voic(label)
    return HttpResponse(status=204)


# to play sound of every object
def voic(label):
    pythoncom.CoInitialize()
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(label)


# view for the index page
def Index(request):
    return render(request, 'IdMain/index.html')


def objectDetection(request):
    if request.method == 'POST' and request.FILES['myFile']:

        myfile = request.FILES['myFile']
        fs = FileSystemStorage()
        unique_filename = str(uuid.uuid4())
        full_file_path = settings.BASE_DIR + '/media/uploaded/' + unique_filename + myfile.name
        # Save uploaded file in local directory
        filename = fs.save(full_file_path, myfile)

        # Get prediction results
        image_np, list_of_percentage, list_of_classes = object_detection.detect_img(filename)

        # Save image with bounded boxes in local dir
        img = Image.fromarray(image_np, 'RGB')
        unique_id = str(uuid.uuid4())
        unique_filename_and_address = '/predicted/' + unique_id + '.jpg'
        img.save(settings.MEDIA_ROOT + unique_filename_and_address)

        # Image to display on frontend
        pimg = PredictedImage()
        pimg.pic = unique_filename_and_address

        list_of_classes_modified = []
        list_of_percentage_modified = []

        # Convert bytes array into string
        for class_name in list_of_classes:
            list_of_classes_modified.append(bytes.decode(class_name))

        # Format percentages correctly
        for percentage in list_of_percentage:
            list_of_percentage_modified.append(round(percentage * 100, 2))

        detection = zip(list_of_classes_modified, list_of_percentage_modified);

        return render(request, 'objectDetection.html', {'pimg': pimg, 'detection': detection})

    return render(request, 'objectDetection.html')
