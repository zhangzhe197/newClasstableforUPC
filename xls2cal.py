import pandas as pd
import datetime
import re,math
class ICalendar:
    mainICS = ''
    #这里输入这个学期的第一周的第一个星期一的具体日期
    termStartDate = datetime.datetime(2025,2,23)        # you should put the date of first Sunday of one term, which is the first day of the week
    def getFormatedTime(self, week, day):
        # week starts from 1, day is between 0 and 6 
        target_time = self.termStartDate + datetime.timedelta(weeks=week - 1, days=day)
        return target_time.strftime("%Y%m%d")
    
    def getClassTime(self,section, schoolTime):
        section_long = [['080000','093500'], ['095500','122000'], ['140000','153500'],['155500','173000'],['190000','212500']]
        section_sort = [['080000','093500'], ['095500','113000'], ['140000','153500'],['155500','173000'],['190000','203000']]
        if (section == 2 and schoolTime == '04') or (section == 5 and schoolTime == '11'):
            return section_sort[section - 1]
        else : 
            return section_long[section - 1]
        
    def addClassEvent(self, className, week, day , section, schoolTime, location, classAndTeacher):
        st, ed = self.getClassTime(section, schoolTime)
        event = f'''BEGIN:VEVENT
DTSTART:{self.getFormatedTime(week, day)}T{st}
DTEND:{self.getFormatedTime(week, day)}T{ed}
DESCRIPTION:{classAndTeacher}
LOCATION:{location}
STATUS:CONFIRMED
SUMMARY:{className}
END:VEVENT
'''
        self.mainICS += event
        return
    

    def exportResult(self):
        st = '''BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:zhangzhe197109@gmail.com
X-WR-TIMEZONE:Asia/Shanghai
'''
        ed = 'END:VCALENDAR'
        return st + self.mainICS + ed


class Course:
    def __init__(self,courseStr:str, weekDay:int,section):
            infoList = list(filter(None, courseStr.split('\n')))
            self.section = section
            self.couresName = infoList[0]
            self.teacherName = infoList[2]
            self.weekList = []
            rangedList =  infoList[3].split('(')[0].split(',')
            for weekRange in rangedList:
                if '-' in weekRange:
                    st, ed = weekRange.split('-')
                    self.weekList += [week for week in range(int(st), int(ed) + 1 )]
            self.Location = infoList[4]
            self.weekday = weekDay
            self.schoolTime = extract_text_in_brackets(infoList[3])[3:5]

    def sendToCalendar(self):
        for week in self.weekList:
            calendar.addClassEvent(self.couresName, week, self.weekday, 
                                   self.section, self.schoolTime, self.Location, self.teacherName)

def readXls(filepath, sheet_name=0, output_filepath=None, **kwargs):
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name, engine='xlrd', **kwargs)  # 使用 xlrd 引擎读取 xls 文件
        return df[2:]
    except FileNotFoundError:
        print(f"找不到文件: {filepath}")
        raise
    except Exception as e:
        print(f"读取或处理 XLS 文件时出错: {e}")
        raise

def extract_text_in_brackets(text):
    """提取字符串中括号内的文本。"""
    match = re.search(r"\[(.*?)节\]", text)
    if match:
        return match.group(1)
    return None  # 或返回空字符串 ""

def processDF(df: pd.DataFrame):
    for section, row in df.iterrows():
        for weekday , data in enumerate(row[1:]):
            if type(data) == str:
                classlist = data.split("\n\n")
                for item in classlist:
                    if not item.isspace():
                        coures = Course(item, (weekday + 1) % 7, section - 1 )
                        coures.sendToCalendar()
            else :pass
calendar = ICalendar()                                  
classdf = readXls('/home/zhangzhe/Downloads/tar.xls')  # 这里输入你的导出的文件的路径
processDF(classdf)
with open("classtable.ics",'w',encoding='utf-8') as f:
        f.write(calendar.exportResult())
        f.close()
