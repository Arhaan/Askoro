from django.shortcuts import render, get_object_or_404
from .models import Question, Answer
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .forms import AnswerUpdateForm, AnswerCreationForm, QuestionCreationForm, QuestionUpdateForm
from django.contrib.auth.models import User

class IndexView(generic.ListView):
    model = Question
    template_name = "doubts/index.html"
    context_object_name = "latest_question_list"
    ordering = ['-date_asked']
    paginate_by = 10

class UserIndexView(generic.DetailView):
    model = User
    template_name = "doubts/user_index.html"

class QuestionDetailsView(generic.DetailView):
    model = Question
    template_name = "doubts/details.html"

class QuestionCreateView(LoginRequiredMixin ,generic.CreateView):
    model = Question
    form_class=QuestionCreationForm

    def form_valid(self, form):
        form.instance.asker = self.request.user
        return super().form_valid(form)

class QuestionEditView(LoginRequiredMixin, UserPassesTestMixin ,generic.UpdateView):
    model = Question
    form_class=QuestionUpdateForm
    def form_valid(self, form):
        form.instance.asker = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.asker

class AnswerCreateView(LoginRequiredMixin , UserPassesTestMixin,generic.CreateView):
    model = Answer
    form_class=AnswerCreationForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question.objects.get(id = self.kwargs['qid'])
        return super().form_valid(form)
    def test_func(self):
        question = Question.objects.get(id = self.kwargs['qid'])
        return not question.hasUserAnswered(self.request.user)

class AnswerEditView(LoginRequiredMixin, UserPassesTestMixin ,generic.UpdateView):
    model = Answer
    form_class = AnswerUpdateForm
    def get_initial(self):
        initial= super().get_initial()
        obj = self.get_object()
        initial['text'] = obj.text
        return initial
    def get_success_url(self):
        question = self.object.question
        return reverse('doubts:details', kwargs={'pk':question.id})
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question.objects.get(id = self.kwargs['qid'])
        return super().form_valid(form)

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin ,generic.DeleteView):

    model= Answer
    def get_success_url(self):
        question = self.object.question
        return reverse('doubts:details', kwargs={'pk':question.id})
    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

class QuestionUpvoteView(LoginRequiredMixin, UserPassesTestMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        question = get_object_or_404(Question, pk = self.kwargs['pk'])
        url = question.get_absolute_url()
        user = self.request.user
        ud = self.kwargs['ud']
        userwasdown = user in question.downvotes_total.all()
        userwasup = user in question.upvotes_total.all()
        if ud == 1:
            if userwasup:
                question.upvotes_total.remove(user)
                question.hardness_points-=1

            elif userwasdown:
                question.downvotes_total.remove(user)
                question.upvotes_total.add(user)
                question.hardness_points+=2
            else:
                question.upvotes_total.add(user)
                question.hardness_points+=1
        else:
            if userwasdown:
                question.downvotes_total.remove(user)
                question.hardness_points+=1

            elif userwasup:
                question.upvotes_total.remove(user)
                question.downvotes_total.add(user)
                question.hardness_points-=2
            else:
                question.hardness_points-=1
                question.downvotes_total.add(user)
        question.save()
        return url
    def test_func(self):
        question = get_object_or_404(Question, pk = self.kwargs['pk'])
        user = self.request.user
        return not user == question.asker

class AnswerUpvoteView(LoginRequiredMixin, UserPassesTestMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        answer = get_object_or_404(Answer, pk = self.kwargs['pk'])
        diff=0
        url = answer.get_absolute_url()
        user = self.request.user

        ud = self.kwargs['ud']
        userwasdown = user in answer.downvoters.all()
        userwasup = user in answer.upvoters.all()
        if ud == 1:
            if userwasup:
                answer.upvoters.remove(user)
                diff=-1
            elif userwasdown:
                answer.downvoters.remove(user)
                answer.upvoters.add(user)
                diff=+2
            else:
                answer.upvoters.add(user)
                diff=+1
        else:
            if userwasdown:
                answer.downvoters.remove(user)
                diff=+1

            elif userwasup:
                answer.upvoters.remove(user)
                answer.downvoters.add(user)
                diff=-2
            else:
                diff=-1
                answer.downvoters.add(user)
        answer.upvotes+=diff
        answer.author.profile.karma_points+=diff
        answer.author.save()
        answer.save()
        return url
    def test_func(self):
        answer = get_object_or_404(Answer, pk = self.kwargs['pk'])
        user = self.request.user
        return not user == answer.author
