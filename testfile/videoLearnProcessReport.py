import requests


# cookies = {
#     'acw_tc': '784e2c9117149378338908532e2d3b984c7c8e7079ff99dd10e5438046105c',
#     'Authorization': '070d1cd2-eb37-46c6-8777-439906f6f5dd',
#     'Authorization': '070d1cd2-eb37-46c6-8777-439906f6f5dd',
#     'loginToken': '070d1cd2-eb37-46c6-8777-439906f6f5dd',
#     'JSESSIONID': 'E77BF31F2853DCFBC27317048AFBA377',
# }

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Authorization': '070d1cd2-eb37-46c6-8777-439906f6f5dd',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'acw_tc=784e2c9117149378338908532e2d3b984c7c8e7079ff99dd10e5438046105c; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; loginToken=070d1cd2-eb37-46c6-8777-439906f6f5dd; JSESSIONID=E77BF31F2853DCFBC27317048AFBA377',
    'Pragma': 'no-cache',
    'Referer': 'https://www.51xinwei.com/student/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}




def EnterSession(session_id):
    response = requests.post(
    'https://www.51xinwei.com/api/learning-service/admin/studentLearning/getSingleChapterData/'+session_id,
    #cookies=cookies,
    headers=headers,
    )
    print(response.text)

def videoLearnProcessReport(session_id,studyTime,totalTime,ClassId):
    '提交观看记录'
    if studyTime == None:
        studyTime = 0

    while studyTime < totalTime+30:

        studyTime+=30
        json_data = {
            'endPosition': studyTime,
            'itemId': session_id,
            'platform': 'web',
            'playPosition': studyTime,
            'playbackRate': 1,
            'recordCount': 9,
            'startPosition': studyTime,
            'teachingClassId': ClassId,
            # 'teachingCourseId': 'ae3b70ea8b1b1e62dc0bf53c05e69cb8',
            # 'userSsoId': 'e4c41ee9089146eaa146f9ca4b422c7d',
            # 'videoMilSeconds': 477520.0000000001,
        }

        response = requests.post(
            'https://www.51xinwei.com/api/learning-service/admin/studentLearning/videoLearnProcessReport',
            #cookies=cookies,
            headers=headers,
            json=json_data,
        )

        print(response.text)

def getChapterData(ClassId):
    '获取学习信息'

    LearnTasks = []
    json_data = {'teachingClassId': ClassId,}

    response = requests.post(
        'https://www.51xinwei.com/api/learning-service/admin/studentLearning/getChapterData',
        #cookies=cookies,
        headers=headers,
        json=json_data,
    )

    js = response.json()['data']
    for chapter in js:  #进入章节
        for unit in chapter['children']: #进入单元
            for session in unit['children']: #进入会话
                title = session['title']
                session_id = session['id']
                status = session['status']
                studyTime = session['studyTime']
                totalTime = session['totalTime']
                print('{}   {}   {}   {}   {}'.format(title,session_id,status,totalTime,studyTime))
                if status != 2:
                    LearnTasks.append([session_id,studyTime,totalTime])
    
    return LearnTasks



def main():
    ClassId = '8d78bc9b1357076113cf7b48cb3972d7'
    LearnTasks = getChapterData(ClassId)

    for i in LearnTasks:
        EnterSession(i[0])
        videoLearnProcessReport(i[0],i[1],i[2],ClassId)

main()