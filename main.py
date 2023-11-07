from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
import requests

app = FastAPI()

USER_DATA_API_URL = 'http://sef.podkolzin.consulting/api/users/'

reports = {}

def fetch_user_data(offset):
    url = f'{USER_DATA_API_URL}lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []

def calculate_daily_average(user_id, user_data):
    user = next((u for u in user_data if u["userId"] == user_id), None)
    if user:
        activity = user.get("activity", [])
        if not activity:
            return 0

        timestamps = [datetime.fromisoformat(ts) for ts in activity]

        timestamps.sort()

        time_diffs = [(timestamps[i + 1] - timestamps[i]).total_seconds() for i in range(len(timestamps) - 1)]

        average_time = sum(time_diffs) / len(time_diffs)
        return round(average_time)
    else:
        return 0

def calculate_weekly_average(user_id, user_data):
    user = next((u for u in user_data if u["userId"] == user_id), None)
    if user:
        activity = user.get("activity", [])
        if not activity:
            return 0

        timestamps = [datetime.fromisoformat(ts) for ts in activity]

        timestamps.sort()

        time_diffs = [(timestamps[i + 1] - timestamps[i]).total_seconds() for i in range(len(timestamps) - 1)]

        average_time = sum(time_diffs) / len(time_diffs)

        average_time_minutes = average_time / 60

        weekly_average_time = average_time_minutes * 7

        return round(weekly_average_time)
    else:
        return 0

def calculate_total_time(user_id, user_data):
    user = next((u for u in user_data if u["userId"] == user_id), None)
    if user:
        activity = user.get("activity", [])
        if not activity:
            return 0

        timestamps = [datetime.fromisoformat(ts) for ts in activity]

        timestamps.sort()

        total_time = (timestamps[-1] - timestamps[0]).total_seconds()
        return round(total_time)
    else:
        return 0

def calculate_min_time(user_id, user_data):
    user = next((u for u in user_data if u["userId"] == user_id), None)
    if user:
        activity = user.get("activity", [])
        if not activity:
            return 0

        timestamps = [datetime.fromisoformat(ts) for ts in activity]

        min_time = min(timestamps).timestamp()

        min_time_seconds = int(min_time)

        return min_time_seconds
    else:
        return 0

def calculate_max_time(user_id, user_data):
    user = next((u for u in user_data if u["userId"] == user_id), None)
    if user:
        activity = user.get("activity", [])
        if not activity:
            return 0

        timestamps = [datetime.fromisoformat(ts) for ts in activity]

        max_time = max(timestamps).timestamp()

        max_time_seconds = int(max_time)

        return max_time_seconds
    else:
        return 0

@app.post("/api/report/{report_name}", response_model=dict)
async def create_report(report_name: str, report_data: Dict[str, List[str]]):
    if report_name in reports:
        raise HTTPException(status_code=400, detail="Report with this name already exists")

    metrics = report_data.get("metrics", [])
    users = report_data.get("users", [])

    offset = 20
    user_data = fetch_user_data(offset)

    report_result = {}
    for user_id in users:
        user_metrics = {}
        for metric in metrics:
            if metric == "dailyAverage":
                user_metrics["dailyAverage"] = calculate_daily_average(user_id, user_data)
            elif metric == "weeklyAverage":
                user_metrics["weeklyAverage"] = calculate_weekly_average(user_id, user_data)
            elif metric == "total":
                user_metrics["total"] = calculate_total_time(user_id, user_data)
            elif metric == "min":
                user_metrics["min"] = calculate_min_time(user_id, user_data)
            elif metric == "max":
                user_metrics["max"] = calculate_max_time(user_id, user_data)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported metric: {metric}")

        report_result[user_id] = user_metrics

    reports[report_name] = report_result

    return report_result

@app.get("/api/report/{report_name}", response_model=List[Dict[str, Optional[Dict[str, int]]]])
async def get_report(report_name: str):
    if report_name not in reports:
        raise HTTPException(status_code=404, detail="Report not found")

    return reports[report_name]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
