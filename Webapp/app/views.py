from django.shortcuts import render
import cv2
import keras
import numpy as np
from keras.preprocessing import image
from bs4 import BeautifulSoup as soup
from PIL import Image
from urllib.request import urlopen as uReq
import tensorflow as tf
import re
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

model = tf.keras.models.load_model('models/cnn_model.h5')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        context1 = home(filename)
        #home(uploaded_file_url)
        return render(request, 'webapp/LND.html', context1)
    return render(request, 'webapp/form.html')



# Create your views here.
def home(file) :
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    #img = cv2.imread (file)
    dir = 'media/' + file
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    img = test_images[1]
    img = (np.expand_dims(img, 0))
    predictions = probability_model.predict(img)
    result = np.argmax(predictions)
    if result == 0:
        prediction = 'T-shirt'
    elif result == 1:
        prediction = 'Trouser'
    elif result == 2:
        prediction = 'Pullover'
    elif result == 3:
        prediction = 'Dress'
    elif result == 4:
        prediction = 'coat'
    elif result == 5:
        prediction = 'Sandal'
    elif result == 6:
        prediction = 'Shirt'
    elif result == 7:
        prediction = 'Sneaker'
    elif result == 8:
        prediction = 'Bag'
    elif result == 9:
        prediction = 'boot'
    # img = cv2.imread(test_images[0])

    # dir = 'media/'+file
    # from keras.preprocessing import image
    # test_image1 = image.load_img(dir, target_size=(28, 28))
    # test_image = image.img_to_array(test_image1)
    # test_image = np.expand_dims(test_image, axis=0)
    # result1 = probability_model.predict(test_image)
    # if result[0][0] == 1:
    #     prediction = 'T-shirt/top'
    # elif result[0][1] == 1:
    #     prediction = 'Trouser'
    # elif result[0][2] == 1:
    #     prediction = 'Pullover'
    # elif result[0][3] == 1:
    #     prediction = 'Dress'
    # elif result[0][4] == 1:
    #     prediction = 'Coat'
    # elif result[0][5] == 1:
    #     prediction = 'Sandal'
    # elif result[0][6] == 1:
    #     prediction = 'Shirt'
    # elif result[0][7] == 1:
    #     prediction = 'Sneaker'
    # elif result[0][8] == 1:
    #     prediction = 'Bag'
    # elif result[0][9] == 1:
    #     prediction = 'Ankle boot'










    name = 'shoess'

    my_url = "https://www.flipkart.com/search?q=" + prediction + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    uClient = uReq ( my_url )
    page_html = uClient.read ( )
    uClient.close ( )
    page_soup = soup ( page_html, "html.parser" )

    containers = page_soup.find ( "div", {"class" : "_3O0U0u"} )

    items = containers.find_all ( class_='_2B_pmu' )
    prices = containers.find_all ( class_='_1vC4OE' )

    names = list ( )
    for i in items :
        names.append ( i.text )

    price = list ( )
    for i in prices :
        price.append ( i.text )

    list1 = list ( )
    links = containers.find_all ( class_='IIdQZO _1SSAGr' )
    for i in links :
        tint = i.find_all ( class_="_3dqZjq", href=True )
        for link in tint :
            list1.append ( link [ 'href' ] )

    name1 = "shoes"
    my_url1 = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=" + prediction + "&_sacat=0"
    uClient1 = uReq ( my_url1 )
    page_html1 = uClient1.read ( )
    uClient1.close ( )
    page_soup1 = soup ( page_html1, "html.parser" )

    containers1 = page_soup1.find_all ( "div", {"class" : "s-item__wrapper clearfix"} )

    temp = list ( )
    links = list ( )
    names1 = list ( )
    price1 = list ( )
    for i in range ( 0, 4 ) :
        container = containers1 [ i ]
        items = container.find ( "h3", {"class" : "s-item__title s-item__title--has-tags"} )
        names1.append ( items.text )
        prices1 = container.find ( "span", {"class" : "s-item__price"} )
        price1.append ( prices1.text )
        container_tint = container.find ( "div", {"class" : "s-item__info clearfix"} )
        tint = container_tint.find_all ( 'a', href=True )
        for link in tint :
            temp.append ( link [ 'href' ] )
        links.append ( temp [ 0 ] )
        temp = list ( )

    context = {'name1': names[0],'name2': names[1],'name3': names[2],'name4': names[3], 'price1': price[0],'link1':list1[0],
               'price2': price[1],'price3': price[2],'price4': price[3],'link2':list1[1],'link3':list1[2],'link4':list1[3],
               'name5': names1[0],'name6': names1[1],'name7': names1[2],'name8': names1[3],'price5': price1[0],
               'price6': price1[1],'price7': price1[2],'price8': price1[3],'link5':links[0],'link6':links[1],'link7':links[2],
               'link8':links[3]}
    return context