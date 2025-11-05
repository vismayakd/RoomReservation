from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import RoomCategory,Room,SpecialRate,Reservation
from . forms import RoomCategoryForm,RoomForm,SpecialRateForm


from datetime import datetime, timedelta
from decimal import Decimal

def index(request):
    return render(request,'base.html')



# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_home')

    return render(request,'admin_login.html')

@login_required
def admin_home(request):

    return render(request,'admin_home.html')


@login_required
def roomcategory_list(request):
    categories = RoomCategory.objects.all()
    return render(request, "roomcategory_list.html", context={"categories": categories})


@login_required
def roomcategory_add(request):
    if request.method == "POST":
        form = RoomCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Room Category added successfully')
            return redirect("roomcategory_list")
    else:
        form = RoomCategoryForm()
    return render(request, "roomcategory_form.html", context={"form": form, "title": "Add Category"})

def roomcategory_edit(request, id):
    category = get_object_or_404(RoomCategory, pk=id)
    if request.method == "POST":
        form = RoomCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Room Category Updated successfully')
            return redirect("roomcategory_list")
    else:
        form = RoomCategoryForm(instance=category)
    return render(request, "roomcategory_form.html", {"form": form, "title": "Edit Category"})


def roomcategory_delete(request, id):
    category = get_object_or_404(RoomCategory, pk=id)
    category.delete()
    messages.success(request,'Room Category Deleted successfully')
    return redirect("roomcategory_list")



@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, "room_list.html", context={"rooms": rooms})

@login_required
def room_add(request):
    if request.method == "POST":
        form = RoomForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Room added successfully')
            return redirect("room_list")
    else:
        form = RoomForm()
    return render(request, "room_form.html", context={"form": form,"title": "Add Room"})


@login_required
def room_edit(request, id):
    room = get_object_or_404(Room, pk=id)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES,instance=room)
        if form.is_valid():
            form.save()
            messages.success(request,'Room Updated successfully')
            return redirect("room_list")
    else:
        form = RoomForm(instance=room)
    return render(request, "room_form.html", {"form": form, "title": "Edit Room"})

@login_required
def room_delete(request, id):
    room = get_object_or_404(Room, pk=id)
    room.delete()
    messages.success(request,'Room Deleted successfully')
    return redirect("room_list")

@login_required
def specialrate_list(request):
    rates = SpecialRate.objects.all()
    return render(request, "specialrate_list.html", {"rates": rates})

@login_required
def specialrate_add(request):
    if request.method == "POST":
        form = SpecialRateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Special Rate added successfully')
            return redirect("specialrate_list")
    else:
        form = SpecialRateForm()
    return render(request, "specialrate_form.html", {"form": form, "title": "Add Special Rate"})

@login_required
def specialrate_edit(request, id):
    rate = get_object_or_404(SpecialRate, pk=id)
    if request.method == "POST":
        form = SpecialRateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            messages.success(request,'Special Rate updated successfully')
            return redirect("specialrate_list")
    else:
        form = SpecialRateForm(instance=rate)
    return render(request, "specialrate_form.html", {"form": form, "title": "Edit Special Rate"})

@login_required
def specialrate_delete(request, id):
    rate = get_object_or_404(SpecialRate, pk=id)
    rate.delete()
    messages.success(request,'Special Rate deleted successfully')
    return redirect("specialrate_list")


@login_required
def view_reservations(request):
    reservations = Reservation.objects.all().order_by('start_date')
    return render(request,'view_reservations.html',{'reservations':reservations})


@login_required
def checkout_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    room = reservation.room
    if request.method == "POST":
        reservation.status = True
        reservation.save()
        room.is_available = True
        room.save()
        return redirect('view_reservations')
    return render(request, 'checkout_form.html', {'reservation': reservation})



@login_required
def admin_logout(request):
    logout(request)
    return redirect('index')


def check_availability(request):
    categories = RoomCategory.objects.all()
    available_rooms = []
    special_rate_info = None
    if request.method == "POST":
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        rooms = Room.objects.filter(category_id=category_id)
        overlap = Reservation.objects.filter(room__in=rooms,
            start_date__lt=end_date_obj, end_date__gte=start_date_obj, status=False
            ).values_list('room_id', flat=True)

        print("Check", start_date_obj, end_date_obj)
        available_rooms = rooms.exclude(id__in=overlap)
        print("Available rooms", available_rooms)
        special_rate_info = SpecialRate.objects.filter(
            room_category_id=category_id,
            end_date__gte=start_date_obj,
            start_date__lte=end_date_obj
        ).first()

        context = {
            'categories': categories,
            'rooms': available_rooms,
            'start_date': start_date,
            'end_date': end_date,
            'special_rate': special_rate_info,
        }
        return render(request, 'room_book.html', context)

    return render(request, 'room_book.html', {'categories': categories})

def reservation(request, id):
    room = get_object_or_404(Room, id=id)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    num_of_nights = (end_date_obj - start_date_obj).days
    base_price = room.category.base_price

    price_list = []
    total_price = Decimal('0.00')
    current_date = start_date_obj

    while current_date < end_date_obj:
        special_rate = SpecialRate.objects.filter(
            room_category=room.category,
            start_date__lte=current_date,
            end_date__gte=current_date
        ).first()

        if special_rate:
            day_price = base_price * special_rate.rate_multiplier
            price_list.append({
                'date': current_date,
                'price': day_price,
                'note': f"Special rate ({special_rate.rate_multiplier}x)"
            })
        else:
            day_price = base_price
            price_list.append({
                'date': current_date,
                'price': day_price,
                'note': "Normal rate"
            })

        total_price += day_price
        current_date += timedelta(days=1)

    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        reservation = Reservation.objects.create(
            room=room,
            start_date=start_date_obj,
            end_date=end_date_obj,
            customer_name=customer_name,
            total_price=total_price
        )
        room.is_available = False
        room.save()
        return redirect('reservation_success', reservation_id=reservation.id)
    context = {
        'room': room,
        'start_date': start_date,
        'end_date': end_date,
        'num_nights': num_of_nights,
        'price_list': price_list,
        'total_price': total_price,
    }
    return render(request, 'reservation.html', context)


def reservation_success(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'confirmation.html', {'reservation': reservation})

def gallery(request):
    rooms = Room.objects.all()
    return render(request,'gallery.html',context={'rooms':rooms})