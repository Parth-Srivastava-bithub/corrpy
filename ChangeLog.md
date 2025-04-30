
# v 0.3.15

## Added new method `explainAI(result, character="Data analyst", mode="Sarcastic", prompt="Null")`

```python
# Add result and prompt and get your result
  cp.explainAI(result, character = "Data analyst", mode = "Sarcastic", prompt = "Null")

```

## The `prompt` parameter

The `prompt` parameter allows you to provide your own prompt to the AI to generate insights.  
This is a powerful feature that lets you control the output of the AI.  
You can use this to generate insights that are more relevant to your specific use case.

By default, the `prompt` parameter is set to `"Null"`.  
This means that the AI will generate insights based on the default prompt.  
However, you can override this by providing your own prompt.  

The `result` parameter is the output of the method that you want the AI to generate insights about.

For example, if you called `cp.getGroupInf(objColumn, numColumn, df)`, the `result` parameter would be the output of the `getGroupInf` method.  
The AI will then generate insights based on this output.

# v 0.3.13

## Added `prompt` parameter in eacy ai method

## Added `prompt` parameter in eacy ai method

This allows you to provide your own prompt to the AI to generate insights.  
This is a powerful feature that lets you control the output of the AI.  
You can use this to generate insights that are more relevant to your specific use case.

Example:

```python
cp.explainShift("col1", "col2", shift, df, prompt="Explain like obama")

# more methods

cp.explainTransitForColumn(df, prompt = "Explain like alien gonna attack on earth now and you are in hurry")

```

## Or

```python

# A sarcastic manager comparing column shifts
explainShift("Sales", "Revenue", 2, df, character="Manager", mode="Sarcastic")

# Chandler Bing being confused by outliers
explainAITC(df, feature="Anomaly", character="Chandler Bing", mode="Confused")

```


# v 0.3.11 🚀

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

