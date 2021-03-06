from django import forms
from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.forms.widgets import *
from pages.models import *
import datetime

'''Used to select the variables that define the dataset queries'''
class DatasetForm(forms.Form):
    label = forms.CharField(max_length=40)
    facility = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple(), initial=('all', 'All'), 
                                         choices=(('all', 'All'), ('rec', 'Rec Center'), ('clawson', 'Clawson'), ('nq', 'North Quad')))
    area = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple(), initial=('all', 'All'), 
                                         choices=(('all','All'), ('fc','Fitness Center'), ('gf', 'Group Fitness')))
    start_date = forms.DateTimeField(label="Start Date", initial=datetime.datetime.now().strftime("%Y-%m-%d"))
    end_date = forms.DateTimeField(label='End Date', initial=datetime.datetime.now().strftime("%Y-%m-%d"))
    units = forms.ChoiceField(choices = (('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year'), ('all', 'One Group')), label='Increment Units')
    gender = forms.ChoiceField(choices=(('all', 'All'), ('m', 'Male'), ('f', 'Female')), label='Gender')
    color = forms.ChoiceField(choices=(('rgb(0, 0, 0, .6)', 'Black'), ('rgb(255, 0, 0, .6)', 'Red'), ('rgb(255, 127, 0, .6)', 'Orange'), ('rgb(255, 255, 0, .6)', 'Yellow'), 
                                        ('rgb(127, 255, 0, .6)', 'Light Green'), ('rgb(0, 255, 0, .6)', 'Green'), ('rgb(0, 255, 127, .6)', 'Blue Green'),
                                        ('rgb(0, 255, 255, .6)', 'Cyan'), ('rgb(0, 0, 255, .6)', 'Blue'), ('rgb(127, 0, 255, .6)', 'Violet'), 
                                        ('rgb(255, 0, 255, .6)', 'Magenta')))
    time = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('6:30', '6:30'), ('7:30', '7:30'), ('8:30', '8:30'), ('9:30', '9:30'),
                                            ('10:30', '10:30'), ('11:30', '11:30'), ('12:30', '12:30'), ('13:30', '13:30'), ('14:30', '14:30'),
                                            ('15:30', '15:30'), ('16:30', '16:30'), ('17:30', '17:30'), ('18:30', '18:30'), ('19:30', '19:30'),
                                            ('20:30', '20:30'), ('21:30', '21:30'), ('22:30', '22:30')))
    year = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'),
                                            ('2011', '2011'), ('2010', '2010'),('2009', '2009'), ('2008', '2008'),('2007', '2007'), ('2006', '2006')))
    month = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
                                            ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'),('11', 'November'), ('12', 'December')))
    week = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('1', 'Week 1'), ('2', 'Week 2'), ('3', 'Week 3'), ('4', 'Week 4'), ('5', 'Week 5'), ('6', 'Week 6'),
                                              ('7', 'Week 7'), ('8', 'Week 8'), ('9', 'Week 9'),('10', 'Week 10'), ('11', 'Week 11'),('12', 'Week 12'),
                                              ('13', 'Week 13'), ('14', 'Week 14'), ('15', 'Week 15'), ('16', 'Week 16'), ('17', 'Week 17'),
                                              ('18', 'Week 18'), ('19', 'Week 19'), ('20', 'Week 20'), ('21', 'Week 21'), ('22', 'Week 22'),
                                              ('23', 'Week 23'), ('24', 'Week 24'), ('25', 'Week 25'), ('26', 'Week 26'), ('27', 'Week 27'),
                                              ('28', 'Week 28'), ('29', 'Week 29'), ('30', 'Week 30'), ('31', 'Week 31'), ('32', 'Week 32'),
                                              ('33', 'Week 33'), ('34', 'Week 34'), ('35', 'Week 35'), ('36', 'Week 36'), ('37', 'Week 37'),
                                              ('38', 'Week 38'), ('39', 'Week 39'), ('40', 'Week 40'), ('41', 'Week 41'), ('42', 'Week 42'),
                                              ('43', 'Week 43'), ('44', 'Week 44'), ('45', 'Week 45'), ('46', 'Week 46'), ('47', 'Week 47'),
                                              ('48', 'Week 48'), ('49', 'Week 49'), ('50', 'Week 50'), ('51', 'Week 51'), ('52', 'Week 52'),
                                              ('53', 'Week 53')))
    day_of_month = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3'), ('4', 'Day 4'), ('5', 'Day 5'), ('6', 'Day 6'),
                                                     ('7', 'Day 7'), ('8', 'Day 8'), ('9', 'Day 9'), ('10', 'Day 10'), ('11', 'Day 11'), ('12', 'Day 12'),
                                                     ('13', 'Day 13'), ('14', 'Day 14'), ('15', 'Day 15'), ('16', 'Day 16'), ('17', 'Day 17'),
                                                     ('18', 'Day 18'), ('19', 'Day 19'), ('20', 'Day 20'), ('21', 'Day 21'), ('22', 'Day 22'),
                                                     ('23', 'Day 23'), ('24', 'Day 24'), ('25', 'Day 25'), ('26', 'Day 26'), ('27', 'Day 27'),
                                                     ('28', 'Day 28'), ('29', 'Day 29'), ('30', 'Day 30'), ('31', 'Day 31')))
    day_of_week = forms.MultipleChoiceField(initial=('all', 'All'), choices=(('all', 'All'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'),
                                                     ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('0', 'Sunday')))

'''Used to define a chart's type on the chart creation page'''
class ChartForm(forms.Form):
    type = forms.ChoiceField(initial=('line', 'Line Chart'), required=True, widget=forms.RadioSelect(), choices=(('line', 'Line Chart'), ('bar', 'Bar Chart'), ('pie', 'Pie Chart'),
                                                  ('scatter', 'Scatter Plot')))

'''Used to name a template on the home page'''
class SaveTemplateForm(forms.Form):
    name = forms.CharField()

'''Helper method that displays the names of saved templates to select from'''
class SelectTemplateChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.name)

'''Used to select a different template on the home page'''
class SelectTemplateForm(forms.Form):
    name = SelectTemplateChoiceField(queryset = ChartSet.objects.filter(saved=1), widget=forms.RadioSelect(), empty_label=None)

'''Used to select a chart on the home page'''
class SelectChartForm(forms.Form):
    selected_chart_id = forms.CharField()

'''Used to select a graph on the chart creation page'''
class SelectGraphForm(forms.Form):
    selected_graph_id = forms.CharField()

'''Used to update one week of the database on the update page'''
class UpdateWeekDBForm(forms.Form):
    date = forms.DateTimeField(label='Date', initial=datetime.datetime.now().strftime("%Y-%m-%d"))
    type_week = forms.ChoiceField(initial=('all', 'All'), required=True, widget=forms.RadioSelect(), choices=(('all', 'All'), ('Rec Patron Counts', 'Rec Center'), ('North Quad', 'North Quad'),
                                                  ('Clawson', 'Clawson')))

'''Used to update alll weeks of the database on the update page'''
class UpdateAllDBForm(forms.Form):
    type_all = forms.ChoiceField(initial=('all', 'All'), required=True, widget=forms.RadioSelect(), choices=(('all', 'All'), ('Rec Patron Counts', 'Rec Center'), ('North Quad', 'North Quad'),
                                                  ('Clawson', 'Clawson')))