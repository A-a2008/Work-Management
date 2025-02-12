from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.apps import apps
from accounts.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from .decorators import login_required, group_required
from itertools import chain
from operator import attrgetter

Litigation = apps.get_model("main", "Litigation")
WorkLigitation = apps.get_model("main", "WorkLigitation")
NonLitigation = apps.get_model("main", "NonLitigation")
WorkNonLitigation = apps.get_model("main", "WorkNonLitigation")
PaymentsLitigation = apps.get_model("main", "PaymentsLitigation")
PaymentsNonLitigation = apps.get_model("main", "PaymentsNonLitigation")
PaymentsLitigationDate = apps.get_model("main", "PaymentsLitigationDate")
PaymentsNonLitigationDate = apps.get_model("main", "PaymentsNonLitigationDate")
NoticeSent = apps.get_model("main", "NoticeSent")
NoticeSentRejoinder = apps.get_model("main", "NoticeSentRejoinder")
NoticeSentReply = apps.get_model("main", "NoticeSentReply")
NoticeReceived = apps.get_model("main", "NoticeReceived")
NoticeReceivedRejoinder = apps.get_model("main", "NoticeReceivedRejoinder")

# Create your views here.

def home(request):
    return render(request, "index.html")

@login_required("login")
@group_required("Litigation")
def litigation_new(request):
    if request.method == "POST":
        name = request.POST["name"]
        case_type = request.POST.get("case_type")
        if not case_type:
            data = {
                "error_message": "Case Type not specified. Please specify"
            }
            return render(request, "main/litigation_new.html", data)
        case_number = f'{request.POST["case_number_1"]}/{request.POST["case_number_2"]}'
        document_link = request.POST["document_link"]
        representing_for = request.POST["representing_for"]

        Litigation.objects.create(
            name=name,
            case_type=case_type,
            case_number=case_number,
            representing_for=representing_for,
            document_link=document_link,
            rough_work_pic=request.FILES.get("rough_picture")
        )

        return redirect("litigation_view_all")
    else:
        return render(request, "main/litigation_new.html")

@login_required("login")
@group_required("Litigation")
def litigation_view_all(request):
    files = Litigation.objects.all()
    data = {
        "files": files,
    }
    return render(request, "main/litigation_view_all.html", data)

@login_required("login")
@group_required("Litigation")
def litigation_view_file(request, file_id): # TODO: Arrange works in reverse order. Both litigation and non litigation
    file = Litigation.objects.get(id=file_id)
    document_link = True if file.document_link else False
    works = WorkLigitation.objects.filter(litigation=file).order_by('-id')
    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(name="Payments")

    data = {
        "file": file,
        "works": works,
        "document_link": document_link,
        "is_admin": True if group in user.groups.all() else False,
    }
    return render(request, "main/litigation_view_file.html", data)

@login_required("login")
@group_required("Litigation")
def litigation_file_add_document_link(request, file_id):
    file = Litigation.objects.get(id=file_id)
    file.document_link = request.POST["document_link"]
    file.save()

    return redirect(f"/litigation/view/{file_id}")

@login_required("login")
@group_required("Litigation")
def litigation_work_new(request, file_id):
    if request.method == 'POST':
        litigation = Litigation.objects.get(id=file_id)
        work = request.POST["work"]
        details = request.POST["details"]
        to = User.objects.get(id=request.POST["to"])
        completion_date = request.POST["completion_date"]
        priority_level = request.POST["priority_level"]
        reminder_start_date = request.POST["reminder_start_date"]

        WorkLigitation.objects.create(
            litigation=litigation,
            work=work,
            details=details,
            to=to,
            completion_date=completion_date,
            priority_level=priority_level,
            reminder_start_date=reminder_start_date,
        )
        return redirect(f"/litigation/view/{file_id}")
    else:
        employees = User.objects.filter(groups__name="Employees")
        completion_date = datetime.now() + timedelta(days=5)
        reminder_start_date = completion_date - timedelta(days=3)
        data = {
            "employees": employees,
            "file_id": file_id,
            "completion_date": completion_date.strftime("%Y-%m-%d"),
            "reminder_start_date": reminder_start_date.strftime("%Y-%m-%d"),
        }
        return render(request, "main/litigation_work_new.html", data)
    
