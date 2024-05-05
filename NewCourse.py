import re
import requests

class Course:
    '''
    芯位教育新版刷课脚本
    '''
    def __init__(self,classId,cookies):
        # self.cookies = cookies
        print(re.search(r'Authorization=(\S+);',cookies).group(1))
        self.classId = classId

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Authorization': re.search(r'Authorization=(\S+);',cookies).group(1),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': str(cookies),
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
    def EnterSession(self,session_id):
        response = requests.post(
        'https://www.51xinwei.com/api/learning-service/admin/studentLearning/getSingleChapterData/'+session_id,
        # cookies=self.cookies,
        headers=self.headers,
        )
        print(response.text)

    def videoLearnProcessReport(self,session_id,studyTime,totalTime):
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
                'teachingclassId': self.classId,
            }

            response = requests.post(
                'https://www.51xinwei.com/api/learning-service/admin/studentLearning/videoLearnProcessReport',
                cookies=self.cookies,
                headers=self.headers,
                json=json_data,
            )

            print(response.text)

    def getChapterData(self):
        '获取学习信息'

        LearnTasks = []
        json_data = {'teachingclassId': self.classId,}

        response = requests.post(
            'https://www.51xinwei.com/api/learning-service/admin/studentLearning/getChapterData',
            # cookies=self.cookies,
            headers=self.headers,
            json=json_data,
        )
        print(response.text)
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



    def start(self):
        '开始刷课'

        LearnTasks = self.getChapterData()

        for i in LearnTasks:
            self.EnterSession(i[0])
            self.videoLearnProcessReport(i[0],i[1],i[2])

        print('刷课结束亦或未发现未完成任务')

if __name__ == '__main__':

    classId = '8d78bc9b1357076113cf7b48cb3972d7'   #课程ID编号
    cookies = 'acw_tc=784e2c9117149378338908532e2d3b984c7c8e7079ff99dd10e5438046105c; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; loginToken=070d1cd2-eb37-46c6-8777-439906f6f5dd; JSESSIONID=E77BF31F2853DCFBC27317048AFBA377'    #输入cookie
    course = Course(classId,cookies)
    course.start()