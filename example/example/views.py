from django.views.generic import TemplateView


#########
# index #
#########

index_view = TemplateView.as_view(template_name="example/index.html")
