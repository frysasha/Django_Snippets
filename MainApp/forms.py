from django.forms import ModelForm, TextInput, Textarea, CharField, PasswordInput, ValidationError
from MainApp.models import Snippet, Comment
from django.contrib.auth.models import User


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code', 'private']
        widgets = {
            'name': TextInput({"class": "form-control form-control-lg", 'placeholder': 'Название сниппета'}),
            'code': Textarea({"class": "form-control form-control-lg", 'placeholder': 'Код сниппета'})
        }


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ['text']