@login_required("login")
@group_required("Litigation")
def litigation_add_rough_pic(request, file_id):
    file = Litigation.objects.get(id=file_id)
    file.rough_work_pic=request.FILES.get("rough_picture")
    file.save()

    return redirect(f"/litigation/view/{file_id}/")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_new(request):
    if request.method == 'POST':
        name = request.POST["name"]
        project_name = request.POST["project_name"]
        situation = request.POST["situation"]
        property_type = request.POST.get("property_type")
        if not property_type:
            data = {
                "error_message": "Property Type not specified. Please specify"
            }
            return render(request, "main/litigation_new.html", data)
        site_no = request.POST["site_no"]
        present_owner = request.POST["present_owner"]
        document_link = request.POST["document_link"]

        nonlitigation = NonLitigation.objects.create(
            name=name,
            project_name=project_name,
            situation=situation,
            property_type=property_type,
            site_no=site_no,
            present_owner=present_owner,
            document_link=document_link,
            rough_work_pic=request.FILES.get("rough_picture"),
            case_stage=1
        )

        employees = User.objects.filter(groups__name="Employees")
        completion_date = datetime.now() + timedelta(days=7)
        reminder_start_date = completion_date - timedelta(days=3)
        data = {
            "file": nonlitigation,
            "work": "Required List of Documents",
            "employees": employees,
            "completion_date": completion_date.strftime("%Y-%m-%d"),
            "reminder_start_date": reminder_start_date.strftime("%Y-%m-%d"),
        }

        return render(request, "main/nonlitigation_work_new.html", data)
    else:
        return render(request, "main/nonlitigation_new.html")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_view_all(request):
    files = NonLitigation.objects.all()
    data = {
        "files": files,
    }
    return render(request, "main/nonlitigation_view_all.html", data)

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_view_file(request, file_id):
    file = NonLitigation.objects.get(id=file_id)
    document_link = True if file.document_link else False
    works = WorkNonLitigation.objects.filter(non_litigation=file).order_by('-id')
    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(name="Payments")

    data = {
        "file": file,
        "works": works,
        "document_link": document_link,
        "is_admin": True if group in user.groups.all() else False,
    }
    return render(request, "main/nonlitigation_view_file.html", data)

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_file_add_document_link(request, file_id):
    file = NonLitigation.objects.get(id=file_id)
    file.document_link = request.POST["document_link"]
    file.save()

    return redirect(f"/nonlitigation/view/{file_id}")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_add_rough_pic(request, file_id):
    file = NonLitigation.objects.get(id=file_id)
    file.rough_work_pic=request.FILES.get("rough_picture")
    file.save()

    return redirect(f"/nonlitigation/view/{file_id}/")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_work_stage1_new(request, file_id):
    file = NonLitigation.objects.get(id=file_id)
    work = request.POST["work"]
    to = User.objects.get(id=request.POST["to"])
    completion_date = request.POST["completion_date"]
    reminder_start_date = request.POST["reminder_start_date"]

    WorkNonLitigation.objects.create(
        non_litigation=file,
        work=work,
        to=to,
        completion_date=completion_date,
        reminder_start_date=reminder_start_date,
    )

    file.case_stage += 1
    file.save()

    return redirect(f"/nonlitigation/view/{file_id}/")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_work_stage1_other(request, file_id):
    if request.method == "POST":
        file = NonLitigation.objects.get(id=file_id)
        work = request.POST["work"]
        to = User.objects.get(id=request.POST["to"])
        completion_date = request.POST["completion_date"]
        reminder_start_date = request.POST["reminder_start_date"]

        if file.case_stage > 3:
            details = request.POST["details"]
            WorkNonLitigation.objects.create(
                non_litigation=file,
                work=work,
                details=details,
                to=to,
                completion_date=completion_date,
                reminder_start_date=reminder_start_date,
            )
        else:
            WorkNonLitigation.objects.create(
                non_litigation=file,
                work=work,
                to=to,
                completion_date=completion_date,
                reminder_start_date=reminder_start_date,
            )

        file.case_stage += 1
        file.save()

        return redirect(f"/nonlitigation/view/{file_id}/")
    else:
        file = NonLitigation.objects.get(id=file_id)
        if file.case_stage == 2:
            work = "Remind client to send details"
            completion_date = datetime.now() + timedelta(days=3)
            reminder_start_date = completion_date - timedelta(days=2)
        elif file.case_stage == 3:
            work = "Send Opinion"
            completion_date = datetime.now() + timedelta(days=3)
            reminder_start_date = completion_date - timedelta(days=2)
        else:
            return redirect("nonlitigation_work_stage2_new")
        employees = User.objects.filter(groups__name="Employees")
        data = {
            "file": file,
            "work": work,
            "employees": employees,
            "completion_date": completion_date.strftime("%Y-%m-%d"),
            "reminder_start_date": reminder_start_date.strftime("%Y-%m-%d"),
        }

        return render(request, "main/nonlitigation_work_new.html", data)

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_work_stage2_new(request, file_id):
    if request.method == "POST":
        file = NonLitigation.objects.get(id=file_id)
        work = request.POST["work"]
        to = User.objects.get(id=request.POST["to"])
        completion_date = request.POST["completion_date"]
        reminder_start_date = request.POST["reminder_start_date"]
        details = request.POST["details"]

        WorkNonLitigation.objects.create(
            non_litigation=file,
            work=work,
            details=details,
            to=to,
            completion_date=completion_date,
            reminder_start_date=reminder_start_date,
        )

        return redirect("nonlitigation_view_all")
    else:
        file = NonLitigation.objects.get(id=file_id)
        completion_date = datetime.now() + timedelta(days=5)
        reminder_start_date = completion_date - timedelta(days=3)
        employees = User.objects.filter(groups__name="Employees")

        data = {
            "file": file,
            "employees": employees,
            "completion_date": completion_date.strftime("%Y-%m-%d"),
            "reminder_start_date": reminder_start_date.strftime("%Y-%m-%d"),
        }

        return render(request, "main/nonlitigation_work_new.html", data)

