# FQW

## Docker образ
[Ссылка](https://hub.docker.com/repository/docker/fox1209/gm_scripts)

## GitHub Action - script 1
[Ссылка](https://github.com/marketplace/actions/pull-request-bot-synchronizes-two-services-github-moodle-script-1)

## GitHub Action - script 2
[Ссылка](https://github.com/marketplace/actions/pull-request-bot-synchronizes-two-services-github-moodle-script-2)

## Пример настроки и использования
[Ссылка](https://github.com/Dmitriy129/fqw-example)

## Локальный запуск

```
python main.py <script_name> <? "mock"> <? mock_grade>
```
### Передаваемые парметры
`script_name` - script1 или script2

`"mock"` - указать, если нужно указать, какую оценку нужно ставить. Для работы необходимо указать mock_grade

`mock_grade` - оценка, на которую заменятся все, которые пришли с Moodle 

## src

### Github Client
Инициализируется в самом начале.

Позволяет получить GitHub PR по id, словарь `{ [GitHub Login]: PR }`

### GoogleSheets Client

Инициализируется в самом начале.

Позволяет получить словарь, где ключ и значение взяты из указанный колонок таблицы.

### Moodle Client

Инициализируется в самом начале.

Позволяет получить словарь `{ [Moodle User]: GradeInfo }`

### helpers/getDictPRGradeInfo

Из словарей `{ [Moodle User]: GradeInfo }`, `{ [Moodle User]: GitHub Login }`, `{ [GitHub Login]: GitHub PR }` формирует словарь , `{ [GitHub PR]: GradeInfo }`

### helpers/getGradeByPR

По словарям `{ [Moodle User]: GradeInfo }`, `{ [GitHub Login]: Moodle User }` и `GitHub PR` получает  `GradeInfo`

### helpers/getGradeByPR

По `GradeInfo` и кофигу скрипта получает отформатированный конфиг - инфструкцию для работы с `GitHub PR`

### helpers/addLabelToPRByGrade

По `GitHub PR` и `GradeInfo` работает с `GitHub PR`, может создать/изменить тэг, оставить комментарий, закрыть PR

### helpers/addLabelToPRsByGrade

Обрабатывает словарь `{ [GitHub PR]: GradeInfo }` функцией `helpers/addLabelToPRByGrade`

### helpers/chooseMoodleRunConfigByPrTitle

Выбирает конфигурацию для 1го скрипта по `GitHub PR Title`



