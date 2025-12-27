import webbrowser
from my_class import htmlstr

file_path = "D:\\文档\\Research diary\\RESEARCH DIARY.html"
# load the file
f = open(file_path, 'r')
origin_content = f.read()
f_content = htmlstr(origin_content)
# print(f_content)
f.close()

print(f_content.catalog_lvl)
print(f_content.c[4318:4550])
print(f_content.catalog_pos)
