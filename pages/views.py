from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from .forms import *
from .queries import *
# from .sheet_parser import *
from pages.entry_scripts.data_entry_script import *
from pages.entry_scripts.date_entry_script import *
from django.db.models import Max

#Index View -----------------------------------
def index(request):
    # parse_sheet('Rec Patron Counts', datetime.datetime(2017, 8, 27))
    save_template_form = SaveTemplateForm()
    select_template_form = SelectTemplateForm()
    select_chart_form = SelectChartForm()
    if request.method == "POST":
        chart_form = ChartForm(request.POST)
        if 'create-chart' in request.POST:
            if chart_form.is_valid():
                chart = Chart.objects.get(id=request.session.get('current_chart'))
                chart.type=chart_form.cleaned_data['type']
                chart.saved = True
                chart.save()
                return HttpResponseRedirect('/data-visualizer/dashboard')
        elif 'edit-chart' in request.POST:
            if chart_form.is_valid():
                chart = Chart.objects.get(id=request.session.get('current_edit'))
                chart.type = chart_form.cleaned_data['type']
                chart.save()
                return HttpResponseRedirect('/data-visualizer/dashboard')
        else:
            chart_form = ChartForm()
    request.session['current_page'] = 'dashboard'
    if 'current_chartset' not in request.session:
        chartset = ChartSet()
        request.session['current_chartset'] = ChartSet.objects.latest('id').id
    charts = Chart.objects.filter(chart_set_id=request.session['current_chartset'])
    charts = charts & Chart.objects.filter(saved=True)
    chart_number = len(charts)
    chartset_dict = chartset_to_json(ChartSet.objects.get(id=request.session.get('current_chartset')))
    chartset_json = json.dumps(chartset_dict) 
    text = ChartSet.objects.get(id=request.session.get('current_chartset')).name
    # text = create_label(Chart.objects.get(id=44))
    name_taken_flag = request.session.get('name_taken_flag')
    request.session['name_taken_flag'] = 'false'
    return render(request, 'pages/index.html', {'json': chartset_json, 'chart_number':range(chart_number), 'save_template_form': save_template_form, 
    'text':text, 'name_taken_flag':name_taken_flag, 'select_template_form':select_template_form, 'select_chart_form':select_chart_form})

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


def changeselectedchartredirect(request):
    if request.method == "POST":
        select_chart_form = SelectChartForm(request.POST)
        if 'delete' in request.POST:
            if select_chart_form.is_valid():
                Chart.objects.get(id=select_chart_form.cleaned_data['selected_chart_id']).delete()
        elif 'edit' in request.POST:
            if select_chart_form.is_valid():
                request.session['current_edit'] = select_chart_form.cleaned_data['selected_chart_id']
                request.session['current_chart_action'] = 'edit'
                return HttpResponseRedirect('/data-visualizer/chart-creation')
        elif 'new' in request.POST:
            if select_chart_form.is_valid():
                request.session['current_page'] = 'chart-creation'
                chart = Chart(chart_set_id=ChartSet.objects.get(id=request.session.get('current_chartset')).id)
                chart.save()
                request.session['current_chart'] = Chart.objects.latest('id').id
                request.session['current_chart_action'] = 'new'
                return HttpResponseRedirect('/data-visualizer/chart-creation')
        return HttpResponseRedirect('/data-visualizer/dashboard')
    else:
        select_chart_form = SelectChartForm()
    return HttpResponseRedirect('/data-visualizer/dashboard')

#Chart Creation View -----------------------------------

def confirmchartredirect(request):
    if request.session.get('current_chart_action') == 'new':
        chart_id = request.session.get('current_chart')
    elif request.session.get('current_chart_action') == 'edit':
        chart_id = request.session.get('current_edit')
    if request.method == "POST":
        chart_form = ChartForm(request.POST)
        if chart_form.is_valid():
            chart = Chart.objects.get(id=chart_id)
            chart.saved = True
            chart.type = chart_form.cleaned_data['type']
            chart.save()
            return HttpResponseRedirect('/data-visualizer/dashboard') 
        else:
            chart_form = ChartForm()
    return HttpResponseRedirect('/data-visualizer/dashboard')

