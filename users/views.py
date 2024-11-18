from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings

def get_weather_data(location):
    """Helper function to fetch weather data from WeatherAPI.com"""
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={location}&aqi=yes'
        response = requests.get(url)
        
        # Check if the API request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Print the raw data for debugging
            print("API Response:", data)
            
            # Ensure 'location' is in the response data
            if 'location' in data:
                return {
                    'location': data['location']['name'],
                    'region': data['location']['region'],
                    'temp_f': data['current']['temp_f'],
                    'temp_c': data['current']['temp_c'],
                    'condition': data['current']['condition']['text'],
                    'icon': data['current']['condition']['icon'],
                    'wind_mph': data['current']['wind_mph'],
                    'humidity': data['current']['humidity'],
                    'lat': data['location']['lat'],
                    'lon': data['location']['lon'],
                }
            else:
                print("Location key not found in response.")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")  # Network error or timeout
        return None

def home(request):
    # Define major US cities for initial weather display
    major_cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "Miami"
    ]
    
    weather_data = []
    for city in major_cities:
        data = get_weather_data(city)
        if data:
            weather_data.append(data)
    
    if not weather_data:
        messages.error(request, 'Error fetching weather data')
    
    return render(request, 'home.html', {'weather_data': weather_data})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get weather for user's location if available
    local_weather = None
    if user_profile.location:
        local_weather = get_weather_data(user_profile.location)
    
    return render(request, 'users/profile.html', {
        'profile': user_profile,
        'local_weather': local_weather
    })

@login_required
def profile_settings(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'users/settings.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signing up
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Redirect to the homepage or desired page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
