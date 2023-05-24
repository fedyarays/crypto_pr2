import numpy as np
import math
vocabulary_en = "abcdefghijklmnopqrstuvwxyz"
vocabulary_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?"


def key_generate(alphabet, nums, dimention):
    matrix = np.ones((dimention, dimention))
    for i in range(dimention):
        for j in range(dimention):
            matrix[i][j] = int(nums[0])
            nums.pop(0)
    det = int(np.linalg.det(matrix))
    if math.gcd(det, len(alphabet)) == 1:
        return matrix
    else:
        raise ValueError("введен некорректный ключ")


def open_text_supplement(opentxt, dimention, alphabet):
    count_of_supplement_letters = 0
    if len(opentxt) % dimention != 0:
        count_of_supplement_letters = dimention - len(opentxt) % dimention
    opentxt += "".join(np.random.choice(list(alphabet), count_of_supplement_letters))
    return opentxt


open_text = input("Введите текст, который вы хотите зашифровать: ")
key = input("Введите значения ключа через пробел: ").split()
vocab_choice = input("Выберите используемый алфавит: 1 -- RU, 2 -- EN: ")
if vocab_choice == "1":
    vocabulary = vocabulary_ru
elif vocab_choice == "2":
    vocabulary = vocabulary_en
n = int(math.sqrt(len(key)))
key_matrix = key_generate(vocabulary, key, n)
print("Ключ зашифровки: ")
print(key_matrix)
open_text_supp = open_text_supplement(open_text, n, vocabulary)
chunks, chunk_size = len(open_text_supp), n
chunk_strings = [list(open_text_supp[i:i+chunk_size]) for i in range(0, chunks, chunk_size)]
for i in range(len(chunk_strings)):
    for j in range(n):
        chunk_strings[i][j] = vocabulary.index(chunk_strings[i][j])

arr = np.array(chunk_strings)
for i in range(len(arr)):
    arr[i] = np.dot(arr[i], key_matrix)
arr %= len(vocabulary)
cipher = ''
for i in range(len(chunk_strings)):
    for j in range(n):
        cipher += vocabulary[arr[i][j]]
print(cipher)


