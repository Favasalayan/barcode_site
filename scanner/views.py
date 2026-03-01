import pandas as pd
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product

from .models import Product, Scanhistory



# HOME PAGE

def home(request):
    return render(request, "home.html")



# SCANNER PAGE

def index(request):
    return render(request, "index.html")



# CHECK BARCODE (NO AUTO SAVE HERE)

def check_barcode(request):
    barcode = request.GET.get('barcode')

    if barcode:
        barcode = barcode.strip().replace('.0', '')

    try:
        product = Product.objects.get(barcode=barcode)

        return JsonResponse({
            'exists': True,
            'name': product.name,
            'qty': product.qty
        })

    except Product.DoesNotExist:
        return JsonResponse({'exists': False})



# SAVE SCAN (ONLY SAVE HERE)

@csrf_exempt
def save_scan(request):
    if request.method == "POST":
        data = json.loads(request.body)

        barcode = data.get("barcode")
        name = data.get("name")
        qty = int(data.get("qty", 1))

        Scanhistory.objects.create(
            barcode=barcode,
            name=name,
            scanned_qty=qty
        )

        return JsonResponse({"status": "saved"})



# HISTORY PAGE

def history(request):
    scans = Scanhistory.objects.all().order_by('-id')  # safer than scan_time
    return render(request, "history.html", {'scans': scans})



# EXCEL UPLOAD

def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            messages.error(request, "No file uploaded.")
            return redirect('upload_excel')

        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            Product.objects.update_or_create(
                barcode=str(row['item_number']),
                defaults={
                    'name': row['Name'],   # match Excel column exactly
                    'qty': int(row['QTY'])
                }
            )

        messages.success(request, "Excel uploaded successfully.")
        return redirect('home')

    return render(request, 'upload.html')

#API

@api_view(['GET'])
def check_barcode(request, barcode):
    try:
        product = Product.objects.get(barcode=barcode)
        return Response({
            "name": product.name,
            "stock": product.stock,
            "price": product.price
        })
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

