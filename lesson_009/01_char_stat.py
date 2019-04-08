# -*- coding: utf-8 -*-
import zipfile
import os
import pprint


# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
# Ширину таблицы подберите по своему вкусу

class CharStat:

    # TODO Раз реализовано немного больше чем указано в задании, то необходимо
    # TODO передавать немного больше аргументов (path_to_archive, path_to_file,
    # TODO filename_in_archive).
    # TODO Это необходимо, чтобы извлечение файла из архива было более
    # TODO правильным и корректно обрабатывалась ситуация, когда в архиве может
    # TODO быть несколько файлов можно было проверить есть в архиве нужный
    # TODO файл или нет.
    def __init__(self, file_path):
        self.file_path = file_path
        self.dir_path = os.path.dirname(self.file_path)
        self.file_name = None
        self.stat = {}
        self.count_char = 0
        print(file_path)
        if zipfile.is_zipfile(file_path):
            self.unzip()
        else:
            self.file_name = os.path.basename(file_path)

    def print_header(self):
        # TODO Это лишнее усложение, не нужно текст заголовка выносить в
        # TODO отедельную переменную
        header = ('буква', 'кол-во')
        print(f'')
        print('+', f'{chr(45):-^9}', '+', f'{chr(45):-^10}', '+', sep='')
        print('|', f'{header[0]: ^9}', '|', f'{header[1]: ^10}', '|', sep='')
        print('+', f'{chr(45):-^9}', '+', f'{chr(45):-^10}', '+', sep='')

    def print_result(self):
        # TODO Это лишнее усложение, не нужно текст заголовка выносить в
        # TODO отедельную переменную
        res = 'Итого'
        print('+', f'{chr(45):-^9}', '+', f'{chr(45):-^10}', '+', sep='')
        print('|', f'{res: ^9}', '|', f'{self.count_char: ^10}', '|', sep='')
        print('+', f'{chr(45):-^9}', '+', f'{chr(45):-^10}', '+', sep='')

    def print_body(self):
        if not self.stat:
            self.get_stat()

        for char, cnt in sorted(self.stat.items()):
            # TODO Пробельный символ, это не часть алфавита, это условие не
            # TODO имеет смысла
            if char == 10:
                symbol = 'enter'
            else:
                symbol = chr(char)
            print('|', f'{symbol: ^9}', '|', f'{cnt: ^10}', '|', sep='')

    def print_stat(self):
        self.print_header()
        self.print_body()
        self.print_result()

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_path, 'r')
        for filename in zfile.namelist():
            zfile.extractall(self.dir_path)
            self.file_name = filename

    def get_stat(self):
        with open(os.path.join(self.dir_path, self.file_name), mode='r', encoding='CP1251') as file:

            for line in file:
                for char in line:
                    if char.isalpha():
                        # TODO Обратите внимание на метод словрей setdefault
                        # TODO с его помощью можно упростить код и избавиться
                        # TODO от данного условия
                        if ord(char) in self.stat:
                            # TODO Строка может быть ключом словаря, нет ни
                            # TODO какого смысла хранить код символа, а не сроку
                            self.stat[ord(char)] += 1
                        else:
                            self.stat[ord(char)] = 1
                        self.count_char += 1

        return self.stat


if __name__ == '__main__':
    src_file_path = './python_snippets/voyna-i-mir.txt.zip'
    war_and_peace = CharStat(file_path=src_file_path)
    war_and_peace.print_stat()
