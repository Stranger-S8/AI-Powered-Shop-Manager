import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

class Predict:
    def __init__(self):
        self.df = pd.read_csv("temp_data.csv")
    
    def preprocess_data_fn(self):

        self.df["ord_date"] = pd.to_datetime(self.df["ord_date"])
        self.df["ord_time"] = pd.to_datetime(self.df["ord_time"], format=("%I : %M : %S %p"))

        self.df["year"] = self.df["ord_date"].dt.year
        self.df["month"] = self.df["ord_date"].dt.month
        self.df["day"] = self.df["ord_date"].dt.day
        
        self.df["weekday"] = self.df["ord_date"].dt.weekday

        self.X = self.df[["year", "month", "day", "weekday", "p_id", "quantity_sold"]]
        self.Y = self.df["total_sales"]
    
    def future_dates(self, s_type):
        last_date = self.df["ord_date"].max()
        last_date = pd.to_datetime(last_date)

        if s_type == "Next 7 Days":
            self.future_date = [last_date + timedelta(days=i) for i in range(0, 7)]

        elif s_type == "Next 30 Days":
            self.future_date = [last_date + timedelta(days=i) for i in range(0, 30)]
        
        print(self.future_date)
        print(s_type)
        
        self.future_df = pd.DataFrame({"ord_date" : self.future_date})

        self.future_df["year"] = self.future_df["ord_date"].dt.year
        self.future_df["month"] = self.future_df["ord_date"].dt.month
        self.future_df["day"] = self.future_df["ord_date"].dt.day
        self.future_df["weekday"] = self.future_df["ord_date"].dt.weekday

        self.future_df["p_id"] = self.df["p_id"]

        self.future_df["quantity_sold"] = self.df["quantity_sold"].mean()

        future_features = self.future_df[["year", "month", "day", "weekday", "p_id", "quantity_sold"]]

        self.future_df["predicted_sales"] = self.model.predict(future_features)

    def train_model_fn(self):

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=42)

        self.model = RandomForestRegressor(n_estimators=110, random_state=42)
        self.model.fit(self.X_train, self.Y_train)

        with open("AI Models/sales_model.pkl", "wb") as f:
            pickle.dump(self.model, f)

    def predict_model_fn(self):
        y_pred = self.model.predict(self.X_test)

        mse = mean_squared_error(self.Y_test, y_pred)
        r2 = r2_score(self.Y_test, y_pred)

        print(f"Mean Squared Error : {mse}")
        print(f"R2 Score : {r2}")
    
    def get_future_sales_fn(self, s_type):
        with open("AI Models/sales_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        self.future_dates(s_type)
        
        return self.future_date, self.future_df["predicted_sales"]


A = Predict()
# A.preprocess_data_fn()
# A.train_model_fn()
# A.predict_model_fn()
# a, b = A.get_future_sales_fn("Next 30 Days")





        

