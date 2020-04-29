from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

# Creating our own class for signing up, built upon built-in UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")
