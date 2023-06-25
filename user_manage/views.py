from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .forms import UserRegistrationForm, UserEditForm
from django.contrib.auth.models import User, Group
from inbay_app.utills import set_dynamic_database


def create_user(request):
    
    if request.method == 'POST':
        role = request.POST.get('role')

        database_name = role+'_db'
        set_dynamic_database(database_name)
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save(using=database_name)
            
            print("user here", user)
             # Add the user to the corresponding group based on the role
            role = form.cleaned_data['role']
            print("role found", role)
            group,_ = Group.objects.using(database_name).get_or_create(name=role)
            print("group ", group)
            print("user", user)
            group.user_set.add(user)
            
            # Save the user to the database


            return redirect('user_search')
        else:
            print("get errors", form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'create_user.html', {'form': form})


def edit_user(request, user_id, role):
    database_name = f'{role}_db'
    set_dynamic_database(database_name)
    user = User.objects.using(database_name).get(pk=user_id)

    if request.method == 'POST':
        role = request.POST.get('role')
        
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.save(using=database_name)

            return redirect('user_search')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})


def user_delete_confirmation(request, user_id, role):
    database_name = f'{role}_db'
    set_dynamic_database(database_name)
    user = User.objects.using(database_name).get(pk=user_id)
    return render(request, 'delete_confirm.html', {'user': user, "role": user.groups.using(database_name).first().name})


def user_delete(request, user_id, role):
    database_name = f'{role}_db'
    print("role", database_name)
    set_dynamic_database(database_name)

    user = User.objects.using(database_name).get(pk=user_id)
    user.delete()
    return redirect('user_search')


class UserSearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get('username') 
        backend_users = User.objects.using('backend_db').all()
        frontend_users = User.objects.using('frontend_db').all()
        graphic_users = User.objects.using('graphic_db').all()

        if username:
            backend_users = backend_users.filter(username__icontains=username)
            frontend_users = frontend_users.filter(username__icontains=username)
            graphic_users = graphic_users.filter(username__icontains=username)

        final_users = []
        
        for user in backend_users:
            user_data = {
                'id' : user.id,
                'username': user.username,
                'email' : user.email,
                'role' : 'backend'
            }
            final_users.append(user_data)

        for user in frontend_users:
            user_data = {
                'id' : user.id,
                'username': user.username,
                'email' : user.email,
                'role' : 'frontend'
            }
            final_users.append(user_data)

        for user in graphic_users:
            user_data = {
                'id' : user.id,
                'username': user.username,
                'email' : user.email,
                'role' : "graphic"
            }
            final_users.append(user_data)
            
        context['users'] = final_users
        context['backend_users'] = backend_users.count()
        context['frontend_users'] = frontend_users.count()
        context['graphic_users'] = graphic_users.count()
        return context