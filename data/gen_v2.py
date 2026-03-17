import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Параметры
num_rows = 1000
start_date = datetime(2025, 9, 18)
end_date = datetime(2026, 3, 18)
assignees = ["Alex", "Maria", "John", "Sophia", "David", "Emma", "Michael", "Olivia", "Daniel", "Isabella", "James",
             "Mia", "Robert", "Charlotte", "William"]
priorities = ["Low", "Medium", "High"]
types = ["Bug", "Feature", "Task", "Improvement"]


# Функция для генерации рабочей даты (исключаем выходные и праздники)
def random_workday(start, end):
    while True:
        delta = end - start
        random_days = random.randint(0, delta.days)
        date = start + timedelta(days=random_days)
        # Выходные
        if date.weekday() >= 5:
            continue
        # Праздники: 1-7 Jan, 1-3 May (для примера)
        if (date.month == 1 and 1 <= date.day <= 7) or (date.month == 5 and 1 <= date.day <= 3):
            continue
        return date


# Генерация данных
data = []
for i in range(1, num_rows + 1):
    created_date = random_workday(start_date, end_date)

    # Прогресс и закрытие
    in_progress_date = created_date + timedelta(days=random.randint(0, 5))
    review_date = in_progress_date + timedelta(days=random.randint(0, 3)) if random.random() > 0.1 else None
    closed_date = review_date + timedelta(days=random.randint(0, 5)) if review_date and random.random() > 0.2 else None
    changed_date = closed_date if closed_date else created_date + timedelta(days=random.randint(0, 5))

    due_date = created_date + timedelta(days=random.randint(1, 20))

    linked = "" if random.random() < 0.95 else str(random.randint(1, num_rows))

    r = random.random()
    if r < 0.8:
        story_points = random.randint(3, 5)
    elif r < 0.9:
        story_points = random.randint(6, 10)
    elif r < 0.98:
        story_points = random.randint(11, 15)
    else:
        story_points = random.randint(16, 20)

    lines_add = random.randint(10, 500)
    lines_removed = random.randint(5, 400)
    total_commits = random.randint(1, 10)

    data.append([i,
                 f"Summary {i}",
                 f"Description for task {i}",
                 created_date.strftime("%Y-%m-%d"),
                 changed_date.strftime("%Y-%m-%d"),
                 in_progress_date.strftime("%Y-%m-%d"),
                 review_date.strftime("%Y-%m-%d") if review_date else "",
                 closed_date.strftime("%Y-%m-%d") if closed_date else "",
                 due_date.strftime("%Y-%m-%d"),
                 random.choice(types),
                 linked,
                 random.randint(0, 3),
                 story_points,
                 random.choice(assignees),
                 random.choice(priorities),
                 lines_add,
                 lines_removed,
                 total_commits
                 ])

columns = ["id", "summary", "description", "created_date", "changed_date", "in_progress_date", "review_date",
           "closed_date", "due_date",
           "Type", "linked", "reopen_times", "story_points", "assignee", "priority", "lines_add", "lines_removed",
           "total_commits"]

df = pd.DataFrame(data, columns=columns)

# Сохраняем CSV
file_path = "dev_tasks_dataset_1002_rows_ru.csv"
df.to_csv(file_path, index=False)