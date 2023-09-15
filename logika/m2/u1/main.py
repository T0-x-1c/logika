with open('123.txt', 'r', encoding='utf-8') as file:
    file_text = file.read()

    print(file_text)

avtor = input('Добав автора')

with open('123.txt', 'a', encoding='utf-8') as file:
    file_text = file.write(f'({avtor})')


with open('123.txt', 'r', encoding='utf-8') as file:
    file_text = file.read()

    print(file_text)