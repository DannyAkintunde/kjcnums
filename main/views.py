from django.shortcuts import render,redirect
from . import forms
from . import models
from .utils import upload_image_to_imgur
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator


def index(request):
    return render(request,'main/index.html')

def signup(request):
    
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(f'/setup/{user.username}')

    else:
        form = forms.RegistrationForm()

    return render(request,'registration/sign_up.html',{'form':form})

@login_required(login_url='/login')
def nums(request):
    categories = models.Category.objects.all()
    context = {
        'userdata':models.Userdata.objects.all(),
        'college_students':models.Userdata.objects.filter(category=categories[0]),
        'tutorial_students':models.Userdata.objects.filter(category=categories[1]),
        'college':{student:False for student in models.Userdata.objects.filter(category=categories[0])},
        'tutorial':{student:False for student in models.Userdata.objects.filter(category=categories[1])}
    }
    def get_college_ristrictions(students):
        for student in students:
            if student.user != request.user:
                if student.ristrictions.type == 'all':
                    context['college'][student] = False
                elif student.ristrictions.type == 'except':
                    for user in student.ristrictions.users.all():
                        context['college'][student]=user==request.user
                elif student.ristrictions.type == 'only':
                    for user in student.ristrictions.users.all():
                        context['college'][student]=user!=request.user
            else:
                context['college'][student]=False
    def get_tutorial_ristrictions(students):
        for student in students:
            if student.user != request.user:
                if student.ristrictions.type == 'all':
                    context['tutorial'][student] = False
                elif student.ristrictions.type == 'except':
                    for user in student.ristrictions.users.all():
                        context['tutorial'][student]=user==request.user
                elif student.ristrictions.type == 'only':
                    for user in student.ristrictions.users.all():
                        context['tutorial'][student]=user!=request.user
            else:
                context['tutorial'][student]=False
    get_college_ristrictions(context['college_students'])
    get_tutorial_ristrictions(context['tutorial_students'])
    try :
        if request.GET['search'] != None :
            context['search'] = request.GET['search']
            context['college_students'] = context['college_students'].filter(
                Q(user__username__icontains=context['search'])|
                Q(user__first_name__icontains=context['search'])|
                Q(user__last_name__icontains=context['search'])|
                Q(user__email__icontains=context['search'])
                )       
            context['tutorial_students'] = context['tutorial_students'].filter(
                Q(user__username__icontains=context['search'])|
                Q(user__first_name__icontains=context['search'])|
                Q(user__last_name__icontains=context['search'])|
                Q(user__email__icontains=context['search'])
                )
            context['count'] = len(context['college_students'])+len(context['tutorial_students'])
            get_college_ristrictions(context['college_students'])
            get_tutorial_ristrictions(context['tutorial_students'])
            return render(request,'main/numssearch.html',context)
    except:
        print('an error occured')
    return render(request,'main/nums.html',context)

@login_required(login_url='/login')
def addnum(request):
    model = models.Nums()
    form = forms.NumForm()
    if request.method == 'POST':
        form = forms.NumForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.POST['username'])
            model.num = form.data['num']
            model.user = user
            model.save()
            models.Userdata.objects.get(user=user).nums.add(model)
            return redirect('/')

    return render(request,'main/addnum.html',{'form':form})

@login_required(login_url='/login')
def profile(request,username):
    user = User.objects.get(username=username)
    context = {
        'User': user,
        'userdata':models.Userdata.objects.get(user=user),
        'ristricted':False
    }
    if user != request.user:
        if context['userdata'].ristrictions.type == 'all':
            context['ristricted'] = False
        elif context['userdata'].ristrictions.type == 'except':
            for user in context['userdata'].ristrictions.users.all():
                context['ristricted'] = user==request.user
        elif context['userdata'].ristrictions.type == 'only':
            for user in context['userdata'].ristrictions.users.all():
                context['ristricted'] = user!=request.user
    else:
        context['ristricted'] = False
    return render(request,'main/profile.html',context)
