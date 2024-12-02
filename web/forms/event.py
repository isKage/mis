from django import forms
from web import models
from web.forms.bootstrap import BootStrapForm


class ArticleForm(forms.ModelForm, BootStrapForm):
    class Meta:
        model = models.Article
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = forms.Textarea(attrs={
            "class": "form-control",
            "rows": 10,
            "placeholder": "请输入文章内容（支持 Markdown 格式）"
        })
        self.fields["title"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "请输入文章标题"
        })
