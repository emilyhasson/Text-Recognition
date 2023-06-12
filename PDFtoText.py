import os

# Set up the credentials for the API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Text-Recognition/boreal-graph-381820-4847d49f0433.json'

import json
import re
from google.cloud import vision
from google.cloud import storage

SOURCE_URI = 'gs://pdf-tests-ehasson/example1.pdf'
DEST_URI = 'gs://pdf-tests-ehasson/ocr-results/'

def async_detect_document(gcs_source_uri, gcs_destination_uri):
    
    mime_type = 'application/pdf'
    batch_size=100

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type=vision.Feature.Type.DOCUMENT_TEXT_DETECTION
    )

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type
    )

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(
        requests=[async_request]
    )

    print('Waiting')
    operation.result(timeout=420)


def write_to_text(gcs_destination_uri):

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    print("bucket name: ", bucket_name)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print("blob name :", blob.name)

    output = blob_list[1]
    print("output: ", output)

    json_string = output.download_as_string()
    response = json.loads(json_string)

    file = open("Text-Recognition/ex1.txt".format(str(1)), "w")

    for m in range(len(response['responses'])):
        first_page_response = response['responses'][m]
        annotation = first_page_response['fullTextAnnotation']

        print('Full text:\n')
        print(annotation['text'])
        file.write(annotation['text'])\

write_to_text(DEST_URI)