def chartcreation(request):
    chart_form = ChartForm()
    select_graph_form = SelectGraphForm()
    if request.method == "POST":
        dataset_form = DatasetForm(request.POST)
        if dataset_form.is_valid():
            if request.session.get('current_chart_action') == 'new':
                current_id = request.session.get('current_chart')
            elif request.session.get('current_chart_action') == 'edit':
                current_id = request.session.get('current_edit')
            if request.session.get('current_graph_action') == 'new':
                graph_id = -1
                if len(Graph.objects.all()) == 0:
                    graph_id = 0
                else:
                    graph_id = Graph.objects.latest('id').id 
                graph = Graph(id=graph_id + 1, chart_id=current_id, label=dataset_form.cleaned_data['label'], 
                    facility=dataset_form.cleaned_data['facility'], area=dataset_form.cleaned_data['area'], start_date=dataset_form.cleaned_data['start_date'], 
                    end_date=dataset_form.cleaned_data['end_date'], gender=dataset_form.cleaned_data['gender'], year=dataset_form.cleaned_data['year'], 
                    month=dataset_form.cleaned_data['month'], week=dataset_form.cleaned_data['week'], day_of_month=dataset_form.cleaned_data['day_of_month'], 
                    day_of_week=dataset_form.cleaned_data['day_of_week'], time=dataset_form.cleaned_data['time'],
                    color=dataset_form.cleaned_data['color'], unit=dataset_form.cleaned_data['units'] )
                graph.save()
                for graph_loop in Graph.objects.filter(chart_id=current_id):
                    graph_loop.unit = dataset_form.cleaned_data['units']
                    graph_loop.save()
                query_dicts = Query().query_every_day(graph)
                for single_dictionary in query_dicts:
                    for data_object in query_dicts[single_dictionary]:
                        graph.data.add(data_object)
                graph.save()
            elif request.session.get('current_graph_action') == 'edit':
                graph = Graph.objects.get(id=request.session.get('current_graph_edit'))
                graph.label=dataset_form.cleaned_data['label']
                graph.facility=dataset_form.cleaned_data['facility']
                graph.area=dataset_form.cleaned_data['area']
                graph.start_date=dataset_form.cleaned_data['start_date']
                graph.end_date=dataset_form.cleaned_data['end_date']
                graph.gender=dataset_form.cleaned_data['gender']
                graph.year=dataset_form.cleaned_data['year'] 
                graph.month=dataset_form.cleaned_data['month']
                graph.week=dataset_form.cleaned_data['week']
                graph.day_of_month=dataset_form.cleaned_data['day_of_month'] 
                graph.day_of_week=dataset_form.cleaned_data['day_of_week']
                graph.time=dataset_form.cleaned_data['time']
                graph.color=dataset_form.cleaned_data['color']
                graph.unit=dataset_form.cleaned_data['units'] 
                graph.save()
                for graph_loop in Graph.objects.filter(chart_id=current_id):
                    graph_loop.unit=dataset_form.cleaned_data['units'] 
                    graph_loop.save()
                query_dicts = Query().query_every_day(graph)
                for single_dictionary in query_dicts:
                    for data_object in query_dicts[single_dictionary]:
                        graph.data.add(data_object)
                graph.save()
            return HttpResponseRedirect('/data-visualizer/chart-creation')
        else:
            dataset_form = DatasetForm()
    if request.session.get('current_chart_action') == 'new':
        current_chart = request.session.get('current_chart')
        chart_type = Chart.objects.get(id=current_chart).type
        labels_and_colors = graph_to_json_no_data(Graph.objects.filter(chart_id=current_chart))
        graphs_json = json.dumps(labels_and_colors) 
        graph_count = range(len(Graph.objects.filter(chart_id=current_chart)))
    elif request.session.get('current_chart_action') == 'edit':
        current_chart = request.session.get('current_edit')
        chart_type = Chart.objects.get(id=current_chart).type
        labels_and_colors = graph_to_json_no_data(Graph.objects.filter(chart_id=current_chart))
        graphs_json = json.dumps(labels_and_colors) 
        graph_count = range(len(Graph.objects.filter(chart_id=current_chart)))
    return render(request, 'pages/chart-creation.html', {'graph_count':graph_count, 'chart_form':chart_form, 'chart_type':chart_type,
    'graphs':graphs_json, 'select_graph_form':select_graph_form, 'text':current_chart})

