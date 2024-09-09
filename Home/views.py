from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests
import json
import os

def home(request):
    if request.method == "POST":
        # Extract data from form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # EmailJS parameters
        service_id = os.getenv('service_j21odkc')
        template_id = os.getenv('template_6jc57jk')
        user_id = os.getenv('ReL8vTrgs4W5q25lG')
        url = 'https://api.emailjs.com/api/v1.0/email/send'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + user_id,  # Assuming Basic authentication
        }
        payload = {
            'service_id': service_id,
            'template_id': template_id,
            'user_id': user_id,
            'template_params': {
                'name': name,
                'email': email,
                'message': message,
            }
        }

        # Send request to EmailJS
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            
            # Check if response is JSON and handle it
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                messages.error(request, f"Failed to decode JSON response from EmailJS: {e}")
                return render(request, 'index.html')

            # Check if EmailJS API response contains error
            if 'error' in data:
                messages.error(request, f"EmailJS error: {data['error']}")
                return render(request, 'index.html')

            messages.success(request, "Email sent successfully!")
        except requests.RequestException as e:
            messages.error(request, f"Failed to send email: {e}")

    return render(request, 'index.html')