@login_required(login_url='/login')
def setup(request,username):
    user = User.objects.get(username=username)
    context = {
        'User': user,
    }
    if request.method == 'POST':
        if request.POST.get('error') != 'no-num':
            if request.FILES.get('image'):
                image = upload_image_to_imgur(request.FILES.get('image'))
            else: image = '/static/images/no-image-found-360x260.png'
            student_type = request.POST.get('studenttype')
            gender = request.POST.get('gender')
            ristrictions=models.Ristriction(type='all')
            ristrictions.save()
            userdata = models.Userdata(image=image,user=user,gender=gender,category=models.Category.objects.get(name=student_type),ristrictions=ristrictions)
            userdata.save()
            context['userdata'] = userdata
            return render(request,'main/signadd.html',context)
        else:
            userdata = models.Userdata.objects.get(user=models.User.objects.get(username=username))
            context['userdata'] = userdata
            context['message'] = 'Add at least one number to continue'
            return render(request,'main/signadd.html',context)
    try:
        if models.Userdata.objects.get(user=user) :
            context['userdata'] = models.Userdata.objects.get(user=user)
            return render(request,'main/signadd.html',context)
    except:

        return render(request,'main/profilesetup.html',context)

@login_required(login_url='/login')
def edit_deatails(request,mode,username,property):
    user = User.objects.get(username=username)
    page = {
        'title':'',
        'message':'',
        'message2':'',
        'message3':'',
        'hint':''
    }
    if property == 'social':
        form = forms.SociallinkForm()
        page['title'] = 'Add Social link'
        page['message'] = 'Don\'t have a Whatsapp link create one <a href=\'/\' class=\'link\'>here</a>'
        page['hint'] = 'Input your details'
        print(page)
        if request.method == 'POST':
            form = forms.SociallinkForm(request.POST)
            if 'http://' in form.data['link'] or 'https://' in form.data['link']:  
                if form.is_valid():
                    model = models.Sociallink(user=user,link=form.data['link'],platform=models.Platform.objects.get(id=form.data['platform']))
                    model.save()
                    models.Userdata.objects.get(user=user).sociallinks.add(model)
                    if mode != 'edit':
                        return redirect(f'/{mode}/{user.username}')
                    else:
                        return redirect('main:edit_contact_info')
            else:
                page['message2']='links must start wit http:// or https://'
    elif property == 'link':
        form = forms.OtherlinkForm()
        page['title'] = 'Add Other link'
        page['hint'] ='Input your details'
        
        if request.method == 'POST':
            form = forms.OtherlinkForm(request.POST)
            if 'http://' in form.data['link'] or 'https://' in form.data['link']:   
                if form.is_valid():
                    model = models.Otherlink(user=user,link=form.data['link'],display_text=form.data['display_text'])
                    model.save()
                    models.Userdata.objects.get(user=user).otherlinks.add(model)
                    if mode != 'edit':
                        return redirect(f'/{mode}/{user.username}')
                    else:
                        return redirect('main:edit_contact_info')
            else:
                page['message2']='links must start wit http:// or https://'   
    elif property == 'num':
        form = forms.NumForm()
        page['title'] = 'Add Number'
        page['hint'] ='Input your details'
        if request.method == 'POST':
            form = forms.NumForm(request.POST)   
            if form.is_valid():
                model = models.Nums(user=user,num=form.data['num'])
                model.save()
                models.Userdata.objects.get(user=user).nums.add(model)
                if mode != 'edit':
                    return redirect(f'/{mode}/{user.username}')
                else:
                    return redirect('main:edit_contact_info')  
    elif property == 'nin':
        form = forms.NinForm()
        page['title'] = 'Add NIN'
        page['hint'] ='hold up last thing'
        page['message3'] = 'Input your NIN for easy account recovery'
        if request.method == 'POST':
            form = forms.NinForm(request.POST)   
            if form.is_valid():
                model = models.Nin(user=user,nin=form.data['nin'])
                model.save()
                userdata = models.Userdata.objects.get(user=user)
                userdata.nin = model
                userdata.save()
                return redirect('/') 
    return render(request,'main/edit.html',{'form':form,'page':page})
