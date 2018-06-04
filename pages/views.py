
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from .forms import *
from .queries import *
from pages.entry_scripts.data_entry_script import *
from pages.entry_scripts.date_entry_script import *
from django.db.models import Max


#Index View -----------------------------------
def index(request):
    request.session['current_datasets'] = []
    request.session['current_titles'] = []
    return render(request, 'pages/index.html',)

def create_chartset_index(request):
    new_chart_set = ChartSet()
    new_chart_set.save()
    request.session['current_chartset'] = ChartSet.objects.latest('id').id
    return HttpResponseRedirect('/data-visualizer/dashboard')

#Chart Creation View -----------------------------------
def chartcreation(request):
    query = ''
    chart_form = ChartCreationForm()
    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/data-visualizer/dashboard/':
            chart = Chart(chart_set_id=ChartSet.objects.latest('id').id)
            chart.save()
            request.session['current_chart'] = Chart.objects.latest('id').id
    elif request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/data-visualizer/data-selection/':
        if request.method == "POST":
            dataset_form = DatasetForm(request.POST)
            if dataset_form.is_valid():
                querier = Query()
                graph = Graph(id=Graph.objects.latest('id').id + 1, chart_id=Chart.objects.latest('id').id, unit=dataset_form.cleaned_data['units'], 
                    facility=dataset_form.cleaned_data['facility'], area=dataset_form.cleaned_data['area'], start_date=dataset_form.cleaned_data['start_date'], 
                    end_date=dataset_form.cleaned_data['end_date'], gender=dataset_form.cleaned_data['gender'], year=dataset_form.cleaned_data['year'], 
                    month=dataset_form.cleaned_data['month'], week=dataset_form.cleaned_data['week'], day_of_month=dataset_form.cleaned_data['day_of_month'], 
                    day_of_week=dataset_form.cleaned_data['day_of_week'], time=dataset_form.cleaned_data['time'], )
                graph.save()
                query_dicts = Query().query_every_day(graph)
                for single_dictionary in query_dicts:
                    for data_object in query_dicts[single_dictionary]:
                        graph.data.add(data_object)
                graph.save()
                request.session['check'] = 'true'
                return HttpResponseRedirect('/data-visualizer/chart-creation')
            else:
                request.session['check'] = dataset_form.is_valid()
                dataset_form = DatasetForm()
    titles = request.session.get('current_titles')

    graph_list = []
    for x in Graph.objects.filter(chart_id=request.session.get('current_chart')):
        graph_list.append(x)
    titles_list = []
    for title in graph_list:
        titles_list.append(title.label) 
    value_list = []
    for graph in graph_list:
        graph_data = []
        for data in graph.data.all():
            graph_data.append(data.value)
        value_list.append(graph_data)
    query = Query().sort_results(Graph.objects.latest('id'))
    return render(request, 'pages/chart-creation.html', {'variable':query, 'chart_form':chart_form, 'graphs':graph_list, 'labels':titles_list, 'values':value_list, 'titles':'hello'})

def convert_queryset_to_list(queryset):
    return_list = []
    for x in queryset:
        return_list.append(x)
    return return_list

def date_creation_loop(start, end):
    flag = True
    while (flag):
        if (start == end):
            flag = False
        date = DateEntryScript(start)
        date.create_date()
        start += timedelta(days=1)

def create_label(form):
    dates =  str(form.cleaned_data['start_date'].month) + '/' + str(form.cleaned_data['start_date'].day) + '/' + str(form.cleaned_data['start_date'].year) + '-'
    dates =  dates + str(form.cleaned_data['end_date'].month) + '/' + str(form.cleaned_data['end_date'].day) + '/' + str(form.cleaned_data['end_date'].year)
    facility = str(form.cleaned_data['facility'])
    area = str(form.cleaned_data['area'])
    return dates + ', ' + facility + ', ' + area

def create_dates():
    start = datetime(2016, 1, 1)
    end = datetime(2020, 12, 31)
    date_creation_loop(start, end)

#Data Selection View -----------------------------------
def dataselection(request):

    dataset_form = DatasetForm()
    return render(request, 'pages/data-selection.html', {'dataset_form':dataset_form})


