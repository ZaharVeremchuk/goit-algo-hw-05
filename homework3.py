from timeit import timeit

# Aлгоритм БОЄРА-МУРА
def build_shift_table(pattern):
  """Створити таблицю зсувів для алгоритму Боєра-Мура."""
  table = {}
  length = len(pattern)
  # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
  table.setdefault(pattern[-1], length)
  return table

def boyer_moore_search(text, pattern):
  # Створюємо таблицю зсувів для патерну (підрядка)
  shift_table = build_shift_table(pattern)
  i = 0 # Ініціалізуємо початковий індекс для основного тексту

  # Проходимо по основному тексту, порівнюючи з підрядком
  while i <= len(text) - len(pattern):
    j = len(pattern) - 1 # Починаємо з кінця підрядка

    # Порівнюємо символи від кінця підрядка до його початку
    while j >= 0 and text[i + j] == pattern[j]:
      j -= 1 # Зсуваємось до початку підрядка

    # Якщо весь підрядок збігається, повертаємо його позицію в тексті
    if j < 0:
      return i # Підрядок знайдено

    # Зсуваємо індекс i на основі таблиці зсувів
    # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
    i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

  # Якщо підрядок не знайдено, повертаємо -1
  return -1


# Aлгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Рабіна Карпа 
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(pattern)
    main_string_length = len(text)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1
# Результати cтатті 1 
# БОЄРА-МУРА (реальний) : 0.16884200007189065 секунд (найшвидший реальний)
# Кнута-Морріса-Пратта (реальний): 0.32043269998393953 секунд
# Рабін Карп (реальний): 0.6245020000496879 секунд
# БОЄРА-МУРА (вигаданий): 0.14592999999877065 секунд (найшвидший вигаданий)
# Кнута-Морріса-Пратта (вигаданий):0.27127659996040165 секунд
# Рабіна Карп (вигаданий): 0.8390362999634817 секунд
print('Стаття 1')

with open('стаття 1.txt', 'r') as file:
   main_text = file.read()

sub_text = 'Ознаки'
bad_sub_text = 'dementor'

# Aлгоритм БОЄРА-МУРА
mur_seconds_real = timeit(stmt='boyer_moore_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('БОЄРА-МУРА (реальний) : '+ str(mur_seconds_real) + ' секунд')

# Aлгоритм Кнута-Морріса-Пратта
kmp_seconds_real = timeit(stmt='kmp_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('Кнута-Морріса-Пратта (реальний): '+ str(kmp_seconds_real) + ' секунд')

# Алгоритм Рабіна Карпа 
karp_search_seconds_real = timeit(stmt='rabin_karp_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('Рабін Карп (реальний): '+ str(karp_search_seconds_real) + ' секунд')

# Aлгоритм БОЄРА-МУРА
mur_seconds_not_real = timeit(stmt='boyer_moore_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('БОЄРА-МУРА (вигаданий): '+ str(mur_seconds_not_real) + ' секунд')

# Aлгоритм Кнута-Морріса-Пратта
kmp_seconds_not_real = timeit(stmt='kmp_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('Кнута-Морріса-Пратта (вигаданий):'+ str(kmp_seconds_not_real) + ' секунд')

# Алгоритм Рабіна Карпа 
karp_seconds_not_real = timeit(stmt='rabin_karp_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('Рабіна Карп (вигаданий): '+ str(karp_seconds_not_real) + ' секунд')


# Результати cтатті 2 
# БОЄРА-МУРА (реальний) : 0.07711880002170801 секунд (найшвидший реальний)
# Кнута-Морріса-Пратта (реальний): 0.188537499983795 секунд
# Рабін Карп (реальний): 0.6235494000138715 секунд
# БОЄРА-МУРА (вигаданий): 0.2314699999988079 секунд (найшвидший вигаданий)
# Кнута-Морріса-Пратта (вигаданий):0.4605465999338776 секунд
# Рабіна Карп (вигаданий): 1.6527735999552533 секунд

print('Стаття 2')

with open('стаття 2.txt', 'r',  encoding='latin-1') as file:
    main_text = file.read()

sub_text = 'unrolled'
bad_sub_text = 'dementor'

# Aлгоритм БОЄРА-МУРА
mur_seconds_real = timeit(stmt='boyer_moore_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('БОЄРА-МУРА (реальний) : '+ str(mur_seconds_real) + ' секунд')

# Aлгоритм Кнута-Морріса-Пратта
kmp_seconds_real = timeit(stmt='kmp_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('Кнута-Морріса-Пратта (реальний): '+ str(kmp_seconds_real) + ' секунд')

# Алгоритм Рабіна Карпа 
karp_search_seconds_real = timeit(stmt='rabin_karp_search(text=main_text, pattern=sub_text)', globals=globals(), number=100)
print('Рабін Карп (реальний): '+ str(karp_search_seconds_real) + ' секунд')

# Aлгоритм БОЄРА-МУРА
mur_seconds_not_real = timeit(stmt='boyer_moore_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('БОЄРА-МУРА (вигаданий): '+ str(mur_seconds_not_real) + ' секунд')

#Aлгоритм Кнута-Морріса-Пратта
kmp_seconds_not_real = timeit(stmt='kmp_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('Кнута-Морріса-Пратта (вигаданий):'+ str(kmp_seconds_not_real) + ' секунд')

# Алгоритм Рабіна Карпа 
karp_seconds_not_real = timeit(stmt='rabin_karp_search(text=main_text, pattern=bad_sub_text)', globals=globals(), number=100)
print('Рабіна Карп (вигаданий): '+ str(karp_seconds_not_real) + ' секунд')

