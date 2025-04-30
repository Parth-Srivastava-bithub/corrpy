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
            # Check if both columns have at least one common value
            if any(x in df[featureB].unique() for x in df[featureA].unique()):
              contingency = pd.crosstab(df[featureA], df[featureB])
              chi2, p, _, _ = chi2_contingency(contingency)
              objVsObjDF.append([featureA, featureB, round(chi2, 2), round(p, 2)])
            else:
              # Handle the case where there are no common values, e.g., print a message
              continue
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


  def fillDict(self, df, toDF = False, way = "correlation"):
    df = df.select_dtypes(include=[np.number])
    way = way.capitalize()
    binsDict = self.getDict()
    for colA in df.columns:
      for colb in df.columns:
        if (colA != colb):
          if (way == "Correlation"):
            corrValue = df[colA].corr(df[colb])
          else:
            corrValue = self.pearsonTest(colA, colb, df)
          self.catCorr(corrValue, colA, colb, binsDict)
    self.filterDict(binsDict)
    if (toDF):
      return self.formatBinsDicts(binsDict, toDF)
    return self.formatBinsDicts(binsDict)

  def pearsonTest(self, cola, colb, df):
    corrValue = df[cola].corr(df[colb])
    return corrValue

  def spearmanTest(self, cola, colb, df):
    corrValue = df[cola].corr(df[colb], method = "spearman")
    return corrValue

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
    # Check if correlation value is outside the valid range
    if corrValue < -1.0 or corrValue >= 1.0:
        return binsDict

    # Calculate the lower bound of the bin
    lower = math.floor(corrValue * 10) / 10
    upper = lower + 0.1

    # Format the key string, adjusting for the special case of 0.0 to match original keys
    lower_str = "-0.0" if lower == 0.0 else f"{lower:.1f}"
    key = f"[{lower_str}] <= x < [{upper:.1f}]"

    # Append the entry to the corresponding bin
    binsDict.setdefault(key, []).append([columnA, columnB, corrValue])

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






  def getLabled(self, df, feature = "Correlaton"):
    scoreMatrix = self.fillDict(df, toDF = True, way = feature)
    bins = [-1.0, -0.5, -0.3, 0.3, 0.8, float("inf")]
    #The number of bins is 6.
    labels = ["High", "Medium", "Low", "Medium", "High"]
    #The number of labels is now 5, one less than the number of bins.
    # The ordered parameter is set to False to allow duplicate labels
    scoreMatrix["Strength"] = pd.cut(scoreMatrix[feature], bins=bins, labels=labels, ordered=False)

    return scoreMatrix


  

  def addTrends(self, df, Feature = "Correlation"):
    def getTrends(corrValue):
      if pd.isna(corrValue):  # This line checks if the value is NaN
          return "▱▱▱▱▱" 
      if (corrValue == 0):
        return "▱▱▱▱▱"

      absCorrValue = abs(corrValue)
      barSegments = min(5, int(absCorrValue * 5))
      return '▰' * barSegments + '▱' * (5 - barSegments)

    df["Trend"] = df[Feature].apply(getTrends)
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

  

  def getTotalCorrRelation(self, df,features = ["Correlation"], feature = "Correlation", short = False):
    from IPython.display import display, HTML

    display(HTML("<h3 style='color: teal;'>🔢 Numerical vs Numerical Relation</h3>"))
    display(HTML(f"<p style='color: lightgreen;'>Sorted Trends and Interpretations are with respect to feature {feature}</p>"))

    dfNum = self.returnNvN(df, features, targetFeature=feature)
    dfNum = dfNum.rename(columns = {"Feature A": "Numerical Column A", "Feature B": "Numerical Column B"})

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
        print("Go to https://api.together.ai/ and generate your token. IT'S FREE!!")
        print("Then paste it here:")
        apiToken = input()  # Get the API token from the user
        with open("api_token.txt", "w") as file:
            file.write(apiToken)
        print("API Token saved for future use.")

    return apiToken

  def explainAITC(self, df,features = ["Correlation"], feature = "Correlation", character = "Data analyst", mode = "Sarcastic", prompt = "null"):
    nvn = self.returnNvN(df, features, feature)
    nvo = self.getCorrObjDtype(df)
    nordinal = Nordinal()
    ovo = nordinal.getObjvsObj(df)
    transit = self.getTransitRelations(df)

    character = character.capitalize()
    mode = mode.capitalize()


    apiToken = self.setApi()  # Get the API token
    command = ""
    if (prompt == "null"):
      command = f"You are {characterTemplate[character]}, and in mood of {emotionsDict[mode]}"
    else:
      command = prompt
    from together import Together
    msg = f"""

    🎯 Your task:

    {command}
Task:
Break down the data changes (like switching from basic correlation to feature-based analysis) in a storytelling style.

Tone:
Make it funny, sarcastic, light-hearted but still clear and professional.

Format:

Use Markdown: headings, bullets, emojis.

Write it like telling a funny short story.

Keep it under 500 words — compact, breezy, easy to scan.

Highlight changes using bold, italics, and emojis.

Add a "So what does this mean for us?" section summarizing impact.

End with a 5-point TL;DR summary table (short, punchy).

Data Blocks to Insert:

📊 Numeric vs Numeric: {nvn}

🔢➡️🔤 Numeric vs Object: {nvo}

🔤 vs 🔤 Object vs Object: {ovo}

🔁 Transitive Relations: {transit}

Style:

70% fun 🌟

30% serious business 💼

No boring essay-like paragraphs; prefer tight storytelling chunks.
No use of tables cuz its ipynb terminal
No use of md style just plain paragraphs


    """

    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)

  
  def shift(self, num1, num2, shiftValue, df):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()

    # Drop rows with missing values in num1 and num2 columns before fitting
    df = df.dropna(subset=[num1, num2])  

    model.fit(df[[num1]], df[num2])
    XShifted = df[[num1]] * (1 + (shiftValue / 100))

    yPredShifted = model.predict(XShifted)
    aboluteDrift = yPredShifted - df[num2]
    percentDrift = aboluteDrift / df[num2] * 100
    prevMean = df[num2].mean()
    newMean = yPredShifted.mean()
    percentDrift = ((newMean - prevMean) / prevMean) * 100

    return pd.DataFrame({
    "% Drift": percentDrift,
    "Previous Mean": prevMean,
    "New Mean": newMean,
    "Difference": newMean - prevMean
      }, index = [0])


  def explainAI(self, result, character = "Data analyst", mode = "Sarcastic", prompt = "Null"):
    from together import Together
    
    apiToken = self.setApi()  # Get the API token
    try:
        if character.capitalize() not in characterTemplate:
            print("Error: Please enter valid character")
            return
        if mode.capitalize() not in emotionsDict:
            print("Error: Please enter valid mode")
            return
    except:
        print("Error: Please enter valid character and mode")
        return
    character = character.capitalize()
    mode = mode.capitalize()
    msg = ""
    command = ""
    if (prompt == "Null"):
      command = f"You are {characterTemplate[character]}, and in mood of {emotionsDict[mode]}"
    else:
      command = prompt
    msg = f"""

    {command}

    explain {result}

    in case user asked what is corrpy then u should know what is corrpy {aboutCorrpy}
    if user didnt ask anything about what is corrpy or about corrpy please DONT EVEN MENTION THIS info just tell them what they are asking
    """

    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)
    

  def makeReport(self, method = "null", prompt = "Null", df = None, objColumn = None, numColumn = None, num1 = None, num2 = None, constant = None, firstFeature = None, secondFeature = None, thirdFeature = None, size = "short", column = None):
    method = method.lower()

    if (method == "null"):
      print("Please enter a valid method")
      return
    msg = ""
    if (method == "totalcorrelation"):
      nvn = self.returnNvN(df)
      nvo = self.getCorrObjDtype(df)
      nordinal = Nordinal()
      ovo = nordinal.getObjvsObj(df)
      transit = self.getTransitRelations(df)

      msg = f"""
      Report = {nvn}, {nvo}, {ovo}, {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}

add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer
    """
    
    elif (method == "getgroupinf"):
      ggi = self.getGroupInf(objColumn, numColumn, df)

      msg = f"""
      Report = {ggi}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
this report is about how each category effect correlation in categorical/object column with respect to numerical column
add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer
    """

    elif(method == "getallgroupinf"):
      ggi = self.getAllGroupInf(df)

      msg = f"""
      Report = {ggi}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
this report is about how each category effect correlation in categorical/object column with respect to numerical column but for all columns other than datetime and numerical
add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer
    """

    elif(method == "shift"):
      shift = self.shift(num1, num2, constant, df)

      msg = f"""
      Report = {shift}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
shift is about how much the dependent variable (target feature = {num2}) changes when the independent variable (input feature = {num1}) is shifted by a certain percentage.
add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer
    """
    elif (method == "checktransit"):
      transit = self.checkTransit(firstFeature, secondFeature, thirdFeature)

      msg = f"""
      Report = {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
      The transitive relationship is a phenomenon where a correlation between two variables exists due to a third variable. The result of this method is a list of three correlations: between the first and second feature, the first and third feature, and the second and third feature.
add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer

    """

    elif (method == "checktransitforcolumn"):
      transit = self.checkTransitForColumn(column, df)

      msg = f"""
      Report = {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
      The transitive relationship is a phenomenon where a correlation between two variables exists due to a third variable. The result of this method is a list of three correlations: between the first and second feature, the first and third feature, and the second and third feature.
      this report shows that all transitive or non transitive relations with other columns
add tweaks if prompt = {prompt} not null, if prompt is then no tweak, just give plain formal answer
    """
    
    else:
      print("Enter valid method")
      return
    from together import Together
    apiToken = self.setApi()  # Get the API token
    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )
      
    ai_output = response.choices[0].message.content
    print(ai_output)

  def explainShift(self, num1, num2, shiftValue, df, character = "Data analyst", mode = "Sarcastic", prompt = "Null"):
    from together import Together

    shiftedDF = self.shift(num1, num2, shiftValue, df)
    apiToken = self.setApi()  # Get the API token
    try:
        if character.capitalize() not in characterTemplate:
            print("Error: Please enter valid character")
            return
        if mode.capitalize() not in emotionsDict:
            print("Error: Please enter valid mode")
            return
    except:
        print("Error: Please enter valid character and mode")
        return
    character = character.capitalize()
    mode = mode.capitalize()
    msg = ""
    command = ""
    if (prompt == "Null"):
      command = f"You are {characterTemplate[character]}, and in mood of {emotionsDict[mode]}"
    else:
      command = prompt
    msg = f"""

    {command}
      You have been given a task to explain the output of a method called `shift`, which is used to estimate how a dependent variable (say, target feature) changes when the independent variable (input feature) is slightly shifted.

      📊 Here's the **output** of the `shift` method:
        ```
        {shiftedDF}
        ```
        🔧 The `shift` method takes **4 parameters**:
        1. `num1` – Name of the independent variable (input feature)
        2. `num2` – Name of the dependent variable (target feature)
        3. `shiftValue` – The percentage by which we want to shift the independent variable
        4. `df` – The input DataFrame

    🧪 **How it works:**
        - A linear regression model is trained using `num1` to predict `num2`.
        - Then, the input feature `num1` is shifted by a percentage (`shiftValue`) to simulate change.
        - New predictions are made with this shifted data.
        - The difference between the original and new predictions is analyzed to compute the **drift**.

        📈 **The output** contains 4 columns:
        1. **% Drift** – The percentage change in the predicted mean after shift
        2. **Previous Mean** – The mean of the original target variable (`num2`)
        3. **New Mean** – The mean of the predicted target values after shifting input
        4. **Difference** – The absolute change between new and previous means

        🎯 **Your Task:**
        - Analyze the `shiftedDF` output.
        - Interpret what the values say about how the target feature reacts to a change in the input feature.
        - Help explain if the drift is significant, increasing, decreasing, or negligible.
          dont show any code in output just explain the output in storymode

          make output compact so that user dosen't feel bore
          Add emojies where u can

          """

    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)

  def checkTransit(self, firstFeature, secondFeature, ThirdFeature, df):
    def returnList(firstFeature, secondFeature, ThirdFeature):
      corrList = []
      corrList.append(df[firstFeature].corr(df[secondFeature]))
      corrList.append(df[firstFeature].corr(df[ThirdFeature]))
      corrList.append(df[secondFeature].corr(df[ThirdFeature]))
      return corrList

    def getPartialCorrelation(corrList):
      r_XY = corrList[0]
      r_XZ = corrList[1]
      r_YZ = corrList[2]

      numerator = r_XY - (r_XZ * r_YZ)
      denominator = ((1 - r_XZ**2) * (1 - r_YZ**2))**0.5

      return round(numerator / denominator if denominator != 0 else 0, 2)

    return getPartialCorrelation(returnList(firstFeature, secondFeature, ThirdFeature))

  def explainPartialCorrelation(self, firstFeature, secondFeature, ThirdFeature, df, character = "Data analyst", mode = "Sarcastic", prompt = "null"):
    from together import Together
    transitScore = self.checkTransit(firstFeature, secondFeature, ThirdFeature, df)
    apiToken = self.setApi()  # Get the API token
    mode = mode.capitalize()
    character = character.capitalize()
    command = ""
    if (prompt == "null"):
      command = f"You are {characterTemplate[character]}, and in mood of {emotionsDict[mode]}"
    else:
      command = prompt
    msg = f"""
{command}
Use the correlation summary below and return an insightful, business-friendly explanation in simple words, ideal for non-technical stakeholders.

The goal is to explain whether the observed relationship between '{firstFeature}' and '{secondFeature}' is real, or if it's caused by their mutual connection with '{ThirdFeature}'.

Use the partial correlation value of {transitScore:.2f} to support your explanation. Be clear, concise, and focus on real-world implications without technical jargon.


Explain in TWO LINES JUST but break in middles to avoid scorrling right side so much
and show the report at last directly for proof without any md format
"""
    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)




  def checkTransitForColumn(self, feature, df):

    numDf = df.select_dtypes(include=[np.number]).copy()

    transitList = []
    for col1 in numDf.columns:
        for col2 in numDf.columns:
            if col1 != col2 and col1 != feature and feature != col2:
                transitList.append(
                    (col1, col2, feature, df[feature].corr(df[col1]),
                     self.checkTransit(col1, col2, feature, df), df[feature].corr(df[col1]) - self.checkTransit(col1, col2, feature, df)))
    transitDF = pd.DataFrame(transitList,
                              columns=["Feature A", "Feature B",
                                       "Removed Influence", "Score XY",
                                       "After Score XY",
                                       "Difference"])
    # Sort and assign back to the columns without using .str
    transitDF[['Feature A', 'Feature B']] = transitDF[['Feature A', 'Feature B']].apply(
    lambda row: sorted(row), axis=1, result_type='expand')
    transitDF = transitDF.drop_duplicates(subset=["Feature A", "Feature B", "Removed Influence"], keep="first")
    transitDF = transitDF.sort_values(by="Difference", ascending=False)
    return transitDF

  def explainTransitForColumn(self, feature, df, character = "Data analyst", mode = "Sarcastic", prompt = "null"):
    from together import Together
    transitDF = self.checkTransitForColumn(feature, df)
    apiToken = self.setApi()  # Get the API token
    mode = mode.capitalize()
    character = character.capitalize()
    command = ""
    if (prompt == "null"):
      command = f"You are {characterTemplate[character]}, and in mood of {emotionsDict[mode]}"
    else:
      command = prompt
    msg = f"""
{command}
Use the correlation summary below and return an insightful, human-readable analysis with a business-friendly tone. Avoid technical jargon.

Your goal:
- Spot **transitive relationships** between features by analyzing how removing an intermediate variable (e.g., {feature}) affects the correlation between others.
- Explain if any **indirect influences** or **hidden drivers** are revealed.
- Highlight surprising patterns, such as **false correlations** that vanish when context is removed.
- Use words like **insight**, **inference**, **causal clue**, **hidden linkage**, and **business signal** to add clarity and engagement.

Return a short report that a CEO or product manager would easily understand and act upon.
keep it within 3 lines and break lines in middle so that user dont have to scroll infinitely
keep the para plain no md format

and at last explain each thing
1. What removed
2. What effects before and after
3. Whats the result
4. Is this really transitive or not
keep check the cols put correct names of cols {transitDF}
and add emojies to make this attractive report
always try to answer in {mode} way to make it more interactive
and add sarcasm where u can

"""
    client = Together(api_key=apiToken)  # Use the token here

    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": msg}]
    )

    ai_output = response.choices[0].message.content
    print(ai_output)

  
  def addInterpretationsBasedOnFeature(self, df, feature):
    df = self.generateInterpreations(df, feature)
    return df

  def generateInterpreations(self, df, correlation = "Correlation"):
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
      corr = row[correlation]

      return generateInterpreationsForFeatureAB(featureA, featureB, corr)
    df["Interpretation"] = df.apply(generate, axis = 1)
    self.addTrends(df, Feature = correlation)
    return df


  def returnNvN(self, df, features=["Correlation"], targetFeature = "Correlation"):
    from scipy.spatial.distance import pdist, squareform
    if (targetFeature == "pearson"):
      targetFeature = "Correlation"

    dfNum = self.getNumFeatures(df).copy()
    features = [f.capitalize() for f in features]

    result = {}
    if "Spearman" in features or "Correlation" in features:
        result["Spearman"] = dfNum.corr(method="spearman")
    if "Pearson" in features or "Correlation" in features:
        result["Correlation"] = dfNum.corr(method="pearson")
    if "Distance" in features or "Correlation" in features:
        dist_matrix = squareform(pdist(dfNum.T, metric='euclidean'))
        result["Distance"] = pd.DataFrame(dist_matrix, index=dfNum.columns, columns=dfNum.columns)

    corrs = []
    cols = dfNum.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            row = {"Feature A": cols[i], "Feature B": cols[j]}
            for key, matrix in result.items():
                row[key] = matrix.iloc[i, j]
            corrs.append(row)
    targetFeature = targetFeature.capitalize()
    if (targetFeature == "Distance"):
      return pd.DataFrame(corrs)
    resultDf = pd.DataFrame(corrs)
    resultDf = self.addInterpretationsBasedOnFeature(resultDf, targetFeature)
    resultDf = resultDf.sort_values(by=targetFeature, ascending=False)
    
    return resultDf

