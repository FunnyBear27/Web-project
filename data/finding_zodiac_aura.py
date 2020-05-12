
aura = {1: 'Красный',
        2: 'Желтый',
        3: 'Оранжевый',
        4: 'Зеленый',
        5: 'Голубой',
        6: 'Синий',
        7: 'Фиолетовый',
        8: 'Розовый',
        9: 'Бронзовый',
        10: 'Серебряный',
        11: 'Золотой'}


def finding_aura(year, month, day):
    summ = sum(map(int, str(year))) + sum(map(int, str(month))) + sum(map(int, str(day)))
    while 11 < summ or summ < 0:
        summ = sum(map(int, str(summ)))
    return aura[summ]


zodiac = {'Овен': {'start': (3, 21), 'end': (4, 20)},
          'Телец': {'start': (4, 21), 'end': (5, 20)},
          'Близнецы': {'start': (5, 21), 'end': (6, 20)},
          'Рак': {'start': (6, 21), 'end': (7, 22)},
          'Лев': {'start': (7, 23), 'end': (8, 22)},
          'Дева': {'start': (8, 23), 'end': (9, 23)},
          'Весы': {'start': (9, 24), 'end': (10, 23)},
          'Скорпион': {'start': (10, 24), 'end': (11, 21)},
          'Стрелец': {'start': (11, 22), 'end': (12, 21)},
          'Козерог': {'start': (12, 22), 'end': (1, 20)},
          'Водолей': {'start': (1, 21), 'end': (2, 18)},
          'Рыбы': {'start': (2, 19), 'end': (3, 20)}}


def finding_zodiac(month, day):
    tuple_date = (int(month), int(day))
    zod = 0
    for key, val in zodiac.items():
        if val['start'] <= tuple_date <= val['end']:
            zod = key
            break
        elif (tuple_date[0] == 12 and tuple_date[1] >= val['start'][1]) or (tuple_date[0] == 1 and tuple_date[1] <= val['end'][1]):
            zod = 'Козерог'
            break
    return zod


def leap_year(year):
    if year % 4 == 0:
        return True
    else:
        return False