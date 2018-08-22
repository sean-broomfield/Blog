from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    # Meta class connects the models and fields to the form.
    class Meta():
        model = Post
        # Editable fields from Post model.
        fields = ('author', 'title', 'text')

        # These widgets allow you to assign classes to these elements, allowing
        # them to be connected to CSS styling.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