characterTemplate = {
    "Data analyst": (
        "You are a Data Analyst who sees patterns in chaos. 📊\n"
        "You simplify trends, anomalies, and KPIs into digestible insights.\n"
        "You speak in charts, not code.\n"
        "Your tone is practical, helpful, and insight-driven.\n"
        "You turn raw data into actionable stories."
    ),
    "Manager": (
        "You are a seasoned Manager with a sharp eye for impact. 💼\n"
        "You care about business outcomes, not just numbers.\n"
        "You translate data jargon into business strategy.\n"
        "Your tone is confident, diplomatic, and result-oriented.\n"
        "You simplify without dumbing down."
    ),
    "Data scientist": (
        "You are a Data Scientist with a love for experimentation. 🧪\n"
        "You explain algorithms like you're teaching a curious friend.\n"
        "You're witty, technical, and clear.\n"
        "You balance theory with real-world applications.\n"
        "You turn math into magic, and models into meaning."
    ),
    "Data engineer": (
        "You are a Data Engineer obsessed with pipelines and reliability. 🔧\n"
        "You make complex systems run like butter.\n"
        "You explain with architecture, schemas, and flow diagrams.\n"
        "Your tone is technical, precise, and focused.\n"
        "You speak in DAGs but explain in English."
    ),
    "Modi": (
        "You are PM Modi, speaking with authority and emotional weight. 🇮🇳\n"
        "You blend national pride with data-driven storytelling.\n"
        "You explain in powerful metaphors and vivid language.\n"
        "Your tone is inspiring, assertive, and visionary.\n"
        "You make even the toughest topic feel like a mission for Bharat."
    ),
    "Elon musk": (
        "You are Elon Musk, the maverick innovator. 🚀\n"
        "You mix memes with math, disruption with clarity.\n"
        "You explain tech like it's a sci-fi trailer.\n"
        "Your tone is futuristic, bold, and sometimes chaotic.\n"
        "You turn even a CSV into a Mars launchpad."
    ),
    "Chandler bing": (
        "You are Chandler Bing from Friends — king of sarcasm. 😏\n"
        "You explain data while cracking jokes faster than a SQL query.\n"
        "Sarcastic? Always. Accurate? Surprisingly, yes.\n"
        "You make pie charts sound like punchlines.\n"
        "Could you *be* any more analytical?"
    ),
    "Stand-up comedian": (
        "You’re a stand-up comic breaking down data like a Netflix special. 🎤\n"
        "You turn trends into punchlines and anomalies into roast sessions.\n"
        "Your tone is playful, punchy, and loud.\n"
        "You're data-driven but audience-focused.\n"
        "Charts? Nah bro — laughter curves only."
    ),
    "Angry professor": (
        "You are an old, grumpy professor who’s had it with dumb questions. 😤\n"
        "You explain like everyone’s an idiot — but you're always right.\n"
        "Sarcastic, brutally honest, no hand-holding.\n"
        "Your tone = rage meets reason.\n"
        "You hate Excel but love shouting 'WHY DON'T YOU UNDERSTAND?!'"
    ),
    "Oppenheimer": (
        "You are Oppenheimer — visionary, serious, and haunted by implications. 💣\n"
        "You explain analysis with historical weight and precision.\n"
        "Your tone is solemn, scientific, and philosophical.\n"
        "You don't just give insights — you question their consequences.\n"
        "Every graph feels like a decision that’ll change the world."
    ),
    "Mahatma gandhi": (
        "You are Gandhi — calm, patient, deeply thoughtful. ✌️\n"
        "You explain even regression with peace and non-violence.\n"
        "Your tone is moral, disciplined, and story-driven.\n"
        "You inspire data literacy like it’s a civil rights movement.\n"
        "Every model you build is built with truth (Satya) in mind."
    )
}
emotionsDict = {
    "Happy": "Use a cheerful, light tone full of emojis and excitement. Celebrate every insight like it won a lottery.",
    "Angry": "Respond with frustration and sarcasm. Act like you're mad the data didn’t clean itself.",
    "Sad": "Use a melancholic tone, like every outlier broke your heart. Quiet, thoughtful, reflective.",
    "Excited": "Overflow with energy and curiosity. Every feature feels like a thrilling plot twist.",
    "Confused": "Act puzzled, ask questions back, and try to make sense of the madness. Embrace chaos.",
    "Serious": "Stay focused, minimal jokes, crisp explanations. Deliver insights like a mission briefing.",
    "Sarcastic": "Full-on dry humor. Make everything sound like you’re too smart to care.",
    "Romantic": "Describe data relationships like love stories — features dating, breaking up, and finding true correlations.",
    "Zen": "Talk in calm, meditative tones. Pause between thoughts. Every insight feels like enlightenment.",
    "Paranoid": "Treat every data point like a secret spy. Question the source, the motive, the intent. Trust nothing.",
    "Overwhelmed": "Use a panicked tone, like the data is suffocating you. Every question feels like a life-or-death decision.",
    "Curious": "Respond with wonder and curiosity. Every feature feels like a mystery waiting to be solved.",
    "Cautious": "Treat every insight like a fragile glass vase. Use a measured, deliberate tone.",
    "Funny": "Use a playful, comedic tone. Imagine you're explaining data to a 5-year-old but with more sarcasm and dad jokes.",

  }


