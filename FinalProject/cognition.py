from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os, requests, uuid, json
from PIL import Image
import sys
import time


subscription_key = "f9dae2268b544fa39299493730318557"
endpoint = "https://imagetotransaltor.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

'''
Batch Read File, recognize handwritten text - local
This example extracts text from a handwritten local image, then prints results.
This API call can also recognize remote image text (shown in next example, Batch Read File - remote).
'''
"""print("===== Batch Read File - local =====")
# Get image of handwriting
local_image_handwritten_path = "resources\\handwritten_text.jpg"
# Open the image
local_image_handwritten = open(local_image_handwritten_path, "rb")

# Call API with image and raw response (allows you to get the operation location)
recognize_handwriting_results = computervision_client.batch_read_file_in_stream(local_image_handwritten, raw=True)
# Get the operation location (URL with ID as last appendage)
operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
# Take the ID off and use to get results
operation_id_local = operation_location_local.split("/")[-1]

# Call the "GET" API and wait for the retrieval of the results
while True:
    recognize_handwriting_result = computervision_client.get_read_operation_result(operation_id_local)
    if recognize_handwriting_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print results, line by line
if recognize_handwriting_result.status == OperationStatusCodes.succeeded:
    for text_result in recognize_handwriting_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()"""
'''
END - Batch Read File - local
'''

'''
Batch Read File, recognize handwritten text - remote
This example will extract handwritten text in an image, then print results, line by line.
This API call can also recognize handwriting (not shown).
'''
# def get_imagetext(source_link):
#     # Get an image with handwritten text
    
#     remote_printed_text_image_url = source_link
#     result = []
#     ocr_result_remote = computervision_client.recognize_printed_text(remote_printed_text_image_url,language='zh-Hant')
#     for region in ocr_result_remote.regions:
#         for line in region.lines:
#             s = ""
#             for word in line.words:
#                 s += word.text + " "
#             print(s)
#             result.append(s)
#     print(result)
#     return json.dumps(result)

import http.client, urllib.request, urllib.parse, urllib.error, base64


def get_imagetext(source_link):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '4c2b7987d30e4dff87969cb91131f84f',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'language': 'zh-Hant'
    })

    body = {"url":source_link}

    # body = [source_link]

    
    base_url = 'https://centralus.api.cognitive.microsoft.com'
    path = "/vision/v3.2-preview.2/read/analyze?%s" % params
    constructed_url = base_url+path
    
    response = requests.post(constructed_url, headers=headers, json=body)

    get_path = response.headers["Operation-Location"]
    get_header = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '4c2b7987d30e4dff87969cb91131f84f',
    }

    analysis = {}
    poll = True

    #waiting the API finish analysis
    while (poll):
        response_final = requests.get(get_path, headers=get_header)
        analysis = response_final.json()
    
        # print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    
    if ("analyzeResult" in analysis):
        return analysis['analyzeResult']
    else:
        return analysis['status']
    #result save in analyzeResult.readResults.line.text
    

