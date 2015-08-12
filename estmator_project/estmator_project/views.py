from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from est_quote.forms import QuoteCreateForm, ClientListForm
from est_client.models import Client, Company
from est_client.forms import ClientCreateForm
from est_quote.models import Quote, Category, Product, ProductProperties


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class QuoteView(TemplateView):
    template_name = 'quote.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(QuoteView, self).get_context_data(**kwargs)
            context['quotes'] = Quote.objects.all()
            context['categories'] = Category.objects.all()
            context['products'] = Product.objects.all()
            context['prods_in_quote'] = ProductProperties.objects.all()
            context['quote_client'] = self.request.GET.get('client')
            context['quote_name'] = self.request.GET.get('name')
        except (KeyError, ValueError):
            return redirect('menu')

        return context


@login_required
def menu_view(request):
    if request.method == 'GET':
        client_form = ClientCreateForm()
        quote_form = QuoteCreateForm()
        client_list_form = ClientListForm()
        context = {
            'client_form': client_form.as_p,
            'quote_form': quote_form.as_p,
            'client_list_form': client_list_form.as_p
        }
        return render(
            request, 'menu.html', context
        )
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def quote_form_view(request):
    if request.method == 'GET':
        quote_form = QuoteCreateForm()
        return HttpResponse(quote_form.as_p())
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def quote_edit_form_view(request):
    if request.method == 'GET':
        # client = Client.objects.get(id=request.GET['pk'])
        quote = Quote.objects.get(client__id=request.GET['pk'])
        quote_form = QuoteCreateForm(instance=quote)  # Fix this form
        return HttpResponse(quote_form.as_p())
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def client_form_view(request):
    if request.method == 'GET':
        client_form = ClientCreateForm()
        return HttpResponse(client_form.as_p())
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def client_edit_form_view(request):
    if request.method == 'GET':
        client = Client.objects.get(id=request.GET['pk'])
        client_form = ClientCreateForm(instance=client)
        return HttpResponse(client_form.as_p())
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def client_list_form_view(request):
    if request.method == 'GET':
        client_list_form = ClientListForm()
        return HttpResponse(client_list_form.as_p())
    else:
        return HttpResponseNotAllowed(['GET'])
