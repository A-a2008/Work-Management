from django.contrib.auth.models import Group

def group_context(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            data = {
                "litigation_": True,
                "nonlitigation_": True,
            }
        else:
            litigation = Group.objects.get(name="Litigation")
            nonlitigation = Group.objects.get(name="Non Litigation")

            data = {
                "litigation_": True if litigation in request.user.groups.all() else False,
                "nonlitigation_": True if nonlitigation in request.user.groups.all() else False,
            }
    else:
        data = {}
    return data