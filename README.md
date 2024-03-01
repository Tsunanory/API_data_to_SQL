Код позволяет получить данные с сайта hh.ru по заданным работодателям и сохранить эти данные в Postgres(автоматизирован процесс создания базы данных, таблиц с нужными колонками и, наконец, внесения в таблицы всего полученного). Далее можно получить информацию обо всех вакансиях работодателей, получить зарплаты выше средней среди имеющихся, осуществить поиск по ключевым словам и тд.

Для запуска проекта необходимо иметь в доступе активный SQL сервер, на который будет происходить запись данных. 
В папку с кодом добавлен файл database.ini с искусственным примером данных для подключения к базе данных. 
Пожалуйста, заполните ее соответствующими данными для вашей собственно базы данных SQL.

Работа происходит через файл main.py. 
Основная функция - main() - собирает все данные и записывает их на сервер. В теле функции вы также можете изменить интерусующих вас работодателей, внеся их ID с сайта hh.ru вместо или после тех ID, которые туда уже записаны.
Внизу файла main.py расположены закомментированные вызовы функций класса DBManager.
Эти функции позволяют реализовать парсинг записей в базе данных по интересующим вас параметрам. Если вы хотите воспользоваться этим функционалом, просто разкомментируйте начальную инициализацию объекта - 
строку # mng = DBManager() и ниже идущие функции по вашему усмотрению. Перед повторным запуском скрипта можно также закомментировать вызов функции main.py, чтобы код работал быстрее и чтобы снова не получать данные по API и не перезаписывать их в базу.
