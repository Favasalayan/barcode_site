import pandas as pd
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Scanhistory
from .forms import ExcelUploadForm
from django.http import JsonResponse


# -----------------------
# WEB PAGES
# -----------------------

def home(request):
    total_products = Product.objects.count()
    total_scans = Scanhistory.objects.count()

    return render(request, "home.html", {
        "total_products": total_products,
        "total_scans": total_scans
    })
    
    
def scan_page(request):
    return render(request, "scan.html")

def check_barcode_api(request):
    barcode = request.GET.get("barcode")

    try:
        product = Product.objects.get(barcode=barcode)

        return JsonResponse({
            "exists": True,
            "name": product.name,
            "required_qty": product.required_qty
        })

    except Product.DoesNotExist:
        return JsonResponse({"exists": False})


def history(request):
    scans = Scanhistory.objects.all().order_by("-scan_time")
    return render(request, "history.html", {"scans": scans})


# -----------------------
# EXCEL UPLOAD
# -----------------------

def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES["excel_file"]

            try:
                with transaction.atomic():

                    # 🔥 Delete old order list
                    Product.objects.all().delete()

                    # 🔥 Delete old scan history
                    Scanhistory.objects.all().delete()

                    # 🔥 Read new Excel
                    df = pd.read_excel(excel_file)

                    for _, row in df.iterrows():
                        barcode = str(row["item_number"]).split(".")[0].strip()

                        Product.objects.create(
                            barcode=barcode,
                            name=str(row["Name"]).strip(),
                            required_qty=int(row["QTY"])
                        )

                messages.success(request, "New order uploaded. Old data cleared successfully.")
                return redirect("home")

            except Exception as e:
                messages.error(request, f"Upload failed: {str(e)}")
                return redirect("upload_excel")

    else:
        form = ExcelUploadForm()

    return render(request, "upload.html", {"form": form})

# -----------------------
# ANDROID APIs
# -----------------------

# 1️⃣ Check Product Exists
@api_view(["GET"])
def scan_product(request, barcode):
    try:
        product = Product.objects.get(barcode=barcode)

        return Response({
            "exists": True,
            "name": product.name,
            "required_qty": product.required_qty
        })

    except Product.DoesNotExist:
        return Response({"exists": False})


# 2️⃣ Save Scan Result
@api_view(["POST"])
def save_scan_api(request):
    barcode = request.data.get("barcode")
    available_qty = int(request.data.get("available_qty"))

    try:
        product = Product.objects.get(barcode=barcode)

        Scanhistory.objects.create(
            barcode=product.barcode,
            name=product.name,
            required_qty=product.required_qty,
            available_qty=available_qty
        )

        return Response({"status": "saved"})

    except Product.DoesNotExist:
        return Response({"error": "Product not found"})