@login_required("login")
@group_required("Litigation")
def litigation_finished_work(request, work_id):
    work = WorkLigitation.objects.get(id=work_id)
    work.finished = True
    work.finished_time = datetime.now()
    if datetime.strptime(str(work.finished_time).split()[0], "%Y-%m-%d") <= datetime.strptime(str(work.completion_date), "%Y-%m-%d"):
        work.finished_in_time = True
    else:
        work.finished_in_time = False
    work.save()

    return redirect(f"/litigation/view/{work.litigation.id}#work-{work.id}/")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_finished_work(request, work_id):
    work = WorkNonLitigation.objects.get(id=work_id)
    work.finished = True
    work.finished_time = datetime.now()
    if datetime.strptime(str(work.finished_time).split()[0], "%Y-%m-%d") <= datetime.strptime(str(work.completion_date), "%Y-%m-%d"):
        work.finished_in_time = True
    else:
        work.finished_in_time = False
    work.save()

    return redirect(f"/nonlitigation/view/{work.non_litigation.id}#work-{work.id}/")

@login_required("login")
@group_required("Litigation")
def litigation_mark_unfinished_work(request, work_id):
    work = WorkLigitation.objects.get(id=work_id)
    work.finished = False
    work.finished_time = None
    work.finished_in_time = False
    work.save()

    return redirect(f"/litigation/view/{work.litigation.id}#work-{work.id}/")

@login_required("login")
@group_required("Non Litigation")
def nonlitigation_mark_unfinished_work(request, work_id):
    work = WorkNonLitigation.objects.get(id=work_id)
    work.finished = False
    work.finished_time = None
    work.finished_in_time = False
    work.save()

    return redirect(f"/litigation/view/{work.non_litigation.id}#work-{work.id}/")

@group_required("Payments")
def litigation_payments(request, file_id):
    file = Litigation.objects.get(id=file_id)
    payments = PaymentsLitigation.objects.filter(litigation=file)
    payments_dates = []
    for payment in payments:
        dates = PaymentsLitigationDate.objects.filter(payment=payment)
        payments_dates.append((payment, dates))

    data = {
        "file": file,
        "payments_dates": payments_dates,
    }

    return render(request, "main/litigation_payments.html", data)

@group_required("Payments")
def nonlitigation_payments(request, file_id):
    file = NonLitigation.objects.get(id=file_id)
    payments = PaymentsNonLitigation.objects.filter(non_litigation=file)
    payments_dates = []
    for payment in payments:
        dates = PaymentsNonLitigationDate.objects.filter(payment=payment)
        payments_dates.append((payment, dates))

    data = {
        "file": file,
        "payments_dates": payments_dates,
    }

    return render(request, "main/nonlitigation_payments.html", data)

@group_required("Payments")
def litigation_payments_new(request, file_id):
    if request.method == "POST":
        file = Litigation.objects.get(id=file_id)
        name = request.POST["name"]
        amount = int(request.POST["amount"])

        PaymentsLitigation.objects.create(
            litigation=file,
            name=name,
            amount=amount,
        )

        return redirect(f"/litigation/payments/{file_id}/")
    else:
        file = Litigation.objects.get(id=file_id)

        data = {
            "file": file,
            "litigation": True,
        }

        return render(request, "main/payments_new.html", data)
    
