from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.urls import reverse

# Create your views here.
app_name = "flights"
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found")
    
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request,flight_id):
    # đối với request Post, thêm 1 chuyến bay mới.
    if request.method == "POST":
        # truy cập vào bảng Flight
        try:
            flight = Flight.objects.get(pk=flight_id)
            passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))

        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        
        #Tìm passenger dựa trên id
        passenger.flights.add(flight)

        #Điều hướng người dùng đến trang chuyến bay
        return HttpResponseRedirect(reverse("flight", args = (flight.id,)))