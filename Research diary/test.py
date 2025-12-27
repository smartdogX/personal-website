from my_class import htmlstr,sort_catalog,modify,catalog_print
from datetime import datetime

now = datetime.now()
print(datetime.now().year)
def myFunc(a):
    return a[1]

file_path = "D:\\文档\\Research diary\\RESEARCH DIARY.html"
file_path2 = "D:\\文档\\Research diary\\type_in.html"
# load the file
f = open(file_path,'r')
f_content = htmlstr(f.read())
#print(f_content)
f.close()

#print(sort_catalog(['h','h','h1','h1','h2','h2']))

#print(f_content.catalog)

#print(f_content.cataloglist)

#print(f_content.get_content_general(['daily_thoughts'])[0])
f2 = open(file_path2,'r')
text = f2.read()

f_content.add_daily_thoughts(2024,11,20,text)

#print(f_content.c)
