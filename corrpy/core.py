# prompt: import needed libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Example usage (you can remove this if not needed)
# print("Libraries imported successfully")
pd.set_option('display.expand_frame_repr', False)


class Nordinal:
    def __init__(self):
        pass

    def sort_group_by_column(self, df, column):
      df_sorted = df.sort_values(by = column)
      return df_sorted

    def group_bicolumn(self, df, column, target_column):
      bi_df = df[[column, target_column]]
      return bi_df

    def encode_relative_column(self, df, column, relative_column):
      value_dict = df[column].unique()
      ordinal_map = {}
      for i, value in enumerate(value_dict):
        ordinal_map[value] = i
      df[f"{column}_ordinal"] = df[column].map(ordinal_map)
      df = df.reset_index(drop = True)
      df = self.sort_group_by_column(df, relative_column)

      return df


    def check_sparsity(self, df, encoded_column, tolerance = 0.3):
      index_dict = {}
      df = df.reset_index(drop = True)
      for value in df[encoded_column].unique():
        index_dict[value] = list(df[df[encoded_column] == value].index)
      total_gaps = 0
      sparse_cases = 0

      for value, indices in index_dict.items():
        for i in range(1, len(indices)):
          gap = indices[i] - indices[i - 1]
          total_gaps += 1
          if gap > 1:
            sparse_cases += 1

      if total_gaps == 0:
        sparsity_rate = 0
      else:
        sparsity_rate = sparse_cases / total_gaps

      return 1 - sparsity_rate


    def is_ordinal(self, df, relative_column, target_column, tolerance = 0.3):
      df = self.group_bicolumn(df, relative_column, target_column).copy()
      df = self.encode_relative_column(df, target_column, relative_column)
      df = self.sort_group_by_column(df, relative_column)

      return self.check_sparsity(df, f"{target_column}_ordinal", tolerance)

   
    def getObjvsObj(self, df):
      from scipy.stats import chi2_contingency
      dfObj = df.select_dtypes(include=[object]).copy()
      objVsObjDF = []
      for featureA in dfObj.columns:
        for featureB in dfObj.columns:
          if (featureA != featureB):
            contingency = pd.crosstab(df[featureA], df[featureB])
            chi2, p, _, _ = chi2_contingency(contingency)
            objVsObjDF.append([featureA, featureB, round(chi2, 2), round(p, 2)])
      objVsObjDF = pd.DataFrame(objVsObjDF, columns = ["Feature A", "Feature B", "Chi2", "P-Value"])
      return objVsObjDF

