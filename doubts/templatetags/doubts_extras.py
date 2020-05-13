from django import template
from doubts.models import Question
register =template.Library()

@register.filter(name='get_answer_set', is_safe=True)
def get_answer_set(q):
    return q.answer_set.order_by('-upvotes')


@register.filter(name='has_answered', is_safe=True)
def has_answered(u, q):
    return q.hasUserAnswered(u)

@register.filter(name='has_upvotedques', is_safe=True)
def has_upvotedques(u, q):
    return u in q.upvotes_total.all()

@register.filter(name='has_downvotedques', is_safe=True)
def has_downvotedques(u, q):
    return u in q.downvotes_total.all()

@register.filter(name='has_downvotedans', is_safe=True)
def has_downvotedans(u, a):
    return u in a.downvoters.all()

@register.filter(name='has_upvotedans', is_safe=True)
def has_upvotedans(u, a):
    return u in a.upvoters.all()

