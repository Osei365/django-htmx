from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dashboard, DataFile, Charts, User
from .forms import DataForm, ChartForm, PivotForm, UpdateForm, SignupForm
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import get_delimiter, createchart
from django.contrib import messages
from io import StringIO
import pandas as pd


# Create your views here.
def home(request):
   
    return render(request, 'homepage.html') 

def create_dashboard(request):
    length = request.user.dashboard_set.filter(title__icontains ='Untitled').count()
    index = '' if length == 0 else str(length)
    instance = Dashboard.objects.create(
        user= request.user,
        title = 'Untitled{}'.format(index)
    )
    instance.save()
    return redirect('charts:dashboard', instance.id)

#detailed view
@login_required
def dashboard(request, pk):

    dashboard = Dashboard.objects.get(id=pk)
    if request.user == dashboard.user:
        datafiles = dashboard.datafile_set.all()
        charts = dashboard.charts_set.all()
        fig_lists =[]
        for chart in charts:
            fig_html = createchart(
                        chart.X,
                        chart.Y,
                        chart.data,
                        chart.chart_type
                    )
            fig_lists.append(fig_html)
        context = {
            'dashboard' : dashboard,
            'datafiles' : datafiles,
            'pk': pk,
            'fig_lists': fig_lists
        }
        return render(request, 'charts/dashboard.html', context)
    else:
        pass
  
def upload_view(request, pk):
    form = DataForm()

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            datafile = form.save(commit=False)
            datafile.user = request.user
            datafile.dashboard = request.user.dashboard_set.get(id=pk)
            datafile.workingfile = request.FILES['workingfile']
            datafile.save()
            return redirect('charts:dashboard', pk)  

    context = {
        'form' : form,
        'pk' : pk
    }
    return render(request, 'charts/upload_data.html', context)
  
def create_chart(request, pk, pk2):

    form = ChartForm()
    form.fields['data'].queryset = form.fields['data'].queryset.filter(dashboard_id=pk)
    if request.method == 'POST':
        form = ChartForm(request.POST)
        try: 
            if form.is_valid():
                instance = form.save(commit=False)
                instance.data = DataFile.objects.get(id=request.POST['data'])
                instance.dashboard = Dashboard.objects.get(id=pk)
                instance.X = request.POST['X']
                instance.Y = request.POST['Y']
                instance.chart_type = pk2

                fig_html = createchart(
                    instance.X,
                    instance.Y,
                    instance.data,
                    instance.chart_type
                )
                instance.save()
                return redirect('charts:new-chart', instance.id)
        except:
            messages.add_message(request, messages.ERROR, 'entered an incorrect field value')
            return redirect('charts:create-chart', pk, pk2)
        
    context = {  
        'form': form,
        'pk': pk,
        'pk2' : pk2,
    }
    return render(request, 'charts/chartform.html', context)

def new_chart(request, pk):
    instance = Charts.objects.get(id=pk)
    fig_html = createchart(
                    instance.X,
                    instance.Y,
                    instance.data,
                    instance.chart_type
                )
    context = {
        'fig_html': fig_html
    }
    return render(request, 'partials/new_chart.html', context)

def update_title(request, pk):
    dashboard = Dashboard.objects.get(id=pk)
    form = UpdateForm(instance=dashboard)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=dashboard)
        try:
            if form.is_valid():
                form.save()
                return redirect('charts:show-update', pk)
        except:
            messages.add_message(request, messages.ERROR, 'A dashboard exists with this title')
            return redirect('charts:update-title', pk)
    context = {
        'form': form,
        'dashboard': dashboard
    }
    return render(request, 'charts/update_title.html', context) 

def show_update(request, pk):
    dashboard = Dashboard.objects.get(id=pk)
    context = {
        'dashboard' : dashboard
    }
    return render(request, 'partials/show_update.html', context)  

def pivot_table(request, pk):
    dashboard = Dashboard.objects.get(id=pk)
    datafile = dashboard.datafile_set.first()
    path = datafile.workingfile.path


    df = pd.read_csv(
        path,
        delimiter= get_delimiter(path)
    )

    columns = df.columns
    db_columns = columns.copy()
    choices = list(zip(db_columns, columns))


    form = PivotForm()
    form.fields['groupby'].choices = choices
    form.fields['focus'].choices = choices  
    if request.method == 'POST':
        print(request.POST)
        if request.POST['agg'] == 'Min':
            pivot_data= df.groupby(request.POST['groupby'])[request.POST['focus']].min()
        elif request.POST['agg'] == 'Max':
            pivot_data= df.groupby(request.POST['groupby'])[request.POST['focus']].max()
        elif request.POST['agg'] == 'Avg':
            pivot_data = df.groupby(request.POST['groupby'])[request.POST['focus']].mean()
        elif request.POST['agg'] == 'Count':
            pivot_data = df.groupby(request.POST['groupby'])[request.POST['focus']].count()
        buffer = StringIO()
        pivot_csv = pivot_data.to_csv(buffer)
        pivot_file = ContentFile(buffer.getvalue().encode('utf-8'))

        instance = DataFile()
        instance.user = request.user
        instance.dashboard = dashboard
        instance.workingfile.save(
            name='{}.csv'.format(request.POST['table_title']),
            content = pivot_file,
            save = True
        )

        return redirect('charts:dashboard', dashboard.id)
        pass

    
    context = {
        'form': form,
        'pk' : pk
    }
    return render(request, 'charts/pivot_table.html', context)

def show_dataframe(request, pk):
    instance = DataFile.objects.get(id=pk)
    path = instance.workingfile.path
    df = pd.read_csv(
        path,
        delimiter= get_delimiter(path)
    )

    df_html = df.values.tolist()
    columns = df.columns
    context = {
        'df_html' : df_html,
        'columns' : columns,
        'pk': pk
        
        
    }

    return render(request, 'charts/dataframe.html', context)


def row_deleter(request, pk):
    instance = DataFile.objects.get(id=pk)
    path = instance.workingfile.path
    df = pd.read_csv(
        path,
        delimiter= get_delimiter(path)
    )
    if request.method == 'POST':
        rows = [int(i) for i in list(request.POST.keys())[:-1]]  
        df.drop(rows, axis=0, inplace=True)
        df.to_csv(path, index=False)
        return redirect('charts:dataframe', pk)
    


def remover(request):
    return HttpResponse('')

def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        print(request.POST)
        form = SignupForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        if form.is_valid():
            form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    context = {
        'form': form
    }

    return render(request, 'signup.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    dashboards = user.dashboard_set.all()
    context = {  
        'user' : user,
        'dashboards': dashboards
    }
    return render(request, 'profile.html', context)

def delete_view(request, pk):
    dashboard = Dashboard.objects.get(id=pk)
    user_id = dashboard.user.id
    if request.method == 'POST':
        dashboard.delete()
        return redirect('profile', user_id)
    context = {
        'dashboard': dashboard
    }
    return render(request, 'partials/delete.html', context)

#FUNCTIONED BASED AND CLASS BASED VIEWS