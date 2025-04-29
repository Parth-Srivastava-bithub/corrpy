
# V 0.3.7 🚀

## 🔧 What's New?

The function `cp.getTotalCorrRelation(df)` has been upgraded with **2 new optional parameters**:

```python
cp.getTotalCorrRelation(df, features=["correlation", "pearson", "distance"], feature="correlation")
```

### 🆕 New Parameters:

- **`features`** *(list)*:  
  Choose which statistical relationships you want to calculate.  
  Options include:
  - `"correlation"` *(alias for Spearman)*
  - `"pearson"`
  - `"distance"`

- **`feature`** *(string)*:  
  Pick one test from the list above for deeper insights and trend interpretations.

### 💡 Example Use Case:

```python
cp.getTotalCorrRelation(df, features=["pearson", "distance"], feature="pearson")
```

This gives you a DataFrame with:
- `Feature A`, `Feature B`
- Pearson values
- Distance values  
...and focuses analysis around **Pearson** correlation.

### 🤝 TL;DR
Want multiple insights at once? Use `features`.  
Want to focus analysis on one? Use `feature`.

*No more confusion, just clean comparisons.* ✅
