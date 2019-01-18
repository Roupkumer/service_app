from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login
from .form import ClientSignUpForm, ServerSignUpForm
from .models import Client, Server, Category
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# def _login(request):
#     return redirect('http://127.0.0.1:8000/accounts/login/')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_client:
            user = Client.objects.get(name=request.user.name)
            return render(request, 'home.html', {'client': user})
        elif request.user.is_server:
            user = Server.objects.get(name=request.user.name)
            return render(request, 'home.html', {'server': user})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login/')


def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            client = form.save(commit=False)
            client.is_client = True
            client.save()

            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password1']

            # authenticate user then login
            user = authenticate(phone=phone, password=password)
            login(request, user)

            return redirect('home')
        else:
            return render(request,'signup.html', {'form': form})
    else:
        form = ClientSignUpForm()
        return render(request, 'signup.html', {'form': form})


def server_signup(request):
    if request.method == 'POST':
        form = ServerSignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            server = form.save(commit=False)
            server.is_server = True
            server.joined_date = timezone.now()
            server.save()

            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password1']

            print(phone)

            # authenticate user then login
            user = authenticate(phone=phone, password=password)
            login(request, user)

            return redirect('home')
        else:
            return render(request,'signup.html', {'form': form})
    else:
        form = ServerSignUpForm()
        return render(request, 'signup.html', {'form': form})


def all_category(request):


    return render(request, 'home.html',context)

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'c'


class AllServers(ListView):
    model = Server
    template_name = 'all_server.html'
    context_object_name = 'server'


def ClientProfile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    servers=client.clients.all()
    for s in servers:
        print(s.name)

    context={'c':client,'servers':servers}

    return render(request, 'client_profile.html', context)


def ServerProfile(request, server_id):
    server = get_object_or_404(Server, pk=server_id)

    avg_rate = server.avg_rate
    n_s = 0
    h_s = 0
    f_s = int(avg_rate)
    h_s = avg_rate - f_s;
    if h_s > 0:
        n_s = 5 - f_s - 1
        h_s = 1
    else:
        n_s = 5 - f_s
        h_s = 0
    print(f_s)
    print(h_s)
    print(n_s)

    clients_=server.clients.all()
    is_requested = False
    client=None
    if request.user.is_authenticated:
        if request.user.is_client:
            client = request.user
            print(client.name)

            for c in clients_:
                print(c.name)
                if client.id == c.id:
                    print("Client requested")
                    is_requested = True
                    break
                else:
                    print("Client Not Request")

    context = {'s': server, 'f_s': range(f_s), 'h_s': range(h_s), 'n_s': range(n_s),'cl':clients_,'is_requested':is_requested}
    return render(request, 'server_profile.html', context)


class ClientUpdate(UpdateView):
    model = Client
    fields = ['name', 'phone', 'gender', 'birth_date', 'address', 'image']
    template_name = 'update.html'
    success_url = reverse_lazy('accounts:client_profile')


class ServerUpdate(UpdateView):
    model = Server
    fields = ['name', 'phone', 'gender', 'birth_date', 'address', 'image', 'category', 'experience']
    template_name = 'update.html'
    success_url = reverse_lazy('home')


class AddExperience(UpdateView):
    model = Server
    fields = ['experience']
    template_name = 'add_experience.html'
    success_url = reverse_lazy('home')


def add_rating(request, server_id):
    s = get_object_or_404(Server, pk=server_id)
    if request.method == 'POST':
        form = request.POST.dict()
        data = form.get("ratings")
        d = int(data)
        r = int(s.total_rating)
        t = r + d
        s.ratings = d
        s.total_rating = str(t)
        s.number_of_rating += 1
        avg_rate = t / s.number_of_rating
        avg_rate = round(avg_rate, 2)
        s.avg_rate = avg_rate
        s.save()

        return redirect('accounts:server_profile', server_id)
    else:
        return render(request, 'home.html')


def add_request(request, server_id):
    s = get_object_or_404(Server, pk=server_id)
    if request.method == 'POST':
        form = request.POST.dict()

        c = form.get("client")

        print("Contact id=%d", c)
        client = get_object_or_404(Client, pk=c)
        s.clients.add(client)
        s.save()

        return redirect('accounts:server_profile', server_id)
    else:
        return render(request, 'home.html')
