import requests

class Start:
    def __init__(self,courseId,cookie):
        self.courseId = courseId
        self.not_learn = []
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'https://teaching.51xinwei.com',
            'Pragma': 'no-cache',
            'Referer': 'https://teaching.51xinwei.com/learning/student/studentIndex.action',
            'Cookie': cookie,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'dataType': 'json',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
    def requests(self,itemId):
        '单次请求视频进度保存'
        params = {'functionCode': 'sendVideoLearnRecord',}
        data = {
            'courseId': self.courseId,
            'itemId': itemId,
            'recordCount': '60',
            'playPosition': '70.436051',
            'playbackRate': '1',
            'key': '1686631761301',
        }

        response = requests.post(
            'https://www.51xinwei.com/learning/student/studentDataAPI.action',
            params=params,
            headers=self.headers,
            data=data,verify=False)
        print(response.text)

    def GetNotLearnItems(self):
        '获取学习内容 提取出未学习项次及其时长'
        params = {'functionCode': 'queryVideoLearningProcessDetail',}
        data = {'courseId': self.courseId,}
        response = requests.post(
            url='https://www.51xinwei.com/learning/student/studentDataAPI.action',
            params=params,
            headers=self.headers,
            data=data,verify=False
            )

        js = response.json()
        for i in js['videoLearningObj']['videoLearningInfoList']:
            print(i['title'],end='    ')
            print(i['id'],end='    ')
            if i['status'] == 0 or i['status'] == 1:
                print('未学习')
                self.not_learn.append([i['id'],int((i['completeTime']-i['finishTime']) / 60 )+1]) #[[当前视频ID,剩余未学习时长]...]
                continue
            else:
                print('学习完')

    def queryVideoItemDetail(self,itemId):
        '刷取新视频前需要先进入这个页面  以免警告'
        params = {'functionCode': 'queryVideoItemDetail',}
        data = {'courseId': self.courseId,'itemId': itemId,}
        response = requests.post(
            'https://www.51xinwei.com/learning/student/studentDataAPI.action',
            params=params,
            headers=self.headers,
            data=data,verify=False)

    def main(self):

        self.GetNotLearnItems()  #获取未学习项次及其时长

        if self.not_learn != []:
            print('开始刷取')
            for i in self.not_learn:
                self.queryVideoItemDetail(i[0])
                for a in range(i[1]):
                    self.requests(i[0])
            print('结束')
        else:
            print('未发现仍未完成的视频项目')

if __name__ == '__main__':

    courseId = ''   #课程ID编号
    
    cookies = ''    #输入cookie

    start = Start(courseId,cookies)
    start.main()



