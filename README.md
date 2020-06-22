### ТЕСТОВОЕ ЗАДАНИЕ
***
Для запуска проекта вам понадобится виртуальное окуржение и python 3.7+

Установите виртуальное окружение и зависимости из файла requirements.txt в корне проекта.
```
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```
Создайте файл .env в корне проекта и вставьте SECRET_KEY.
```
SECRET_KEY="UNIQUE KEY"
```
Перед запуском сервера примените все миграции. Приложение использует различные настройки для локального и боевого сервера.
Так для локального сервера - Awesome_test.settings.local, а для боевого - Awesome_test.settings.production
```
python manage.py migrate --Awesome_test.settings.local
```
Запустите приложение командой:
```
python manage.py runserver --settings=Awesome_Test.settings.local
```
Перейдите по адресу:
```
http://127.0.0.1:8000/
```
