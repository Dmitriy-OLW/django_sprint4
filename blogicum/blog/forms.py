from django import forms

from .models import Post, Comment, User, Location  


class PostForm(forms.ModelForm):
    new_location = forms.CharField(
        required=False,
        label="Или введите новое местоположение"
    )

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False  

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_location = self.cleaned_data.get('new_location')
        
        if new_location:
            location = Location.objects.create(name=new_location)
            instance.location = location
            
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
