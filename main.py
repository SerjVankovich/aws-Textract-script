import os
import sys

import boto3

directory = sys.argv[1]
files = os.listdir(directory)

text_path = os.path.abspath(os.path.join(directory, "../")) + '/text'
try:
    os.mkdir(text_path)
except:
    print('Dir with "' + text_path + '" name is already exist')

client = boto3.client(
    service_name='textract',
    region_name='us-east-1',
    endpoint_url='https://textract.us-east-1.amazonaws.com'
)


def get_text(path):
    full_filename, file_extension = os.path.splitext(path)
    file_name = os.path.split(full_filename)[1]

    lines = []
    with open(path, 'rb') as f:
        img = f.read()
        bytes_test = bytearray(img)
        print('Image ' + file_name + ' loaded')

    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS'])

    blocks = response['Blocks']

    for block in blocks:
        if block['BlockType'] == 'LINE':
            lines.append(block['Text'])

    with open(text_path + '/' + file_name + '.txt', 'w') as f:
        for line in lines:
            f.write("%s\n" % line)


for file in files:
    _, file_ext = os.path.splitext(directory + '/' + file)
    if file_ext.lower() in ['.jpg', '.png', '.bmp']:
        get_text(directory + '/' + file)

