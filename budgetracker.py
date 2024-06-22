import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import datetime 
import calendar
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder as le

def create_user():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def register(username,password):
    conn=sqlite3.connect("expenses.db")
    c=conn.cursor()
    c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def login(username,password):
    conn=sqlite3.connect("expenses.db")
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password = ?",(username,password))
    user=c.fetchone()
    conn.commit()
    conn.close()
    return user

def check_users():
    conn=sqlite3.connect("expenses.db")
    c=conn.cursor()
    c.execute("SELECT COUNT(*)  FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count > 0
    
def main():
    create_user()
    st.sidebar.title("SWIFT")
    st.sidebar.header("NAVIGATION")

    page = st.sidebar.selectbox("Go to",["Lander","Home","Budget Tracking","Predictions","Clusters"])

    if page == "Lander":
        st.title("SWIFT")
        st.header("Budgeting Made Effortless: Control Your Money, Transform Your Life.")
        st.write("Welcome to SWIFT – the ultimate solution for mastering your finances effortlessly!")
        st.write("Are you tired of feeling stressed about money? Do you want to take control of your financial future? Look no further – SWIFT is here to help you achieve your financial goals and live the life you've always dreamed of.")
        st.write("With SWIFT , budgeting becomes a breeze. Say goodbye to guesswork and hello to clarity as you effortlessly track every dollar you spend. Our intuitive interface makes it easy to categorize your expenses, set savings goals, and monitor your progress – all in one convenient place.")
        st.header("KEY FEATURES")
        st.write("--> Simplified Budgeting: Take the complexity out of budgeting with our user-friendly interface. Say goodbye to spreadsheets and hello to streamlined financial management.")
        st.write("--> Real-Time Tracking: Stay up-to-date on your finances with real-time expense tracking. See where your money is going and make informed decisions about your spending habits.")
        st.write("--> Insightful Reports: Gain valuable insights into your spending patterns with detailed reports and analytics. Identify areas for improvement, track trends over time, and make smarter financial decisions.")
        st.write("--> Secure & Private: Rest easy knowing that your financial data is safe and secure with encryption. Your privacy is our top priority – your information will never be shared or sold to third parties.")
        st.write("Take the first step towards financial freedom today with SWIFT and start tracking your way to a brighter future!")
        st.subheader("Ready to take control of your finances? Get started now!")
        st.write("Navigate to the sidebar")
    if page == "Home":
        st.header("Welcome to SWIFT - Budget Tracking and Analysis App")
        st.subheader("Log In or Sign Up")
        select_mode = option_menu(menu_title=None,options=["Log In", "Sign up"])

        if select_mode == "Log In":
            user_login = st.text_input("Username")
            pass_login = st.text_input("Password",type="password")
            if st.button("Log In"):
                if user_login and pass_login:
                    user = login(user_login,pass_login)
                    if user:
                        st.success(f"Logged in as {user_login}")
                        st.info("Redirecting.....")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
        else:
            user_sign = st.text_input("Username")
            password_sign = st.text_input("Password",type="password")
            if st.button("Sign Up"):
                if user_sign and password_sign:
                    register(user_sign,password_sign)
                    st.success("Account created successfully")
                else:
                    st.warning("Please enter both username and password")
    if page == "Budget Tracking":
        if check_users():
            selected = option_menu(menu_title=None, options=["Add expense", "View expenses", "Visualise expenses"])

            if selected == "Add expense":
                st.title("Add your expenses")
                category = st.radio("Categories", ["Housing", "Transportation", "Foodandgroceries", "Healthcare", "PersonalandLifestyle", "DebtandSavings"])
                #budget = st.number_input("Enter your budget",min_value=0.01,step=0.01)
                expense_name = st.text_input("Expense Name", "")
                amount = st.number_input("Amount", min_value=0.01, step=0.01)
                description = st.text_area("Description", "")

                if st.button("Add"):
                    add_expense(expense_name, category, amount)
                    st.success("Transaction added successfully!")

            elif selected == "View expenses":
                st.title("View your expenses")
                df = load_transactions()
                st.write("Expense Data : ")
                st.write(df)
                if df.empty:
                    st.write("No transactions recorded yet")
                else:
                    st.download_button(label="Download as CSV",data=convert_df_to_csv(df),file_name='expense_data.csv',mime='text/csv')
            elif selected == "Visualise expenses":
                transactions = load_transactions()
                if transactions.empty:
                    st.error("No transactions recorded yet.")
                else:
                    #transactions_df = pd.DataFrame(transactions, columns=["ID", "Name", "Category", "Amount", "Date"])
                    transactions_df = load_transactions()
                    category_totals = transactions_df.groupby("category")["amount"].sum()

                    st.subheader("Expense Distribution by Category")
                    fig_pie = px.pie(category_totals, values=category_totals.values, names=category_totals.index)
                    st.plotly_chart(fig_pie, use_container_width=True)

                    transactions_df["Day"] = pd.to_datetime(transactions_df["date"]).dt.date
                    daily_totals = transactions_df.groupby("Day")["amount"].sum()

                    st.subheader("Daily Expenses")
                    daily_df = daily_totals.reset_index()
                    daily_df["Day"] = daily_df["Day"].astype(str)
                    fig_bar = px.bar(daily_df, x="Day", y="amount", labels={'Amount':'Total Expense'})
                    fig_bar.update_xaxes(title_text='Day')
                    fig_bar.update_yaxes(title_text='Total Expense')
                    st.plotly_chart(fig_bar, use_container_width=True)

        else:
            st.error("Please log in to access this page")

    elif page == "Predictions":
        if check_users():
            transactions_df = load_transactions()
            st.header("Future Predictions")
            st.write("Enter the category and amount for future prediction:")
            category_input = st.selectbox("category", ["Housing", "Transportation", "Foodandgroceries", "Healthcare", "PersonalandLifestyle", "DebtandSavings"])
            #amount_input = st.number_input("amount", min_value=0.01, step=0.01)

            if st.button("Predict"):
                existing_dates, preds_e, future_dates, preds_f = predict_expenses(category_input)
                fig = go.Figure()
                existing_daily_totals = transactions_df[transactions_df['category'] == category_input].groupby(pd.to_datetime(transactions_df["date"]).dt.date)["amount"].sum()
                fig.add_trace(go.Scatter(x=existing_dates,
                                         y=existing_daily_totals,
                                         mode='markers',
                                         name='Existing Expenses'))
                fig.add_trace(go.Scatter(x=np.concatenate((existing_dates, future_dates)),
                                     y=np.concatenate((preds_e, preds_f)),
                                     mode='lines', name='Predicted Expenses'))

                fig.update_layout(title='Expense Prediction',
                      xaxis_title='Date',
                      yaxis_title='Expense Amount',
                      showlegend=True)
                future_dates1 = [dt.date() for dt in future_dates]
                future_data = {'Date': future_dates1, 'Predicted Expense': preds_f}
                future_df = pd.DataFrame(future_data)
                
                st.write("Future Predicted Expenses :")
                st.write(future_df)
                st.plotly_chart(fig)
                
                

        else:
            st.error("Please log in to access this page")
            
    elif page == "Clusters":
        if check_users():
            st.header("Visualizations")
            expenses_df = load_transactions()
            opt = st.selectbox("Cluster by", ["Categories", "Dates", "Amount"])
            expenses_df['l'] = le().fit_transform(expenses_df['category'])
            expenses_df['dl'] = le().fit_transform(expenses_df['date'])

            if opt == "Categories":
                features = ['l']
            
            elif opt == "Dates":
                features = ['dl']
                
            elif opt == "Amount":
                features = ['amount']

            X = expenses_df[features]

            kmeans = KMeans(n_clusters=6)  
            clusters = kmeans.fit_predict(X)
            expenses_df['cluster'] = clusters

            custom_color_scale = px.colors.qualitative.Plotly
            if opt == "Categories":
                fig = px.scatter(x=expenses_df['id'], y=expenses_df['category'], color=clusters,color_continuous_scale=custom_color_scale, title="Clustering by Categories")
                fig.update_yaxes(title=opt)

            elif opt == "Dates":
                fig = px.scatter(x=expenses_df['id'], y=expenses_df['date'], color=clusters,color_continuous_scale=custom_color_scale, title="Clustering by Dates")
                fig.update_yaxes(title=opt)
            elif opt == "Amount":
                fig = px.scatter(x=expenses_df['id'], y=expenses_df['amount'], color=clusters,color_continuous_scale=custom_color_scale, title="Clustering by Amount")
                fig.update_yaxes(title=opt)
            
            fig.update_xaxes(title="Entry ID")
            fig.update_layout(showlegend=False)

            st.write(expenses_df[['id','name','category','amount','date','cluster']])
            st.plotly_chart(fig)
            

            
        else:
            st.error("Please log in to access this page")

def add_expense(expense_name,category,amount):
    #add expense code
    conn=sqlite3.connect("expenses.db")
    c=conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO expenses(name,category,amount,date) VALUES(?,?,?,?)",(expense_name,category,amount,date))
    conn.commit()
    conn.close()

def load_transactions():
    #load expenses 
    conn=sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses",conn)
    conn.close()
    return df

def predict_expenses(category):
    transactions_df = load_transactions()
    category_data = transactions_df[transactions_df['category']==category]
    category_data['date'] = pd.to_datetime(category_data['date'])
    
    new_df = category_data.groupby('date')['amount'].sum().reset_index()
    new_df.columns = ['date', 'total_amount']
    
    X = new_df['date'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
    y = new_df['total_amount'].values

    #lr = LinearRegression()
    #lr.fit(X,y)
    svr = SVR(kernel='rbf',C=100,gamma=0.1,epsilon=.1)
    svr.fit(X,y)
    
    existing_dates = category_data['date']
    existing_dates_ordinal = np.array([date.toordinal() for date in existing_dates]).reshape(-1, 1)
    preds_e = svr.predict(existing_dates_ordinal)
    
    future_dates = pd.date_range(start=category_data['date'].max(),periods=5,freq='M')
    future_dates_ordinal = np.array([date.toordinal() for date in future_dates]).reshape(-1, 1)
    preds_f = svr.predict(future_dates_ordinal)

    return existing_dates,preds_e,future_dates, preds_f

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

if __name__ == "__main__":
    main()
