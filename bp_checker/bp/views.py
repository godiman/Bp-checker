from django.shortcuts import redirect, render

from django.http import HttpResponse
from .forms import RegistrationForm, BpForm, UserUpdate
from .models import UserProfile, History
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from io import StringIO

#import packages for machines learning
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os
import random
import pygame
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
pygame.mixer.init()

#Index view
def index(request):
    return render(request, 'bp/index.html')


# Render the registration page
def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():   
        n = form.save()
        # Gets the foreiegn key (username) of the registered user 
        n = User.objects.get(pk=n.pk)
        print('foreiegn key after registration:', n )
        #Store user phone number and gender in user profile model
        phone_no = form.cleaned_data['phone_no'] 
        gender = form.cleaned_data['gender']
        user_profile = UserProfile.objects.create(user=n, phone_no=phone_no, gender=gender)
        #print(form.cleaned_data)
        #Display success message
        messages.success(request, 'Account created successfully')
        return redirect('login')
        form = RegistrationForm()
    return render(request, 'bp/register.html', context = {'form': form})

    
#Renders user dashboard page
def user_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('login')
    return render(request, 'bp/dashboard.html', {'user': user})
  

# function that play music
def playMusic(path):
    #m = playsound(musicPath, False)
    file = os.path.join(path, random.choice(os.listdir(path)))
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    
    
    #print('Music time: ', m_time)s
# function that plot graph
def plotgraph(data, y_pred):
    fig = plt.figure(figsize=(5,5))
    plt.scatter(int(data["education"]), y_pred, color='purple')
    plt.scatter(int(data["bmi"]), y_pred, color='blue')
    plt.scatter(int(data["c_smoker"]), y_pred,  color='green' )
    plt.scatter(int(data["age"]), y_pred,  color='brown' )
    plt.scatter(int(data["heart_rate"]), y_pred,  color='red')
    plt.ylabel('Hypertension Predictor', color='red')
    plt.xlabel('Education, BMI, CurrentSmoker, Age, HeartRate', color='red')
    plt.legend(['Education', 'Body mass index', 'Current smoker', 'Age', 'Heart rate'])
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    graph = imgdata.getvalue()
    #plt.show()
    return graph

# function that generate random numbers
def simulator():
    bp_var = []  
    edu = random.randint(1,4)
    age = random.randint(30,70) 
    bmi = random.randint(19,39)
    s = random.randint(1,2)  
    hrate = random.randint(55,115)  
    # convert the random numbers into list        
    bp_var.extend((edu, age, bmi, s, hrate))
    return bp_var

# # converter list to dictionary
def converter(data): 
    bp_keys = ['education', 'age', 'bmi', 'c_smoker', 'heart_rate']
    #zip a list and convert to dictionary
    simulated_values = dict(zip(bp_keys, data))
    #print('Simulator inputs: ', simulated_values) 
    return simulated_values

# lisval = simulator()
# #print(converter(lisval))

# dict_data = converter(lisval)
#print('Data in list: ', dict_data)

# Render Prediction form
def bp_form(request):
    if request.user.is_authenticated:
        lisval = simulator()
        #print(converter(lisval))

        dict_data = converter(lisval)
        #print(dict_data)
        if request.method == 'POST':
            predict_form = BpForm(initial=dict_data)
        else:
           
            predict_form = BpForm(initial=dict_data)
    else:
        return redirect('login')
    return render(request, 'bp/predict.html', {'predict_form':predict_form})


#Renders the prediction result
def bp_prediction(request):
    if request.user.is_authenticated:
        predict_form = BpForm(request.POST or None) 
        if predict_form.is_valid():
            #print(predict_form.cleaned_data['age'])
            df = pd.read_csv('bp/data_set/Hypertension_data.csv') 
            #print(df.head(10))
            
            #split dataset into dependent 
            X = df[['education', 'age', 'BMI', 'currentSmoker', 'heartRate']]
            #print(X)
            
            # split the data set into independent variable
            Y = df['prevalentHyp']
            #print(Y)
            
            # Split the data set into training and testing.
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.25, random_state = 0)

            # Using random forest classifier
            forest = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
            forest.fit(X_train, Y_train)
            
            # Prediction accuracy
            #print('Accuracy:', forest.score(X_train, Y_train))
            
            # Predict from the test dataset
            #Predicting the test data
            #y_pred = forest.predict(X_test)
            #print('Y pred: ', y_pred)
            
            # Input from the user interface (form)
            #my_testData = [[ 58, 0, 0, 100, 248, 0, 0, 122, 0, 1.0, 1, 0, 2]]
            form_data = predict_form.cleaned_data
            #print('Form data: ', form_data)
            user_input = list(form_data.values())
            form_val = np.array(user_input)
            #print('Array: ', form_val)

            #Predicting the user data
            y_pred = forest.predict(form_val.reshape(1, -1))
            #print('X test: ',form_val,'-', 'Y pred: ', y_pred)
                
            user_input = predict_form.cleaned_data
            path = 'bp/Bp_music'
            userId = request.user.id
            u = User.objects.get(pk=userId)
            #print('Logged in user: ', u) 
            
            # Save the prediction result to the db 
            history = History.objects.create(user=u, education=form_data['education'], 
            age=form_data['age'], bmi=form_data['bmi'], current_smoker=form_data['c_smoker'], 
            heart_rate=form_data['heart_rate'], result=y_pred)
            

            # if the prediction is 0, the user's blood pressure is normal else the blood pressure is high
            if(y_pred == 0):
                #n = 'Your blood presure is normal'   
                #print('Your blood pressure is normal')         
                # Plot the graph.
                pygame.mixer.music.stop()           
                graph = plotgraph(form_data, y_pred)                   
            else:
                #n = 'Your blood presure is High'                
                # Plot the graph.
                graph = plotgraph(form_data, y_pred)
                #Plays music
                playMusic(path)
                #print(predict_form.cleaned_data)         
    else:
        return redirect('login')
    return render(request, 'bp/result.html', {'user_input': user_input, 'prediction': y_pred, 'graph': graph})   



# Define user's settings
def user_setting(request):
    if request.user.is_authenticated:
        u = UserProfile.objects.get(pk=request.user.id)
        p = u.user
        #print(u.user.username, u.gender, u.phone_no)         
        # Edit phone number form in user's settings
        f = UserUpdate(request.POST or None)
        if f.is_valid():
           u.phone_no = f.cleaned_data['phone_no']
           u.save()
           messages.success(request, 'Phone number updated')
    else:
        return redirect('login')
    return render(request, 'bp/setting.html', {'user': u, 'edit': f})

# Define the history function 
def history(request):
    # get the user id
    #userId = request.user.username
    #print(userId)
    hist = History.objects.filter(user=request.user.id)
    #print(hist)
    
    # for item in hist:
    #     print(item.age)
        
    return render(request, 'bp/history.html', {'history': hist}) 

# Delet user's history
def deletHistory(request, id):
    h = History.objects.get(pk=id).delete()
    #print('History id: ', id) 
    messages.success(request, 'History Deleted.')
    hist = History.objects.filter(user=request.user.id)
    return render(request, 'bp/history.html', {'history': hist}) 

# Data set description
def des_dataset(request):
    
    return render(request, 'bp/dataset_des.html') 

def logout(request):
    auth.logout(request)
    return redirect('login')