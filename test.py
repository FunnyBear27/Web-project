import requests


# Готовим запрос.
geocoder_request = "https://moscow.sm-news.ru/goroskop-na-12-maya-komu-iz-znakov-zodiaka-ulybnetsya-udacha-a-komu-sleduet-byt-ostorozhnee-59928"

# Выполняем запрос.
response = requests.get(geocoder_request)
if response:
    # Запрос успешно выполнен, печатаем полученные данные.
    print(response.content)
else:
    # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")