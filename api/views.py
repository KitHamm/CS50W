from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from volunteercenter.serializers import UserSerializer, deliverySerializer, prescriptionSerializer, welfareSerializer
from volunteercenter.models import User, Delivery, Prescription, Welfare
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

@csrf_exempt
@login_required
def user_search(request):
    clients = []
    if request.user.is_authenticated:
        _clients = User.objects.filter(user_type="client")
        for client in _clients:
            serializer = UserSerializer(client)
            clients.append(serializer.data)
        return JsonResponse({
            "clients": clients
        }, safe=False)
    else:
        return

@csrf_exempt
@login_required
def client_details(request, id):
    list = {}
    if request.user.is_authenticated:
        client = User.objects.get(pk=id)
        if Delivery.objects.filter(delivery_client=client).exists():
            delivery = []
            for _delivery in Delivery.objects.filter(delivery_client=client):
                _deliverySerializer = deliverySerializer(_delivery)
                delivery.append(_deliverySerializer.data)
            list["delivery"] = delivery
        if Prescription.objects.filter(prescription_client=client).exists():
            prescription = []
            for _prescription in Prescription.objects.filter(prescription_client=client):
                _prescriptionSerializer = prescriptionSerializer(_prescription)
                prescription.append(_prescriptionSerializer.data)
            list["prescription"] = prescription
        if Welfare.objects.filter(welfare_client=client).exists():
            welfare = []
            for welfare in Prescription.objects.filter(welfare_client=client):
                welfareSerializer = prescriptionSerializer(welfare)
                welfare.append(welfareSerializer.data)
            list["welfare"] = welfare
        return JsonResponse({
            "data": list
        }, safe=False)
    else:
        return

@csrf_exempt
@login_required
def order_details(request, id):
    if request.user.is_authenticated:

        if Delivery.objects.filter(order_number=id).exists():
            details = Delivery.objects.get(order_number=id)
            client = User.objects.get(username=details.delivery_client)
            operator = User.objects.get(username=details.operator)
            detailsSerializer = deliverySerializer(details)
            clientSerializer = UserSerializer(client)
            operatorSerializer = UserSerializer(operator)
        if Prescription.objects.filter(order_number=id).exists():
            details = Prescription.objects.get(order_number=id)
            serializer = prescriptionSerializer(details)
        if Welfare.objects.filter(order_number=id).exists():
            details = Welfare.objects.get(order_number=id)
            serializer = welfareSerializer(details)   

        return  JsonResponse({
            "details": detailsSerializer.data,
            "client": clientSerializer.data,
            "operator": operatorSerializer.data
        }, safe=False)

@csrf_exempt
@login_required
def pdf(request, order_number):
    if Delivery.objects.filter(order_number=order_number).exists():
        details = Delivery.objects.get(order_number=order_number)
        created_at = details.date_created.strftime("%d %b %Y, %I:%M %p")
        due_at = details.date_due.strftime("%d %b %Y")
        client = User.objects.get(username=details.delivery_client)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(50, 790, f"Request no. {order_number}")
        p.drawString(50, 755, f"{client.last_name}, {client.first_name}")
        p.drawString(50, 740, f"{client.address_1}")
        if client.address_2 != "":
            p.drawString(50, 725, f"{client.address_2}")
            p.drawString(50, 710, f"{client.city}")
            p.drawString(50, 695, f"{client.county}")
            p.drawString(50, 680, f"{client.postcode}")
            p.drawString(50, 665, f"{client.email}")
            p.drawString(50, 650, f"{client.phone_number}")
        else:
            p.drawString(50, 725, f"{client.city}")
            p.drawString(50, 710, f"{client.county}")
            p.drawString(50, 695, f"{client.postcode}")
            p.drawString(50, 680, f"{client.email}")
            p.drawString(50, 665, f"{client.phone_number}")
        topLine = [(50,650,540,650)]
        p.lines(topLine)
        p.drawString(50, 620, "Delivery Details")
        paragraph = Paragraph(f"{details.order}")
        paragraph.wrapOn(p, 800, 600)
        paragraph.drawOn(p, 50, 580)
        botLine = [(50,100,540,100)]
        p.drawString(50, 80, f"Call Handler: {request.user.username}")
        p.drawString(50, 65, f"Created: {created_at}")
        p.drawString(50, 50, f"Due on: {due_at}")
        p.drawString(400, 80, f"Assigned to: {details.operator}")
        p.drawString(400, 65, f"Status: {details.status}")
        p.lines(botLine)
        p.showPage()
        p.save()
        buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Order-{order_number}.pdf")
    if Prescription.objects.filter(order_number=order_number).exists():
        details = Prescription.objects.get(order_number=order_number)
    if Welfare.objects.filter(order_number=order_number).exists():
        details = Welfare.objects.get(order_number=order_number)  

