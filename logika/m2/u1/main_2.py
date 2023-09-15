with open('123.txt', 'r', encoding='utf-8') as file:
    file_text = file.read()

    print(file_text)

while True:
    avtor = input('Хто написав ці рядки?')
    avtor.lower()
    if avtor == 'тарас григорович шевченко' or 'тарас г. ш.':
        break
    else:
        print('Ні! Спробуй ще раз')

cutata = input('Хочеш добавити цитату(так\ні)')
cutata.lower()
if cutata == 'так' or 'да':
    input('Введіть цитату: ')
    input('Введіть автора: ')
elif cutata == 


with open('123.txt', 'r', encoding='utf-8') as file:
    file_text = file.read()

    print(file_text)