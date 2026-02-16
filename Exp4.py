import numpy as np
import pandas as pd

print("\n=========== ATTRIBUTE 1 : CGPA ===========")

data1 = {
    "CGPA": [">=9", "<9", ">=9", "<9", ">=9", ">=9"],
    "Predicted_Job": ["Yes","Yes","No","No","Yes","Yes"],
    "Actual_Job": ["Yes","Yes","No","No","Yes","Yes"]
}

df1 = pd.DataFrame(data1)

y1 = np.array([1 if v=="Yes" else -1 for v in df1["Actual_Job"]])
h1 = np.array([1 if v=="Yes" else -1 for v in df1["Predicted_Job"]])

N = len(y1)
w1 = np.ones(N)/N
df1["Weight"] = w1

epsilon1 = np.sum(w1[y1 != h1])
alpha1 = 0.5*np.log((1-epsilon1)/(epsilon1+1e-10))

w1_new = w1*np.exp(-alpha1*y1*h1)
w1_new = w1_new/np.sum(w1_new)

df1["Updated_Weight"] = np.round(w1_new,4)

print(df)

print("\n=========== ATTRIBUTE 2 : INTEREST ===========")

data2 = {
    "Interest":["Yes","No","No","No","Yes","Yes"],
    "Predicted_Job":["Yes","No","No","No","Yes","Yes"],
    "Actual_Job":["Yes","Yes","No","No","Yes","Yes"],
    "Weight":w1_new
}

df2 = pd.DataFrame(data2)

y2 = np.array([1 if v=="Yes" else -1 for v in df2["Actual_Job"]])
h2 = np.array([1 if v=="Yes" else -1 for v in df2["Predicted_Job"]])
w2 = np.array(df2["Weight"])

epsilon2 = np.sum(w2[y2 != h2])
alpha2 = 0.5*np.log((1-epsilon2)/(epsilon2+1e-10))

w2_new = w2*np.exp(-alpha2*y2*h2)
w2_new = w2_new/np.sum(w2_new)

df2["Updated_Weight"] = np.round(w2_new,4)

print(df2)


print("\n=========== ATTRIBUTE 3 : FINAL CLASSIFIER ===========")

data3 = {
    "Sr_No":[1,2,3,4,5,6],
    "CGPA":["Yes","No","Yes","No","Yes","Yes"],
    "Interest":["Yes","No","No","No","Yes","Yes"]
}

df3 = pd.DataFrame(data3)

cgpa = np.array([1 if x=="Yes" else 0 for x in df3["CGPA"]])
interest = np.array([1 if x=="Yes" else 0 for x in df3["Interest"]])

alpha_cgpa = 0.347
alpha_interest = 0.5490

final_value = alpha_cgpa*cgpa + alpha_interest*interest

df3["Final_Value"] = np.round(final_value,3)
df3["Final_Result"] = ["Yes" if v>0 else "No" for v in final_value]

print(df3)

