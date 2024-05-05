from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("litigation/new/", views.litigation_new, name="litigation_new"),
    path("litigation/view/", views.litigation_view_all, name="litigation_view_all"),
    path("litigation/view/<int:file_id>/", views.litigation_view_file, name="litigation_view_file"),
    path("litigation/work/new/<int:file_id>/", views.litigation_work_new, name="litigation_work_new"),
    path("litigation/file_add_document_link/<int:file_id>/", views.litigation_file_add_document_link, name="litigation_file_add_document_link"),
    path("nonlitigation/new/", views.nonlitigation_new, name="nonlitigation_new"),
    path("nonlitigation/view/", views.nonlitigation_view_all, name="nonlitigation_view_all"),
    path("nonlitigation/view/<int:file_id>/", views.nonlitigation_view_file, name="nonlitigation_view_file"),
    path("nonlitigation/file_add_document_link/<int:file_id>/", views.nonlitigation_file_add_document_link, name="nonlitigation_file_add_document_link"),
    path("litigation/add_rough_work_pic/<int:file_id>/", views.litigation_add_rough_pic, name="litigation_add_rough_pic"),
    path("nonlitigation/add_rough_work_pic/<int:file_id>/", views.nonlitigation_add_rough_pic, name="nonlitigation_add_rough_pic"),
    path("litigation/finished_work/<int:work_id>/", views.litigation_finished_work, name="litigation_finished_work"),
    path("nonlitigation/finished_work/<int:work_id>/", views.nonlitigation_finished_work, name="nonlitigation_finished_work"),
    path("litigation/mark_unfished_work/<int:work_id>/", views.litigation_mark_unfinished_work, name="litigation_mark_unfinished_work"),
    path("nonlitigation/mark_unfished_work/<int:work_id>/", views.nonlitigation_mark_unfinished_work, name="nonlitigation_mark_unfinished_work"),
    path("nonlitigation/work/new/stage1/<int:file_id>/", views.nonlitigation_work_stage1_new, name="nonlitigation_work_stage1_new"),
    path("nonlitigation/work/new/stage1/other/<int:file_id>/", views.nonlitigation_work_stage1_other, name="nonlitigation_work_stage1_other"),
    path("nonlitigation/work/new/stage2/<int:file_id>/", views.nonlitigation_work_stage2_new, name="nonlitigation_work_stage2_new"),
]