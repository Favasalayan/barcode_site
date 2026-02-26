import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .forms import ExcelUploadForm

def index(request):
    return render(request, "index.html")

def check_barcode(request):
    barcode = request.GET.get('barcode')

    if barcode:
        barcode = barcode.strip()
        barcode = barcode.replace('.0', '')  # Fix scanner/excel issue

    try:
        product = Product.objects.get(barcode=barcode)

        return JsonResponse({
            'exists': True,
            'name': product.name,
            'qty': product.qty
        })

    except Product.DoesNotExist:
        return JsonResponse({'exists': False})
    
def upload_excel(request):
    message = ""

    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES['file']

            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                barcode = str(row['item_number']).replace('.0', '').strip()

                Product.objects.get_or_create(
                    barcode=barcode,
                    defaults={
                        'name': row['Name'],
                        'qty': int(row['QTY'])
                    }
                )

            message = "✅ Excel uploaded successfully!"

    else:
        form = ExcelUploadForm()

    return render(request, "upload.html", {
        'form': form,
        'message': message
    })