import re
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from threadedcomments.models import ThreadedComment, FreeThreadedComment
from django import template

# Regular expressions for getting rid of newlines and witespace
inbetween = re.compile('>[ \r\n]+<')
newlines = re.compile('\r|\n')

def get_contenttype_kwargs(content_object):
    """
    Gets the basic kwargs necessary for almost all of the following tags.
    """
    kwargs = {
        'content_type' : ContentType.objects.get_for_model(content_object).id,
        'object_id' : getattr(content_object, 'pk', getattr(content_object, 'id')),
    }
    return kwargs

def get_comment_url(content_object, parent=None):
    """
    Given an object and an optional parent, this tag gets the URL to POST to for the
    creation of new ``ThreadedComment`` objects.
    """
    kwargs = get_contenttype_kwargs(content_object)
    if parent:
        if not isinstance(parent, ThreadedComment):
            raise template.TemplateSyntaxError, "get_comment_url requires its parent object to be of type ThreadedComment"
        kwargs.update({'parent_id' : getattr(parent, 'pk', getattr(parent, 'id'))})
        return reverse('tc_comment_parent', kwargs=kwargs)
    else:
        return reverse('tc_comment', kwargs=kwargs)

def get_comment_url_ajax(content_object, parent=None, ajax_type='json'):
    """
    Given an object and an optional parent, this tag gets the URL to POST to for the
    creation of new ``ThreadedComment`` objects.  It returns the latest created object
    in the AJAX form of the user's choosing (json or xml).
    """
    kwargs = get_contenttype_kwargs(content_object)
    kwargs.update({'ajax' : ajax_type})
    if parent:
        if not isinstance(parent, ThreadedComment):
            raise template.TemplateSyntaxError, "get_comment_url_ajax requires its parent object to be of type ThreadedComment"
        kwargs.update({'parent_id' : getattr(parent, 'pk', getattr(parent, 'id'))})
        return reverse('tc_comment_parent_ajax', kwargs=kwargs)
    else:
        return reverse('tc_comment_ajax', kwargs=kwargs)

def get_comment_url_json(content_object, parent=None):
    """
    Wraps ``get_comment_url_ajax`` with ``ajax_type='json'``
    """
    try:
        return get_comment_url_ajax(content_object, parent, ajax_type="json")
    except template.TemplateSyntaxError:
        raise template.TemplateSyntaxError, "get_comment_url_json requires its parent object to be of type ThreadedComment"
    return ''

def get_comment_url_xml(content_object, parent=None):
    """
    Wraps ``get_comment_url_ajax`` with ``ajax_type='xml'``
    """
    try:
        return get_comment_url_ajax(content_object, parent, ajax_type="xml")
    except template.TemplateSyntaxError:
        raise template.TemplateSyntaxError, "get_comment_url_xml requires its parent object to be of type ThreadedComment"
    return ''

def get_free_comment_url(content_object, parent=None):
    """
    Given an object and an optional parent, this tag gets the URL to POST to for the
    creation of new ``FreeThreadedComment`` objects.
    """
    kwargs = get_contenttype_kwargs(content_object)
    if parent:
        if not isinstance(parent, FreeThreadedComment):
            raise template.TemplateSyntaxError, "get_free_comment_url requires its parent object to be of type FreeThreadedComment"
        kwargs.update({'parent_id' : getattr(parent, 'pk', getattr(parent, 'id'))})
        return reverse('tc_free_comment_parent', kwargs=kwargs)
    else:
        return reverse('tc_free_comment', kwargs=kwargs)

def get_free_comment_url_ajax(content_object, parent=None, ajax_type='json'):
    """
    Given an object and an optional parent, this tag gets the URL to POST to for the
    creation of new ``FreeThreadedComment`` objects.  It returns the latest created object
    in the AJAX form of the user's choosing (json or xml).
    """
    kwargs = get_contenttype_kwargs(content_object)
    kwargs.update({'ajax' : ajax_type})
    if parent:
        if not isinstance(parent, FreeThreadedComment):
            raise template.TemplateSyntaxError, "get_free_comment_url_ajax requires its parent object to be of type FreeThreadedComment"
        kwargs.update({'parent_id' : getattr(parent, 'pk', getattr(parent, 'id'))})
        return reverse('tc_free_comment_parent_ajax', kwargs=kwargs)
    else:
        return reverse('tc_free_comment_ajax', kwargs=kwargs)

def get_free_comment_url_json(content_object, parent=None):
    """
    Wraps ``get_free_comment_url_ajax`` with ``ajax_type='json'``
    """
    try:
        return get_free_comment_url_ajax(content_object, parent, ajax_type="json")
    except template.TemplateSyntaxError:
        raise template.TemplateSyntaxError, "get_free_comment_url_json requires its parent object to be of type FreeThreadedComment"
    return ''

