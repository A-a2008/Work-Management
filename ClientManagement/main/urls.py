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
    path("litigation/payments/<int:file_id>/", views.litigation_payments, name="litigation_payments"),
    path("nonlitigation/payments/<int:file_id>/", views.nonlitigation_payments, name="nonlitigation_payments"),
    path("litigation/payments/new/<int:file_id>/", views.litigation_payments_new, name="litigation_payments_new"),
    path("nonlitigation/payments/new/<int:file_id>/", views.nonlitigation_payments_new, name="nonlitigation_payments_new"),
    path("litigation/payments/edit/<int:payment_id>/", views.litigation_payments_edit, name="litigation_payments_edit"),
    path("nonlitigation/payments/edit/<int:payment_id>/", views.nonlitigation_payments_edit, name="nonlitigation_payments_edit"),
    path("notices/view/", views.notices_view_all, name="notices_view_all"),
    path("notices/new/choice/", views.notices_create_choices, name="notices_create_choices"),
    path("notices/new/sent/", views.notices_new_sent, name="notices_new_sent"),
    path("notices/new/received/", views.notices_new_received, name="notices_new_received"),
    path("notices/view/sent/<int:notice_id>/", views.notices_view_sent_notice, name="notices_view_sent_notice"),
    path("notices/update/sent/add_notice_document/<int:notice_id>/", views.notices_view_sent_notice_add_notice_document, name="notices_view_sent_notice_add_notice_document"),
    path("notices/update/sent/add_sent_date/<int:notice_id>/", views.notices_view_sent_notice_add_sent_date, name="notices_view_sent_notice_add_sent_date"),
    path("notices/update/sent/add_tracking_number/<int:notice_id>/", views.notices_view_sent_notice_add_tracking_number, name="notices_view_sent_notice_add_tracking_number"),
    path("notices/update/sent/add_acknowledgement_details/<int:notice_id>/", views.notices_view_sent_notice_add_acknowledgement_details, name="notices_view_sent_notice_add_acknowledgement_details"),
    path("notices/update/sent/completed/<int:notice_id>/", views.notices_view_sent_notice_completed, name="notices_view_sent_notice_completed"),
    path("notices/view/received/<int:notice_id>/", views.notices_view_received, name="notices_view_received"),
    path("notices/update/received/add_reply_notice_document/<int:notice_id>/", views.notices_view_received_add_reply_notice, name="notices_view_received_add_reply_notice"),
    path("notices/update/received/completed/<int:notice_id>/", views.notices_view_received_completed, name="notices_view_received_completed"),
    path("notices/sent_to_litigation/<int:notice_id>/", views.notices_sent_transfer, name="notices_sent_transfer"),
    path("notices/received_to_litigation/<int:notice_id>/", views.notices_received_transfer, name="notices_received_transfer"),


    # Errors
    path("no_access/", views.no_access, name="no_access"),
]