# Тестовое django

## Овервью проекта:

- Используем **pytest** для тестирования моделей и views. Тесты в \*\_test.py файлах. Формат ответа не тестирую, его гарантирует pydantic.
- Используем **django-treenode** для эффективной работы с древовидной структурой departments
- Для избежания n+1 используется select_related + аннотации для упрощения кода
- Для API используем **django-ninja**.

**Структура проекта:**

```
.
├── db.sqlite3
├── manage.py
├── org
│   ├── __init__.py
│   ├── conf
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── departments
│       ├── __init__.py
│       ├── admin.py
│       ├── api_test.py
│       ├── api.py
│       ├── apps.py
│       ├── migrations
│       ├── models_test.py
│       └── models.py
├── pyproject.toml
├── README.md
└── uv.lock
```

### Сотрудники

- [x] CMS Создание и редактирование сотрудника и должность
- [x] Тесты модели и api роутов
- [x] GET /api/v1/employees/1 — получить сотрудника
- [x] GET /api/v1/employees — получить список сотрудников (поддерживается limit-offset паджинация)

### Департаменты

- [x] Тесты модели и api роутов
- [x] CMS Создание и редактирование
- [x] GET /api/v1/departments/1 — получить информацию об отделе
- [x] GET /api/v1/departments — Получить все отделы
- [x] GET /api/v1/departments/1/employees — Получить сотрудников отдела
- [x] hierarchy api

### Фронтенд

- [ ] Вывести структуру компании

### Инфраструктура

- [x] Добавить seed файл для генерации 50_000 сотрудников и 25 отделов
- [ ] Перенести хранение сессий в базу
- [ ] Добавить Dockerfile для сборки бекенда
- [ ] Добавить docker compose
- [ ] Переехать на postgresql
- [ ] Развернуть демку
- [ ] Написать инструкцию для разворачивания

## Как поднять проект

- `python manage.py seed_employees` - Заполнить базу работниками
