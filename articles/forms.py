from django import forms

from .models import Article, Comment


class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content')

   
class UserCommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': 'Leave your comment here'
    }))
    class Meta:
        model = Comment
        fields = ('content',)
