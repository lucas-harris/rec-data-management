
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .queries import *
from pages.entry_scripts.data_entry_script import *
from pages.entry_scripts.date_entry_script import *
# from django.utils import simplejson


#Index View -----------------------------------
def index(request):
    request.session['current_datasets'] = []
    return render(request, 'pages/index.html',)


#Chart Creation View -----------------------------------
def chartcreation(request):
    query = ''
    chart_form = ChartCreationForm()
    if (request.method == "POST"):
        dataset_form = DatasetForm(request.POST)
        if dataset_form.is_valid():
            querier = Query()
            pulled_session = request.session.get('current_datasets')
            pulled_session.append(querier.sort_results(dataset_form))
            request.session['current_datasets'] = pulled_session

            return HttpResponseRedirect(request.path_info)
    else:
        dataset_form = DatasetForm()
    datasets = request.session.get('current_datasets')
    key_list = []
    value_list = []
    for x in datasets:
        key_list.append(list(x.keys()))
        value_list.append(list(x.values()))


    query = value_list
    return render(request, 'pages/chart-creation.html', {'variable':query, 'chart_form':chart_form, 'labels':key_list[0], 'values':value_list})

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