def deletechartredirect(request):
    return HttpResponseRedirect('/data-visualizer/dashboard')

#Data Selection View -----------------------------------
def dataselection(request):
    dataset_form = DatasetForm()
    if request.session.get('current_graph_action') == 'edit':
        request.session['current_page'] = 'data-selection'
        graph_dictionary = graph_to_json_all_fields(Graph.objects.get(id=request.session.get('current_graph_edit')))
        graph_json = json.dumps(graph_dictionary) 
        use_json = True
    elif request.session.get('current_graph_action') == 'new':
        graph_json = {}
        use_json = False
    return render(request, 'pages/data-selection.html', {'dataset_form':dataset_form, 'graph_json':graph_json, 'use_json':use_json})



def editdataset(request):
    dataset_form = DatasetForm()
    if request.session.get('current_graph_action') == 'edit':
        request.session['current_page'] = 'data-selection'
        graph_dictionary = graph_to_json_all_fields(Graph.objects.get(id=request.session.get('current_graph_edit')))
        graph_json = json.dumps(graph_dictionary) 
        use_json = True
    elif request.session.get('current_graph_action') == 'new':
        graph_json = {}
        use_json = False
    return render(request, 'pages/data-selection.html', {'dataset_form':dataset_form, 'graph_json':graph_json, 'use_json':use_json})

def selectdatasetredirect(request):
    if request.method == "POST":
        select_graph_form = SelectGraphForm(request.POST)
        if 'delete' in request.POST:
            if select_graph_form.is_valid():
                Graph.objects.get(id=select_graph_form.cleaned_data['selected_graph_id']).delete()
                return HttpResponseRedirect('/data-visualizer/chart-creation')
        elif 'edit' in request.POST:
            if select_graph_form.is_valid():
                request.session['current_graph_edit'] = select_graph_form.cleaned_data['selected_graph_id']
                request.session['current_graph_action'] = 'edit'
                return HttpResponseRedirect('/data-visualizer/data-selection')
        elif 'new' in request.POST:
            request.session['current_graph_action'] = 'new'
            return HttpResponseRedirect('/data-visualizer/data-selection')
        return HttpResponseRedirect('/data-visualizer/chart-creation')
    else:
        select_graph_form = SelectGraphForm()
    return HttpResponseRedirect('/data-visualizer/dashboard')    


