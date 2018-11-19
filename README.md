# YandexMapGeojsonDescriptorBot
Telegram bot in Python

It accepts a Geojson file generated on Yandex Map Constructor and outputs the amount of polygons, lines and points created within it.



### Описание процесса поднятия бота:

Для начала, мы пишем @BotFather в Телеграм чтобы создать новый бот, и получаем к нему токен, пользуясь которым мы сможем обращаться к Telegram API. 

Далее мы создаем Python проект, в моем случае я использовал Visual Studio. 
Импортируем библиотеку [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) (telegram), которая упростит работу с API.

Теперь мы создаем обработчики (handlers) для разных типов обновлений/вводов, которых наш бот может получить от пользователей. 
В нашем случае приветствие при первой активации бота (start_handler), призыв/инструкция пользователя отправить файл Geojson при получении текстового сообщения (echo) и основная логика программы - подсчет количества многоугольников, линий и меток созданных в конструкторе карта Яндекс и экспортированных в формате geojson (document_handler). Последний handler активизируется только при получении файла в сообщении, что обеспечивается указанием Filters.document при создании обработчика.

За каждым обработчким стоит функция. В случае с document_handler это функция document_parsing(), которая принимает файл и пытается подсчитать количество многоугольников, линий и меток в нем, после чего отправляет результат пользователю. Если полученный файл не является файлом .json, созданным в конструкторе карт Yandex, то пользователю отправляется сообщение о том, что файл некорректен.

Теперь мы можем создать приложение Heroku. Для этого переместившись в терминале в ту папку, где находится наш Git репозиторий, мы вводим команду heroku create и получаем ссылку на созданный веб-сервер (в этом случае это https://infinite-bayou-65542.herokuapp.com/). 

На этом этапе нам нужно создать webhook в конце Python скрипта, указав полученную ссылку heroku, что позволит нам получать обновления от API нашего бота. 

После этого мы делаем коммит нашего проекта и отправляем этот коммит на удаленный репозиторий.

Чтобы heroku распознал проект как Python приложение, мы должны создать requirements.txt со всеми необходимыми пакетами, и также файл Procfile с указанием скрипта .py, который должен быть запущен на веб сервере (в нашем случае это run.py). 

С помощью команды "git push heroku master" в терминале мы совершаем деплой проекта на Heroku. Команда "heroku ps:scale web=1" запускает  приложение на сервере. Итоговый бот работает согласно ожиданиям. 


Для прояснения любых вопросов, либо внесения предложений по этому проекту, просьба писать на телеграм @b_dot - я отвечу при первой возможности.
