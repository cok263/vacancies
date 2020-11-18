# Сравниваем вакансии программистов

Программа выводит количество вакансий и среднюю зарплату по самым популярным языкам программирования

### Как установить

1. Скачайте код
2. Зарегистрируйте приложение на [SuperJob](https://api.superjob.ru/register) и получите его secret key
3. Создайте файл .env в папке проекта и поместите в него ключ

Пример .env
```
SUPERJOB_SECRET=v3.r.15554355345.f72ed76ccc058434699d7c7777777fc691a46a50.d7cfe684ddeb1397980e3c6efbe287528cbc3481
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Запуск
Запустите программу, передав ссылку в качестве аргумента.

Пример команды запуска
```
python3 vacancies.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).