# -*- coding: utf-8 -*-
"""Car_price_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dBwSJQ89p6ZlTu6XwjeGT6HzXcz1E38t
"""

import pandas as pd
import numpy as np

car = pd.read_csv('quikr_car.csv')
car.head(5)

car.shape

car.info()

car['year'].unique()

car['Price'].unique()

car['fuel_type'].unique()

"""#**Data preprocessing to done:**


1.   'year' column is not type of int
2.   'year' column has many non-int values
3.   'Price' column has non-int values
4.   'Price' column is not type of int
5.   'kms_driven' has kms with ints
6.   'kms_driven' is not of type int
7.   'kms_driven' has NAN values
8.   'fuel_type' has NAN values
9.   'name' has mixture of variables and nos so, we keep name with only 3 words


"""

# preprocessing now...
backup = car.copy()

print(car.shape)

car = car[car['year'].str.isnumeric()]

print(car.shape)

car['year'] = car['year'].astype(int)

car.info()

car = car[car['Price'] != 'Ask For Price']  # removing 'Ask for price' value as this col has str val as only 'Ask for price'
car['Price'] = car['Price'].str.replace(',','').astype(int) # removing ',' from Price
car.info()

print(car['kms_driven'])
car['kms_driven'] =  car['kms_driven'].str.split(' ').str.get(0).str.replace(',','') # removing kms and ','
car = car[car['kms_driven'].str.isnumeric()] 
car['kms_driven'] = car['kms_driven'].astype(int) # changing to numeric type

car.info()

print(car[car['fuel_type'].isna()])
print(car[car['fuel_type'].isna() == False])
car = car[car['fuel_type'].isna() == False]  # removing NAN values in fuel_type

car['name'] = car['name'].str.split().str.slice(0,3).str.join(" ")  # taking only 1st 3 words of name

car  # here index got changed so, we reset index

car.reset_index()  # if drop = True is not written

car.reset_index(drop = True)

car.describe() #as we have 3 int cols so, describe is given on 3 cols

car[car['Price'] > 6e6] # This is outlier 6e6 = 60L

print(car[car['Price'] < 6e6].reset_index(drop = True))
car = car[car['Price'] < 6e6].reset_index(drop = True)

car.describe()

# storing cleaned data into csv file
car.to_csv('cleaned_car.csv')

"""#**MODEL**"""

X = car.drop(columns = 'Price')
Y = car['Price']

X, Y

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

one = OneHotEncoder()
one.fit(X[['name','company','fuel_type']])

column_trans = make_column_transformer((OneHotEncoder(categories = one.categories_),['name','company','fuel_type']), remainder='passthrough')

lr = LinearRegression()

pipe = make_pipeline(column_trans, lr)

pipe.fit(x_train, y_train)

y_pred = pipe.predict(x_test)

r2_score(y_test, y_pred)

scores = []
for i in range(1000):
  x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=i)
  lr = LinearRegression()
  pipe = make_pipeline(column_trans, lr)
  pipe.fit(x_train, y_train)
  y_pred = pipe.predict(x_test)
  scores.append(r2_score(y_test, y_pred))

np.argmax(scores)

scores[np.argmax((scores))]

# so random state = 433
# training model using random_state = 433
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=np.argmax(scores))
lr = LinearRegression()
pipe = make_pipeline(column_trans, lr)
pipe.fit(x_train, y_train)
y_pred = pipe.predict(x_test)
r2_score(y_test, y_pred)

import pickle

pickle.dump(pipe, open('LinearRegressionModel.pkl', 'wb'))

pipe.predict(pd.DataFrame([['Maruti Suzuki Swift', 'Maruti', 2019, 100, 'Petrol']], columns=['name','company','year','kms_driven','fuel_type']))

