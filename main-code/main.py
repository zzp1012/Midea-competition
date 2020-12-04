from datetime import date

class good:
    def __init__(self,name,weight):
        self.name = name
        self.name = weight
        today = date.today()
        self.date = today.strftime("%b-%d-%y")
        self.last_weight = weight
    
    def get_name(self):
        return self.name
    
    def get_weight(self):
        return self.weight
    
    def get_date(self):
        return self.date
    
    def get_last_weight(self):
        return self.last_weight
        
    def add_weight(self,new_weight):
        self.weight += new_weight
        self.last_weight = new_weight
        
import os,sys

# Alternate to the working path
print('========= Access the local Path =========')
working_path = os.getcwd()
print("Previous Path:\t"+working_path)
# access the local path
        
print('========= Change the local Path =========')
target_path = "/home/pi/Desktop/camera"
os.chdir(target_path)   
# change working directory

path = os.getcwd()
print("Changed to:\t"+path)
# verifsy

file_current1 = "./res.txt"
f = open(file_current1,"r")
temp_lines = f.readlines()
f.close()
#read the file

if not temp_lines:
    exit(0)
#if files has not content, then exit the code.

temp_result = list()
for line in temp_lines:
    line = line.strip('\n')
    temp_result.append(line)
print(temp_result)
#split the temp results

temp_goods = []
for i in temp_result:
    str_list = i.split()
    name = str_list[0]
    weight = int(str_list[1])
    temp_goods.append(good(name,weight))
#get the list of instances of goods
    
temp_goods2 = temp_goods
temp_goods = []

for i in temp_goods2:
    if not temp_goods:
        temp_goods.append(i)
    else:
        temp_check = 0
        for j in temp_goods:
            if i.get_name() == j.get_name():
                temp_check = 1
                j.add_weight(i.get_weight())
                break
        if temp_check == 0:
            temp_goods.append(i)

file_current2 = "./final_res.txt"
f = open(file_current2,"r")
final_lines = f.readlines()
f.close()

final_goods = []
if not final_lines:
    final_goods = temp_goods 
    
else:
    final_result = list()
    for line in final_lines:
        line = line.strip('\n')
        final_result.append(line)
    print(final_result)
    
    for i in final_result:
        str_list = i.split()
        name = str_list[0]
        weight = int(str_list[1])
        final_goods.append(good(name,weight))

    for i in final.goods:
        for j in temp_goods:
            if i.get_name() == j.get_name():
                i.add_weight(j.get_weight())
    for i in temp_goods:
        check_lock = 0
        for j in final_goods:
            if i.get_name() == j.get_name():
                check_lock = 1
                break
        if check_lock == 0:
            final_goods.append(i)
    
for i in final_goods:
    f = open(file_current2,"w+")
    if i.get_weight() < 0:
        last_message = "at"+i.get_date()+i.get_name()+"lose"+str(i.get_last_weight())+"g"
    else:
        last_message = "at"+i.get_date()+i.get_name()+"gain"+str(i.get_last_weight())+"g"
    f.write("%s %d %s\n" % (i.get_name(),i.get_weight(),last_message))
f.close()
    
        