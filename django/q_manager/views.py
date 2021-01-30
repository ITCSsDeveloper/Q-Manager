from django.shortcuts import render


# Index
def index(request):
    return render(request, "default.index.html")

# Create
def create_view(request):
    return render(request, "create.index.html")

# Update
def update_view(request):
    return render(request, "update.index.html")

# Delete
def delete_view(request):
    return render(request, "delete.index.html")

# Monitor
def monitor(request):
    return render(request, "monitor.index.html")