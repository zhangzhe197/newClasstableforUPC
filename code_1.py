import requests,pdb,time,datetime,re
from bs4 import BeautifulSoup
def showCookies(cookies):
    for cookie in cookies:
        print(f"{cookie.name} = {cookie.value}")
def cookieOutput(cookies):
    res = ''
    for cookie in cookies:
        res += f"{cookie.name}={cookie.value};"
    return res[:-1]
def getGeneralGetHeaders(cookies):
        headers3 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-encoding": "gzip, deflate, br, zstd",
        "Accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-control": "max-age=0",
        "Priority": "u=0, i",
        "Sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "Sec-ch-ua-mobile": "?0",
        "Sec-ch-ua-platform": "\"Windows\"",
        "Sec-fetch-dest": "document",
        "Sec-fetch-mode": "navigate",
        "Sec-fetch-site": "cross-site",
        "Sec-fetch-user": "?1",
        "Upgrade-insecure-requests": "1",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        'Cookie' : cookieOutput(cookies)
    }
        return headers3
def postHeadersGeneral(cookies,payload):
     headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'cas.upc.edu.cn',
    'Origin': 'https://cas.upc.edu.cn',
    'Referer': 'https://cas.upc.edu.cn/cas/login?service=http://jwxt.upc.edu.cn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-length': str(len(payload)),
    'Cookie' : cookieOutput(cookies)
    }
     return headers2
def postHedersLoggedin(cookies,payload):
    headers2 = {
        ':authority:': 'jwxt.upc.edu.cn',
        ':method:': 'POST',
        ':path:': '/jsxsd/xskb/xskb_list.do',
        ':scheme:' : 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://jwxt.upc.edu.cn',
        'Referer': 'https://jwxt.upc.edu.cn/jsxsd/xskb/xskb_list.do',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-length': str(len(payload)),
        'Cookie' : cookieOutput(cookies)
    }
    return headers2

class ICalender:
    mainICS = ''
    termStartDate = datetime.datetime(2024,9,2)
    def getFormatedTime(self, week, day):
        # week starts from 1, day is between 0 and 6 
        target_time = self.termStartDate + datetime.timedelta(weeks=week - 1, days=day - 1)
        return target_time.strftime("%Y%m%d")
    
    def getClassTime(self,section, schoolTime):
        section_long = [['080000','093500'], ['095500','122000'], ['140000','153500'],['155500','173000'],['190000','212500']]
        section_sort = [['080000','093500'], ['095500','113000'], ['140000','153500'],['155500','173000'],['190000','203000']]
        if (section == '2' and schoolTime == '03') or (section == '5' and schoolTime == '10'):
            return section_sort[section - 1]
        else : 
            return section_long[section - 1]
        
    def addClassEvent(self, className, week, day , section, schoolTime, location, classAndTeacher):
        st, ed = self.getClassTime(section, schoolTime)
        event = f'''BEGIN:VEVENT
DTSTART:{self.getFormatedTime(week, day)}T{st}Z
DTEND:{self.getFormatedTime(week, day)}T{ed}Z
DESCRIPTION:{classAndTeacher}
LOCATION:{location}
SUMMARY:{className}
END:VEVENT
'''
        self.mainICS += event
        return
    

    def exportResult(self):
        st = '''BEGIN:VCALENDAR 
VERSION:2.0 
CALSCALE:GREGORIAN 
METHOD:PUBLISH 
X-WR-TIMEZONE:Asia/Shanghai
'''
        ed = 'END:VCALENDAR'
        return st + self.mainICS + ed
        
username = '*****************'
password = '*****************'  
with requests.session() as session:
    #============================================================================
    # First Request to get execution code
    session.cookies.update({"service": "http://jwxt.upc.edu.cn/"})
    url = "https://cas.upc.edu.cn/cas/login?service=http://jwxt.upc.edu.cn/"
    para = {'service':'http://jwxt.upc.edu.cn/'}
    headers1 = getGeneralGetHeaders(session.cookies)
    resp = session.get(url=url, headers=headers1)
    soup = BeautifulSoup(resp.text,features="html.parser")
    execution = soup.find_all('input' , {'name':'execution'})[0]['value'] 
    #============================================================================
    #============================================================================
    # Second Request to post password
    url = "https://cas.upc.edu.cn/cas/login?service=http://jwxt.upc.edu.cn/"
    payload=f'username={username}&password={password}&submit=LOGIN&type=username_password&_eventId=submit&execution={execution}'
    headers2 = postHeadersGeneral(session.cookies, payload)
    response = session.post( url=url, headers=headers2, data=payload)
    #============================================================================
    # Third and Fourth to get cookies
    try:
        nextLocation = response.history[0].url
    except:
        nextLocation = response.url
    headers3 = getGeneralGetHeaders(cookies=session.cookies)
    nextResp = session.get( url=nextLocation, headers=headers3)
    finalResp = session.get(url=url, headers=getGeneralGetHeaders(session.cookies))
    #============================================================================
    print(f"logged in as {username} successfully")
# try to get classtable now
    time.sleep(1)
    url_Classtable = 'https://jwxt.upc.edu.cn/jsxsd/xskb/xskb_list.do'
    mainClasstable = session.get(url=url_Classtable, headers=getGeneralGetHeaders(session.cookies))
    mainClassSoup = BeautifulSoup(mainClasstable.text,features="html.parser")
    res = mainClassSoup.find_all('select', {'id': 'kbjcmsid'})
    code = BeautifulSoup(str(res[0]),features="html.parser").find_all('option')[0]['value']



    calender = ICalender()

# get classtable for every week 
    for week in range(1, 21):
        print(f"getting classtable of week{week}")
        time.sleep(1.5)
        payload_class = f"cj0701id=&zc={week}&demo=&xnxq01id=2024-2025-1&sfFD=1&wkbkc=1&kbjcmsid={code}"
        classTableWeekly = session.post(url=url_Classtable, headers=postHeadersGeneral(session.cookies, payload_class),data=payload_class)
        weekSoup = BeautifulSoup(classTableWeekly.text,features="html.parser")
        trs = weekSoup.find('table', id='timetable').find_all('tr')
        for section, tr in enumerate(trs):
            tds = tr.find_all('td')
            for day, td in enumerate(tds):
                try:
                    content = td.find_all('font')
                    className = content[0].find_all("br")[0].previous_sibling
                    pattern = r"\[(\d+)-(\d+)节\]"
                    schoolTime = re.findall(pattern,td.text)[0][0]
                    location = td.find_all('font', {'title': '教室'})[0].text
                    classAndTeacher = td.find_all('font', {'title': '教师'})[0].text
                    calender.addClassEvent(className, week, day , section, schoolTime, location, classAndTeacher)

                    # debug
                    # print(f"section = {section} day = {day} \n {calender.mainICS}" )
                    # pdb.set_trace()
                except: 
                    continue
    with open("classtable.ics",'w',encoding='utf-8') as f:
        f.write(calender.exportResult())
        f.close()


    

