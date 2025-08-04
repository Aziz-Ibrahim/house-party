from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    """
    Render the main index page for the frontend.
    """
    return render(request, 'frontend/index.html')