import numpy as np
import math
vocabulary_en = "abcdefghijklmnopqrstuvwxyz"
vocabulary_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?"


def inv_key(key_matrix, vocabulary, dim):
    inv_det_key_matrix = pow(int(np.linalg.det(key_matrix)), -1, len(vocabulary))
    inv_key_matrix = np.ones((dim, dim), dtype="int64")
    for i in range(n):
        for j in range(n):
            inv_key_matrix[i][j] = ((-1) ** (i + j) * round(np.linalg.det(minor(key_matrix, i, j))))
    inv_key_matrix = np.transpose(inv_key_matrix * inv_det_key_matrix) % len(vocabulary)
    return inv_key_matrix


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
        return matrix.astype("int64")
    else:
        raise ValueError("введен некорректный ключ")


def arr_key_generate(arr, count):
    for i in range(2, count):
        arr.append(np.dot(arr[i - 1], arr[i - 2]).astype("int64"))
    return arr


cipher = input("Введите текст, который вы хотите зашифровать: ")
key1 = input("Введите значение первого ключа через пробел: ").split()
key2 = input("Введите значение второго ключа через пробел: ").split()
vocab_choice = input("Выберите используемый алфавит: 1 -- RU, 2 -- EN: ")
if vocab_choice == "1":
    vocabulary = vocabulary_ru
elif vocab_choice == "2":
    vocabulary = vocabulary_en
n = int(math.sqrt(len(key1)))
key_matrix1 = inv_key(key_generate(vocabulary, key1, n), vocabulary, n)
key_matrix2 = inv_key(key_generate(vocabulary, key2, n), vocabulary, n)
key_matrix_space = [key_matrix1, key_matrix2]
chunks, chunk_size = len(cipher), n
chunk_strings = [list(cipher[i:i + chunk_size]) for i in range(0, chunks, chunk_size)]
for i in range(len(chunk_strings)):
    for j in range(n):
        chunk_strings[i][j] = vocabulary.index(chunk_strings[i][j])
arr = np.array(chunk_strings)
count_of_chunks = len(arr)
key_matrix_space = arr_key_generate(key_matrix_space, count_of_chunks)
for i in range(len(arr)):
    arr[i] = np.dot(arr[i], key_matrix_space[i])
arr %= len(vocabulary)
open_text = ''
for i in range(len(chunk_strings)):
    for j in range(n):
        open_text += vocabulary[arr[i][j]]
print(open_text)







