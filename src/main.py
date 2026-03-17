from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.gigachat import gigachat_answer
from src.prompt import get_promt, get_prompt_for_developer
from src.utils import load_developers_from_csv, get_week_stats, \
    get_story_points_by_month, get_types_distribution, get_top_developers, \
    parse_ai_report, find_anomalies, get_week_stats_by_dev, get_story_points_by_month_and_dev
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Dashboard")
templates = Jinja2Templates(directory="templates")

_CSV = os.getenv("CSV_PATH")
_AI = os.getenv("AI_RECOMMENDATION_PATH")
_AI_DEV = os.getenv("AI_RECOMMENDATION_PATH_DEV")

developers_list = load_developers_from_csv(_CSV)

pie_labels, pie_data = get_types_distribution(_CSV)
bar_labels, bar_data = get_top_developers(_CSV, top_n=5)
anomalies = find_anomalies(_CSV)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    labels, commits_data, closed_data, bugs_data = get_week_stats(_CSV)
    months, sp_data, current_month = get_story_points_by_month(_CSV)
    sections = parse_ai_report(_AI)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "developers": developers_list,
            "labels": labels,
            "commits": commits_data,
            "closed": closed_data,
            "bugs": bugs_data,
            "months": months,
            "sp_data": sp_data,
            "current_month": current_month,
            "pie_labels": pie_labels,
            "pie_data": pie_data,
            "bar_labels": bar_labels,
            "bar_data": bar_data,
            "ai_sections": sections,
            "anomalies": anomalies
        }
    )

@app.get("/developer/{dev_name}", response_class=HTMLResponse)
def dev_dashboard(request: Request, dev_name: str):
    a_count_low = sum(1 for a in anomalies if a['severity'] == 'low' and a['assignee'] == dev_name)
    a_count_medium = sum(1 for a in anomalies if a['severity'] == 'medium' and a['assignee'] == dev_name)
    a_count_high = sum(1 for a in anomalies if a['severity'] == 'high' and a['assignee'] == dev_name)
    a_count = {"a_low": a_count_low, "a_medium": a_count_medium, "a_high": a_count_high}
    labels, commits_data, closed_data, bugs_data = get_week_stats_by_dev(_CSV, dev_name)
    months, sp_data, current_month = get_story_points_by_month_and_dev(_CSV, dev_name)
    sections = parse_ai_report(_AI_DEV)
    return templates.TemplateResponse(
        request=request,
        name="dashboard_staff.html",
        context={
            "developers": developers_list,
            "selected_dev": dev_name,
            "labels": labels,
            "commits": commits_data,
            "closed": closed_data,
            "bugs": bugs_data,
            "months": months,
            "sp_data": sp_data,
            "current_month": current_month,
            "pie_labels": pie_labels,
            "pie_data": pie_data,
            "bar_labels": bar_labels,
            "bar_data": bar_data,
            "ai_sections": sections,
            "anomalies": anomalies,
            "a_count": a_count
        }
    )

@app.post("/generate-report")
async def generate_report():
    # print(gigachat_answer(get_promt(_CSV)))
    return {"status": "ok"}

@app.post("/generate-report/{dev_name}")
async def generate_report(dev_name: str):
    # print(gigachat_answer(get_promt(_CSV)))
    # print(gigachat_answer(get_prompt_for_developer(_CSV, dev_name), for_dev=True))
    return {"status": "ok"}