# Operator
- stack
`python FastApi SQLAlchemy PosgeSQL`
- to run
  `uvicorn main:app --reload`
## Description
- веб-сервис мобильного оператора. Созданы таблицы пользователей, номеров телефонов, тарифов, опций.
- Документация находится по адресу `http://127.0.0.1:8000/docs`
- Описание запросов:
  - GET/users - отдаёт информацию о всех пользователей. Для каждого составляет список номеров, зарегистраированных на этого пользователя. Отдаёт сколько пользователь платит в месяц с учётом тарифа и опций для каждого номера.ппп
  - GET/user/id - отдаёт информацию о пользователе
  - DELETE/user/id -удаляет пользователя
  - GET/numbers - отдаёт список всех номеров с указанием тарифа и пользователя(владельца) номера
  - GET/tarifs_mobile - отдаёт список тарифов с их описанием
  - POST/imports/users - загружает пользователей
  - POST/imports/numbers - загружает номера
  - POST/imports/options_mobile - загружает опции
  - POST/imports/numbers_options - загружает связи номер-опция
  - GET/stat/age - отдаёт статистику по возрастам пользования тем или иным тарифом
- Описание архитектуры базы данных:
   - Один пользователь привязан к неограниченному количеству номеров и один номер привязан к одному пользователю
   - Один номер привязан к определённому тарифу и тариф может быть привязан к любому количеству номеров
   - Каждый номер может иметь сколько угодно опций и каждая опция может быть привязана к любому количеству номеров
<img src="images/readme1.png" title="Документация" width="100%" height="100%" />
