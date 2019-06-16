import re
import datetime
from google.cloud import vision
from google.cloud.vision import types
import io
from PIL import Image, ImageDraw
from enum import Enum
import re
import string 
from aadhar import isValid
import math
import os
from boundingBox import *
from regexMatcher import *
from stringOperations import *
import numpy as np
from scipy import ndimage
import cv2
import string
def process_policy(image_path):
    #reading file
    image  = Image.open(image_path)

    # Calling the API

    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
        content_image = types.Image(content=content)
        response = client.document_text_detection(image=content_image)
        document = response.full_text_annotation
    policy_attr={}
    #policy Number
    import datetime
    policy_location = find_compound_word_location(document,'Policy number')
    if not policy_location:
        policy_location=find_compound_word_location(document,'Policy Number')
    if not policy_location:
        policy_location=find_compound_word_location(document,'Policy No')
    if not policy_location:
        policy_location=find_compound_word_location(document,'Policy Certificate No')
    if policy_location:
            #Extracting the Date in same line in locality
            min_x = policy_location.vertices[2].x + 20
            max_x = policy_location.vertices[2].x + 20 * (policy_location.vertices[2].x-policy_location.vertices[0].x)
            min_y = policy_location.vertices[0].y - (policy_location.vertices[2].y - policy_location.vertices[0].y)/2.0
            max_y = policy_location.vertices[2].y + (policy_location.vertices[2].y - policy_location.vertices[0].y)/2.0
            policy_number = text_within(document,min_x,min_y,max_x,max_y)
    print('policy number: ', policy_number)
    policy_attr['policy_number']=policy_number
   
    RegNo=''
    #Registration Number
    Regno_location = find_compound_word_location(document,'Registration Number')
    if not Regno_location:
        Regno_location = find_compound_word_location(document,'Registration no')
    #searching in same line

    if Regno_location:
            #Extracting the Regno in same line in locality
            min_x = Regno_location.vertices[0].x - 2*(Regno_location.vertices[2].x-Regno_location.vertices[0].x)
            max_x = Regno_location.vertices[2].x + 2 * (Regno_location.vertices[2].x-Regno_location.vertices[0].x)
            min_y = Regno_location.vertices[2].y + 1
            max_y = Regno_location.vertices[2].y + (Regno_location.vertices[2].y - Regno_location.vertices[0].y) * 2 
            RegNo = text_within(document,min_x,min_y,max_x,max_y)[:14].strip().rstrip('\r\n')
            print(RegNo)

    print('Registration number: ', RegNo)
    policy_attr['Registration Number']=RegNo
    #Make

    make=''
    make_location = find_word_location(document,'Make')

    #searching in same line

    if make_location:
        min_x = make_location.vertices[0].x -(make_location.vertices[2].x-make_location.vertices[0].x)
        max_x = make_location.vertices[2].x + (make_location.vertices[2].x-make_location.vertices[0].x)/1.05
        min_y = make_location.vertices[2].y + 1
        max_y = make_location.vertices[2].y + (make_location.vertices[2].y - make_location.vertices[0].y) * 2 
        make = text_within(document,min_x,min_y,max_x,max_y)
    print('Make : ', make)
    policy_attr['Make']=make
    #model
    model=''
    model_location=find_word_location(document,'Model')

    if model_location:
        min_x = model_location.vertices[0].x -(model_location.vertices[2].x-model_location.vertices[0].x)/4
        max_x = model_location.vertices[2].x + (model_location.vertices[2].x-model_location.vertices[0].x)/2
        min_y = model_location.vertices[2].y + 1
        max_y = model_location.vertices[2].y + (model_location.vertices[2].y - model_location.vertices[0].y) * 2 
        model = text_within(document,min_x,min_y,max_x,max_y)
    print("model: ", model)
    policy_attr['Model']=model

    #Type of Body

    body=''
    body_location=find_word_location(document,'body')


    if body_location:
        min_x = body_location.vertices[0].x -2*(body_location.vertices[2].x-body_location.vertices[0].x)
        max_x = body_location.vertices[2].x + (body_location.vertices[2].x-body_location.vertices[0].x)/2
        min_y = body_location.vertices[2].y + 1
        max_y = body_location.vertices[2].y + (body_location.vertices[2].y - body_location.vertices[0].y) * 2 
        body = text_within(document,min_x,min_y,max_x,max_y)
    print("body: ",body)   
    policy_attr['body']=body
    chassis=''
    chassis_location=find_compound_word_location(document,'Chassis Number')

    if chassis_location:
        min_x = chassis_location.vertices[0].x -1.5*(chassis_location.vertices[2].x-chassis_location.vertices[0].x)
        max_x = chassis_location.vertices[2].x + (chassis_location.vertices[2].x-chassis_location.vertices[0].x)/1.05
        min_y = chassis_location.vertices[2].y + 1
        max_y = chassis_location.vertices[2].y + (chassis_location.vertices[2].y - chassis_location.vertices[0].y) * 2 
        chassis = text_within(document,min_x,min_y,max_x,max_y)
    print("chassis number: ", chassis)
    policy_attr['Chassis Number']=chassis
    engine=''
    engine_location=find_compound_word_location(document,'Engine Number')

    if engine_location:
        min_x = engine_location.vertices[0].x -(engine_location.vertices[2].x-engine_location.vertices[0].x)
        max_x = engine_location.vertices[2].x + (engine_location.vertices[2].x-engine_location.vertices[0].x)/1.05
        min_y = engine_location.vertices[2].y + 1
        max_y = engine_location.vertices[2].y + (engine_location.vertices[2].y - engine_location.vertices[0].y) * 2 
        engine = text_within(document,min_x,min_y,max_x,max_y)
    print("Engine number", engine)
    policy_attr['Engine no']=engine
    validity=''
    date_location=find_compound_word_location(document, 'of Insurance')
    if not date_location:
        date_location=find_compound_word_location(document, 'of cover')
    if not date_location:
        date_location=find_compound_word_location(document, 'Effective From')

    if date_location:
        min_x = date_location.vertices[2].x + 20
        max_x = date_location.vertices[2].x + 20 * (date_location.vertices[2].x-date_location.vertices[0].x)
        min_y = date_location.vertices[0].y - (date_location.vertices[2].y - date_location.vertices[0].y)/2.0
        max_y = date_location.vertices[2].y + (date_location.vertices[2].y - date_location.vertices[0].y)/2.0
        validity = text_within(document,min_x,min_y,max_x,max_y).strip()
    print('validity date:',validity)

    months=['Jan','Feb','Mar','Apr','May','Jun','Jul', 'Aug','Sep','Oct' ,'Nov','Dec'] 

    for i in months:
        if(validity.find(i))!=-1:
            print(i)
            month_number = datetime.datetime.strptime(i, '%b').month
            validity=validity.replace(i,str(month_number))
    print(validity)
    list=validity.split('to')
    start=list[0]
    end=list[1]
    startDate = date_pattern.search(start).group(0)
    endDate=date_pattern.search(end).group(0)
    print(startDate)
    print(endDate)
    policy_attr['start date']=startDate
    policy_attr['end date']=endDate
    print(policy_attr)
	return policy_attr
process_policy('Insurance Policy Doc-1.jpg')
