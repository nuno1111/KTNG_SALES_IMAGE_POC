# POSM 종류
posm_list = ['TOP_ADV', 'CDU', 'MAT', 'ADV']


def get_detection_info(response):

    detection_info_list = []

    detection_id = 0

    for customLabel in response['CustomLabels']:
        detection_info = {}

        # 0. id
        detection_info['id'] = detection_id
        detection_id = detection_id + 1

        # 1. POSM 유형 : posm
        posm = str(customLabel['Name'])
        detection_info['posm'] = posm

        # 2. 감지여부 : detected
        detection_info['detected'] = 'SUCCESS'

        # 3. 상대위치 : position
        box = customLabel['Geometry']['BoundingBox']
        left = box['Left']
        width = box['Width']
        center = round(100 * (left + width / 2), 2)
        detection_info['position'] = center

        # 4. 상태 : status
        if(posm == 'TOP_ADV'):
            if(center >= 40 and center <= 60):
                detection_info['status'] = 'GOOD'
            else:
                detection_info['status'] = 'BAD'
        elif(posm == 'MAT'):
            if(center >= 40 and center <= 60):
                detection_info['status'] = 'GOOD'
            else:
                detection_info['status'] = 'BAD'
        else:
            detection_info['status'] = 'None'

        detection_info_list.append(detection_info)

    # 99. posm 중 detect이 되지 않았던게 있다면,

    if (len(posm_list) > len(detection_info_list)):

        for posm in posm_list:

            is_find = False
            for detection_info in detection_info_list:
                if posm == detection_info['posm']:
                    is_find = True

            if(not is_find):
                detection_info = {}

                # 0. id
                detection_info['id'] = detection_id
                detection_id = detection_id + 1

                # 1. POSM 유형 : posm
                detection_info['posm'] = posm

                # 2. 감지여부 : detected
                detection_info['detected'] = 'FAIL'

                # 3. 상대위치 : position
                detection_info['position'] = 0

                # 4. 상태 : status
                detection_info['status'] = 'None'
                
                detection_info_list.append(detection_info)

    return detection_info_list
