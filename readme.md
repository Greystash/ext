# TZ News blog

## Implemented over requirements
- Basic custom authorization + authorization backend
- Basic roles management with admin's permission
- Extended filtering

## Installation

- Clone repository
```sh
cd ext/ex_back
pip install -r requirements.txt
```
OR
```sh
pipenv install
```
- Activate preferable env manager
```sh
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
Now server is running on localhost:8000
- Move back to 'ext' folder in a new shell window
```sh
cd ex_front
npm i
npm start
```
Now render server is running on localhost:3000

- Navigate to [localhost](http://localhost:3000) in your browser

# Ремарки
- Обычно я пишу много тестов и документации там, где это необходимо (здесь почти не стал покрывать).
- Немного увлекся и в целом написал больше, чем требовалось.
- Не стал добавлять роутер, делать новые запросы при добавлении/обновлении данных и сустейн данных через локалсторэдж. Поэтому, чтобы наблюдать изменения придется перезагружать страницу.
- Некоторые косяки на фронте возникли благодаря моему нулевому опыту с реакт-бутстрапом, который я выбрал, думая, что это будет самая быстрая юай либа для прототипирования (пробовал очень много разных, но эту никогда). Это было ошибкой. 
- Обычно для обработки ошибок использую сентри.
- Код до рефакторинга.
