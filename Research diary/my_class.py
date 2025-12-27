# htmlstr is used to deal with my research html

from datetime import datetime
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aus', 'Sep', 'Oct', 'nov', 'Dec']


def myFunc(a):
    return a[1]


def sort_catalog(clist):
    sort_catalog_list = []
    if len(modify(clist)[0]) == 0 and len(modify(clist)[1]) == 0:
        sort_catalog_list += [clist[0]]
    if len(modify(clist)[0]) != 0 and len(modify(clist)[1]) == 0:
        sort_catalog_list += [clist[0], sort_catalog(modify(clist)[0])]
    if len(modify(clist)[0]) == 0 and len(modify(clist)[1]) != 0:
        sort_catalog_list += [clist[0]]
        sort_catalog_list += sort_catalog(modify(clist)[1])
    if len(modify(clist)[0]) != 0 and len(modify(clist)[1]) != 0:
        sort_catalog_list += [clist[0], sort_catalog(modify(clist)[0])]
        sort_catalog_list += sort_catalog(modify(clist)[1])
    return sort_catalog_list


deep = -1


def catalog_print(catalog_list):
    global deep
    catalog_str = str()
    catalog_str_list = []
    if type(catalog_list) is str:
        catalog_str += deep*'\t' + catalog_list+'\n'
        catalog_str_list.append([catalog_list,deep])
    else:
        deep += 1
        for i in catalog_list:
            catalog_str += catalog_print(i)[0]
            catalog_str_list += catalog_print(i)[1]
        deep -= 1
    return catalog_str,catalog_str_list

def modify(list):
    count = 0
    for i in range(1, len(list)):
        if list[i] == list[0]:
            count = i
            break
    return list[1:count], list[count+1:]


