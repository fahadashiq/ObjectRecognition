from django.shortcuts import render
from django.http import HttpResponse
from .models import PredictedImage
import pythoncom
import win32com.client as wincl
import base64
from django.shortcuts import redirect
from django.core.files.base import ContentFile
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
        filename = fs.save(full_file_path, myfile)
        list_of_name = []
        #ImgObj = UploadedImage(pic=myfile)


        # image_np, list_of_classes = object_detection_custom.perdictMultiObj(ImgObj.pic.path)
        image_np, list_of_percentage, list_of_classes = object_detection.detect_img(filename)
        # convert those ids into names
        '''
        for li in list_of_classes:
            class_name = object_detection_custom.category_index[li]['name']
            list_of_name.append(class_name)
            print(class_name)

        # get image from numpy array and save it in perdicted folder with a unique name
        img = Image.fromarray(image_np, 'RGB')
        unique_filename = str(uuid.uuid4())
        print(unique_filename)
        unique = settings.BASE_DIR + '/media' + '/perdicted/' + unique_filename + '.jpg'
        img.save(unique)
        # make a string of perdictions
        list_2 = []
        for li in list_of_name:
            if li in list_2:
                print("nohing")
                # do nothing
            else:
                list_2.append(li)
        names = ""
        print(list_2)
        for li in list_2:
            if names == "":
                names = li
            else:
                names = names + '-' + li
        names = names.replace(' ', '_')
        # save the image address in database

        ImgObj.perdiction = names
        ImgObj.derived_perdiction = 'Let me find'
        ImgObj.save()
        pimg = PredictedImage()
        pimg.pic = settings.BASE_DIR + '/media' + '/perdicted/' + unique_filename + '.jpg'
        pimg.perdiction = names
        pimg.save()
        print("passed")'''
        img = Image.fromarray(image_np, 'RGB')
        unique_id = str(uuid.uuid4())
        unique_filename_and_address = '/predicted/' + unique_id + '.jpg'
        img.save(settings.MEDIA_ROOT + unique_filename_and_address)

        pimg = PredictedImage()
        pimg.pic = unique_filename_and_address

        list_of_classes_modified = []
        list_of_percentage_modified = []

        for class_name in list_of_classes:
            list_of_classes_modified.append(bytes.decode(class_name))

        for percentage in list_of_percentage:
            list_of_percentage_modified.append(round(percentage * 100, 2))

        detection = zip(list_of_classes_modified, list_of_percentage_modified);

        return render(request, 'objectDetection.html', {'pimg': pimg, 'detection': detection})
    return render(request, 'objectDetection.html')