def get_free_comment_url_xml(content_object, parent=None):
    """
    Wraps ``get_free_comment_url_ajax`` with ``ajax_type='xml'``
    """
    try:
        return get_free_comment_url_ajax(content_object, parent, ajax_type="xml")
    except template.TemplateSyntaxError:
        raise template.TemplateSyntaxError, "get_free_comment_url_xml requires its parent object to be of type FreeThreadedComment"
    return ''

def auto_transform_markup(comment):
    """
    Given a comment (``ThreadedComment`` or ``FreeThreadedComment``), this tag
    looks up the markup type of the comment and formats the output accordingly.
    
    It can also output the formatted content to a context variable, if a context name is
    specified.
    """
    try:
        from django.contrib.markup.templatetags import markup
        from django.utils.html import escape
        from threadedcomments.models import MARKDOWN, TEXTILE, REST, HTML, PLAINTEXT
        if comment.markup == MARKDOWN:
            return markup.markdown(comment.comment)
        elif comment.markup == TEXTILE:
            return markup.textile(comment.comment)
        elif comment.markup == REST:
            return markup.restructuredtext(comment.comment)
#        elif comment.markup == HTML:
#            return mark_safe(force_unicode(comment.comment))
        elif comment.markup == PLAINTEXT:
            return escape(comment.comment)
    except ImportError:
        # Not marking safe, in case tag fails and users input malicious code.
        return force_unicode(comment.comment)

def do_auto_transform_markup(parser, token):
    try:
        split = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag must be of format {%% %r COMMENT %%} or of format {%% %r COMMENT as CONTEXT_VARIABLE %%}" % (token.contents.split()[0], token.contents.split()[0], token.contents.split()[0])
    if len(split) == 2:
        return AutoTransformMarkupNode(split[1])
    elif len(split) == 4:
        return AutoTransformMarkupNode(split[1], context_name=split[3])
    else:
        raise template.TemplateSyntaxError, "Invalid number of arguments for tag %r" % split[0]

class AutoTransformMarkupNode(template.Node):
    def __init__(self, comment, context_name=None):
        self.comment = template.Variable(comment)
        self.context_name = context_name
    def render(self, context):
        comment = self.comment.resolve(context)
        if self.context_name:
            context[self.context_name] = auto_transform_markup(comment)
            return ''
        else:
            return auto_transform_markup(comment)

def do_get_threaded_comment_tree(parser, token):
    """
    Gets a tree (list of objects ordered by preorder tree traversal, and with an
    additional ``depth`` integer attribute annotated onto each ``ThreadedComment``.
    """
    try:
        split = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag must be of format {%% get_threaded_comment_tree for OBJECT as CONTEXT_VARIABLE %%}" % token.contents.split()[0]
    return CommentTreeNode(split[2], split[4])

def do_get_free_threaded_comment_tree(parser, token):
    """
    Gets a tree (list of objects ordered by traversing tree in preorder, and with an
    additional ``depth`` integer attribute annotated onto each ``FreeThreadedComment.``
    """
    try:
        split = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag must be of format {%% get_free_threaded_comment_tree for OBJECT as CONTEXT_VARIABLE %%}" % token.contents.split()[0]
    return FreeCommentTreeNode(split[2], split[4])

class CommentTreeNode(template.Node):
    def __init__(self, content_object, context_name):
        self.content_object = template.Variable(content_object)
        self.context_name = context_name
    def render(self, context):
        content_object = self.content_object.resolve(context)
        context[self.context_name] = ThreadedComment.public.get_tree(content_object)
        return ''

class FreeCommentTreeNode(template.Node):
    def __init__(self, content_object, context_name):
        self.content_object = template.Variable(content_object)
        self.context_name = context_name
    def render(self, context):
        content_object = self.content_object.resolve(context)
        context[self.context_name] = FreeThreadedComment.public.get_tree(content_object)
        return ''

def oneline(value):
    """
    Takes some HTML and gets rid of newlines and spaces between tags, rendering
    the result all on one line.
    """
    try:
        return mark_safe(newlines.sub('', inbetween.sub('><', value)))
    except:
        return value

register = template.Library()
register.simple_tag(get_comment_url)
register.simple_tag(get_comment_url_json)
register.simple_tag(get_comment_url_xml)
register.simple_tag(get_free_comment_url)
register.simple_tag(get_free_comment_url_json)
register.simple_tag(get_free_comment_url_xml)

register.filter('oneline', oneline)

register.tag('auto_transform_markup', do_auto_transform_markup)
register.tag('get_threaded_comment_tree', do_get_threaded_comment_tree)
register.tag('get_free_threaded_comment_tree', do_get_free_threaded_comment_tree)