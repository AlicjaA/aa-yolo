'''
converts pascal_voc annotations to yolo txt annotations

TODO
[X] check if conversion is correct - bboxes draw corectly
[] delete " from the begining and the end of row in csv file --- TO TEST - implemented 1 version
[] train/val generation with choosen split
'''

import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd


def blood_cells_types(argument):
    """
    maping blood cell types to yolo classes parameters in order as is in bccd.names

    :param argument: string blood cell name
    :return: string parameter
    """
    switcher = {
        'RBC':0,
        'WBC':1,
        'Platelets':2,
    }
    return switcher.get(argument, 0)



def conversion(dir_path, out_filepath, out_filename):
    """
    converts pascal_voc annotations to yolo txt annotations

    :param dir_path: path to dir with annotations files
    :param out_filepath: path to output folder
    :param out_filename: output filename
    """
    df = []
    dir_path = dir_path + '/*.xml'
    annotations = sorted(glob(dir_path))
    for file in annotations:
        counter = 0
        prev_filename = file.split('/')[-1].split('.')[0] + '.jpg'
        row=''
        parsedXML = ET.parse(file)
        width = int(parsedXML.getroot().find('size/width').text)
        hight = int(parsedXML.getroot().find('size/height').text)
        for node in parsedXML.getroot().iter('object'):
            blood_cells = str(int(blood_cells_types(node.find('name').text)))
            xmin = int(node.find('bndbox/xmin').text)
            xmax = int(node.find('bndbox/xmax').text)
            ymin = int(node.find('bndbox/ymin').text)
            ymax = int(node.find('bndbox/ymax').text)
            dw = 1./(width)
            dh = 1./(hight)
            x = (xmin + xmax)/2.0 - 1
            y = (ymin + ymax)/2.0 - 1
            w = xmax - xmin
            h = ymax - ymin
            x = x*dw
            w = w*dw
            y = y*dh
            h = h*dh
            if(counter==0):
                row = prev_filename +' ' + blood_cells+',' + str(x)+',' + str(y)+',' + str(w)+',' + str(h)
            else:
                row+=' '+blood_cells+',' + str(x)+',' + str(y)+',' + str(w)+',' + str(h)
            counter+=1
        df.append(row)
        row =''

    final_filename = out_filepath + '/' + out_filename
    with open("final_filename", "w") as finalfile:
        finalfile.write("\n".join(map(str, df)))

