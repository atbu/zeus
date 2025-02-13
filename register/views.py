from django.shortcuts import redirect, render
from .forms import UserRegistrationForm

# Allows a user to register using the UserRegistrationForm.
def register(request):
  if(request.method == 'POST'): # if the form has been completed
    form = UserRegistrationForm(request.POST)
    if(form.is_valid()): # and it's valid
      new_user = form.save(commit=False) # save the details of the newly created user
      new_user.set_password(form.cleaned_data['password']) # set the new user's password to the cleaned one from the form
      new_user.save() # save this user to the database
      return render(request, 'register/register_done.html', {'new_user': new_user,}) # redirect them to tell them it's a success
  else:
    form = UserRegistrationForm() # if not already complete, send them to the form
  return render(request, 'register/register.html', {'form':form,})