@group_required("Payments")
def nonlitigation_payments_new(request, file_id):
    if request.method == "POST":
        file = NonLitigation.objects.get(id=file_id)
        name = request.POST["name"]
        amount = int(request.POST["amount"])

        PaymentsNonLitigation.objects.create(
            non_litigation=file,
            name=name,
            amount=amount,
        )

        return redirect(f"/nonlitigation/payments/{file_id}/")
    else:
        file = NonLitigation.objects.get(id=file_id)

        data = {
            "file": file,
            "litigation": False,
        }

        return render(request, "main/payments_new.html", data)
    
@group_required("Payments")
def litigation_payments_edit(request, payment_id):
    if request.method == "POST":
        payment = PaymentsLitigation.objects.get(id=payment_id)
        amount_paid = int(request.POST["amount_paid"])

        payment.amount_paid = amount_paid
        payment.save()

        PaymentsLitigationDate.objects.create(
            payment=payment,
            date_paid=datetime.now().date(),
            amount=amount_paid,
        )

        return redirect(f"/litigation/payments/{payment.litigation.id}/")
    else:
        payment = PaymentsLitigation.objects.get(id=payment_id)

        data = {
            "litigation": True,
            "payment": payment,
        }

        return render(request, "main/payments_edit.html", data)
    
@group_required("Payments")
def nonlitigation_payments_edit(request, payment_id):
    if request.method == "POST":
        payment = PaymentsNonLitigation.objects.get(id=payment_id)
        amount_paid = int(request.POST["amount_paid"])

        payment.amount_paid = amount_paid
        payment.save()

        PaymentsNonLitigationDate.objects.create(
            payment=payment,
            date_paid=datetime.now().date(),
            amount=amount_paid,
        )

        return redirect(f"/nonlitigation/payments/{payment.non_litigation.id}/")
    else:
        payment = PaymentsNonLitigation.objects.get(id=payment_id)

        data = {
            "litigation": False,
            "payment": payment,
        }

        return render(request, "main/payments_edit.html", data)

@group_required("Litigation")
def notices_view_all(request):
    notices_unsorted = list(chain(NoticeSent.objects.all(), NoticeReceived.objects.all()))
    notices = sorted(notices_unsorted, key=lambda x: (x.completed, x.completion_date))

    data = {
        "notices": notices,
    }

    return render(request, "main/notices_view_all.html", data)


@group_required("Litigation")
def notices_create_choices(request):
    return render(request, "main/notices_new_choice.html")


@group_required("Litigation")
def notices_new_sent(request):
    if request.method == "POST":
        name = request.POST["name"]
        completion_date = request.POST["completion_date"]

        NoticeSent.objects.create(
            name=name,
            completion_date=completion_date
        )

        return redirect("notices_view_all")
    else:
        return render(request, "main/notices_new_sent.html")
    

@group_required("Litigation")
def notices_new_received(request):
    if request.method == "POST":
        name = request.POST["name"]
        notice_type = request.POST["type"]
        if notice_type == "NI":
            ni_deadline = request.POST["ni_deadline"]
        received_date_client = request.POST["received_date_client"]
        received_date_office = request.POST["received_date_office"]
        received_employee = User.objects.get(id=request.POST["received_employee"])
        completion_date = request.POST["completion_date"]

        NoticeReceived.objects.create(
            name=name,
            type=notice_type,
            received_date_client=received_date_client,
            received_date_office=received_date_office,
            received_employee=received_employee,
            completion_date=completion_date,
            ni_deadline=ni_deadline if notice_type == "NI" else None,
        )

        return redirect("notices_view_all")
    else:
        employees = User.objects.filter(groups__name="Employees")
        ni_deadline = datetime.now() + timedelta(days=30)
        data = {
            "employees": employees,
            "ni_deadline": ni_deadline.strftime("%Y-%m-%d"),
            "office_received_date": datetime.now().strftime("%Y-%m-%d"),
        }

        return render(request, "main/notices_new_received.html", data)
    

@group_required("Litigation")
def notices_view_sent_notice(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)

    data = {
        "notice": notice
    }
    
    return render(request, "main/notices_view_sent_notice.html", data)


