# 🧠 CorrPY – Correlation Made Easy

![PyPI version](https://img.shields.io/pypi/v/corrpy)
![Downloads](https://img.shields.io/pypi/dm/corrpy)
![License](https://img.shields.io/pypi/l/corrpy)
![Python](https://img.shields.io/pypi/pyversions/corrpy)

---

**CorrPY** is your lightweight buddy for fast, smart correlation analysis.  
Forget just numbers — CorrPY tells you **what they *mean***. 📊✨

Built for data scientists who want **insights**, not just values.

---

## 🚀 Install

```bash
pip install corrpy
```

---

## 📦 Quickstart

```python
from corrpy import Corrpy

corrpy = Corrpy()
corrpy.getTotalCorrRelation(df)
```

✅ Analyze correlation across features  
✅ Get trends + easy-to-read interpretations  
✅ Go deeper with AI explanations (optional)

---

## 🔥 Key Features

- **Numerical vs Numerical** — Classic correlations + strength.
- **Object vs Numerical** — Category impacts, clear trends.
- **Object vs Object** — Categorical association (Chi2).
- **Transitive Trap Alerts** — Detect hidden indirect links. 🚨
- **AI-Generated Insights** — Explain data like a boss 🧠📜

---

### All Methods you can use 

1. `getMethods()`: Returns a list of all available methods in Corrpy.

2. `getTotalCorrRelation(df, features = ["Correlation", "Pearson", "Distance"], feature = "Correlation", short = False)`: Pass a pandas DataFrame to get correlation analysis across all columns and get trends, interpretations and score with respect to feature u added in parameter.

3. `getGroupInf(objColumn, numColumn, df)`: Compute the correlation between the given object column and the given numeric column.
4. `getAllGroupInf(df)`: Compute the correlation between all object columns and all numeric columns.
5. `setApi()`: Securely handles your [Together.ai](https://www.together.ai/) API token.
6. `explainAITC(df, feature="Correlation", character="Data analyst", mode="Confused")`: Get AI insights for correlation analysis.
7. `shift(num1, num2, shiftValue, df)`: Test how your dependent variable reacts to small changes in an input variable.
8. `explainShift(num1, num2, shiftValue, df, character = "Data analyst", mode = "Funny...")`: An AI analyst explains the output of `shift()` like you're in a meeting with your CEO.
9. `checkTransit(firstFeature, secondFeature, ThirdFeature)`: Check for transitive correlation between three features.
10. `explainPartialCorrelation(num1, num2, df, character = "Data analyst", mode = "Funny...")`: Get AI insights for partial correlation analysis.
11. `checkTransitForColumn(column, df)`: Check for transitive correlation between a column and all other columns.
12. `explainTransitForcolumn(column, df, character = "Data analyst", mode = "Funny...")`: An AI analyst explains the output of `checkTransitForColumn()` like you're in a meeting with your CEO.
---


---

## 👤 Available Characters

- Data Analyst  
- Manager  
- Data Scientist  
- Data Engineer  
- Modi  
- Elon Musk  
- Angry Professor  
- Chandler Bing  
- AI Guru  
- Startup Bro  

(*More being added weekly – you can easily expand the template!*)

---

## 🎭 Emotion Modes (aka `mode`)

- Happy 🎉  
- Angry 😠  
- Sad 😢  
- Excited 🤩  
- Confused 😕  
- Serious 💼  
- Sarcastic 🙃  
- Romantic 💘  
- Zen 🧘  
- Paranoid 🕵️
- Overwhelmed 😩
- Curious 🤔
- Cautious ⚠️
- Funny 😂




---





## 🧠 Example Insights

> *"Age and Fare have a moderate positive correlation.  
Pclass has a strong inverse relation with Fare."*

✨ Plus visual trends, interpretation tags, and more!

---

## 👨‍💻 Author

**YellowForest**  
🔗 [GitHub](https://github.com/Parthdsaiml)

---

## 📄 License

BSD 3-Clause License

---

# ⚡ TL;DR

| # | What CorrPY Gives You |
|:-|:--|
| 🚀 | Quick, meaningful correlation analysis |
| 🤖 | AI-driven explanations |
| 🧩 | Find hidden patterns |
| 🔥 | Detect transitive traps |
| 🎯 | Ideal for both beginners and pros |

---

# 📢 FINAL NOTE:

> **CorrPY isn't just another EDA tool...  
> It's your data's best storyteller. 📚🚀**

---

# 🧹 How to use:
- README for Quick Start 📑
- Full GUIDE.md for Deep Dive 📚
