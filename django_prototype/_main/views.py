from django.http import HttpResponse
from django.views.generic import View
from django.template import loader


class PetalHomeView(View):

    # def petalhome(request):
    #     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #     # context = {'latest_question_list': latest_question_list}
    #     context = dict(title='Home')
    #     return render(request, 'petal_main/index.html', context)
    #     # return HttpResponse('Hello')

    def get(self, request, *args, **kwargs):
        template = loader.get_template('petal_main/index.html')
        context = dict(title='Home')
        return HttpResponse(template.render(context, request))