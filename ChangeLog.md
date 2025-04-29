

# v 0.3.10 🚀

## ✨ What's New

### 🎭 Character Personalization
Added `character` parameter to both `explainAITC()` and `explainShift()` functions.  
Now your insights can be delivered by anyone — from **Krishna** to **Chandler Bing** to **Elon Musk**. Pick your storyteller.  

### 🎨 Emotion Control
Added `mode` parameter that lets you pick the *mood* of the explanation: want it sarcastic, sad, or romantic? Your call.

---

## 🛠 Updated Functions

- `explainAITC(df, feature="Correlation", character="Chandler Bing", mode="Confused")`
- `explainShift("col1", "col2", shift, df, character="Manager", mode="Excited")`

---

## 🚀 How to Use

### 🔧 Parameters

- `character`: The persona delivering the output.
- `mode`: The emotional tone of the explanation.

### ✅ Examples

```python
# Krishna calmly explaining correlation shift
explainAITC(df, feature="Correlation", character="Krishna", mode="Zen")

# A sarcastic manager comparing column shifts
explainShift("Sales", "Revenue", 2, df, character="Manager", mode="Sarcastic")

# Chandler Bing being confused by outliers
explainAITC(df, feature="Anomaly", character="Chandler Bing", mode="Confused")

# And other explain Methods too
```

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

---



---

## 🧾 Summary Table

| Feature       | Description                                              |
|---------------|----------------------------------------------------------|
| `character`   | Choose the personality explaining the output             |
| `mode`        | Control the emotion/mood of the response                 |
| API Used      | Together AI - LLaMA 4 Maverick 17B                       |
| Ideal For     | Storytelling, reporting, demo dashboards, Slack bots    |


---



# V 0.3.7 🚀

## 🔧 What's New?

The function `cp.getTotalCorrRelation(df)` just got a **power boost** ⚡ with 2 new optional parameters:

```python
cp.getTotalCorrRelation(df, features=["correlation", "pearson", "distance"], feature="correlation")
```

### 🆕 New Parameters:

- **`features`** *(list)*:  
  Select which statistical relationships you want to calculate:
  - `"correlation"` *(alias for Spearman)*
  - `"pearson"`
  - `"distance"`

- **`feature`** *(string)*:  
  Choose the one you want deeper insights or interpretations on.

---

### 💡 Example Use Case:

```python
cp.getTotalCorrRelation(df, features=["pearson", "distance"], feature="pearson")
```

This gives a table like:

| Feature A | Feature B | Pearson | Distance |
|-----------|------------|---------|----------|

…and all trend-based logic will revolve around **Pearson** here.

---

### 🚀 Performance Boost:

The entire computation logic is now **way more optimized** —  
⚡ From taking **minutes** → now it's done in **seconds**.  
So large datasets won't slow you down anymore.

---

### 🤝 TL;DR
- Use `features` for multiple comparisons.
- Use `feature` for focused interpretation.
- Super fast. Beginner-friendly. One call does it all.

