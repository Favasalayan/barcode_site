from django.urls import path
from . import views

urlpatterns = [
    # Web pages
    path("", views.home, name="home"),
    path("history/", views.history, name="history"),
    path("upload/", views.upload_excel, name="upload_excel"),

    # APIs for Android
    path("api/scan/<str:barcode>/", views.scan_product),
    path("api/save-scan/", views.save_scan_api),
    path("scan/", views.scan_page, name="scan_page"),
    path("api/check-barcode/", views.check_barcode_api),
]