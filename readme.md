# Задание

Создать форму для регистрации пользователей на сайте. Форма должна содержать поля *"Имя", "Фамилия", "Email", "Пароль"* и кнопку *"Зарегистрироваться"*. При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

# Реализация

создание БД с консоли перед первым запуском: flask init-db
1. / - кнопка с перенаправлением на страницу с формой регистрации 
2. /registration/ - сама форма с проверкой:
    - на совпадение имени + фамилии с имеющимися в базе
    - на правильность email
    - на совпадение email с имеющимся в базе
    - на длину пароля
3. /users/ - вывод базы (для проверки шифрования пароля)
