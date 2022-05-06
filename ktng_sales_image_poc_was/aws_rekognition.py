import boto3
import io
import logging
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont

logger = logging.getLogger(__name__)


def display_image(image, response):

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    # print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('./Library/Fonts/arial.ttf', 50)
            draw.text(
                (left, top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left, top),
                (left + width, top),
                (left + width, top + height),
                (left, top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    return image


def show_custom_labels(model, photo, min_confidence):

    client = boto3.client('rekognition')

    # Get image Bytes
    image = Image.open(photo)
    image_type = Image.MIME[image.format]

    if (image_type == "image/jpeg" or image_type == "image/png") == False:
        logger.error("Invalid image type for %s", photo)
        raise ValueError(
            f"Invalid file format. Supply a jpeg or png format file: {photo}"
        )

    # get images bytes for call to detect_anomalies
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes = image_bytes.getvalue()

    # Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'Bytes': image_bytes},
                                           MinConfidence=min_confidence,
                                           ProjectVersionArn=model)

    # For object detection use case, uncomment below code to display image.
    image = display_image(image, response)

    return response, image
