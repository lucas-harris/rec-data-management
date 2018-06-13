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
    save_template_form = SaveTemplateForm()
    select_template_form = SelectTemplateForm()
    if request.method == "POST":
        chart_form = ChartForm(request.POST)
        if chart_form.is_valid():
            chart = Chart.objects.get(id=request.session.get('current_chart'))
            chart.type=chart_form.cleaned_data['type']
            chart.save()
            return HttpResponseRedirect('/data-visualizer/dashboard')
        else:
            chart_form = ChartForm()
    request.session['current_page'] = 'dashboard'
    if 'current_chartset' not in request.session:
        chartset = ChartSet()
        request.session['current_chartset'] = ChartSet.objects.latest('id').id
    chart_number = len(Chart.objects.filter(chart_set_id=request.session['current_chartset']))
    chartset_dict = chartset_to_json(ChartSet.objects.get(id=request.session.get('current_chartset')))
    chartset_json = json.dumps(chartset_dict) 
    text = ChartSet.objects.get(id=request.session.get('current_chartset')).name
    # text = create_label(Chart.objects.get(id=44))
    name_taken_flag = request.session.get('name_taken_flag')
    request.session['name_taken_flag'] = 'false'
    return render(request, 'pages/index.html', {'json': chartset_json, 'chart_number':range(chart_number), 'save_template_form': save_template_form, 
    'text':text, 'name_taken_flag':name_taken_flag, 'select_template_form':select_template_form})

def createchartset(request):
    new_chart_set = ChartSet()
    new_chart_set.save()
    request.session['current_chartset'] = ChartSet.objects.latest('id').id
    request.session['current_page'] = 'create-chartset-redirect'
    return HttpResponseRedirect('/data-visualizer/dashboard')

def savechartset(request):
    request.session['name_taken_flag'] = 'false'
    if request.method == "POST":
        save_template_form = SaveTemplateForm(request.POST)
        if save_template_form.is_valid():
            if ChartSet.objects.filter(name=save_template_form.cleaned_data['name']).count()==0:
                chartset = ChartSet.objects.get(id=request.session.get('current_chartset'))
                chartset.name = save_template_form.cleaned_data['name']
                chartset.saved = True
                chartset.save()
                request.session['current_chartset'] = chartset.id
            else:
                request.session['name_taken_flag'] = 'true'
            return HttpResponseRedirect('/data-visualizer/dashboard')
        else:
            save_template_form = SaveTemplateForm()
    return HttpResponseRedirect('/data-visualizer/dashboard')

def changechartset(request):
    if request.method == "POST":
        select_template_form = SelectTemplateForm(request.POST)
        if 'change' in request.POST:
            if select_template_form.is_valid():
                request.session['current_chartset'] = select_template_form.cleaned_data['name'].id
        elif 'delete' in request.POST:
            if select_template_form.is_valid():
                select_template_form.cleaned_data['name'].delete()
                chartset = ChartSet()
                chartset.save()
                request.session['current_chartset'] = ChartSet.objects.latest('id').id
        return HttpResponseRedirect('/data-visualizer/dashboard')
    else:
        select_template_form = SelectTemplateForm()
    return HttpResponseRedirect('/data-visualizer/dashboard')

def deleteselectedchart(request):
    
    return HttpResponseRedirect('/data-visualizer/dashboard')

#Chart Creation View -----------------------------------
def chartcreation(request):
    query = ''
    chart_form = ChartForm()
    if request.session.get('current_page') == 'dashboard':
        request.session['current_page'] = 'chart-creation'
        chart = Chart(chart_set_id=ChartSet.objects.get(id=request.session.get('current_chartset')).id)
        chart.save()
        request.session['current_chart'] = Chart.objects.latest('id').id
    elif request.session.get('current_page') == 'data-selection':
        request.session['current_page'] = 'chart-creation'
        if request.method == "POST":
            dataset_form = DatasetForm(request.POST)
            if dataset_form.is_valid():
                graph_id = -1
                if len(Graph.objects.all()) == 0:
                    graph_id = 0
                else:
                    graph_id = Graph.objects.latest('id').id 
                graph = Graph(id=graph_id + 1, chart_id=request.session.get('current_chart'), unit=dataset_form.cleaned_data['units'], 
                    facility=dataset_form.cleaned_data['facility'], area=dataset_form.cleaned_data['area'], start_date=dataset_form.cleaned_data['start_date'], 
                    end_date=dataset_form.cleaned_data['end_date'], gender=dataset_form.cleaned_data['gender'], year=dataset_form.cleaned_data['year'], 
                    month=dataset_form.cleaned_data['month'], week=dataset_form.cleaned_data['week'], day_of_month=dataset_form.cleaned_data['day_of_month'], 
                    day_of_week=dataset_form.cleaned_data['day_of_week'], time=dataset_form.cleaned_data['time'],
                    color=dataset_form.cleaned_data['color'])
                graph.save()
                query_dicts = Query().query_every_day(graph)
                for single_dictionary in query_dicts:
                    for data_object in query_dicts[single_dictionary]:
                        graph.data.add(data_object)
                graph.save()
                return HttpResponseRedirect('/data-visualizer/chart-creation')
            else:
                dataset_form = DatasetForm()
    labels_and_colors = graph_to_json_no_data(Graph.objects.filter(chart_id=request.session.get('current_chart')))
    graphs_json = json.dumps(labels_and_colors) 
    graph_count = range(len(Graph.objects.filter(chart_id=request.session.get('current_chart'))))
    return render(request, 'pages/chart-creation.html', {'graph_count':graph_count, 'chart_form':chart_form, 
    'graphs':graphs_json})

