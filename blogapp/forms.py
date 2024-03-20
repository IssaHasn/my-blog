from django import forms
from .models import Comment

# simple form to add comment on post by any user
class CommentForm(forms.ModelForm):
    
    class Meta:

        model = Comment
        fields = ['user_name', 'body']