@group_required("Litigation")
def notices_view_sent_notice_add_sent_date(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    notice.sent_date = request.POST["notice_sent_date"]
    notice.save()

    return redirect(f"/notices/view/sent/{notice_id}/")


@group_required("Litigation")
def notices_view_sent_notice_add_tracking_number(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    notice.tracking_number = request.POST["tracking_number"]
    notice.save()

    return redirect(f"/notices/view/sent/{notice_id}/")


@group_required("Litigation")
def notices_view_sent_notice_add_acknowledgement_details(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    notice.acknowledgement = request.POST["acknowledgement"]
    notice.acknowledgement_received_date = request.POST["acknowledgement_received_date"]
    notice.save()

    return redirect(f"/notices/view/sent/{notice_id}/")


@group_required("Litigation")
def notices_view_sent_notice_add_notice_document(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    notice_document = request.FILES.get("notice_document")
    path = f"{notice_id}/notice_document/{notice_document.name}"
    notice.notice_document.save(path, notice_document)
    notice.save()

    return redirect(f"/notices/view/sent/{notice_id}/")


@group_required("Litigation")
def notices_view_sent_notice_completed(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    if not notice.completed:
        notice.completed = True
    else:
        notice.completed = False
    notice.save()

    return redirect(f"/notices/view/")


@group_required("Litigation")
def notices_sent_transfer(request, notice_id):
    notice = NoticeSent.objects.get(id=notice_id)
    if request.method == "POST":
        name = request.POST["name"]
        case_type = request.POST.get("case_type")
        if not case_type:
            data = {
                "notice": notice,
                "error_message": "Case Type not specified. Please specify"
            }
            return render(request, "main/notices_to_litigation.html", data)
        case_number = f'{request.POST["case_number_1"]}/{request.POST["case_number_2"]}'
        document_link = request.POST["document_link"]
        representing_for = request.POST["representing_for"]

        Litigation.objects.create(
            name=name,
            case_type=case_type,
            case_number=case_number,
            representing_for=representing_for,
            document_link=document_link,
            rough_work_pic=request.FILES.get("rough_picture")
        )

        return redirect("litigation_view_all")
    else:
        data = {
            "type": "sent",
            "notice": notice
        }

        return render(request, "main/notices_to_litigation.html", data)


@group_required("Litigation")
def notices_view_received(request, notice_id):
    notice = NoticeReceived.objects.get(id=notice_id)

    data = {
        "notice": notice,
    }

    return render(request, "main/notices_view_received_notice.html", data)


@group_required("Litigation")
def notices_view_received_add_reply_notice(request, notice_id):
    notice = NoticeReceived.objects.get(id=notice_id)
    reply_notice_document = request.FILES.get("reply_notice_document")
    path = f"{notice_id}/reply_notice_document/{reply_notice_document.name}"
    notice.reply_notice_document.save(path, reply_notice_document)
    notice.reply_notice_sent = True
    notice.reply_notice_sent_date = datetime.now().date()
    notice.save()

    return redirect(f"/notices/view/received/{notice_id}/")


@group_required("Litigation")
def notices_view_received_completed(request, notice_id):
    notice = NoticeReceived.objects.get(id=notice_id)
    if not notice.completed:
        notice.completed = True
    else:
        notice.completed = False
    notice.save()

    return redirect(f"/notices/view/")


@group_required("Litigation")
def notices_received_transfer(request, notice_id):
    notice = NoticeReceived.objects.get(id=notice_id)
    if request.method == "POST":
        name = request.POST["name"]
        case_type = request.POST.get("case_type")
        if not case_type:
            data = {
                "notice": notice,
                "error_message": "Case Type not specified. Please specify"
            }
            return render(request, "main/notices_to_litigation.html", data)
        case_number = f'{request.POST["case_number_1"]}/{request.POST["case_number_2"]}'
        document_link = request.POST["document_link"]
        representing_for = request.POST["representing_for"]

        Litigation.objects.create(
            name=name,
            case_type=case_type,
            case_number=case_number,
            representing_for=representing_for,
            document_link=document_link,
            rough_work_pic=request.FILES.get("rough_picture")
        )

        return redirect("litigation_view_all")
    else:
        data = {
            "type": "received",
            "notice": notice
        }

        return render(request, "main/notices_to_litigation.html", data)


# Errors
def no_access(request):
    return render(request, "errors/group.html")

def error_400(request, exception):
    data = {
        "error": "400 - Bad Request",
        "tagline": "The request could not be understood by the server. Please check your request and try again."
    }
    return render(request, "errors/error.html", data)

def error_403(request, exception):
    data = {
        "error": "403 - Forbidden",
        "tagline": "You don't have permission to access this page. If you believe this is an error, please contact support."
    }
    return render(request, "errors/error.html", data)

def error_404(request, exception):
    data = {
        "error": "404 - Page Not Found",
        "tagline": "The requested page was not found. Please try another one."
    }
    return render(request, "errors/error.html", data)

def error_500(request):
    data = {
        "error": "500 - Internal Server Error",
        "tagline": "Something went wrong on our end. Please try again later or contact support."
    }
    return render(request, "errors/error.html", data)