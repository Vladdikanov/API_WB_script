import re
def sum_numbers():
    with open("numbers.txt", 'r') as file:
        data = file.readlines()
    print(data)
    sum = 0
    for num in data:
        try:
            sum += int(re.sub('\D', '', num))
        except:
            print(f"Ошибка при преобразовании числа: {num}", )
    print(f"Сумма чисел: {sum}")

sum_numbers()