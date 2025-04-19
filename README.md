# CorrPY - Correlation with Ease

## How to install this library

```cmd
pip install corrpy
```

## Basic Commands

1. Initialization

```python
from corrpy import Corrpy
```

This line imports the main class `Corrpy` which contains the main correlation calculation functionality

2. Using Instance

```python
corrpy = Corrpy()
```

This creates an instance of the `Corrpy` class which can then be used to perform all the correlation calculations

3. Getting Overview

```python
corrpy.getTotalCorrRelation(df)
```

This will return a dataframe that contains the correlation between each column in the dataframe. For now, Corrpy only supports pandas DataFrames

### Demo Result

![alt text](image.png)