class htmlstr():
    def __init__(self, content, time=datetime.now(), version=1.10):
        self.c = content
        self.catalog = catalog_print(sort_catalog(self.get_catalog()))[0]
        self.cataloglist = sort_catalog(self.get_catalog())
        self.catalog_lvl = catalog_print(sort_catalog(self.get_catalog()))[1]
        self.catalog_pos = self.get_catalog_pos()
        self.time = time
        
        self.version = version
    def get_catalog_pos(self):
        cataloglvl = self.catalog_lvl
        catalogpos = []
        for i in range(len(cataloglvl)):
            start = '<'+str(cataloglvl[i][0])+'>'
            end = '</'+str(cataloglvl[i][0])+'>'
            
            if i == 0:
                start_point = self.c.find(start)
                end_point = self.c.find(end)
                
            else:
                if cataloglvl[i][1]<=cataloglvl[i-1][1]:
                    start_point = self.c.find(start,catalogpos[-1][1][1],len(self.c)-1)
                    end_point = self.c.find(end,start_point,len(self.c)-1)
                    if start_point == -1:
                        start_space = '<'+str(cataloglvl[i][0]) + ' '
                        start_point = self.c.find(start_space,catalogpos[-1][1][1],len(self.c)-1)
                    if end_point == -1:
                        end_space = '</'+str(cataloglvl[i][0])
                        end_point = self.c.find(end_space,start_point,len(self.c)-1)
                else:
                    start_point = self.c.find(start,catalogpos[-1][1][0],catalogpos[-1][1][1])
                    end_point = self.c.find(end,start_point,catalogpos[-1][1][1])
                    if start_point == -1:
                        start_space = '<'+str(cataloglvl[i][0])+ ' '
                        start_point = self.c.find(start_space,catalogpos[-1][1][0],catalogpos[-1][1][1])
                    if end_point == -1:
                        end_space = '</'+str(cataloglvl[i][0])
                        end_point = self.c.find(end_space,start_point,catalogpos[-1][1][1])
            catalogpos.append([cataloglvl[i][0],[start_point,end_point]])
        return catalogpos
    
    def get_catalog(self):
        name_list_s = []
        write_down_s = 0
        name_list_e = []
        write_down_e = 0
        for i in range(len(self.c)):
            if write_down_s == 1:
                if self.c[i] == '>':
                    end = i
                    write_down_s = 0
                    name_list_s.append((self.c[start:end], start))
            if self.c[i] == '<' and self.c[i+1] != '/':
                start = i+1
                write_down_s = 1
            if write_down_e == 1:
                if self.c[i] == '>':
                    end_e = i
                    write_down_e = 0
                    name_list_e.append((self.c[start_e:end_e], start_e))
            if self.c[i] == '<' and self.c[i+1] == '/':
                start_e = i+2
                write_down_e = 1
        new_name_list_s = []
        new_name_list_e = []
        for i in name_list_e:
            count = 0
            for j in name_list_s:
                if i[0] == j[0]:
                    count += 1
            if count != 0:
                new_name_list_s.append(i)
        for i in name_list_s:
            count = 0
            for j in name_list_e:
                if i[0] == j[0]:
                    count += 1
            if count != 0:
                new_name_list_e.append(i)

        l = new_name_list_s+new_name_list_e

        l.sort(key=myFunc)

        l_names = [x[0] for x in l]
        return l_names
        

    def get_content_general(self, path_list):
        content_list = []
        content_list.append(self.c)
        for i in path_list:
            start = '<' + i
            end = '</' + i + '>'
            start_point = content_list[-1].find(start)
            end_point = content_list[-1].find(end)+len(end)
            content_list.append(content_list[-1][start_point:end_point])
        return content_list

    def add_content_general(self, text, add_place):
        add_point = self.c.find(add_place)
        new_content = self.c[0:add_point] + \
            '\n' + text + '\n' + self.c[add_point:]
        self.c = new_content

    def add_daily_thoughts(self, year, month, date, text):
        thoughts_start = '<daily_thoughts>'
        thoughts_end = '</daily_thoughts>'
        year_start = '<year'+str(year)+'>'
        year_end = '</year'+str(year)+'>'
        month_start = '<'+month_list[int(month)-1]+'>'
        month_end = '</'+month_list[int(month)-1]+'>'
        date_start = '<date'+str(date)+'>'
        date_end = '</date'+str(date)+'>'
        thoughts_start_point = self.c.find(thoughts_start)
        thoughts_end_point = self.c.find(thoughts_end)
        if year_end in self.c[thoughts_start_point:thoughts_end_point]:
            year_start_point = self.c.find(
                year_start, thoughts_start_point, thoughts_end_point)
            year_end_point = self.c.find(
                year_end, thoughts_start_point, thoughts_end_point)
            if month_end in self.c[year_start_point:year_end_point]:
                date_end_point = self.c.find(
                    month_end, year_start_point, year_end_point)
                format_text = date_start+'\n'+'<h3>' + \
                    month_list[int(month)-1]+' '+str(date)+' '+str(datetime.now().time()) + \
                    '</h3>'+'\n'+text+'\n'+date_end+'\n'
            else:
                date_end_point = self.c.find(year_end)
                format_text = month_start + '\n' + date_start+'\n'+'<h3>' + \
                    month_list[int(month)-1]+' '+str(date)+' '+str(datetime.now().time())+'</h3>' + \
                    '\n'+text+'\n'+date_end+'\n' + month_end+'\n'
        else:
            date_end_point = thoughts_end_point
            format_text = year_start + '\n' + '<h2>' + str(year) + '</h2> ' + month_start + '\n' + date_start+'\n'+'<h3>'+month_list[int(
                month)-1]+' '+str(date)+' '+str(datetime.now().time())+'</h3>'+'\n'+text+'\n'+date_end+'\n' + month_end+'\n'+year_end+'\n'
        updated_content = self.c[:date_end_point] + \
            format_text + self.c[date_end_point:]
        self.c = updated_content
    def add_interesting_things(self,area,sub_area,text):
        intersting_things_start = '<interesting_things>'
        intersting_things_end = '</interesting_things>'
        area_start = '<'+str(area)+'>'
        area_end = '</'+str(area)+'>'
        sub_area_start = '<'+str(sub_area)+'>'
        sub_area_end = '</'+str(sub_area)+'>'
        i_date_start = '<date'+ str(datetime.now().year)+'.'+str(datetime.now().month)+'.'+str(datetime.now().day)+'>'
        i_date_end = '</date'+ str(datetime.now().year)+'.'+str(datetime.now().month)+'.'+str(datetime.now().day)+'>'
        things_start_point = self.c.find(intersting_things_start)
        things_end_point = self.c.find(intersting_things_end)
        if self.c.find(area_start,things_start_point,things_end_point) != -1:
            area_start_point = self.c.find(area_start,things_start_point,things_end_point)
            area_end_point = self.c.find(area_end,things_start_point,things_end_point)
            if self.c.find(sub_area_start,area_start_point,area_end_point) != -1:
                sub_area_end_point = self.c.find(sub_area_end,area_start_point,area_end_point)
                text_start_point = sub_area_end_point
                format_text = str(i_date_start)+'\n'+'<h4>'+str(datetime.now().year)+'.'+str(datetime.now().month)+'.'+str(datetime.now().day)+'</h4>'+'\n'+text+'\n'+str(i_date_end)
            else:
                text_start_point = area_end_point
                format_text = str(sub_area_start)+'\n'+'<h3>'+str(sub_area)+'</h3>'+'\n'+'\n'+str(i_date_start)+'\n'+'<h4>'+str(datetime.now().year)+'.'+str(datetime.now().month)+'.'+str(datetime.now().day)+'</h4>'+'\n'+text+'\n'+str(i_date_end)+str(sub_area_end)
        else:
            text_start_point = self.c.find(str('''</div name = 'title'
                                            class="content">'''))
            format_text = str(area_start)+'\n'+ '<h2>'+str(area)+'</h2>' +'\n'+ str(sub_area_start)+'\n'+'<h3>'+str(sub_area)+'</h3>'+'\n'+'\n'+str(i_date_start)+'\n'+'<h4>'+str(datetime.now().year)+'.'+str(datetime.now().month)+'.'+str(datetime.now().day)+'</h4>'+'\n'+text+'\n'+str(i_date_end)+'\n'+str(sub_area_end)+'\n'+str(area_end)
        updated_content = self.c[:text_start_point] + format_text + self.c[text_start_point:]
        self.c = updated_content