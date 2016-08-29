from django.template.defaulttags import register
from openach.models import Evaluation, Eval
import logging
from django.urls import reverse


logger = logging.getLogger(__name__)


@register.simple_tag
def get_detail(dictionary, evidence_id, hypothesis_id):
    """Returns the evaluation Eval for a given hypothesis and piece of evidence"""
    return dictionary.get((evidence_id, hypothesis_id))


@register.filter
def detail_name(value):
    if value:
        return next(e[1] for e in Evaluation.EVALUATION_OPTIONS if e[0] == value.value)
    else:
        return 'No Assessments'


@register.filter
def detail_classname(value):
    mapping = {
        None: "eval-no-assessments",
        Eval.consistent: "eval-consistent",
        Eval.inconsistent: "eval-inconsistent",
        Eval.very_inconsistent: "eval-very-inconsistent",
        Eval.very_consistent: "eval-very-consistent",
        Eval.not_applicable: "eval-not-applicable",
        Eval.neutral: "eval-neutral"
    }
    return mapping.get(value)


@register.simple_tag
def get_source_tags(dictionary, source_id, tag_id):
    """Performs a dictionary lookup, returning None if the key is not in the dictionary"""
    return dictionary.get((source_id, tag_id))


@register.filter
def disagreement_category(value):
    if value is None:
        return 'No Assessments'
    elif value < 0.5:
        return 'Consensus'
    elif value < 1.5:
        return 'Mild Dispute'
    elif value < 2.0:
        return 'Large Dispute'
    else:
        return 'Extreme Dispute'


@register.filter
def disagreement_style(value):
    if value is None:
        return 'disagree-no-assessments'
    elif value < 0.5:
        return 'disagree-consensus'
    elif value < 1.5:
        return 'disagree-mild-dispute'
    elif value < 2.0:
        return 'disagree-large-dispute'
    else:
        return 'disagree-extreme-dispute'


@register.filter
def bootstrap_alert(tags):
    """
    If value is a Django message level, returns the corresponding bootstrap alert css class. Assumes a single tag
    for the message. See https://docs.djangoproject.com/en/1.10/ref/contrib/messages/#message-tags
    """
    mapping = {
        'debug': 'alert-info',
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-error',
    }
    return mapping[tags] if tags in mapping else tags


@register.filter
def board_url(board):
    """Return the URL for the board, including the slug if available."""
    if board.board_slug:
        return reverse('openach:detail_slug', args=(board.id, board.board_slug,))
    else:
        return reverse('openach:detail', args=(board.id,))
