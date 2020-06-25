from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from .models import Request
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from datetime import datetime
from .utils import render_to_pdf
# Create your views here.


class Home(View):
    def get(self, request, *args, **kwargs):
        qs = Request.objects.filter(accepted=True)
        context = {
            'project_funded': 0,
            'total_funding': 0
        }
        if qs.exists():
            context = {
                'project_funded': qs.count(),
                'total_funding': qs.aggregate(Sum('budget'))['budget__sum']
            }
        return render(request, 'request/index.html', context)

class UserRequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'request/dashboard.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'requests'

    def get_queryset(self):
        user = get_object_or_404(User, username = self.request.user.username)
        return Request.objects.filter(requester = user)

class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    template_name = 'request/apply.html'
    fields = ['title', 'abstract', 'hardware', 'software', 'budget']
    success_url = '/dashboard'
    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)

class DownloadPDF(View):
    def get(self, request, id=None, *args, **kwargs):
        qs = Request.objects.filter(id=id)
        if not qs.exists():
            raise Http404
        obj = qs.first()
        print(obj.title)
        context = {
            'current_year': datetime.now().year,
            'username': obj.requester.username,
            'first_name': obj.requester.first_name,
            'last_name': obj.requester.last_name,
            'email': obj.requester.email,
            'college': obj.requester.profile.college,
            'year': obj.requester.profile.year,
            'branch': obj.requester.profile.branch,
            'aadhar': obj.requester.profile.id_proof,
            'application_no': obj.id,
            'title': obj.title,
            'abstract': obj.abstract,
            'hardware': obj.hardware,
            'software': obj.software,
            'budget': obj.budget,
            'date': obj.date,
            'accepted': obj.accepted,
            'pending': obj.pending
        }
        pdf = render_to_pdf('request/pdf.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = '{}-{}.pdf'.format(request.user.username, obj.id)
        content = "attachment; filename={}".format(filename)
        response['Content-Disposition'] = content
        return response