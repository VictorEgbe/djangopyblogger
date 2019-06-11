from django import forms

from .models import Article


class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content')

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     title = str(title)
    #     if len(title.strip()) == 0:
    #         raise forms.ValidationError('Invalid title')
    #     return title

    # def clean_content(self):
    #     content = self.cleaned_data.get('content')
    #     content = str(content)
    #     if len(content.strip()) == 0:
    #         raise forms.ValidationError('Invalid content')
    #     return content
