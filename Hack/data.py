from asyncore import read
from scipy import stats 
import pandas as pd
import seaborn as sns 
import datetime
from catboost import CatBoostRegressor 
from flask import Flask, request
import matplotlib.pyplot as plt
import csv

#formula = price(1 - age X 0.05) + (mileage/10000 X 0.05))

#Machine Learning:
#CLeans the data and gets rid of outliers
#Replaces year with car age
#Replaces column with columns of 0s and 1s for machine learning (prob not needed)
def dataClean(cars):
    cars['age'] = datetime.now().year - cars['year'] 
    cars = cars.drop('year', 1) 
    cars = cars.dropna() 
    cars = cars[stats.zscore(cars.price) < 3] 
    cars = cars[stats.zscore(cars.hp) < 3] 
    cars = cars[stats.zscore(cars.mileage) < 3] 
    offerTypeDummies = pd.get_dummies(cars.offerType) 
    cars = cars.join(offerTypeDummies) 
    cars = cars.drop('offerType', 1) 
    
    gearDummies = pd.get_dummies(cars.gear) 
    cars = cars.join(gearDummies) 
    cars = cars.drop('gear', 1) 

#Gets heatmap of cars
def correlationHeatMap(cars):
    sns.heatmap(cars.corr(), annot=True, cmap='coolwarm') 
    plt.show() 
    
#Graph of HP and price
def horsePowerMileagePriceGraph(cars):
    sns.set_theme(style="darkgrid") 
    sns.jointplot(x="hp", y="price", data=cars, 
	kind="reg", color="m", line_kws={'color': 'red'}) 
    plt.show() 
    
def priceModel(cars):
    makeDummies = pd.get_dummies(cars.make) 
    cars = cars.join(makeDummies) 
    cars = cars.drop('make', 1) 
    
    modelDummies = pd.get_dummies(cars.model) 
    cars = cars.join(modelDummies) 
    cars = cars.drop('model', 1) 
    
    # the rest of the features, just as before 
    # split train and test data 
    
    model = CatBoostRegressor(iterations=6542, learning_rate=0.03) 
    model.fit( 
        X_train, y_train, 
        eval_set=(X_test, y_test), 
    ) 
    print(model.score(X, Y)) # 0.9664 
    
def featureImportace(model, cars):
    sorted_feature_importance = model.get_feature_importance().argsort( 
	)[-20:] 
    plt.barh( 
        cars.columns[sorted_feature_importance], 
        model.feature_importances_[sorted_feature_importance] 
    ) 
    plt.xlabel("Feature Importance") 
    plt.show() 
    
def calc(realData, cars, model):
    realData['age'] = datetime.now().year - realData['year'] 
    realData = realData.drop('year', 1) 
    
    # all the other transformations and dummies go here 
    
    fitModel = pd.DataFrame(columns=cars.columns) 
    fitModel = fitModel.append(realData, ignore_index=True) 
    fitModel = fitModel.fillna(0) 
    
    featureImportace(model, cars)
    
    priceModel(cars)
    
    preds = model.predict(fitModel) 
    print(preds)

##################################################################################

#Read file and use rough formula:
def getPrice(make, model, year):
    with open('germany-cars-zenrows.csv') as csvFile:
        csvReader = csv.DictReader(csvFile)
        mileage,make,model,fuel,gear,offerType,price,hp,year = csvReader.fieldnames 
        for row in csvReader:
            if row[make] == make and row[model] == model and row[year] == year:
                return row[price]
                
                
def getMiles(make, model, year):
    with open('germany-cars-zenrows.csv') as csvFile:
        csvReader = csv.DictReader(csvFile)
        mileage,make,model,fuel,gear,offerType,price,hp,year = csvReader.fieldnames 
        for row in csvReader:
            if row[make] == make and row[model] == model and row[year] == year:
                return row[mileage]
       
def getUsedPrice(make, model, year):
    mileage = 0 #can be parameter; miles driven as new car = 0
    price = getPrice(make, model, year)
    age = datetime.datetime.today().year - year
    return price * (1 - ((age * 0.05) + (mileage/10000 * 0.05)))

def getUsedPrice(make, model, year, mileage):
    price = getPrice(make, model, year)
    age = datetime.datetime.today().year - year
    return price * (1 - ((age * 0.05) + (mileage/10000 * 0.05)))
    
         
def graphs(make, model, year):
    mileage = 0 #mileage can be parameter too
    cur = datetime.datetime.today().year
    x = [year for year in range(year, cur + 1)]
    price = getPrice(make, model, year)
    y = []
    for ye in x:
        curAge = ye - year
        y.append(price * (1 - ((curAge * 0.05) + (mileage/10000 * 0.05))))
    plt.plot(x, y)
    plt.title('Prices Over Time')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.show()

#Assumes drove same miles per year
def graphs(make, model, year, mileage):
    cur = datetime.datetime.today().year
    x = [year for year in range(year, cur + 1)]
    price = getPrice(make, model, year)
    y = []
    for ye in x:
        curAge = ye - year
        curMileage = 0 #New car = no miles driven
        if curAge > 0:
            curMileage += mileage / curAge
        y.append(price * (1 - ((curAge * 0.05) + (curMileage/10000 * 0.05))))
    plt.plot(x, y)
    plt.title('Prices Over Time')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.show()

#@app.route('/', methods=['POST'])
def userInput():
    if request.method == 'POST':
        text = request.form['text']
        return text
    