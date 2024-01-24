## 芯位教育刷网课视频脚本
一键刷完课程内视频

### 原理
目前`2024-1-24`芯位教育中有个bug，就是可以重复提交观看视频节点数据，从而达到一步刷完视频的效果。

说白了用py写了个简单的重复请求脚本

### 特性
- 跳过已完成学习内容
- 根据未学习视频长度调节请求次数

### 使用
下载python并且安装requests库，在文件里修改对应的cookie以及想要刷课的课程ID即可
#### courseId获取
在课程页面URL
![](https://raw.githubusercontent.com/Evileyesaint/51xinwei/main/id.png)

#### cookie获取
使用F12开发者工具 随便抓取一个包即可获取
![](https://raw.githubusercontent.com/Evileyesaint/51xinwei/main/cookie.png)


#### 开始
```
if __name__ == '__main__':
    courseId = ''   #课程ID编号
    cookies = ''    #输入cookie
    start = Start(courseId,cookies)
    start.main()
```
保存后运行即可,如果报错大概率是cookie不规范亦或是过期导致.

### 声明
仅用于学习与测试，不对任何后果负责。