def deletechart(request):
    Chart.objects.get(id=request.session.get('current_chart')).delete()
    return HttpResponseRedirect('/data-visualizer/dashboard')

#Data Selection View -----------------------------------
def dataselection(request):
    request.session['current_page'] = 'data-selection'
    dataset_form = DatasetForm()
    return render(request, 'pages/data-selection.html', {'dataset_form':dataset_form})


#Additional Methods -----------------------------------
def create_dates():
    start = datetime(2015, 1, 1)
    end = datetime(2015, 12, 31)
    date_creation_loop(start, end)

def date_creation_loop(start, end):
    flag = True
    while (flag):
        if (start == end):
            flag = False
        date = DateEntryScript(start)
        date.create_date()
        start += timedelta(days=1)

def create_label(chart):
    queryset = Graph.objects.filter(chart_id = chart.id)
    label = ''
    facility_dict = dict()
    area_dict = dict()
    gender_dict = dict()
    month_dict = dict()
    week_dict = dict()
    year_dict = dict()
    dom_dict = dict()
    dow_dict = dict()
    time_dict = dict()
    start_date_dict = dict()
    end_date_dict = dict()
    for graph in queryset:
        facility_dict[graph.facility] = True
        area_dict[graph.area] = True
        gender_dict[graph.gender] = True
        month_dict[graph.month] = True
        week_dict[graph.week] = True
        year_dict[graph.year] = True
        dom_dict[graph.day_of_month] = True
        dow_dict[graph.day_of_week] = True
        time_dict[graph.time] = True
        start_date_dict[graph.start_date] = True
        end_date_dict[graph.end_date] = True
    if len(facility_dict) == 1:
        for key in facility_dict:
            if key != "['all']":
                label += 'Facilities: ' + key + ', '
    if len(area_dict) == 1:
        for key in area_dict:
            if key != "['all']":
                label += 'Areas: ' + key + ', '
    if len(start_date_dict) == 1 and len(start_date_dict)==1:
        for key in start_date_dict:
            label += 'Dates: (' + str(key)[0:10] + ' - '
        for key in end_date_dict:
            label += str(key)[0:10] + '), '
    if len(gender_dict) == 1:
        for key in gender_dict:
            if key != "['all']":
                label += 'Gender: ' + key + ', '
    if len(month_dict) == 1:
        for key in month_dict:
            if key != "['all']":
                label += 'Months: ' + key + ', '
    if len(year_dict) == 1:
        for key in year_dict:
            if key != "['all']":
                label += 'Years: ' + key + ', '
    if len(week_dict) == 1:
        for key in week_dict:
            if key != "['all']":
                label += 'Weeks: ' + key + ', '
    if len(time_dict) == 1:
        for key in time_dict:
            if key != "['all']":
                label += 'Times: ' + key + ', '
    if len(dom_dict) == 1:
        for key in dom_dict:
            if key != "['all']":
                label += 'Days: ' + key + ', '
    if len(dow_dict) == 1:
        for key in dow_dict:
            if key != "['all']":
                label += 'Week Days: ' + key + ', '
    chart.title = label
    chart.save()
    return label

def chartset_to_json(chartset):
    query = Chart.objects.filter(chart_set_id=chartset.id)
    chart_list = []
    index = 0
    for chart in query:
        chart_list.append(chart_to_json(chart, index))
        index+=1
    return {'chartset':chart_list, 'id':chartset.id}

def chart_to_json(chart, passed_index):
    query = Graph.objects.filter(chart_id=chart.id)
    graph_list = []
    index = 0
    for graph in query:
        graph_list.append(graph_to_json(graph, index))
        index+=1
    return {'charts':graph_list, 'title':chart.title, 'type':chart.type, 'id':chart.id}

def graph_to_json(graph, passed_index):
    graph_values = Query().sort_results(graph)
    data_list = []
    index = 0
    for data in graph_values:
        data_list.append(data_to_json(data, graph_values[data]))
        index+=1
    return {'graph':data_list, 'color':graph.color, 'label':graph.label}

def data_to_json(key, value):
    return {'data':{key:value}}

def graph_to_json_no_data(graph_list):
    return_list = []
    for graph in graph_list:
        return_list.append({'label':graph.label, 'color':graph.color, 'id':graph.id})
    return return_list
