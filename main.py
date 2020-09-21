import sys
import time
import argparse
from itertools import islice


def createParser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f1')
    parser.add_argument('-f2')
    parser.add_argument('-s')
    parser.add_argument('-e')
    return parser


def readFile(path, start=0, end=0):
    if start > end or start < 0 or end < 0:
        return "ERROR START END"
    text = []
    with open(path, 'r', encoding="UTF-8") as fs:
        # ЧИТАЕМ ВЕСЬ ФАЙЛ
        if start == 0 and end == 0:
            text = fs.readlines()
        # ЧИТАЕМ ТОЛЬКО СТРОКИ
        else:
            if start != 0 and end == 0:
                end = None
            start -= 1
            for line in islice(fs, start, end):
                text.append(line)
    return text


def errorStartStop(el, errMsg=""):
    try:
        if int(el) < 0:
            return True
        else:
            return int(el)
    except ValueError:
        print(errMsg)
        return "Not int"
    except TypeError:
        if el is None:
            return None


if __name__ == '__main__':
    # ПАРСИМ ПЕРЕДАВАЕМЫЕ ПАРАМЕТРЫ
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    start_time = time.time()

    # СОДЕРЖИМОЕ ФАЙЛОВ
    text_file1 = text_file2 = ""
    #  БУФЕРНЫЕ ПЕРЕМЕННЫЕ
    buf_i = buf_size = len_file1 = len_file2 = 0

    # ФЛАГ -- ВСЕ ПАРАМЕТРЫ ПЕРЕДАНЫ ВЕРНО
    flag_err = False

    # ПРОВЕРКА ПАРАМЕТРОВ
    if namespace.f1 is None or namespace.f2 is None:
        flag_err = True

    buf_e = errorStartStop(namespace.e, "Необходимо указывать численный формат при указании строки окончания!")
    buf_s = errorStartStop(namespace.s, "Необходимо указывать численный формат при указании строки начала!")

    if buf_s is None:
        namespace.s = 0
    elif buf_s == "Not int":
        flag_err = True
    elif not buf_s:
        namespace.s = buf_s

    if buf_e is None:
        namespace.e = 0
    elif buf_e == "Not int":
        flag_err = True
    elif not buf_e:
        namespace.e = buf_e

    if not flag_err:
        try:
            text_file1 = readFile(namespace.f1, int(namespace.s), int(namespace.e))
            text_file2 = readFile(namespace.f2, int(namespace.s), int(namespace.e))

            if text_file1 != "ERROR START END" or text_file2 != "ERROR START END":

                len_file1 = len(text_file1)
                len_file2 = len(text_file2)

                if namespace.e == 0:
                    buf_size = len_file1 - 1
                else:
                    buf_size = int(namespace.e) - 1

                if namespace.s != 0:
                    buf_i = int(namespace.s) - 1

                buf_line_index = int(namespace.s)

                while buf_i <= buf_size and not flag_err:
                    if text_file1[buf_i] != text_file2[buf_i]:
                        print("Найдено рассхождение в строке " + str(buf_line_index))
                        print(" (1 файл) " + text_file1[buf_i].replace("\n", ""))
                        print(" (2 файл) " + text_file2[buf_i])
                        flag_err = True
                        break
                    else:
                        buf_i += 1
                        buf_line_index += 1
            else:
                print("Передены неверные параметры начала и окончания файла!")
                flag_err = True
        except IOError:
            print("Невозможно прочитать файл! Проверьте правильность переданного пути!")
        except UnicodeDecodeError:
            print("Невозможно использовать файл с данной кодировкой!")
    else:
        print("Введены неверные параметры!")
        flag_err = True

    if not flag_err:
        print("Файлы идентичны!")
    print("--- %s seconds ---" % (time.time() - start_time))
