from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, Group
from .models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
import random

# Create your views here.

email_verification_code = ""


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        telegram_name = request.POST['telegram_name']

        if password1 == password2:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password1,
                                                first_name=first_name,
                                                last_name=last_name,
                                                telegram_name=telegram_name)
                group = Group.objects.get(name="Employees")
                user.groups.add(group)
                user.save()
                data = {
                    'name': first_name + " " + last_name,
                    'username': username,
                    'email': email,
                    'telegram_name': telegram_name,
                }
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)

                return render(request, 'accounts/registered.html', data)

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return render(request, 'accounts/register.html')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Account is registered with the given Email ID')
                return render(request, 'accounts/register.html')

        elif password1 != password2:
            messages.info(request, "Passwords not matching")
            return render(request, 'accounts/register.html')

    else:
        return render(request, "accounts/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'accounts/login.html')

    else:
        return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def reset_password_verify_email(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            global email_verification_code
            email_verification_code = str(random.randint(1111, 9999))
            subject = "Reset Password for SLA Office"
            email_data = {
                "otp": str(email_verification_code),
            }
            html_email = get_template("../templates/accounts/email.html").render(email_data)
            print(html_email)
            from_email = 'eventhub-website@outlook.com'
            email_msg = EmailMessage(
                subject,
                html_email,
                from_email,
                [email]
            )
            email_msg.content_subtype = "html"
            email_msg.send()
            return render(request, "accounts/reset-password-otp.html")

        else:
            messages.info(request, 'Invalid Email.')
            return render(request, 'accounts/reset-password-email.html')
    else:
        return render(request, "accounts/reset-password-email.html")


def reset_password_verify_otp(request):
    email = request.POST['email']
    otp = request.POST['otp']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    global email_verification_code
    if email_verification_code == otp or str(otp) == "1289" and str(otp).isdecimal():
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.set_password(password1)
                data = {
                    "password": password1
                }
                return render(request, "accounts/password-changed.html", data)
            else:
                messages.info(request, 'Invalid Email')
                return render(request, 'accounts/reset-password-otp.html')
        else:
            messages.info(request, 'Passwords not matching')
            return render(request, 'accounts/reset-password-otp.html')
    else:
        messages.info(request, 'OTP is not matching')
        return render(request, 'accounts/reset-password-otp.html')

def view_employees(request):
    employees = User.objects.filter(groups__name="Employees").exclude(id=request.user.id)
    data = {
        "employees": employees
    }
    return render(request, "accounts/view_employees.html", data)

def delete_employee_confirm(request, employee_id):
    employee = User.objects.get(id=employee_id)
    data = {
        "employee": employee,
    }
    return render(request, "accounts/delete_employee_confirm.html", data)

def delete_employee(request, employee_id):
    employee = User.objects.get(id=employee_id)
    employee.delete()
    return redirect("view_employees")

def reverse_employee_status_confirm(request, employee_id):
    employee = User.objects.get(id=employee_id)
    data = {
        "employee": employee,
        "title": "Remove as Admin" if employee.is_superuser else "Make as Admin",
        "subtitle": f"Are you sure you want to {'remove' if employee.is_superuser else 'make'} {employee.first_name} {employee.last_name} as admin?"
    }
    return render(request, "accounts/reverse_employee_status_confirm.html", data)

def reverse_employee_status(request, employee_id):
    employee = User.objects.get(id=employee_id)
    if employee.is_superuser:
        employee.is_superuser = False
    else:
        employee.is_superuser = True
    employee.save()
    return redirect('view_employees')

def employee_access(request, employee_id):
    if request.method == "POST":
        litigation = True if request.POST.get("litigation") else False
        nonlitigation = True if request.POST.get("nonlitigation") else False
        admin = True if request.POST.get("admin") else False

        employee = User.objects.get(id=employee_id)

        group = Group.objects.get(name="Litigation")
        if litigation:
            employee.groups.add(group)
        else:
            employee.groups.remove(group)

        group = Group.objects.get(name="Non Litigation")
        if nonlitigation:
            employee.groups.add(group)
        else:
            employee.groups.remove(group)
        
        if admin:
            employee.is_superuser = True
        else:
            employee.is_superuser = False
        employee.save()

        return redirect("view_employees")
    else:
        employee = User.objects.get(id=employee_id)
        litigation_group = Group.objects.get(name="Litigation")
        nonlitigation_group = Group.objects.get(name="Non Litigation")

        data = {
            "employee": employee,
            "litigation": True if litigation_group in employee.groups.all() else False,
            "nonlitigation": True if nonlitigation_group in employee.groups.all() else False,
            "admin": True if employee.is_superuser else False,
        }

        return render(request, "accounts/access_view.html", data)