import time

class Student():
    def __init__(self, name, sername, mark):
        self.name = name
        self.sername = sername
        self.mark = mark

start_time = time.time()

students = []

all_mark = []

with open('studens.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split(' ')
        obj = Student(data[0], data[1], int(data[2]))
        students.append(obj)

for student in students:
    if student.mark == 5:
        print(student.name, student.sername, student.mark)


all_mark.append(student.mark)
GPA = sum(all_mark) / len(all_mark)
print(GPA)

finish_time = time.time()

elapsed_time = finish_time - start_time

print(f'Часу потрібно для читання файлу: {elapsed_time:.5f}')

print('-----------------------')

start_time = time.time()

students = []

all_mark = []

with open('students_large.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split(' ')
        obj = Student(data[0], data[1], int(data[2]))
        students.append(obj)

for student in students:
    if student.mark == 5:
        print(student.name, student.sername, student.mark)


all_mark.append(student.mark)
GPA = sum(all_mark) / len(all_mark)
print(GPA)

finish_time = time.time()

elapsed_time = finish_time - start_time

print(f'Часу потрібно для читання файлу: {elapsed_time:.5f} cек')
print('тут іде більше часу тому що , наш код прочитує кожну строку з/n студентами а їх тут більше , тому і наш код просчитує файл довше')
