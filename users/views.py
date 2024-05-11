from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from .models import UserProfile


from django.contrib.auth.decorators import login_required
from .models import History

from.help import send_fgt_pssw_mail
import uuid

from .models import Profile




# Create your views here.
    

def first(request):
    return render(request,'users/first.html')




def register(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password2')
        
        if User.objects.filter(username = uname).first():
                messages.success(request, 'Username is taken.')
                return redirect('register')
                
        if User.objects.filter(email = email).first():
                messages.success(request, 'Email existe déja.')
                return redirect('register')

        if pass1!=pass2:
            # return HttpResponse("password not Same!!")
            messages.error(request, "Password not the same!")
            return redirect('register')

        else:
            user_obj = User(username = uname , email = email)
            user_obj.set_password(pass1)
            user_obj.save()
            
            
            # my_user=Profile.objects.create(uname,email,pass1)
            my_user=Profile.objects.create(user = user_obj)
            
            my_user.save()
            return redirect('login')
    return render(request,'users/register.html')




            

    
def user_login(request):

    error_message = None
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        
        if not uname or not pass1:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('login')
        user_obj = User.objects.filter(username = uname).first()
        if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('login')
                

        user = authenticate(request, username=uname, password=pass1)
        
        if user is None:
                messages.success(request, 'Wrong password.')
                return redirect('login')
        
        if user is not None:
            login(request, user)
            return redirect('cal_calc')
        else:

            error_message='Wrong password.'

    return render(request, 'users/login.html' , {'error_message': error_message})









def forget(request):
    try:
        if request.method == 'POST':
            uemail = request.POST.get('email')
            
            if not User.objects.filter(email=uemail).first():
                messages.success(request, "Email n'existe pas.")
                return redirect('forget')
                
            user_obj = User.objects.get(email=uemail)
            token = str(uuid.uuid4())
            
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            
            send_fgt_pssw_mail(user_obj.email,token)
            messages.success(request, "Email sent.")
            return redirect('forget')
    except Exception as e:
        print(e)
        
        
        
    return render(request ,'users/forget.html')







def change_passw(request , token):
    contxt = {}
    
    profile_obj = Profile.objects.filter(forget_password_token = token).first()
    
    # print(profile_obj)
    
    contxt = {'user_id' : profile_obj.user.id}
    
    if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('password2')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'change_password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'Password not the same!.')
                return redirect(f'change_password/{token}/')
                
                
                
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect ('login')
        
    
    
    return render(request,'users/change_passw.html',contxt)










def user_logout(request):
    logout(request)
    messages.success(request,("You were logged out"))
    return redirect("first")




@login_required
def cal_calc(request):
    
    if request.method=='POST':
       age= int(request.POST.get('age'))
       gender = request.POST.get('gender')
       weight = float(request.POST.get('weight'))
       height = float(request.POST.get('height'))
       activity = request.POST.get('activity')
       if not activity:
            error_message = "select an activity."
            return render(request, 'users/cal_calc.html', {'error_message': error_message})



        

       profile = UserProfile.objects.create(
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            activity=activity,
        )
       
        #Pour homme BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
        #For females: BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
       
       calories_weight_loss = 0
       
       if activity == 'sedentary':
             if gender == 'male':
                calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) + 5
                calories_weight_loss = calories_maintenance - 500
                calories_weight_gain =calories_maintenance + 500
                

             else:
                calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) - 161
                calories_weight_loss = calories_maintenance - 500
                calories_weight_gain =calories_maintenance + 500
                
       
       elif activity == 'light':
            if gender == 'male':
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) + 5
            #    BMR = [66.47 + (13.75 * weight ) + (5.003 * height ) - (6.755 * age )]
               
               calories_maintenance *= 1.375
               calories_weight_loss = calories_maintenance - 500
               calories_weight_gain =calories_maintenance + 500
               
            else:
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) - 161
               calories_maintenance *= 1.375
               calories_weight_loss = calories_maintenance - 500
               calories_weight_gain =calories_maintenance + 500
               


       elif activity == 'moderate':
            if gender == 'male':
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) + 5
               calories_maintenance *= 1.55
               calories_weight_loss = calories_maintenance - 500
               calories_weight_gain =calories_maintenance + 500
               
               
            else:
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) - 161
               calories_maintenance *= 1.55
               calories_weight_loss = calories_maintenance - 500   
               calories_weight_gain =calories_maintenance + 500
               
       elif activity == 'active':
            if gender == 'male':
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) + 5
               calories_maintenance *= 1.725
               calories_weight_loss = calories_maintenance - 500  
               calories_weight_gain =calories_maintenance + 500
               
               
            else:
               calories_maintenance = (10 * weight) + (6.25 * height) - (5 * age) - 161
               calories_maintenance *= 1.725
               calories_weight_loss = calories_maintenance - 500
               calories_weight_gain =calories_maintenance + 500
    
    
       
       History.objects.create(
            user=request.user,
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            activity=activity,
            calories_maintenance=calories_maintenance,
            calories_weight_loss=calories_weight_loss,
            calories_weight_gain=calories_weight_gain,
        )
        
        

       return render(request, 'users/cal_calc.html', {
            'profile': profile,
            'calories_maintenance': int(calories_maintenance),
            'calories_weight_loss': int(calories_weight_loss),
            'calories_weight_gain': int(calories_weight_gain),
            
            })
    

    return render(request,'users/cal_calc.html',{
        'calories_maintenance': None,
        'calories_weight_loss': None,
        'calories_weight_gain': None,})
        




# 

#@login_required
def Hprofile(request):
    if request.user.is_authenticated:
        search_history = History.objects.filter(user=request.user).order_by('-timestamp')
        
        uage = search_history.first()
        user_age = uage.age 
        # if uage else None
        user_gender = uage.gender
        return render(request, 'users/profile.html', {'search_history': search_history , 'user_age': user_age ,'user_gender':user_gender })
    else:
    
     return render(request, 'users/profile.html')




def ind(request):
    return render(request, 'users/index.html')

