import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClientManagement.settings')
django.setup()

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
import asyncio
import threading
from datetime import datetime
from asgiref.sync import sync_to_async
import time
from telegram import Bot
from telegram.ext import MessageHandler, filters, Application


Litigation = apps.get_model("main", "Litigation")
WorkLigitation = apps.get_model("main", "WorkLigitation")
NonLitigation = apps.get_model("main", "NonLitigation")
WorkNonLitigation = apps.get_model("main", "WorkNonLitigation")
User = apps.get_model("accounts", "User")

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


def remind_litigation():
    works_incomplete = sort_works_incomplete()
    for incomplete_work in works_incomplete:
        if incomplete_work["type"] == "WorkLigitation":
            work = WorkLigitation.objects.get(id=incomplete_work["id"])
            litigation = Litigation.objects.get(id=work.litigation.id)
            current_message = message.format(employee_name=work.to_name, case_name=litigation.name, work=work.work, work_details=work.details if work.details else 'Not Provided', completion_date=work.completion_date, link=f"http://127.0.0.1:8000/litigation/view/{litigation.id}/")
        
            asyncio.run(send_message(text=current_message, group_id=group_id))


def remind_nonlitigation():
    works_incomplete = sort_works_incomplete()
    for incomplete_work in works_incomplete:
        if incomplete_work["type"] == "WorkNonLitigation":
            work = WorkNonLitigation.objects.get(id=incomplete_work["id"])
            nonlitigation = NonLitigation.objects.get(id=work.non_litigation.id)
            current_message = message.format(employee_name=work.to_name, case_name=nonlitigation.name, work=work.work, work_details=work.details if work.details else 'Not Provided', completion_date=work.completion_date, link=f"http://127.0.0.1:8000/nonlitigation/view/{nonlitigation.id}/")
        
            asyncio.run(send_message(text=current_message, group_id=group_id))


async def new_member_handler(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        user_id = member.id
        username = member.username
        name = f"{member.first_name} {member.last_name}"
        print(f"User ID: {user_id}, User Name: {username}, Name: {name}")
        
        try:
            user = await sync_to_async(User.objects.get)(telegram_name=name)
            user.telegram_user_id = user_id
            await sync_to_async(user.save)()
        except ObjectDoesNotExist:
            print("User not found")
        

def schedule_reminders():
    reminder_times_litigation = ["09:30", "15:00", "18:30"]
    reminder_times_nonlitigation = ["19:30"]

    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time in reminder_times_litigation:
            threading.Thread(target=remind_litigation).start()

        if current_time in reminder_times_nonlitigation:
            threading.Thread(target=remind_nonlitigation).start()

        time.sleep(5)

def main():
    reminder_thread = threading.Thread(target=schedule_reminders)
    reminder_thread.daemon = True
    reminder_thread.start()
    
    application = Application.builder().token(bot_token).build()

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
