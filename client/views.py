from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
  # dummy data for slider
  slides = [
    {
      "heading": "We Provide <span>Medical</span> Services That You Can <span>Trust!</span>",
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed nisl pellentesque, faucibus libero eu, gravida quam.",
      "left_button": "Get Appointment",
      "right_button": "Learn More",
      "background": "img/slider2.jpg"
    },
    {
      "heading": "We Provide <span>Medical</span> Services That You Can <span>Trust!</span>",
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed nisl pellentesque, faucibus libero eu, gravida quam.",
      "left_button": "Get Appointment",
      "right_button": "About Us",
      "background": "img/slider.jpg"
    },
    {
      "heading": "We Provide <span>Medical</span> Services That You Can <span>Trust!</span>",
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed nisl pellentesque, faucibus libero eu, gravida quam.",
      "left_button": "Get Appointment",
      "right_button": "Conatct Now",
      "background": "img/slider3.jpg"
    }
  ]
  return render(request, 'index.html', {'slides': slides})

def error_view(request):
  return render(request, '404.html')

def blog_view(request):
  return render(request, 'blog-single.html')

def contact_view(request):
  return render(request, 'contact.html')

def portfolio_view(request):
  return render(request, 'portfolio-details.html')