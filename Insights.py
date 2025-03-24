import pandas as pd
df = pd.read_excel(r"C:\Users\ASUS\Desktop\python\DigitalX Project\handeled_missing.xlsx")

df['day'] = df['sys_created_on'].dt.day
df['month'] = df['sys_created_on'].dt.month
df['year'] = df['sys_created_on'].dt.year

# Calculate resolution time in hours
df["resolution_time"] = (df["resolved_at"] - df["sys_created_on"]).dt.total_seconds() / 3600

#Average resolution time per Category and Priority
avg_resolution_time = df.groupby(["category", "priority"])['resolution_time'].mean().reset_index()
avg_resolution_time.to_csv("Average resolution Time.csv")

#Ticket closure rate per Assigned Group
def closure_rate_func(x):
    return (x == "Closed").sum() / len(x)

closure_rate = df.groupby("assignment_group")["state"].apply(closure_rate_func).reset_index()
closure_rate.columns = ["assignment_group", "closure_rate"]
closure_rate.to_csv("Tickect Closure Rat.csv")

#Monthly Ticket Summary
df["month_year"] = df["sys_created_on"].dt.to_period("M")
monthly_summary = df.groupby("month_year").agg(
    total_tickets=("category", "count"),
    avg_resolution_time=("resolution_time", "mean"),
    closure_rate=("state", closure_rate_func)
).reset_index()
monthly_summary.to_csv("Monthly Tickect Summary.csv")


print("Average Resolution Time per Category and Priority:\n", avg_resolution_time.head())
print("\nTicket Closure Rate per Assigned Group:\n", closure_rate.head())
print("\nMonthly Ticket Summary:\n", monthly_summary.head())