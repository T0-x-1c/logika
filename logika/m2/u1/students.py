class Student():
    def __init__(self, name, sername, mark):
        self.name = name
        self.sername = sername
        self.mark = mark


students = []

with open('studens.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split(' ')
        obj = Student(data[0], data[1], int(data[2]))
        students.append(obj)

for f in students:
    if f.mark == 5:
        print(f.name, f.sername, f.mark)