@login_required(login_url='/login')
def del_deatails(request,property,id):
    context = {
        'message':'Are you sure you want to delete'
    }
    if property == 'num':
        try:
            num = models.Nums.objects.get(id=id)
            context['message'] = f'Are you sure you want to remove {num.num} from your phone numbers'
            if request.method == 'POST':
                num.delete()
                return redirect('main:edit_contact_info')
        except:
            return redirect('main:edit_contact_info')
    if property == 'link':
        try:
            link = models.Otherlink.objects.get(id=id)
            context['message'] = f"Are you sure you want to remove <a href='{link.link}' class='link'>{link.link}</a>:{link.display_text} from your Other links(external links)"
            if request.method == 'POST':
                link.delete()
                return redirect('main:edit_contact_info')
        except:
            return redirect('main:edit_contact_info')
    if property == 'social':
        try:
            link = models.Sociallink.objects.get(id=id)
            context['message'] = f"Are you sure you want to remove <i clas='bi bi-{link.platform.platform}'></i><a href='{link.link}' class='link'>{link.link}</a>:{link.text} from your Social links(external links)"
            if request.method == 'POST':
                link.delete()
                return redirect('main:edit_contact_info')
        except:
            return redirect('main:edit_contact_info')
    return render(request,'main/edit/del.html',context)
@login_required(login_url='/login')
def edit_basic_info(request):
    user_data = models.Userdata.objects.get(user=request.user)
    if request.method == 'POST':
        form = forms.BasicInfoForm(request.POST,request.FILES, instance=user_data)
        if form.is_valid():
            image = upload_image_to_imgur(request.FILES['image'])
            print(image)
            gender = form.cleaned_data['gender']
            category = form.cleaned_data['category']
            user_data.image,user_data.gender,user_data.category = image,gender,category
            user_data.save()
            return redirect('main:profile',request.user)  # Redirect to profile page after saving
    else:
        form = forms.BasicInfoForm(instance=user_data)
    return render(request, 'main/edit/edit_basic_info.html', {'form': form})

@login_required(login_url='/login')
def edit_contact_info(request):
    context = {
        'userdata' : models.Userdata.objects.get(user = request.user)
    }
    if request.method == 'POST':
        return redirect('main:profile',request.user.username)
    return render(request, 'main/edit/edit_contact_info.html',context)
@login_required(login_url='/login')
def edit_identity_info(request):
    user = request.user
    nin = models.Nin.objects.get(user=user)
    if request.method == 'POST':
        form = forms.NinForm(request.POST,instance=nin)
        if form.is_valid():
            nin.nin = form.data['nin']
            nin.save()
            return redirect('main:profile',request.user) 
    else:
        form = forms.NinForm(instance=nin)
    return render(request, 'main/edit/edit_identity_info.html', {'form': form})
@login_required(login_url='/login')
def edit_user_info(request):
    user = request.user
    if request.method == 'POST':
        form = forms.EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('main:profile',request.user) 
    else:
        form = forms.EditUserForm(instance=user)
    return render(request, 'main/edit/edit_user_info.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

@login_required(login_url='/login')
def edit_privacy(request):
    model = models.Userdata.objects.get(user=request.user).ristrictions
    context= {
        'form':forms.PrivacyForm(instance=model),
        'users':User.objects.all()
    }
    
    if request.method == 'POST':
        context['form'] = forms.PrivacyForm(request.POST,instance=model)
        if context['form'].is_valid():
            context['form'].save()
            return redirect('main:profile',request.user)
    
    return render(request,'main/edit/edit_privacy.html',context)



class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'  # Optional: specify custom template

@method_decorator(login_required, name='dispatch')
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'  # Optional: specify custom template


def account_recover(request):
    message = ''
    form = forms.RecoveryForm()
    if request.method == 'POST':
        form = forms.RecoveryForm(request.POST)
        if form.is_valid():
            nin = form.cleaned_data['nin']
            #get user
            try:
                user = models.Nin.objects.get(nin=nin).user
                login(request,user)
                return redirect('main:edit_user_info')
            except models.Nin.DoesNotExist:
                message = 'No user found with this NIN'

    return render(request,'main/recover_nin.html',{'message':message,'form':form})
