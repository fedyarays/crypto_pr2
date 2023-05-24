import numpy as np
import math
vocabulary_en = "abcdefghijklmnopqrstuvwxyz"
vocabulary_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?"

def minor(arr, i, j):
    return arr[np.array(list(range(i)) + list(range(i + 1, arr.shape[0])))[:, np.newaxis],
               np.array(list(range(j)) + list(range(j + 1, arr.shape[1])))]

def key_generate(alphabet, nums, dimention):
    matrix = np.ones((dimention, dimention))
    for i in range(dimention):
        for j in range(dimention):
            matrix[i][j] = int(nums[0])
            nums.pop(0)
    det = int(np.linalg.det(matrix))
    if math.gcd(det, len(alphabet)) == 1:
        return np.array(matrix)
    else:
        raise ValueError("введен некорректный ключ")


# входные данные: шифр, ключ, выбранный язык
cipher = input("Введите текст, который вы хотите расшифровать: ")
key = input("Введите значения ключа через пробел: ").split()
vocab_choice = input("Выберите используемый алфавит: 1 -- RU, 2 -- EN: ")

# выбор языка
if vocab_choice == "1":
    vocabulary = vocabulary_ru
elif vocab_choice == "2":
    vocabulary = vocabulary_en

# нахождение размера ключевой матрицы
n = int(math.sqrt(len(key)))

# создание ключевой матрицы
key_matrix = key_generate(vocabulary, key, n).astype(int)

# нахождение обратного значения определителя ключевой матрицы
inv_det_key_matrix = pow(int(np.linalg.det(key_matrix)), -1, len(vocabulary))
inv_key_matrix = np.ones((n, n), dtype=int)

# создание обратной ключевой матрицы используя союзную матрицу
for i in range(n):
    for j in range(n):
        inv_key_matrix[i][j] = ((-1)**(i + j) * round(np.linalg.det(minor(key_matrix, i, j))))
inv_key_matrix = np.transpose(inv_key_matrix * inv_det_key_matrix) % len(vocabulary)

# разбиение исходной строки на подстроки определенной длины и замена букв
chunks, chunk_size = len(cipher), n
chunk_strings = [list(cipher[i:i+chunk_size]) for i in range(0, chunks, chunk_size)]
for i in range(len(chunk_strings)):
    for j in range(n):
        chunk_strings[i][j] = vocabulary.index(chunk_strings[i][j])
arr = np.array(chunk_strings)

# перемножение вектора состоящего из индексов с обратной ключевой матрицей
for i in range(len(arr)):
    arr[i] = np.dot(arr[i], inv_key_matrix)
arr %= len(vocabulary)

# формирование открытого текста
open_text = ''
for i in range(len(chunk_strings)):
    for j in range(n):
        open_text += vocabulary[arr[i][j]]
print(open_text)

