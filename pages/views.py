
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
        chart = Chart(chart_set_id=request.session.get('current_chartset'))
        chart.save()
    elif request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/data-visualizer/data-selection/':
        if request.method == "POST":
            dataset_form = DatasetForm(request.POST)
            if dataset_form.is_valid():
                querier = Query()


                graph = Graph(chart_id=1)
                graph.save()
                query_dicts = querier.query_every_day(dataset_form)
                for single_dictionary in query_dicts:
                    for data_object in query_dicts[single_dictionary]:
                        Graph.objects.latest('id').label.add(data_object.key)
                # graph.label.add(Data.objects.get(key='01/01/2018-rec-str-0730-m'))
                # graph.label.add(querier.query_every_day(dataset_form))

                # request.session['current_titles'] = pulled_titles
                return HttpResponseRedirect('/data-visualizer/chart-creation')
        else:
            dataset_form = DatasetForm()
    titles = request.session.get('current_titles')
    key_list = ['yes']
    value_list = []
    query = request.session.get('current_datasets')
    return render(request, 'pages/chart-creation.html', {'variable':query, 'chart_form':chart_form, 'labels':key_list[0], 'values':value_list, 'titles':titles})

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
    start = datetime(2021, 1, 1)
    end = datetime(2024, 12, 31)
    date_creation_loop(start, end)

#Data Selection View -----------------------------------
def dataselection(request):

    dataset_form = DatasetForm()
    return render(request, 'pages/data-selection.html', {'dataset_form':dataset_form})


