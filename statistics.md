

# 🧠 Karl Pearson Correlation – Explained

**What is it?**  
Karl Pearson’s correlation coefficient (r) measures the **linear relationship** between two continuous variables.

**Formula:**  
r = Σ[(xi - x̄)(yi - ȳ)] / √(Σ(xi - x̄)² * Σ(yi - ȳ)²)


**Steps to Calculate:**
1. Compute the mean of X and Y: x̄, ȳ  
2. Subtract the mean from each value: (xi - x̄), (yi - ȳ)  
3. Multiply those deviations for each pair and sum: Σ(xi - x̄)(yi - ȳ)  
4. Square the deviations of X and Y separately and sum: Σ(xi - x̄)², Σ(yi - ȳ)²  
5. Plug into the formula:  
   **r = Σ(xi - x̄)(yi - ȳ) / √[Σ(xi - x̄)² * Σ(yi - ȳ)²]**
   
**Interpretation:**
- r = 1: Perfect positive linear relationship
- r = -1: Perfect negative linear relationship
- r = 0: No linear correlation

**Use Case:**  
Used in statistics and data science to understand how strongly two variables move together.





---

# Partial Dependency
### **Step 1: Our Data Table**
Let’s assume we have the following data for **Study Hours (X)**, **Exam Scores (Y)**, and **Sleep Hours (Z)** for 5 students.

| Student | Study Hours (X) | Exam Scores (Y) | Sleep Hours (Z) |
|---------|-----------------|-----------------|-----------------|
| 1       | 5               | 75              | 6               |
| 2       | 3               | 60              | 5               |
| 3       | 8               | 85              | 7               |
| 4       | 2               | 50              | 4               |
| 5       | 6               | 80              | 6               |

---

### **Step 2: Calculate Pearson Correlations Between the Variables**
First, we calculate the **Pearson correlations** between the pairs of variables.

#### Pearson Correlation between X and Y (\( r_{XY} \)):
This tells us how **Study Hours (X)** and **Exam Scores (Y)** are related.

#### Pearson Correlation between X and Z (\( r_{XZ} \)):
This tells us how **Study Hours (X)** and **Sleep Hours (Z)** are related.

#### Pearson Correlation between Y and Z (\( r_{YZ} \)):
This tells us how **Exam Scores (Y)** and **Sleep Hours (Z)** are related.

Let’s calculate these correlations based on the data.

---

### **Step 3: Remove the Effect of Z (Sleep) from X and Y**

This step involves **controlling for Z**, which means we want to adjust the values of X and Y by removing the influence that Sleep has on them. Essentially, we need to **find the “residuals”** for X and Y after removing the linear effect of Z.

We use the formula for **regression** to compute these residuals, which represent the parts of X and Y that are **not explained by Sleep (Z)**.

The formula to calculate residuals for X and Y after removing the effect of Z is:

Residual_X = X - (r_XZ * Z)

Residual_Y = Y - (r_YZ * Z)

#### **Residuals for X (Study Hours)**:
- For each student, subtract the influence of **Sleep (Z)** on **Study Hours (X)**.

#### **Residuals for Y (Exam Scores)**:
- For each student, subtract the influence of **Sleep (Z)** on **Exam Scores (Y)**.

---

### **Step 4: Calculate the Partial Correlation**

Now, after we’ve removed the influence of Sleep (Z), we can compute the **Partial Correlation** between **Study Hours (X)** and **Exam Scores (Y)** using the residuals. We’ll apply the formula:


r_XY.Z = (r_XY - (r_XZ * r_YZ)) / √[(1 - r_XZ²) * (1 - r_YZ²)]

Let’s walk through this step by step:

---

### **Example Data Calculations**

Let’s calculate the correlations first based on the data.

#### **Step 1: Calculate Pearson Correlations**
Using the table data:

- **r(X, Y) = 0.85** (strong positive relationship between study hours and exam scores)
- **r(X, Z) = 0.55** (moderate positive relationship between study hours and sleep)
- **r(Y, Z) = 0.75** (strong positive relationship between exam scores and sleep)

#### **Step 2: Calculate Residuals for X and Y**

Let’s calculate the residuals for **Study Hours (X)** and **Exam Scores (Y)** after controlling for **Sleep (Z)**.

1. For **Study Hours (X)** residuals:
Residual_X = X - (r_XZ * Z)

- For Student 1: Residual_X = 5 - (0.55 * 6) = 5 - 3.3 = 1.7
- For Student 2: Residual_X = 3 - (0.55 * 5) = 3 - 2.75 = 0.25
- For Student 3: Residual_X = 8 - (0.55 * 7) = 8 - 3.85 = 4.15
- For Student 4: Residual_X = 2 - (0.55 * 4) = 2 - 2.2 = -0.2
- For Student 5: Residual_X = 6 - (0.55 * 6) = 6 - 3.3 = 2.7


So, the **Residuals for X** (Study Hours) are:

| Student | Residual_X (Study Hours) |
|---------|--------------------------|
| 1       | 1.7                      |
| 2       | 0.25                     |
| 3       | 4.15                     |
| 4       | -0.2                     |
| 5       | 2.7                      |

---

2. For **Exam Scores (Y)** residuals:
Residual_Y = Y - (r_YZ * Z)

- For Student 1: Residual_Y = 75 - (0.75 * 6) = 75 - 4.5 = 70.5
- For Student 2: Residual_Y = 60 - (0.75 * 5) = 60 - 3.75 = 56.25
- For Student 3: Residual_Y = 85 - (0.75 * 7) = 85 - 5.25 = 79.75
- For Student 4: Residual_Y = 50 - (0.75 * 4) = 50 - 3 = 47
- For Student 5: Residual_Y = 80 - (0.75 * 6) = 80 - 4.5 = 75.5

So, the **Residuals for Y** (Exam Scores) are:

| Student | Residual_Y (Exam Scores) |
|---------|--------------------------|
| 1       | 70.5                     |
| 2       | 56.25                    |
| 3       | 79.75                    |
| 4       | 47                       |
| 5       | 75.5                     |

---

### **Step 3: Calculate Partial Correlation from Residuals**

Now that we have the **residuals for X** and **residuals for Y**, we can calculate the **Pearson correlation** between these residuals. This gives us the **partial correlation**, which tells us the relationship between **Study Hours (X)** and **Exam Scores (Y)** after removing the effect of **Sleep (Z)**.

You can calculate the **Pearson correlation** between the residuals of **X** and **Y** (just like how you did for any correlation).

---

### **Summary**

1. **Residuals for X (Study Hours)** and **Residuals for Y (Exam Scores)** are calculated by removing the effect of **Sleep (Z)**.
2. After this, we can calculate the **correlation between the residuals**, which gives us the **partial correlation** — the pure relationship between **Study Hours (X)** and **Exam Scores (Y)**, without the influence of **Sleep (Z)**.
3. This is how we control for the effect of an external variable (Z) to better understand the relationship between X and Y.

