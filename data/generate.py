import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

developers = [
    "alex.ivanov", "maria.smirnova", "dmitry.petrov", "anna.kuznetsova", "sergey.volkov",
    "olga.fedorova", "nikita.popov", "elena.sokolova", "ivan.kozlov", "tatiana.morozova",
    "pavel.novikov", "irina.solovieva", "andrey.lebedev", "victoria.egorova", "roman.pavlov"
]

types = ["Bug", "Task", "Improvement"]
priorities = ["Low", "Medium", "High", "Critical"]

actions = [
    "Исправить", "Доработать", "Оптимизировать", "Реализовать", "Переписать", "Улучшить",
    "Починить", "Обновить", "Добавить", "Ускорить", "Стабилизировать", "Переработать",
    "Проверить", "Упростить", "Расширить", "Устранить", "Снизить", "Поддержать",
    "Синхронизировать", "Автоматизировать", "Нормализовать", "Актуализировать"
]

entities = [
    "авторизацию через API", "сохранение профиля пользователя", "модуль оплаты",
    "SQL-запросы в отчётах", "фоновые джобы", "дашборд аналитики",
    "слой кеширования", "зависимости проекта", "обработку ошибок в сервисе заказов",
    "сбор технических метрик", "модуль уведомлений", "обработчик очередей",
    "логику пагинации", "feature flag механизм", "конвертацию часовых поясов",
    "валидацию входных данных", "экспорт данных в CSV", "импорт файлов от партнёров",
    "поиск по каталогу", "фильтрацию списка пользователей", "генерацию PDF-отчётов",
    "расчёт агрегированных показателей", "создание сессий пользователя",
    "интеграцию с внешним API", "механизм повторных запросов", "обновление токенов",
    "ленивую загрузку данных", "работу websocket-подключений",
    "модуль ролей и прав доступа", "очистку временных файлов",
    "обработку webhook-событий", "формирование Excel-выгрузок",
    "страницу настроек аккаунта", "механизм восстановления пароля",
    "историю изменений сущностей", "логирование ошибок на фронтенде",
    "рендеринг таблиц на клиенте", "сервис рекомендаций",
    "расписание периодических задач", "синхронизацию данных между сервисами"
]

contexts = [
    "для мобильной версии", "после релиза", "в админ-панели", "в личном кабинете",
    "в продакшене", "на staging-окружении", "после миграции БД",
    "при высокой нагрузке", "для новых клиентов", "при пакетной обработке",
    "в nightly job", "для edge-case сценариев", "в процессе онбординга",
    "при массовом импорте", "для VIP-пользователей", "в модуле биллинга",
    "при параллельных запросах", "в отчётах за период",
    "при повторной отправке формы", "для интеграции с партнёрами",
    "в сценарии восстановления после сбоя", "в рамках технического долга",
    "перед выкладкой релиза", "в новом пользовательском потоке"
]

def generate_summary():
    return f"{random.choice(actions)} {random.choice(entities)} {random.choice(contexts)}"

def generate_description():
    return "Автогенерированное описание задачи."

def is_weekend(date):
    return date.weekday() >= 5

today = datetime.now()
start_date = today - timedelta(days=10)

rows = []

for i in range(1, 20):
    created = start_date + timedelta(days=random.randint(0, 180))

    if is_weekend(created):
        in_progress = created + timedelta(days=random.randint(1, 3))
        review = in_progress + timedelta(days=random.randint(2, 5))
        closed = review + timedelta(days=random.randint(2, 4))

        lines_add = random.randint(0, 50)
        lines_removed = random.randint(0, 20)
        commits = random.randint(0, 3)
    else:
        in_progress = created + timedelta(days=random.randint(0, 5))
        review = in_progress + timedelta(days=random.randint(0, 7))
        closed = review + timedelta(days=random.randint(0, 5))

        lines_add = random.randint(5, 500)
        lines_removed = random.randint(0, 250)
        commits = random.randint(1, 18)

    # почти не закрываем в выходные
    if is_weekend(closed) and random.random() < 0.9:
        closed += timedelta(days=random.randint(1, 2))

    changed = closed - timedelta(days=random.randint(0, 3))
    due = created + timedelta(days=random.randint(3, 21))

    task_type = random.choice(types)
    priority = random.choice(priorities)

    if task_type == "Bug":
        story_points = random.choice([1, 2, 3, 5, 8])
    elif task_type == "Improvement":
        story_points = random.choice([2, 3, 5, 8, 13])
    else:
        story_points = random.choice([1, 2, 3, 5, 8, 13])

    reopen_times = random.choice([0, 0, 1, 1, 2, 3])

    # linked логика
    if i > 1 and random.random() < 0.1:
        linked = f"PROJ-{random.randint(1, i-1)}"
    else:
        linked = None

    rows.append({
        "id": f"PROJ-{i+1000}",
        "summary": generate_summary(),
        "description": generate_description(),
        "created_date": created.strftime("%Y-%m-%d"),
        "changed_date": changed.strftime("%Y-%m-%d"),
        "in_progress_date": in_progress.strftime("%Y-%m-%d"),
        "review_date": review.strftime("%Y-%m-%d"),
        "closed_date": None,
        "due_date": due.strftime("%Y-%m-%d"),
        "Type": task_type,
        "linked": linked,
        "reopen_times": reopen_times,
        "story_points": story_points,
        "assignee": random.choice(developers),
        "priority": priority,
        "lines_add": lines_add,
        "lines_removed": lines_removed,
        "total_commits": commits
    })

df = pd.DataFrame(rows)

path = "dev_tasks_dataset_1001_rows_ru.csv"
df.to_csv(path, index=False, encoding="utf-8-sig")

print(f"Файл сохранён: {path}")