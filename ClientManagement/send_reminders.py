import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClientManagement.settings')
django.setup()

from telegram import Bot
from django.apps import apps
import asyncio
from datetime import datetime

Litigation = apps.get_model("main", "Litigation")
WorkLigitation = apps.get_model("main", "WorkLigitation")
NonLitigation = apps.get_model("main", "NonLitigation")
WorkNonLitigation = apps.get_model("main", "WorkNonLitigation")

def sort_works_incomplete():
    incomplete_litigation = WorkLigitation.objects.filter(finished=False, reminder_start_date__lte=datetime.now().date())
    incomplete_non_litigation = WorkNonLitigation.objects.filter(finished=False, reminder_start_date__lte=datetime.now().date())

    all_works = list(incomplete_litigation) + list(incomplete_non_litigation)
    
    # Define a mapping of priority levels to numeric values
    priority_order = {
        "High": 3,
        "Normal": 2,
        "Low": 1
    }
    
    # Get the current date
    current_date = datetime.now().date()
    
    # Sort all incomplete work items based on priority level (if available) and closeness of the completion_date from the current date
    sorted_works = sorted(all_works, key=lambda x: (priority_order.get(getattr(x, 'priority_level', None), 0), abs((x.completion_date - current_date).days)))
    
    # Convert the sorted works into a list of dictionaries
    sorted_works_dicts = [
        {"id": work.id, "type": type(work).__name__}
        for work in sorted_works
    ]
    
    return sorted_works_dicts


group_id = "-4127805355"
bot_token = "7179515450:AAF5dJ4xqcyHxwICuBp3DlDwRCI5ydiTYWQ"
bot = Bot(token=bot_token)

async def send_message(text, group_id):
    async with bot:
        await bot.send_message(text=text, chat_id=group_id)

message = """{employee_name}, you have a work pending.

Details:
Case: {case_name}
Work: {work}
Work Details: {work_details}
Completion Date: {completion_date}

To view more details or to mark it finished, please click on this link: {link}
"""

works_incomplete = sort_works_incomplete()
print(works_incomplete)
for incomplete_work in works_incomplete:
    if incomplete_work["type"] == "WorkLigitation":
        work = WorkLigitation.objects.get(id=incomplete_work["id"])
        litigation = Litigation.objects.get(id=work.litigation.id)
        current_message = message.format(employee_name=work.to_name, case_name=litigation.name, work=work.work, work_details=work.details if work.details else 'Not Provided', completion_date=work.completion_date, link=f"http://127.0.0.1:8000/litigation/view/{litigation.id}/")
    else:
        work = WorkNonLitigation.objects.get(id=incomplete_work["id"])
        nonlitigation = NonLitigation.objects.get(id=work.non_litigation.id)
        current_message = message.format(employee_name=work.to_name, case_name=nonlitigation.name, work=work.work, work_details=work.details if work.details else 'Not Provided', completion_date=work.completion_date, link=f"http://127.0.0.1:8000/nonlitigation/view/{nonlitigation.id}/")

    print(current_message)
    async def main():
        await send_message(text=current_message, group_id=group_id)

    asyncio.run(main())

