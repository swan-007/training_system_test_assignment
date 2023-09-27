# API сервис системы для обучения

Установка:
1. Клонировать репозиторий:
```
https://github.com/swan-007/training_system_test_assignment.git
```
2. Прейти в каталог api_training :
```
cd api_training 
```    
3. Установить зависимости:
 ```
 pip install -r requirements.txt
 ```

4. Применить миграции:
 ```
 python manage.py migrate 
 ```  
5. Запуск сервера:
 ```
 python manage.py runserver
 ```
   

### Использование:

1. Регистрация. 
   #### Метод  POST   
   - url: ```****/register/``` 
   - Обязательные параметры: ```username, password```  
   - Пример запроса: ```Body={"username": "Ivan","password": qwerty123 }```
   - Пример ответа: ```{"Status": true}``` 
   



2. Вход.
   #### Метод  POST   
   - url: ```****/login/``` 
   - Обязательные параметры: ```username, password```  
   - Пример запроса: ```Body={"username": "Ivan","password": qwerty123 }```
   - Пример ответа: ```{"Status": true, "Token": "e1b9fb2048d15f31aded9238c353729440de9012"
}``` 
3. Выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ.
   #### Метод  GET  
   - url: ```****/api/v1/lessons/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"id": 1,
        "watched": false,
        "start_time": 1,
        "end_time": 3,
        "user": 1,
        "lesson": 1]```
   

4. Выведением списка уроков по конкретному продукту к которому пользователь имеет доступ.
   #### Метод  GET  
   - url: ```****/api/v1/products/id-Продукта/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"id": 2,
        "watched": True,
        "start_time": 2,
        "end_time": 4,
        "user": 1,
        "lesson": 2}]``` 
   
4. Отображения статистики по продуктам.
   #### Метод  GET  
   - url: ```****/api/v1/product-stats/``` 
   - Обязательные параметры: ```Authorization token```
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   



