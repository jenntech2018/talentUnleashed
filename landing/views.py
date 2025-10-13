from django.shortcuts import render, redirect
from .forms import ContestantForm

def home(request):
    return render(request, 'landing/home.html')

def register(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ContestantForm()
    return render(request, 'landing/register.html', {'form': form})

def thank_you(request):
    return render(request, 'landing/thank_you.html')