class Corrpy:
  def __init__(self):
    pass

  def getDict(self):
    binsDict = {}

    leftLimit = -1.0
    rightLimit = -0.9

    pointer = leftLimit

    while (leftLimit <= 0.9):
      binsDict[f"[{round(leftLimit, 1)}] <= x < [{round(rightLimit, 1)}]"] = []
      leftLimit += 0.1
      rightLimit += 0.1

    return binsDict


  def fillDict(self, df, toDF = False):
    df = df.select_dtypes(include=[np.number])
    binsDict = self.getDict()
    for colA in df.columns:
      for colb in df.columns:
        if (colA != colb):
          corrValue = df[colA].corr(df[colb])
          self.catCorr(corrValue, colA, colb, binsDict)
    self.filterDict(binsDict)
    if (toDF):
      return self.formatBinsDicts(binsDict, toDF)
    return self.formatBinsDicts(binsDict)

  def filterDict(self, binsDict):
    # Create a list of keys to delete to avoid modifying the dictionary during iteration
    keys_to_delete = [key for key in binsDict if not binsDict[key]]
    # Delete the keys after the iteration
    for key in keys_to_delete:
        del binsDict[key]
    return binsDict

  def createBins(self, df):
    df = df.select_dtypes(include=[np.number])
    binsDict = self.getDict()
    for colA in df.columns:
      for colb in df.columns:
        if (colA != colb):
          corrValue = df[colA].corr(df[colb])
          self.catCorr(corrValue, colA, colb, binsDict)
    self.filterDict(binsDict)


    noDuplicateDict = []
    for key, value in binsDict.items():
      noDuplicateDict = [
          [item[0], item[1], round(float(item[2]), 2)] for item in value
      ]

      binsDict[key] = noDuplicateDict

    seen = set()
    uniqueDict = {}
    for key, value in binsDict.items():
      uniqueCorrs = []
      for cola, colb, corr in value:
        sortedKey = tuple(sorted([cola, colb]))
        if (sortedKey not in seen):
          seen.add(sortedKey)
          uniqueCorrs.append([cola, colb, corr])
      uniqueDict[key] = uniqueCorrs


    return uniqueDict


  def catCorr(self, corrValue, columnA, columnB, binsDict):
    if (-1.0 <= corrValue < -0.9):
        binsDict["[-1.0] <= x < [-0.9]"].append([columnA, columnB, corrValue])
    elif (-0.9 <= corrValue < -0.8):
        binsDict["[-0.9] <= x < [-0.8]"].append([columnA, columnB, corrValue])
    elif (-0.8 <= corrValue < -0.7):
        binsDict["[-0.8] <= x < [-0.7]"].append([columnA, columnB, corrValue])
    elif (-0.7 <= corrValue < -0.6):
        binsDict["[-0.7] <= x < [-0.6]"].append([columnA, columnB, corrValue])
    elif (-0.6 <= corrValue < -0.5):
        binsDict["[-0.6] <= x < [-0.5]"].append([columnA, columnB, corrValue])
    elif (-0.5 <= corrValue < -0.4):
        binsDict["[-0.5] <= x < [-0.4]"].append([columnA, columnB, corrValue])
    elif (-0.4 <= corrValue < -0.3):
        binsDict["[-0.4] <= x < [-0.3]"].append([columnA, columnB, corrValue])
    elif (-0.3 <= corrValue < -0.2):
        binsDict["[-0.3] <= x < [-0.2]"].append([columnA, columnB, corrValue])
    elif (-0.2 <= corrValue < -0.1):
        binsDict["[-0.2] <= x < [-0.1]"].append([columnA, columnB, corrValue])
    elif (-0.1 <= corrValue < 0.0):
        binsDict["[-0.1] <= x < [-0.0]"].append([columnA, columnB, corrValue])
    elif (0.0 <= corrValue < 0.1):
        binsDict["[-0.0] <= x < [0.1]"].append([columnA, columnB, corrValue])
    elif (0.1 <= corrValue < 0.2):
        binsDict["[0.1] <= x < [0.2]"].append([columnA, columnB, corrValue])
    elif (0.2 <= corrValue < 0.3):
        binsDict["[0.2] <= x < [0.3]"].append([columnA, columnB, corrValue])
    elif (0.3 <= corrValue < 0.4):
        binsDict["[0.3] <= x < [0.4]"].append([columnA, columnB, corrValue])
    elif (0.4 <= corrValue < 0.5):
        binsDict["[0.4] <= x < [0.5]"].append([columnA, columnB, corrValue])
    elif (0.5 <= corrValue < 0.6):
        binsDict["[0.5] <= x < [0.6]"].append([columnA, columnB, corrValue])
    elif (0.6 <= corrValue < 0.7):
        binsDict["[0.6] <= x < [0.7]"].append([columnA, columnB, corrValue])
    elif (0.7 <= corrValue < 0.8):
        binsDict["[0.7] <= x < [0.8]"].append([columnA, columnB, corrValue])
    elif (0.8 <= corrValue < 0.9):
        binsDict["[0.8] <= x < [0.9]"].append([columnA, columnB, corrValue])
    elif (0.9 <= corrValue < 1.0):
        binsDict["[0.9] <= x < [1.0]"].append([columnA, columnB, corrValue])
    else:
        pass

    return binsDict

  def formatBinsDicts(self, binsDict, toDF = False):
    formattedDict = {}

    for key, value in binsDict.items():
      formattedDictValues = [
          [item[0], item[1], round(float(item[2]), 2)] for item in value
      ]
      formattedDictValues = self.sortBinsDicts(formattedDictValues)
      formattedDict[key] = formattedDictValues

    seen = set()
    uniqueCorrs = []

    for strength, pairs in formattedDict.items():
      for x, y, corr in pairs:
        key = tuple(sorted([x, y]))

        if (key not in seen):
          seen.add(key)
          uniqueCorrs.append((x, y, corr))
    formattedDict = self.sortBinsDicts(uniqueCorrs)
    if (toDF):
      return pd.DataFrame(formattedDict, columns = ["Feature A", "Feature B", "Correlation"])
    return formattedDict

  def sortBinsDicts(self, binsValues):
    def getCorrValue(item):
      return item[2]
    return sorted(binsValues, key = getCorrValue, reverse = True)


  def getValuesFromBin(self, binsDict):
    corrList = []

    for key in binsDict.keys():
      corrlist = []
      for item in binsDict[key]:
        corrlist.append(item[2])
      corrList.append(corrlist)

    return corrList



  def getVarianceInBin(self, array, threshold = 70):
    start = 0
    end = len(array) - 1
    indexList = []
    while (end >= 0):
      if (self.getDifferPercentage(array[end], array[start]) >= threshold):
        indexList.append([start, end, f"Value = {round(self.getDifferPercentage(array[end], array[start]))}"])
        start += 1
      else:
        end -= 1
        start = 0
    return indexList






  def getLabled(self, df):
    scoreMatrix = self.fillDict(df, toDF = True)
    bins = [0, 0.3, 0.8, float("inf")]
    labels = ["Low", "Medium", "High"]
    scoreMatrix["Strength"] = pd.cut(scoreMatrix["Correlation"], bins = bins, labels = labels)
    return scoreMatrix


  def generateInterpreations(self, df):
    def generateInterpreationsForFeatureAB(featureA, featureB, correlation):
      absCorr = abs(correlation)
      direction = '↑' if correlation > 0 else '↓'
      if (correlation > 0 and correlation < 0.7):
        strengthSymbol = "↑"
      elif (correlation < 0 and correlation > -0.7):
        strengthSymbol = "↓"
      elif (correlation > 0.7 and correlation < 0.9):
        strengthSymbol = "↑↑"
      elif (correlation > -0.9 and correlation < -0.7):
        strengthSymbol = "↓↓"
      elif (correlation > 0.9):
        strengthSymbol = "↑↑↑"
      elif (correlation < -0.9):
        strengthSymbol = "↓↓↓"
      else:
        strengthSymbol = "-"

      if (absCorr >= 0.8):
        insight = f"{strengthSymbol} Strong: Direct Driver"
      elif (0.6 <= absCorr < 0.8):
        insight = f"{strengthSymbol} Key Factor but not only Driver"
      elif (0.4 <= absCorr < 0.6):
        insight = f"{direction} Moderate: Linked Trend"
      elif (0.2 <= absCorr < 0.4):
        insight = f"{direction} Weak: Contextual"
      else:
        insight = f"No linkage"
      return insight

    def generate(row):
      featureA = row["Feature A"]
      featureB = row["Feature B"]
      corr = row["Correlation"]

      return generateInterpreationsForFeatureAB(featureA, featureB, corr)
    df["Interpretation"] = df.apply(generate, axis = 1)
    self.addTrends(df)
    return df

  def addTrends(self, df):
    def getTrends(corrValue):
      absCorrValue = abs(corrValue)
      barSegments = min(5, int(absCorrValue * 5))
      return '▰' * barSegments + '▱' * (5 - barSegments)

    df["Trend"] = df["Correlation"].apply(getTrends)
    return df

  def getNumFeatures(self, df):
    dfNum = df.select_dtypes(include=[np.number])
    return dfNum

  def getCorrObjDtype(self, df):
    dfObj = df.select_dtypes(include=[object]).copy()
    dfNum = df.select_dtypes(include=[np.number]).copy()

    nordinal = Nordinal()
    objNumCorr = {}
    for colA in dfObj.columns:
      for colB in dfNum.columns:
        featureA = colA
        featureB = colB
        corrValue = nordinal.is_ordinal(df, featureB, featureA)
        objNumCorr[(featureA, featureB)] = round(corrValue, 2)
    data = [(a, b, corr) for (a, b), corr in objNumCorr.items()]

    objCorrNum = pd.DataFrame(data, columns = ["Feature A", "Feature B", "Correlation"])
    objCorrNum = objCorrNum.sort_values(by='Correlation', ascending=False)
    objCorrNum = self.generateInterpreations(objCorrNum)
    objCorrNum = self.addTrends(objCorrNum)
    return objCorrNum


  def getTotalCorrRelation(self, df, short = False):
    from IPython.display import display, HTML

    display(HTML("<h3 style='color: teal;'>🔢 Numerical vs Numerical Relation</h3>"))
    dfNum = self.generateInterpreations(self.getLabled(self.getNumFeatures(df).copy()))
    if (short):
      print(dfNum.head())
    else:
      print(dfNum)

    display(HTML("<h3 style='color: purple;'>🧠 Object vs Numerical Relation</h3>"))
    dfObj = self.getCorrObjDtype(df)
    dfObj = dfObj.rename(columns = {"Feature A": "Object Column", "Feature B": "Numerical Column"})
    if (short):
      print(dfObj.head())
    else:
      print(dfObj)
    
    display(HTML("<p style='color: red;'>These correlations show there's some link, but not whether it's positive or negative. Just a heads-up, not a verdict</p>"))

    nordinal = Nordinal()
    objVsObjScore = nordinal.getObjvsObj(df)
    # sort on basis of Chi2 column
    objVsObjScore = objVsObjScore.sort_values(by='Chi2', ascending=False)
    display(HTML("<h3 style='color: green;'>📊 Object vs Object Relation</h3>"))
    objVsObjScore = objVsObjScore.drop(objVsObjScore.index[1::2])
    if (short):
      print(objVsObjScore.head())
    else:
      print(objVsObjScore)

    display(HTML("<h3 style='color: lightblue;'>⌚ Time vs Numerical Relation</h3>"))
    dfTime = self.getTimeNumCorr(df)
    dfTime = dfTime.rename(columns = {"Feature A": "DateTime Column", "Feature B": "Numerical Column", "Correlation": "Correlation Score"})
    if (short):
      print(dfTime.head())
    else:
      print(dfTime)

    display(HTML("<h3 style='color: orange;'>⌚ Time vs Object Relation</h3>"))
    dfTimeObj = self.getTimeObjCorr(df)
    dfTimeObj = dfTimeObj.rename(columns = {"Feature A": "DateTime Column", "Feature B": "Object Column", "Correlation": "Correlation Score"})
    if (short):
      print(dfTimeObj.head())
    else:
      print(dfTimeObj)

    display(HTML("<h3 style='color: crimson;'>⚠️ Transitive Relation Alert</h3>"))
    transitDF = pd.DataFrame(self.getTransitRelations(df), columns = ["Feature A", "Feature B", "Feature C"])
    if (short):
      print(transitDF.head())
    else:
      print(transitDF)





  def getMatrixByKey(self, bins, key):
    return bins[key]

  def findTransitInMatrix(self, matrix):
    counter = 0
    transitList = []
    for row in matrix:
      item = row[0]
      transitList.append(self.findInMatrix(matrix, item, counter, 0))
      item = row[1]
      transitList.append(self.findInMatrix(matrix, item, counter, 1))
      counter += 1
    return transitList
  def findInMatrix(self, matrix, item, rowId, current):
    itemList = []
    for i in range(0, len(matrix)):
      if (i != rowId):
        if (matrix[i][0] == item):
          if (current == 0):
            itemList.append((matrix[i][1], item, matrix[rowId][1]))
          else:
            itemList.append((item, matrix[i][0], matrix[rowId][0]))
        elif (matrix[i][1] == item):
          if (current == 1):
            itemList.append((matrix[i][0], item, matrix[rowId][0]))
          else:
            itemList.append((item, matrix[i][1], matrix[rowId][1]))

    return itemList

  def findTransit(self, bins):
    transitRelations = []
    for key in bins.keys():
      transitRelations.extend(self.findTransitInMatrix(self.getMatrixByKey(bins, key)))  # Extend instead of append
    return transitRelations

  def getTransitRelations(self, df):

    transitList = self.findTransit(self.createBins(df))
    # Convert nested lists to tuples before adding to the set
    # Additionally, sort inner tuples to treat relations as equal regardless of order
    unique_relations = set()
    for outer in transitList:
      for sub in outer:  # Removed extra layer
        if sub:
          unique_relations.add(tuple(sorted(sub)))  # Sort inner tuples before adding


    listOfSet = list(unique_relations)

    for row in listOfSet[:]:
      if (row[0] == row[1] or row[1] == row[2] or row[0] == row[2]):
        listOfSet.remove(row)
    return listOfSet


  def getTimeNumCorr(self, df):
    df = df.copy()
    dfNum = df.select_dtypes(include = [np.number])
    # time series data
    dfTime = df.select_dtypes(include=['datetime64'])
    corrs = []
    for t_col in dfTime.columns:
      for n_col in dfNum.columns:
        corrs.append((t_col, n_col, dfTime[t_col].corr(dfNum[n_col])))
    corrsDf = pd.DataFrame(corrs, columns=["Feature A", "Feature B", "Correlation"])
    corrsDf = corrsDf.sort_values(by='Correlation', ascending=False)
    corrDf = self.generateInterpreations(corrsDf)
    corrDf = self.addTrends(corrDf)
    return corrsDf

  def getTimeObjCorr(self, df):
    df = df.copy()
    dfTime = df.select_dtypes(include=['datetime64'])
    dfObj = df.select_dtypes(include=[object])
    corrs = []

    for col in dfTime.columns:
      dfTime[col] = dfTime[col].astype('int64')

    for col in dfObj.columns:
      dfObj[col] = pd.Categorical(dfObj[col]).codes

    for t_col in dfTime.columns:
      for o_col in dfObj.columns:
        corrs.append((t_col, o_col, dfTime[t_col].corr(dfObj[o_col])))

    corrDf = pd.DataFrame(corrs, columns=["Feature A", "Feature B", "Correlation"])
    corrDf = corrDf.sort_values(by='Correlation', ascending=False)
    corrDf = self.generateInterpreations(corrDf)
    corrDf = self.addTrends(corrDf)
    return corrDf
  def getGroupInf(self, objColumn, numColumn, df):
    dummies = pd.get_dummies(df[objColumn])
    df = pd.concat([df, dummies], axis = 1)
    dfDummies = pd.concat([dummies, df[numColumn]], axis=1)
    correlations = dfDummies.corr()[numColumn].drop(numColumn)

    return correlations
  
  def getAllGroupInf(self, df):
        df = df.copy()
        
        # Separate the object and numerical columns
        dfObj = df.select_dtypes(include=[object])
        dfNum = df.select_dtypes(include=[np.number])

        # Loop through all object and numerical columns and get correlation
        for objCol in dfObj.columns:
            for numCol in dfNum.columns:
                # Get the correlation values
                dfGroup = self.getGroupInf(objCol, numCol, df)
                
                # Convert the correlation series to a DataFrame with 'category' and 'score' columns
                temp_df = pd.DataFrame(dfGroup).reset_index()
                temp_df.columns = ['Category', 'Correlation']  # Rename the columns
                temp_df = temp_df.sort_values(by =  "Correlation", ascending=False)
                temp_df = self.addTrends(temp_df)
                temp_df = temp_df.reset_index(drop=True)

                # Print the DataFrame for each category (separate DataFrames for each)
                print(f"Correlation between {objCol} and {numCol}:")
                print(temp_df)
  def explain(self, func_name):
    docs = {
        "getTotalCorrRelation": (
            "🔍 **getTotalCorrRelation** runs full-scale correlation analysis on all column types:\n"
            "• 🔢 Numerical vs Numerical\n"
            "• 🧠 Object vs Numerical\n"
            "• 🕒 Time-based patterns\n"
            "• ⚠️ Transitive (indirect) relations\n\n"
            "Output includes: Correlation Score, Strength, Interpretation & Trend bar.\n"
            "📘 Terms explained here → https://github.com/Parthdsaiml/corrpy?tab=readme-ov-file#explanation-of-terms-in-correlation-analysis"
        ),

        "getGroupInf": (
            "🧠 **getGroupInf(obj_col, num_col, df)** shows how each category inside `obj_col` affects `num_col` individually.\n"
            "Use it to break down correlations category-wise.\n\n"
            "📊 Example:\n"
            "Correlation between obj_col1 and num_col1:\n"
            "  Category  Correlation  Trend\n"
            "0        C     0.05       ▱▱▱▱▱\n"
            "1        B     0.01       ▱▱▱▱▱\n"
            "2        A    -0.06       ▱▱▱▱▱\n"
            "📘 Terms explained here → https://github.com/Parthdsaiml/corrpy?tab=readme-ov-file#get-to-know-how-each-cateogry-effect-correlation-with-other-numeric-values"

        ),

        "getAllGroupInf": (
            "📊 **getAllGroupInf(df)** auto-applies `getGroupInf` on all combinations of object ↔ numeric columns.\n"
            "Useful when you don’t want to check each manually.\n"
            "Returns grouped correlations for every pair like:\n"
            "• obj_col1 vs num_col1, num_col2, etc.\n"
            "• obj_col2 vs num_col1, num_col2, etc. \n"
            "Please Enter 'getGroupInf' also to get detail explanation\n"
            "📘 Terms explained here → https://github.com/Parthdsaiml/corrpy?tab=readme-ov-file#get-to-know-how-each-cateogry-effect-correlation-with-other-numeric-values"
        )
    }

    print(docs.get(func_name, "❓ No explanation found for this method."))


  def setApi(self):
    import os

    # Check if API token is saved already
    if os.path.exists("api_token.txt"):
        with open("api_token.txt", "r") as file:
            apiToken = file.read().strip()
        print("API Token loaded from file.")
        return apiToken

    print("Do You Have API Token (y/n)?")
    flag = input()

    if (flag.lower() == "y"):
        apiToken = input("Please paste your API token here: ")
        with open("api_token.txt", "w") as file:
            file.write(apiToken)
        print("API Token saved for future use.")
    else:
        print("Go to https://www.together.ai/ and generate your token. IT'S FREE!!")
        print("Then paste it here:")
        apiToken = input()  # Get the API token from the user
        with open("api_token.txt", "w") as file:
            file.write(apiToken)
        print("API Token saved for future use.")

    return apiToken

  def explainAITC(self, df):
    nvn = self.getLabled(self.getNumFeatures(df))
    nvo = self.getCorrObjDtype(df)
    nordinal = Nordinal()
    ovo = nordinal.getObjvsObj(df)
    transit = self.getTransitRelations(df)
    
    apiToken = self.setApi()  # Get the API token

    from together import Together
    msg = f"""
    🧠 You are a skilled data analyst ai agent.
    Use the correlation summary below and return an insightful, business-friendly explanation in simple words, ideal for non-technical stakeholders.

    🧾 Here’s the insight summary:

    📊 Numeric vs Numeric: {nvn}

    🔢➡️🔤 Numeric vs Object: {nvo}

    🔤 vs 🔤 Object vs Object: {ovo}

    🔁 Transitive Relations: {transit}

    🎯 Your task:

    Break it down like you're explaining to a curious manager.

    Use Markdown, large paragraphs, bullet points, and emojis.
    Use Story Telling way of explaining reports. 
    Keep it under 500 words.

    Make it friendly, clear, and actionable.

    Add a short “So what does this mean for us?” section at the end.
    
    """

    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)

  











