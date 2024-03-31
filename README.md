# Домашнє завдання #12

У цьому домашньому завданні ми продовжуємо допрацьовувати наш REST API застосунок із домашнього завдання 11.

## Завдання

- реалізуйте механізм аутентифікації в застосунку;
- реалізуйте механізм авторизації за допомогою JWT токенів, щоб усі операції з контактами проводились лише зареєстрованими користувачами;
- користувач має доступ лише до своїх операцій з контактами;

## Загальні вимоги

- При реєстрації, якщо користувач вже існує з таким `email`, сервер поверне помилку `HTTP 409 Conflict`;
- Сервер хешує пароль і не зберігає його у відкритому вигляді в базі даних;
- У разі успішної реєстрації користувача сервер повинен повернути `HTTP` статус відповіді `201 Created` та дані нового користувача;
- Для всіх операцій POST створення нового ресурсу, сервер повертає статус 201 Created;
- При операції `POST` - аутентифікація користувача, сервер приймає запит із даними користувача (`email`, пароль) у тілі запиту;
- Якщо користувач не існує або пароль не збігається, повертається помилка `HTTP 401 Unauthorized`;
механізм авторизації за допомогою `JWT` токенів реалізований парою токенів: токена доступу `access_token` і токен оновлення `refresh_token`.