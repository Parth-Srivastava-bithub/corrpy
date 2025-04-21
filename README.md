# 🧠 CorrPY – Correlation with Ease

![PyPI version](https://img.shields.io/pypi/v/corrpy)
![PyPI Downloads](https://img.shields.io/pypi/dm/corrpy)
![License](https://img.shields.io/badge/license-BSD%203--Clause-blue)
![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-blue)





**CorrPY** is a lightweight Python library that simplifies correlation analysis with intuitive insights and visual patterns. It's built for data scientists who want quick, meaningful interpretation instead of just numbers.

---

## 🚀 Installation

```bash
pip install corrpy
```

---

## 📦 Import and Initialize

```python
from corrpy import Corrpy

corrpy = Corrpy()
```

---

## 🧪 Quick Usage

```python
corrpy.getTotalCorrRelation(df)
```

> Pass a pandas DataFrame to get correlation analysis across all columns.

---


## Get to know how each cateogry effect Correlation with other numeric values

```python
corrpy.getGroupInf(objColumn, numColumn, df)
```

or 

```python
corrpy.getAllGroupInf(df)
```


`getGroupInf` function takes an object column, a numeric column, and a DataFrame as inputs. It will compute the correlation between the given object column and the given numeric column.

`getAllGroupInf` function takes a DataFrame as an input. It will compute the correlation between all object columns and all numeric columns.

![alt text](image-1.png)
---

## Get AI Insights

```python
corrpy.explainAITC(df)
```
`explainAITC` function takes a DataFrame as an input. It will compute the correlation between all object columns and all numeric columns. The correlation includes the strength of correlation, trend of the correlation, and the type of correlation (positive or negative). If the correlation is not significant, it will return a message indicating that there is no significant correlation.

---

![alt text](image-2.png)

## 🧩 Features

- 📊 **Numerical vs Numerical** → Pearson correlation with strength interpretation  
- 🧠 **Object vs Numerical** → Association analysis (point biserial or ANOVA based)  
- 🔁 **Object vs Object** → Chi-Square based categorical association  
- ⌚ **Time vs Other** → Time-based trend and correlation detection  
- ⚠️ **Transitive Correlation Alert** → Detects misleading indirect relations  

---

## 📈 Example Output

![image](https://github.com/user-attachments/assets/2fa9140e-5ae1-4f18-a030-0dcb74e44ea9)


---

# Explanation of Terms in Correlation Analysis

This document explains the key terms and terminology used in the correlation analysis output. Understanding these terms will help you interpret the relationship between various features in the dataset.

---

## Numerical vs Numerical Relation
- **Feature A / Feature B**: These represent two numerical columns in the dataset that are being compared for correlation.
- **Correlation Strength**: The value indicates how strongly two numerical features are related. Ranges from -1 to 1:
  - **Positive values** (closer to 1) indicate a strong positive relationship.
  - **Negative values** (closer to -1) indicate a strong negative relationship.
  - **Low/No linkage** indicates little to no correlation.
- **Interpretation**: A brief statement explaining the strength and nature of the correlation.
- **Trend**: A graphical representation of the correlation trend, with symbols:
  - ▱▱▱▱▱ = No significant trend
  - ▰▰▱▱▱ = Positive trend with moderate strength.
    

---

## Object vs Numerical Relation
- **Object Column**: A categorical or non-numeric feature (e.g., string, category).
- **Numerical Column**: A numerical feature (e.g., integer, float).
- **Correlation**: The degree of association between an object feature and a numerical feature. It ranges from -1 to 1:
  - **↑** indicates a positive correlation.
  - **↓** indicates a negative correlation.
- **Interpretation**: The explanation of the relationship:
  - **Weak: Contextual** means a weak, context-dependent correlation.
  - **Moderate: Linked Trend** means a moderate correlation showing a clear relationship.
- **Trend**: The visual representation of the correlation trend:
  - ▰▰▱▱▱ =  Trend with moderate strength *For Object Vs Numerical Relation Trends just shows the strength without any direction*.

---

## Object vs Object Relation
- **Feature A / Feature B**: Both are categorical (non-numerical) features.
- **Chi2**: The Chi-square statistic measures the difference between expected and observed frequencies of categorical data.
- **P-Value**: The probability of obtaining a result as extreme as the one observed, assuming the null hypothesis is true. A high p-value (> 0.05) typically means there's no significant relationship between the features.

---

## Time vs Numerical Relation
- **DateTime Column**: A feature representing time or dates.
- **Numerical Column**: A numerical feature being compared with the datetime column.
- **Correlation Score**: The strength of the relationship between time and numerical features. A negative score indicates no linkage.
- **Interpretation**: The relationship between time and numerical features, with **No linkage** indicating no significant correlation.
- **Trend**: The trend representation:
  - ▱▱▱▱▱ = No significant trend.

---

## Time vs Object Relation
- **DateTime Column**: A feature representing time or dates.
- **Object Column**: A categorical feature.
- **Correlation Score**: Indicates the relationship between time and categorical features.
- **Interpretation**: Explains the nature of the correlation, such as **Weak: Contextual** for weak, context-dependent correlation or **No linkage** for no significant correlation.
- **Trend**: Visual representation of the correlation trend, with arrows indicating the strength and direction.

---

## Transitive Relation Alert
- **Feature A / Feature B / Feature C**: A scenario where the correlation between Feature A and Feature B might be influenced by Feature C. This suggests a transitive relationship where indirect connections between features need to be checked.

---

### Conclusion
The correlation and relationships presented in this analysis help you understand how different features in your dataset are connected. Correlations can vary from weak to strong, positive or negative, and these trends provide valuable insights into how to approach data analysis and modeling.


## 💡 Why CorrPY?

- Gives **interpretable insights**, not just raw correlation values  
- Detects **transitive traps** often missed in basic EDA  
- Ideal for **data pre-analysis** before modeling  

---

## 📚 Dependencies

- pandas  
- numpy  
- scipy  
- seaborn  
- IPython  

---

## 👨‍💻 Author

**YellowForest**  
🔗 [GitHub](https://github.com/Parthdsaiml)

---

## 📄 License

BSD 3-Clause License

---