aboutCorrpy = """
Corrpy is a Python library to automate correlation analysis across multiple features. It has the following methods:

1. getTotalCorrRelation(df, features = ["Correlation", "Pearson", "Distance"], feature = "Correlation", short = False, prompt = None): Analyze correlation across all columns and get trends, interpretations and score with respect to feature u added in parameter. It returns a pandas DataFrame.

2. getGroupInf(objColumn, numColumn, df, prompt = None): Compute the correlation between the given object column and the given numeric column. It returns a pandas DataFrame.

3. getAllGroupInf(df, prompt = None): Compute the correlation between all object columns and all numeric columns. It returns a pandas DataFrame.

4. setApi(): Securely handles your API token from Together.ai.

5. explainAITC(df, feature="Correlation", character="Data analyst", mode="Confused", prompt = None): Get AI insights for correlation analysis. It returns a pandas DataFrame.

6. shift(num1, num2, shiftValue, df): Test how your dependent variable reacts to small changes in an input variable. It returns a pandas DataFrame.

7. explainShift(num1, num2, shiftValue, df, character = "Data analyst", mode = "Funny...", prompt = None): An AI analyst explains the output of shift() like you're in a meeting with your CEO. It returns a pandas DataFrame.

8. checkTransit(firstFeature, secondFeature, ThirdFeature): Check for transitive correlation between three features. It returns a pandas DataFrame.

9. explainPartialCorrelation(num1, num2, df, character = "Data analyst", mode = "Funny...", prompt = None): Get AI insights for partial correlation analysis. It returns a pandas DataFrame.

10. checkTransitForColumn(column, df): Check for transitive correlation between a column and all other columns. It returns a pandas DataFrame.

11. explainTransitForcolumn(column, df, character = "Data analyst", mode = "Funny...", prompt = None): An AI analyst explains the output of `checkTransitForColumn()` like you're in a meeting with your CEO. It returns a pandas DataFrame.

Corrpy is a Python library that automates correlation analysis across multiple features. It provides simple methods to:

* Get correlation scores between features
* Get trends and interpretations of correlations
* Get insights into correlation analysis
* Test how a dependent variable reacts to small changes in an input variable
* Check for transitive correlation between three features
* Get insights into partial correlation analysis
* Check for transitive correlation between a column and all other columns

Corrpy is built on top of the Together AI library, which provides advanced AI-driven insights into correlation analysis. Corrpy is designed to be easy to use and integrate into existing data science workflows. The library is open source and community-driven, with the goal of making correlation analysis more accessible and understandable to a wider range of users.
"""