#Report View --------------------------------------
def reportview(request):
    charts = Chart.objects.filter(chart_set_id=request.session['current_chartset'])
    charts = charts & Chart.objects.filter(saved=True)
    chart_number = len(charts)
    chartset_dict = chartset_to_json(ChartSet.objects.get(id=request.session.get('current_chartset')))
    chartset_json = json.dumps(chartset_dict) 
    text = ChartSet.objects.get(id=request.session.get('current_chartset')).name
    label_json = {}
    index = 0
    for chart in charts:
        label_json[index] = create_label(chart)
        index += 1
    label_json = json.dumps(label_json)
    return render(request, 'pages/report.html', {'json': chartset_json, 'chart_number':range(chart_number), 'label':label_json})

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
    querier = Query()
    common_label = dict()
    varying_label = dict()
    independent_label = dict()
    facility_dict = dict()
    area_dict = dict()
    gender_dict = dict()
    month_dict = dict()
    week_dict = dict()
    year_dict = dict()
    day_of_month_dict = dict()
    day_of_week_dict = dict()
    time_dict = dict()
    unit_dict = dict()
    start_date_dict = dict()
    end_date_dict = dict()
    for graph in queryset:
        facility_dict[graph.facility] = True
        area_dict[graph.area] = True
        gender_dict[graph.gender] = True
        month_dict[graph.month] = True
        week_dict[graph.week] = True
        year_dict[graph.year] = True
        day_of_month_dict[graph.day_of_month] = True
        day_of_week_dict[graph.day_of_week] = True
        time_dict[graph.time] = True
        start_date_dict[graph.start_date] = True
        end_date_dict[graph.end_date] = True
        unit_dict[graph.unit] = True

    if len(facility_dict) == 1:
        independent_label['facility'] = []
        facilitylabel = querier.replace_characters(graph.facility)
        common_label['facility'] = facilitylabel
        varying_label['facility'] = []
        for x in queryset:
            independent_label['facility'].append(facilitylabel)
    else:
        varying_label['facility'] = []
        independent_label['facility'] = []
        for graph in queryset:
            facilitylabel = querier.replace_characters(graph.facility)
            varying_label['facility'].append(facilitylabel)
            independent_label['facility'].append(facilitylabel)
        common_label['facility'] =  []

    if len(area_dict) == 1:
        independent_label['area'] = []
        arealabel = querier.replace_characters(graph.area)
        common_label['area'] = arealabel
        varying_label['area'] = []
        for x in queryset:
            independent_label['area'].append(arealabel)
    else:
        varying_label['area'] = []
        independent_label['area'] = []
        for graph in queryset:
            arealabel = querier.replace_characters(graph.area)
            varying_label['area'].append(arealabel)
            independent_label['area'].append(arealabel)
        common_label['area'] = []

    if len(start_date_dict) == 1 and len(end_date_dict)==1:
        independent_label['date'] = []
        datelabel = ''
        for key in start_date_dict:
            datelabel += '(' + str(key)[0:10] + ' - '
        for key in end_date_dict:
            datelabel += str(key)[0:10] + ')'
        common_label['date'] = [datelabel]
        varying_label['date'] = []
        for x in queryset:
            independent_label['date'].append([datelabel])
    else:
        varying_label['date'] = []
        independent_label['date'] = []
        for graph in queryset:
            datelabel = str(graph.start_date)[0:10] + ' - ' + str(graph.end_date)[0:10] + ')'
            varying_label['date'].append(datelabel)
            independent_label['date'].append(datelabel)
        common_label['date'] =  []

    if len(gender_dict) == 1:
        independent_label['gender'] = []
        genderlabel = querier.replace_characters(graph.gender)
        common_label['gender'] = genderlabel
        varying_label['gender'] = []
        for x in queryset:
            independent_label['gender'].append(genderlabel)
    else:
        varying_label['gender'] = []
        independent_label['gender'] = []
        for graph in queryset:
            genderlabel = querier.replace_characters(graph.gender)
            varying_label['gender'].append(genderlabel)
            independent_label['gender'].append(genderlabel)
        common_label['gender'] =  []

    if len(unit_dict) == 1:
        independent_label['unit'] = []
        unitlabel = querier.replace_characters(graph.unit)
        common_label['unit'] = unitlabel
        varying_label['unit'] = []
        for x in queryset:
            independent_label['unit'].append(unitlabel)
    else:
        varying_label['unit'] = []
        independent_label['unit'] = []
        for graph in queryset:
            unitlabel = querier.replace_characters(graph.unit)
            varying_label['unit'].append(unitlabel)
            independent_label['unit'].append(unitlabel)
        common_label['unit'] =  []
    
    if len(month_dict) == 1:
        independent_label['month'] = []
        monthlabel = querier.replace_characters(graph.month)
        common_label['month'] = monthlabel
        varying_label['month'] = []
        for x in queryset:
            independent_label['month'].append(monthlabel)
    else:
        varying_label['month'] = []
        independent_label['month'] = []
        for graph in queryset:
            monthlabel = querier.replace_characters(graph.month)
            varying_label['month'].append(monthlabel)
            independent_label['month'].append(monthlabel)
        common_label['month'] =  []

    if len(year_dict) == 1:
        independent_label['year'] = []
        yearlabel = querier.replace_characters(graph.year)
        common_label['year'] = yearlabel
        varying_label['year'] = []
        for x in queryset:
            independent_label['year'].append(yearlabel)
    else:
        varying_label['year'] = []
        independent_label['year'] = []
        for graph in queryset:
            yearlabel = querier.replace_characters(graph.year)
            varying_label['year'].append(yearlabel)
            independent_label['year'].append(yearlabel)
        common_label['year'] =  []

    if len(week_dict) == 1:
        independent_label['week'] = []
        weeklabel = querier.replace_characters(graph.week)
        common_label['week'] = weeklabel
        varying_label['week'] = []
        for x in queryset:
            independent_label['week'].append(weeklabel)
    else:
        varying_label['week'] = []
        independent_label['week'] = []
        for graph in queryset:
            weeklabel = querier.replace_characters(graph.week)
            varying_label['week'].append(weeklabel)
            independent_label['week'].append(weeklabel)
        common_label['week'] =  []

    if len(time_dict) == 1:
        independent_label['time'] = []
        timelabel = querier.replace_characters(graph.time)
        common_label['time'] = timelabel
        varying_label['time'] = []
        for x in queryset:
            independent_label['time'].append(timelabel)
    else:
        varying_label['time'] = []
        independent_label['time'] = []
        for graph in queryset:
            timelabel = querier.replace_characters(graph.time)
            varying_label['time'].append(timelabel)
            independent_label['time'].append(timelabel)
        common_label['time'] =  []

    if len(day_of_month_dict) == 1:
        independent_label['day_of_month'] = []
        day_of_monthlabel = querier.replace_characters(graph.day_of_month)
        common_label['day_of_month'] = day_of_monthlabel
        varying_label['day_of_month'] = []
        for x in queryset:
            independent_label['day_of_month'].append(day_of_monthlabel)
    else:
        varying_label['day_of_month'] = []
        independent_label['day_of_month'] = []
        for graph in queryset:
            day_of_monthlabel = querier.replace_characters(graph.day_of_month)
            varying_label['day_of_month'].append(day_of_monthlabel)
            independent_label['day_of_month'].append(day_of_monthlabel)
        common_label['day_of_month'] =  []

    if len(day_of_week_dict) == 1:
        independent_label['day_of_week'] = []
        day_of_weeklabel = querier.replace_characters(graph.day_of_week)
        common_label['day_of_week'] = day_of_weeklabel
        varying_label['day_of_week'] = []
        for x in queryset:
            independent_label['day_of_week'].append(day_of_weeklabel)
    else:
        varying_label['day_of_week'] = []
        independent_label['day_of_week'] = []
        for graph in queryset:
            day_of_weeklabel = querier.replace_characters(graph.day_of_week)
            varying_label['day_of_week'].append(day_of_weeklabel)
            independent_label['day_of_week'].append(day_of_weeklabel)
        common_label['day_of_week'] =  []

    json = dict()
    json['common_label'] = common_label
    json['varying_label'] = varying_label
    json['independent_label'] = independent_label
    json['count'] = len(queryset)
    return json

def chartset_to_json(chartset):
    query = Chart.objects.filter(chart_set_id=chartset.id)
    query = query & Chart.objects.filter(saved=True)
    chart_list = []
    index = 0
    for chart in query:
        chart_list.append(chart_to_json(chart, index))
        index+=1
    return {'chartset':chart_list, 'id':chartset.id, 'title':chartset.name}

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

def graph_to_json_all_fields(graph):
    return {'label':graph.label, 'facility':graph.facility, 'area':graph.area, 'start_date':str(graph.start_date)[0:10], 'end_date':str(graph.end_date)[0:10],
    'unit':graph.unit, 'gender':graph.gender, 'year':graph.year, 'month':graph.month, 'week':graph.week, 
    'day_of_month':graph.day_of_month, 'day_of_week':graph.day_of_week, 'time':graph.time, 'color':graph.color}