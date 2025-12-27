import webbrowser
from my_class import htmlstr

file_path = "D:\\文档\\Research diary\\RESEARCH DIARY.html"
file_path2 = "D:\\文档\\Research diary\\type_in.html"
# load the file
f = open(file_path, 'r')
origin_content = f.read()
f_content = htmlstr(origin_content)
# print(f_content)
f.close()

now = f_content.time
year = input('please input the year: ')

wrong = 0

if int(year) == now.year:
    print('correct!')
else:
    wrong += 1
    print('Are you sure?')
month = input('please input the month: ')
if int(month) == now.month:
    print('correct!')
else:
    wrong += 1
    print('Are you sure?')
date = input('please input the date: ')
if int(date) == now.day:
    print('correct!')
else:
    wrong += 1
    print('Are you sure?')
if wrong != 0:
    exit()
    
f2 = open(file_path2, 'r')
text = f2.read()
f2.close()
types = input('daily_thoughts, dialogs or interesting_things?(1,2 or 3): ')
if int(types) == 1:
    f_content.add_daily_thoughts(year, month, date, text)
    f = open(file_path, 'w')
    f.write(f_content.c)
    f.close()
if int(types) == 2:
    version = '1.20'
    dialog_text = '<p>'+'Version'+version+' '+str(now.time())+'</p>'+text
    f_content.add_content_general(dialog_text, str('''</div name = 'dialog' class="content">'''))
    f = open(file_path, 'w')
    f.write(f_content.c)
    f.close()
if int(types) == 3:
    #Program:[(HTML,CSS,JS),Python]
    #physics:[condensed matter field theory]
    f_content.add_interesting_things('physics','condensed matter field theory',text)
    f = open(file_path, 'w')
    f.write(f_content.c)
    f.close()
webbrowser.open_new_tab(file_path)
check = input('Is there any problem?(yes or no): ')
if check == 'no':
    f.close()
    f2 = open(file_path2, 'w')
    f2.close()
else:
    f = open(file_path, 'w')
    f.write(origin_content)
    f.close()
