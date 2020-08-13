from django.test import TestCase
from .models import Question, Answer
from django.contrib.auth.models import User
# Create your tests here.


def createCustomUser():
    return User.objects.create(username='Test')


def createCustomQuestion(u):
    return Question.objects.create(asker=u)


def createCustomAnswer(u, q):
    return Answer.objects.create(author=u, text='Hey', question=q)


class QuestionModelTests(TestCase):

    def test_question_creation_updates_questions_asked(self):
        """
        Asker's questions_asked must be incremented by 1 on creating a question
        """
        user = createCustomUser()
        prevasked = user.profile.questions_asked
        createCustomQuestion(user)
        newasked = user.profile.questions_asked
        self.assertEqual(newasked, prevasked+1)

    def test_question_updating_doesnt_update_questions_asked(self):
        """
        Asker's questions_asked must not be incremented by 1 on updating a question
        """
        user = createCustomUser()
        prevasked = user.profile.questions_asked
        new_ques = createCustomQuestion(user)
        new_ques.question_number = 2
        new_ques.save()
        newasked = user.profile.questions_asked
        self.assertEqual(newasked, prevasked+1)


class AnswerModelTests(TestCase):

    def test_answer_creation_updates_questions_answered(self):
        """
        Answerers's questions_answered must be incremented by 1 on creating a question
        """
        user = createCustomUser()
        prevans = user.profile.questions_answered
        ques = createCustomQuestion(user)
        createCustomAnswer(user, ques)
        newans = user.profile.questions_answered
        self.assertEqual(newans, prevans+1)

    def test_answer_updating_doesnt_update_questions_answered(self):
        """
        Asker's questions_asked must not be incremented by 1 on updating a question
        """
        user = createCustomUser()
        prevans = user.profile.questions_answered
        ques = createCustomQuestion(user)
        new_ans = createCustomAnswer(user, ques)
        new_ans.text = 'No wait I changed this'
        new_ans.save()
        newans = user.profile.questions_answered
        self.assertEqual(newans, prevans+1)
