from django.contrib.auth.models import User
from django import newforms as forms
from models import DEFAULT_MAX_COMMENT_LENGTH
from models import FreeThreadedComment, ThreadedComment
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

try:
    # If magicforms.py from http://fi.am/entry/preventing-spam/ is available,
    # use MagicModelForm as the base class for forms and get some spam
    # prevention for free.
    from magicforms import MagicModelForm
    ModelForm = MagicModelForm
except ImportError:
    class MagicModelForm: pass
    ModelForm = forms.ModelForm

class ThreadedCommentForm(ModelForm):
    """
    Form which can be used to validate data for a new ThreadedComment.
    It consists of just two fields: ``comment``, and ``markup``.
    
    The ``comment`` field is the only one which is required.
    """

    def __init__(self, remote_ip, unique_id, *args, **kwargs):
        if isinstance(self, MagicModelForm):
            args = (remote_ip, unique_id,) + args
        super(ThreadedCommentForm, self).__init__(*args, **kwargs)

    comment = forms.CharField(
        label = _('comment'),
        max_length = DEFAULT_MAX_COMMENT_LENGTH,
        widget = forms.Textarea
    )

    class Meta:
        model = ThreadedComment
        exclude = ('content_type', 'object_id', 'content_object', 'parent',
                   'user', 'date_submitted', 'date_modified', 'date_approved',
                   'is_public', 'is_approved', 'ip_address')

class FreeThreadedCommentForm(ModelForm):
    """
    Form which can be used to validate data for a new FreeThreadedComment.
    It consists of just a few fields: ``comment``, ``name``, ``website``,
    ``email``, and ``markup``.
    
    The fields ``comment``, and ``name`` are the only ones which are required.
    """

    def __init__(self, remote_ip, unique_id, *args, **kwargs):
        if isinstance(self, MagicModelForm):
            args = (remote_ip, unique_id,) + args
        super(FreeThreadedCommentForm, self).__init__(*args, **kwargs)

    comment = forms.CharField(
        label = _('comment'),
        max_length = DEFAULT_MAX_COMMENT_LENGTH,
        widget = forms.Textarea
    )

    class Meta:
        model = FreeThreadedComment
        exclude = ('content_type', 'object_id', 'content_object', 'parent',
                   'date_submitted', 'date_modified', 'date_approved',
                   'is_public', 'is_approved', 'ip_address')
