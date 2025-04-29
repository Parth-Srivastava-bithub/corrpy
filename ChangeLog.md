
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