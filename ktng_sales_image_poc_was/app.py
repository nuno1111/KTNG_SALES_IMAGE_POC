import os
from flask import Flask, request, Response, send_from_directory, jsonify
from datetime import datetime
from aws_rekognition import show_custom_labels
from biz_logic import get_detection_info
from aws_s3 import upload_s3_image, download_s3_image

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MODEL = 'arn:aws:rekognition:ap-northeast-2:610326736716:project/sales_tabaco_detect/version/sales_tabaco_detect.2022-04-26T16.20.26/1650957626427'

S3_BUCKET = 'com-ktng-sales-image-poc'
ORIGINAL_FOLDER = 'original/'
INFERRED_FOLDER = 'inferred/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/download/inferred/<name>')
def download_file(name):
    print(name)
    file = download_s3_image(S3_BUCKET, INFERRED_FOLDER + name)

    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=inferred_image"}
    )


@app.route('/api/upload', methods=['POST'])
def upload_file():

    # 001. Clinet로 부터 파일 받아오기
    file = request.files['file']

    # 002. 파일명 유일하게 만들기 위한 현재일시 받아오기
    now = datetime.now()
    filename = now.strftime('%Y%m%d_%H%M%S%f_') + file.filename

    # 003. 업로드된 파일 저장 TODO. (향후 S3로 변경)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    upload_s3_image(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                    S3_BUCKET,
                    ORIGINAL_FOLDER + filename)

    # 004. aws rekognition 추론하기 TODO. (향후 S3로 변경)
    photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    min_confidence = 66
    rekog_response, rekog_image = show_custom_labels(
        MODEL, photo, min_confidence)

    # 005. 추론된 이미지 image 저장하기 TODO. (향후 S3로 변경)
    rekog_file_name = '[Inferred]'+filename
    rekog_image.save(os.path.join(
        app.config['UPLOAD_FOLDER'], rekog_file_name))
    upload_s3_image(os.path.join(app.config['UPLOAD_FOLDER'], rekog_file_name),
                    S3_BUCKET,
                    INFERRED_FOLDER + rekog_file_name)

    # 06. image 분석 결과 받아오기
    analysis = get_detection_info(rekog_response)

    # 07. 임시파일 삭제
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], rekog_file_name)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], rekog_file_name))

    # 임시
    # rekog_file_name = filename
    # rekog_response = {}
    # analysis = []

    return jsonify(
        downLoadUrl=request.url_root + 'api/download/inferred/' + rekog_file_name,
        rekog_response=rekog_response,
        analysis=analysis
    )


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.debug = True
    app.run()
