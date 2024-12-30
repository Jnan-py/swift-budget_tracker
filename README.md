# SWIFT - Budget Tracking and Analysis App

## Overview

SWIFT is a comprehensive budgeting application designed to make financial management effortless and effective. The app helps users track their expenses, visualize spending patterns, predict future expenses, and analyze spending clusters. With an intuitive interface and robust features, SWIFT empowers users to take control of their financial future.

## Features

### 1. Simplified Budgeting

- User-friendly interface for managing expenses.
- Simplified process of including and categorizing expenses.

### 2. Real-Time Tracking

- Include, view, and track expenses in real-time.
- Track spending habits by category or day.

### 3. Insightful Reports and Visualizations

- Expense distribution represented as pie charts.
- Daily expenses represented as bar charts for trend analysis.

### 4. Predictions

- Use machine learning (SVR model) to predict future expenses for specific categories.
- Represent predictions along with historical data graphically.

### 5. Clustering Analysis

- Clustering of expenses based on categories, dates, or amounts to identify spending patterns.
- Scatter plots to visualize clusters.

### 6. Secure and Private

User authentication with username and password
Secure database storage using SQLite

## Technologies Used

### Frontend

**Streamlit**: For building an intuitive and interactive user interface.

### Backend

**SQLite**: Database for securely storing user data and expenses.

### Data Visualization

**Plotly**: For creating dynamic and interactive charts.

### Machine Learning

- **Scikit-learn**: For expense prediction via SVR and clustering through K-Means.

### Other Libraries

- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical calculations.
- **Datetime and Calendar**: Handling and transforming dates.

## Installation and Setup

### Prerequisites

- Python 3.7+
- Pip Python package manager

### Instructions

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

````
3. Run the app:
   ```bash
   streamlit run app.py
````

## Usage

### 1. Lander Page

Overview of SWIFT's capabilities and functionalities.
Sidebar leads to other sections.

### 2. Home

#### Log In

Username and password for personal details.
Sign up for registration if a new user.

#### Sign Up

Create a new account for a unique username and password.

### 3. Budget Tracking

#### Add Expense

- Enter expense name, category, and amount to record a new transaction.

#### View Expenses

- View all recorded expenses in a tabular format.
- Download expense data as a CSV file.

#### Visualize Expenses

- View spending distribution by category.
- Analyze daily expense trends with bar charts.

### 4. Predictions

- Predict future expenses for selected categories.
- View predictions alongside existing data.

### 5. Clusters

- Group costs by category, date, or amount
  Plot clusters as scatter plot.

## Project Organization

```bash
├── app.py
├── new_expenses.db
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Plotly](https://plotly.com/)
- [SQLite](https://sqlite.org/)

---

Start mastering your finances today with SWIFT!
