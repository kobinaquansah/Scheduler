import re
import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

responsibility=pd.read_csv("responsibility_input.csv")
availability=pd.read_csv("available_slots_input.csv")

class InputParse():
    @staticmethod
    def clean_(entry):
        entry.set_index(entry.columns[0],inplace=True)
        entry=entry.drop_duplicates()
        return(entry)
    @staticmethod
    def clean(entry):
        cleaned=[]
        for i in range(len(entry)):
            cleaned.append(InputParse.clean_(entry[i]))
        return(cleaned[0],cleaned[1])

availability,responsibility=InputParse().clean([availability,responsibility])
class_pseudo={}
for i in range(len(responsibility.columns)):
    class_pseudo.update({chr(i+65):list(responsibility.columns)[i]})
responsibility.columns=list(class_pseudo.keys())
for i in range(len(responsibility.columns)):
    responsibility.iloc[:,i]=responsibility.iloc[:,i].map(lambda x: f'{x}*"{responsibility.columns[i]}"')
responsibility

responsibility_list=[]
for i in range(len(responsibility.index)):
    responsibility_list.append(' '.join(list(responsibility.iloc[i])).split())
    responsibility_list[i]=list(map(eval,responsibility_list[i]))
    responsibility_list[i]=np.array(responsibility_list[i])[np.where(np.array(responsibility_list[i])!='')]
    responsibility_list[i]=(list(''.join(responsibility_list[i])))    

availability=np.array(availability, dtype='str')

class Teacher():
    lister=[]
    def __init__(self,class_list,slots):
        self.class_list=class_list
        self.combinations=[]
        self.schedules=[]
        self.arrangements=[]
        self.slots=slots
        self.co_schedules=dict({})
    
    def addCombination(self,combination):
        if combination not in self.combinations:
            self.combinations.append(combination)  
    
    def AddSchedule(self,schedule):
        self.schedules.append(schedule)

for i in range(len(responsibility_list)):
    a=Teacher(responsibility_list[i],availability[i])
    Teacher.lister.append(a)

for j in range(len(availability)):
    print(j)
    for i in range(100):
        v=random.sample(list(np.where(availability[j]=='0')[0]),len(Teacher.lister[j].class_list))
        v.sort()
        Teacher.lister[j].addCombination(v)

for j in range(len(availability)):
    arrangements=[]
    for i in range(1000):
        object_=Teacher.lister[j].class_list
        sample_size=len(object_)
        prob=random.sample(object_,sample_size)
        if prob not in arrangements:
            arrangements.append(prob)
    Teacher.lister[j].arrangements=arrangements
    
for k in range(len(Teacher.lister)):
    for j in range(len(Teacher.lister[k].combinations)):
        for i in range(len(Teacher.lister[k].arrangements)):
            new_slots=np.array(Teacher.lister[k].slots)        
            new_slots[Teacher.lister[k].combinations[j]]=Teacher.lister[k].arrangements[i]
            if str(new_slots) not in list(map(str,Teacher.lister[k].schedules)):
                Teacher.lister[k].AddSchedule(new_slots)
            else:
                pass
        percentage=round((j/len(Teacher.lister[k].combinations))*100,2)
        print(f'Teacher {k} {percentage} % complete')

df=[]
for i in range(len(Teacher.lister)):
    df.append(pd.DataFrame(Teacher.lister[i].schedules))
print('complete')

time_slots=["8:30-9:00","9:00-9:30","10:30-11:00","11:00-11:30","11:30-12:00","12:00-12:30"]
day_list=["M","T"]
new_slots=[]
for i in range(len(day_list)):
    new_slots.extend(list(map(lambda x: x+str(day_list[i]), time_slots)))

number_of_comparisons=np.math.factorial(len(df)-1)
indices=np.arange(0,6)
comb=[]
i=0
j=0
switch=0
while i<len(indices):
    if j<len(indices):
        if (indices[i]!=indices[j]):
            comb.append([f'df[{indices[i]}]',f'df[{(indices[j])}]'])
        else:
            pass
        j=j+1
    else:
        i=i+1
        j=0+switch+1
        switch=switch+1

class Schedules():
    schedules=[]
    hash_values=set()
    columns=[]
    
    @classmethod
    def producecolumnlist(cls):
        columns=["Teacher"]
        new_slots=[]
        for i in range(len(day_list)):
            new_slots.extend(time_slots)
        columns.extend(new_slots)
        cls.columns=columns
    
    def __init__(self,schedule):
        self.schedule=schedule

    @classmethod
    def add(cls,schedule):        
        a=[]
        for i in range(schedule.shape[0]):
            a.extend(''.join(list(schedule.loc[i])))
        hashed=hash(''.join(a))
        if hashed not in cls.hash_values:
            schedule=cls.indexedit(schedule)
            schedule.columns=cls.columns
            Schedules(schedule)
            cls.schedules.append(schedule)
            cls.hash_values.update({hashed})
            print(f'unique timetable count: {len(cls.schedules)}')
            return(1)
        else:
            return(0)
            pass
    
    @classmethod
    def indexedit(cls,schedule):
        for class_name in class_pseudo:
            schedule=schedule.applymap(lambda x:re.sub(fr"\b{class_name}\b",class_pseudo[class_name],x))
        schedule.reset_index(inplace=True)
        column_list=list(schedule.columns)
        column_list[0]="Teacher ID"
        schedule.columns=column_list
        return(schedule)
    
    @classmethod
    def verifyuniqueness(cls):
        non_unique={}
        unique_count=0
        base=False
        sample_space=list(range(0,len(cls.schedules)))
        while (len(sample_space)>0):
            if base==True:
                break
            pop_sample=random.sample(range(0,len(sample_space)),1)[0]
            sample=sample_space.pop(pop_sample)
            i=0
            while i<len(cls.schedules):
                if(any(cls.schedules[sample]!=cls.schedules[i])):
                    unique_count+=1
                    if unique_count>0.25*len(cls.schedules):
                        base=True
                        print('done')
                        break
                else:
                    non_unique.update(cls.schedules[i])
                i+=1

Schedules.producecolumnlist()
schedule_list=[]
Schedules.schedules=[]
time_slots.extend(time_slots)
pre_hashed=set()
pseudo_list=list(class_pseudo.keys())

def createschedules():
    while True:
        index=list(range(len(Teacher.lister)))
        sample=[]
        for i in range(len(index)):
            sample.append(random.sample(list(range(0,len(Teacher.lister[i].schedules))),1)[0])
        lists=[]
        for i in range(len(sample)):
            lists.append(list(Teacher.lister[i].schedules[sample[i]]))
        listed=pd.DataFrame(lists)
        unique=[]
        i=0
        while i<(listed.shape[1]):
            occurence_bool=pd.Series(listed[i].value_counts().keys()).map(lambda x: x in pseudo_list)
            occurences=listed[i].value_counts().iloc[np.where(occurence_bool==True)]
            try:
                max(occurences)
            except ValueError:
                occurences=[0,2]
            if max(occurences)>1:
                break
            else:
                i+=1
                continue
        if i==(listed.shape[1]):
            returned=Schedules.add(listed)
        if len(Schedules.schedules)==10:
            break

createschedules()
