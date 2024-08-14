from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from contactus_aboutus.forms import ContactUsForm
from site_setting.models import SiteSettings,q_and_answer


class about_us_view(TemplateView):
    template_name = 'about_us/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(about_us_view, self).get_context_data(**kwargs)
        site_setting: SiteSettings = SiteSettings.objects.filter(is_active=True).first()
        context['site_settings'] = site_setting
        return context


class ContactUsView(CreateView):
    form_class = ContactUsForm
    template_name = 'contact_us/contact_us.html'
    success_url = '/contact-us'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting:SiteSettings=SiteSettings.objects.filter(is_active=True).first()
        context['site_settings']=setting
        return context

def q_and_answer_view(request):
    q_and_answers = q_and_answer.objects.all()
    return render(request,'q_and_answer/q_and_answer_component.html',{'q_and_answers':q_and_answers})