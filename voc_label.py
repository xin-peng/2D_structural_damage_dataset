import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
import os.path
from os.path import join

sets=['train', 'val', 'test']

classes = ["crack", "spalling"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('Annotations/%s.xml'%(image_id))
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
    if not os.path.exists('labels/'):
        os.makedirs('labels/')
    image_ids = open('ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        #print(image_id)
        filename1 = '/home/xin/Desktop/2021Spring/0808_train/JPEGImages/%s.jpg'%(image_id)
        filename2 = '/home/xin/Desktop/2021Spring/0808_train/JPEGImages/%s.jpeg'%(image_id)
        if os.path.isfile(filename1):
            list_file.write('/home/xin/Desktop/2021Spring/0808_train/JPEGImages/%s.jpg\n'%(image_id))
        elif os.path.isfile(filename2):
            list_file.write('/home/xin/Desktop/2021Spring/0808_train/JPEGImages/%s.jpeg\n'%(image_id))
        else:
            print(filename1,filename2)
        convert_annotation(image_id)
    list_file.close()

os.system("cat train.txt val.txt > mytrain.txt")
os.system("cat train.txt val.txt test.txt> train.all.txt")