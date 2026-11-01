import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------- LOAD DATA -----------------
df = pd.read_csv("TelcoCustomerChurn.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# ----------------- DETECT COLUMNS -----------------
if 'churnlabel' in df.columns:
    churn_col = 'churnlabel'
elif 'churn' in df.columns:
    churn_col = 'churn'
else:
    st.error("No churn column found")
    st.stop()

if 'tenureinmonths' in df.columns:
    tenure_col = 'tenureinmonths'
elif 'tenure' in df.columns:
    tenure_col = 'tenure'
else:
    st.error("No tenure column found")
    st.stop()

# ----------------- FIX CHURN VALUES -----------------
df[churn_col] = df[churn_col].astype(str).str.strip().str.lower()

df[churn_col] = df[churn_col].replace({
    'yes': 'Yes',
    'no': 'No',
    '1': 'Yes',
    '0': 'No',
    'true': 'Yes',
    'false': 'No',
    'churned': 'Yes',
    'stayed': 'No'
})

# ----------------- FIX NUMERIC -----------------
if 'totalcharges' in df.columns:
    df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce')

df = df.dropna(subset=[churn_col])

# ----------------- TITLE -----------------
st.title("📊 Customer Churn Analysis Dashboard")

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.title("Filters")

churn_options = ["All"] + sorted(df[churn_col].unique())
churn_filter = st.sidebar.selectbox("Select Churn Status", churn_options)

contract_options = ["All"] + sorted(df['contract'].unique()) if 'contract' in df.columns else ["All"]
contract_filter = st.sidebar.selectbox("Select Contract Type", contract_options)

# ----------------- APPLY FILTER -----------------
filtered_df = df.copy()

if churn_filter != "All":
    filtered_df = filtered_df[filtered_df[churn_col] == churn_filter]

if 'contract' in df.columns and contract_filter != "All":
    filtered_df = filtered_df[filtered_df['contract'] == contract_filter]

# ----------------- KPI -----------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", df.shape[0])
col2.metric("Filtered Customers", filtered_df.shape[0])

if len(filtered_df) > 0:
    yes_count = filtered_df[filtered_df[churn_col] == 'Yes'].shape[0]
    total_count = len(filtered_df)
    churn_rate = (yes_count / total_count) * 100
else:
    churn_rate = 0
    yes_count = 0
    total_count = 0

col3.metric("Churn Rate (%)", round(churn_rate, 2))

st.info(f"👉 Out of {total_count} customers, {yes_count} have churned.")

# ----------------- DATA -----------------
st.subheader("📄 Data Preview")
st.write(filtered_df.head())

# ----------------- CHART 1 -----------------
st.subheader("📊 Churn Distribution")

fig1, ax1 = plt.subplots()
filtered_df[churn_col].value_counts().plot(
    kind='bar',
    color=['#ff6b6b', '#4ecdc4'],
    ax=ax1
)
st.pyplot(fig1)

st.success("👉 **A significant portion of customers are leaving — churn is a key business issue.**")

# ----------------- CHART 2 -----------------
if 'monthlycharges' in df.columns:
    st.subheader("💰 Monthly Charges vs Churn")

    fig2, ax2 = plt.subplots()
    filtered_df.boxplot(column='monthlycharges', by=churn_col, ax=ax2)
    plt.title("")
    st.pyplot(fig2)

    st.success("👉 **Customers with higher monthly charges are more likely to churn.**")

# ----------------- TENURE GROUP -----------------
filtered_df = filtered_df.copy()

filtered_df['tenure_group'] = pd.cut(
    filtered_df[tenure_col],
    bins=[0,12,24,36,48,60,100],
    labels=['0-1yr','1-2yr','2-3yr','3-4yr','4-5yr','5+yr']
)

# ----------------- CHART 3 -----------------
st.subheader("📊 Tenure vs Churn")

fig3, ax3 = plt.subplots()
filtered_df.groupby('tenure_group')[churn_col].value_counts().unstack().plot(
    kind='bar',
    stacked=True,
    color=['#74c69d', '#f94144'],
    ax=ax3
)
st.pyplot(fig3)

st.success("👉 **New customers churn more than long-term customers.**")

# ----------------- CHART 4 -----------------
if 'contract' in df.columns:
    st.subheader("📊 Contract vs Churn")

    fig4, ax4 = plt.subplots()
    pd.crosstab(filtered_df['contract'], filtered_df[churn_col]).plot(
        kind='bar',
        color=['#577590', '#f3722c'],
        ax=ax4
    )
    st.pyplot(fig4)

    st.success("👉 **Month-to-month contracts show the highest churn risk.**")

# ----------------- CHART 5 -----------------
if 'paymentmethod' in df.columns:
    st.subheader("💳 Payment Method vs Churn")

    fig5, ax5 = plt.subplots()
    pd.crosstab(filtered_df['paymentmethod'], filtered_df[churn_col]).plot(
        kind='bar',
        color=['#90be6d', '#f9c74f'],
        ax=ax5
    )
    st.pyplot(fig5)

    st.success("👉 **Customers using electronic check tend to churn more.**")

# ----------------- CHART 6 -----------------
if 'internetservice' in df.columns:
    st.subheader("🌐 Internet Service vs Churn")

    fig6, ax6 = plt.subplots()
    pd.crosstab(filtered_df['internetservice'], filtered_df[churn_col]).plot(
        kind='bar',
        color=['#43aa8b', '#577590'],
        ax=ax6
    )
    st.pyplot(fig6)

    st.success("👉 **Fiber optic users show higher churn compared to others.**")

# ----------------- HEATMAP -----------------
if 'contract' in df.columns:
    st.subheader(" Churn Heatmap")

    pivot = filtered_df.pivot_table(
        index="tenure_group",
        columns="contract",
        values=churn_col,
        aggfunc=lambda x: (x == "Yes").mean()
    )

    fig7, ax7 = plt.subplots()
    sns.heatmap(pivot, annot=True, cmap="coolwarm", ax=ax7)
    st.pyplot(fig7)

    st.success("👉 **Low tenure + month-to-month contracts = highest churn risk.**")