from django.forms import widgets

class Select2(widgets.Select):
    template_name = "widgets/select2.html"
    

class DateWidget(widgets.DateInput):
    template_name = "widgets/date.html"

class CkeditorWidget(widgets.Textarea):
    template_name = "widgets/ckeditor.html"

class SelectWidget(widgets.SelectMultiple):
    template_name = "widgets/select.html"

class ImageWidget(widgets.ClearableFileInput):
    template_name = "widgets/imageinput.html"
    
class Start_End_date(widgets.DateInput):
    template_name = "widgets/start_end_date.html"