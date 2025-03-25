import pandas as pd

df = pd.read_excel(r"C:\Users\ASUS\Downloads\Sample Data file for Analysis_Jan'25.xlsx")

df.columns = df.columns.str.replace("inc_","",case=False)

df = df.drop_duplicates()

# Remove two columns which are not required 
df = df.drop(columns=["sla_due","number"])

# conversion of datetime datatype
df["sys_created_on"] = pd.to_datetime(df["sys_created_on"])
df["resolved_at"] = pd.to_datetime(df["resolved_at"])

# impute missing timing 

df["resolution_time"] = (df["resolved_at"] - df["sys_created_on"]).dt.total_seconds()
avg_resolution_time = df["resolution_time"].mean()

df.loc[df["resolved_at"].isnull(),"resolved_at"] = df["sys_created_on"] + pd.to_timedelta(avg_resolution_time,unit = "s")

# impute missing for cmdb_ci
df["cmdb_ci"] = df.groupby("category")["cmdb_ci"].transform(lambda x : x.fillna(x.mode()[0]) if not x.mode().empty else "Unknown")

df["short_description"] = df["short_description"].fillna(df["short_description"].mode()[0])

df["close_code"] = df.groupby("assignment_group")["close_code"].transform(lambda x : x.fillna(x.mode()[0]) if not x.mode().empty else "Unknown")

df["close_notes"] = df.groupby("close_code")["close_notes"].transform(lambda x : x.fillna(x.mode()[0]) if not x.mode().empty else "Unknown")

df.drop(columns=["resolution_time"],inplace = True)

df.to_excel("data/handeled_missing.xlsx",index = False)