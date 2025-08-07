# prompt: import needed libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from google import generativeai as genai
import os
from pathlib import Path
from collections import deque
import IPython.display as display
from IPython.display import HTML, Markdown
from lingam import DirectLiNGAM
from itertools import combinations
# Example usage (you can remove this if not needed)
# print("Libraries imported successfully")
pd.set_option('display.expand_frame_repr', False)

class Memory:
  def __init__(self):
    self.memory_file = Path.home() / ".corrpy_memory.txt"
    self.memory_size = 50  # Keep last 50 interactions
    self._initialize_memory()

  def _initialize_memory(self):
    """Initialize or load memory file"""
    if not self.memory_file.exists():
      self.memory_file.touch()
    self.memory = self._load_memory()
  
  def _load_memory(self):
    """Load last N lines from memory file"""
    try:
      with open(self.memory_file, 'r') as f:
        return deque(f.readlines()[-self.memory_size:], maxlen=self.memory_size)
    except:
      return deque(maxlen=self.memory_size)


      
  def _update_memory(self, prompt, response):
    """Store interaction in memory"""
    entry = f"User: {prompt}\nAI: {response}\n\n"
    self.memory.append(entry)
    with open(self.memory_file, 'a') as f:
      f.write(entry)
  
  def _get_memory_context(self):
    """Get recent memory as context"""
    return "Previous interactions:\n" + "".join(self.memory) if self.memory else "" 



class SetAPI:
    def __init__(self, apiToken=None):
        self.apiToken = apiToken
        self.model = None
        self.configured = False

    def setAPI(self):
        if os.path.exists("api_token.txt"):
            with open("api_token.txt", "r") as file:
                self.apiToken = file.read().strip()
            print("API Token loaded from file.")
            return self.apiToken

        print("Do You Have API Token (y/n)?")
        flag = input()

        if flag.lower() == "y":
            self.apiToken = input("Please paste your API token here: ")
        else:
            print("Go to https://aistudio.google.com/ and generate your API token. IT'S FREE!!")
            print("Then paste it here:")
            self.apiToken = input()

        with open("api_token.txt", "w") as file:
            file.write(self.apiToken)
        print("API Token saved for future use.")
        return self.apiToken

    def _configure_api(self):
        try:
            if not self.apiToken:
                raise ValueError("Missing API Key")

            genai.configure(api_key=self.apiToken)
            self.model = genai.GenerativeModel("gemini-2.0-flash-lite")
            self.configured = True
        except Exception as e:
            print(f"Error configuring API: {str(e)}")
            self.configured = False

    def get_model(self):
        if not self.configured:
            self._configure_api()
        return self.model


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
     self.model = genai.GenerativeModel("gemini-2.0-flash-lite")

  def changeAPI(self, api_token):
    api_handler = SetAPI(api_token)
    model = api_handler.get_model()
    return model

  def getDict(self):
    binsDict = {}

    leftLimit = -1.0
    rightLimit = -0.9

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


  def getGroupInf(self, objColumn, numColumn, df, sort = False):
    dummies = pd.get_dummies(df[objColumn])
    df = pd.concat([df, dummies], axis = 1)
    dfDummies = pd.concat([dummies, df[numColumn]], axis=1)
    correlations = dfDummies.corr()[numColumn].drop(numColumn)
    if (sort):
      correlations = correlations.sort_values(ascending=False)
    return correlations

  def getAllGroupInf(self, df, sort = False):
    df = df.copy()

    # Separate the object and numerical columns
    dfObj = df.select_dtypes(include=[object])
    dfNum = df.select_dtypes(include=[np.number])

    # Loop through all object and numerical columns and get correlation
    for objCol in dfObj.columns:
      for numCol in dfNum.columns:
        # Get the correlation values
        dfGroup = self.getGroupInf(objCol, numCol, df, sort)

        # Convert the correlation series to a DataFrame with 'category' and 'score' columns
        temp_df = pd.DataFrame(dfGroup).reset_index()
        temp_df.columns = ['Category', 'Correlation']  # Rename the columns
        temp_df = temp_df.sort_values(by =  "Correlation", ascending=False)
        temp_df = self.addTrends(temp_df)
        temp_df = temp_df.reset_index(drop=True)

        # Print the DataFrame for each category (separate DataFrames for each)
        print(f"Correlation between {objCol} and {numCol}:")
        print(temp_df)

  
  def explainTC(self, df,features = ["Correlation"], feature = "Correlation", prompt = "null"):
    nvn = self.returnNvN(df, features, feature)
    nvo = self.getCorrObjDtype(df)
    nordinal = Nordinal()
    ovo = nordinal.getObjvsObj(df)
    transit = self.getTransitRelations(df)

    

    command = ""
    if (prompt == "null"):
      command = "You are Data analyst, and in mood of Sarcastic"
    else:
      command = prompt
 
    msg = f"""

    🎯 Your task:

    {command}
    Task:
    Break down the data changes (like switching from basic correlation to feature-based analysis) in a storytelling style.

    Tone:
    Make it funny, sarcastic, light-hearted but still clear and professional.

    Format:


    Write it like telling a funny short story in plain form no markdown or decorators.

    Keep it under 500 words — compact, breezy, easy to scan.

    Highlight changes using emojis.

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

    Remove any line from previous interactions that contains a unicode character
    



    """
    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()   
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())
    from IPython.display import Markdown, display 
    display(Markdown(ai_response))
    
    

  
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


  def explain(self, result, prompt = "Null"):
    
    msg = ""
    command = ""
    if (prompt == "Null"):
      command = "You are Data analyst, and in mood of Sarcastic"
    else:
      command = prompt
    msg = f"""

    {command}

    explain {result}
    
    """
    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())

    from IPython.display import Markdown, display 
    display(Markdown(ai_response))
    

  def makeReport(self, method="null", df=None, column=None, feature=None, target=None, prompt="formal", size="short", constant=None, first=None, second=None, third=None):
    method = method.lower()

    if method == "null":
        print("Please enter a valid method")
        return

    msg = ""

    if method == "totalcorrelation":
        nvn = self.returnNvN(df)
        nvo = self.getCorrObjDtype(df)
        nordinal = Nordinal()
        ovo = nordinal.getObjvsObj(df)
        transit = self.getTransitRelations(df)

        msg = f"""
        Report = {nvn}, {nvo}, {ovo}, {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    elif method == "getgroupinf":
        ggi = self.getGroupInf(column, target, df)

        msg = f"""
        Report = {ggi}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
this report is about how each category affects correlation in categorical/object column with respect to numerical column.
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    elif method == "getallgroupinf":
        ggi = self.getAllGroupInf(df)

        msg = f"""
        Report = {ggi}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
This report is about how each category affects correlation in all object columns (except datetime/numerical) with respect to numerical columns.
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    elif method == "shift":
        shift = self.shift(feature, target, constant, df)

        msg = f"""
        Report = {shift}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
This report shows how much the dependent variable (target = {target}) changes when the independent variable (feature = {feature}) is shifted by a certain percentage.
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    elif method == "checktransit":
        transit = self.checkTransit(first, second, third, df)

        msg = f"""
        Report = {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
The transitive relationship is where a correlation between two variables exists due to a third variable. This result includes correlations between {first}-{second}, {first}-{third}, and {second}-{third}.
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    elif method == "checktransitforcolumn":
        transit = self.checkTransitForColumn(column, df)

        msg = f"""
        Report = {transit}
Generate a human-like, well-written paragraph suitable for direct pasting into a PowerPoint slide. Avoid markdown, bullet points, or formatting—just plain, presentation-friendly text that sounds natural and engaging
size should be {size}
also {prompt} way
This report shows all transitive/non-transitive relationships of '{column}' with other columns based on correlation.
answer while breaking the lines, dont give one loooong line answer 
dont ever print this "If the prompt is "show data on which u r explaining things not null", then the answer will be " or anything comes close to this, dont tell them internal part just tell them what they are asking
        """

    else:
        print("Enter valid method")
        return

    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())

    from IPython.display import Markdown, display 
    display(Markdown(ai_response))


 

  def explainShift(self, num1, num2, shiftValue, df, prompt = "Null"):

    shiftedDF = self.shift(num1, num2, shiftValue, df)
    
    msg = ""
    command = ""
    if (prompt == "Null"):
      command = "You are Data analyst, and in mood of Sarcastic"
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

    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())

    from IPython.display import Markdown, display 
    display(Markdown(ai_response))


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

  def explainTransit(self, firstFeature, secondFeature, ThirdFeature, df, prompt = "null"):
    transitScore = self.checkTransit(firstFeature, secondFeature, ThirdFeature, df)
    command = ""
    if (prompt == "null"):
      command = "You are Data analyst, and in mood of Sarcastic"
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
    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())

    from IPython.display import Markdown, display 
    display(Markdown(ai_response))




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

  def explainTransitForColumn(self, feature, df, prompt = "null"):
    transitDF = self.checkTransitForColumn(feature, df)
    command = ""
    if (prompt == "null"):
      command = "You are Data analyst, and in mood of Sarcastic"
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
always try to answer in way to make it more interactive
and add sarcasm where u can

"""
    api_handler = SetAPI()
    api_handler.setAPI()
    model = api_handler.get_model()
    memory = Memory()
    full_prompt = msg + ''.join([line for line in memory._get_memory_context().splitlines(True) if '\u2728' not in line])
    response = model.generate_content(full_prompt)
    ai_response = response.text.strip()
    try:
        memory._update_memory(prompt, ai_response)
    except UnicodeEncodeError:
        memory._update_memory(prompt, ai_response.encode('ascii', errors='ignore').decode())

    from IPython.display import Markdown, display 
    display(Markdown(ai_response))

  
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
  
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from itertools import combinations
from lingam import DirectLiNGAM
from scipy import stats

class EnhancedCorrPy:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def preprocess_data(self, df):
        """Enhanced data preprocessing"""
        # Handle missing values
        df = df.dropna()
        
        # Remove constant columns
        df = df.loc[:, df.nunique() > 1]
    
        # Process only numerical columns
        num_cols = df.select_dtypes(include=[np.number]).columns
    
        # Winsorize outliers (1st and 99th percentiles)
        for col in num_cols:
            df[col] = df[col].clip(
            lower=df[col].quantile(0.01),
            upper=df[col].quantile(0.99)
        )
    
        # Check non-Gaussianity only for numerical columns
        for col in num_cols:
            skew_val = stats.skew(df[col])
            kurt_val = stats.kurtosis(df[col])
            if abs(skew_val) < 0.5 and abs(kurt_val) < 1:
                print(f"Warning: {col} appears Gaussian (skew={skew_val:.2f}, kurt={kurt_val:.2f})")
    
        return df

    def infer_causal_direction(self, A, B, n_bootstrap=50):
        """Improved causal inference with bootstrapping"""
        try:
            # Bootstrap stability check
            a_to_b_vals = []
            b_to_a_vals = []
            
            for _ in range(n_bootstrap):
                sample_idx = np.random.choice(len(A), size=len(A), replace=True)
                A_sample = A.iloc[sample_idx].values
                B_sample = B.iloc[sample_idx].values
                
                model = DirectLiNGAM()
                model.fit(np.column_stack((A_sample, B_sample)))
                adj_matrix = model.adjacency_matrix_
                
                a_to_b_vals.append(abs(adj_matrix[1, 0]))
                b_to_a_vals.append(abs(adj_matrix[0, 1]))
                
            # Calculate confidence intervals
            a_to_b_mean = np.mean(a_to_b_vals)
            b_to_a_mean = np.mean(b_to_a_vals)
            a_to_b_std = np.std(a_to_b_vals)
            b_to_a_std = np.std(b_to_a_vals)
            
            # Significance threshold (2 sigma)
            if (a_to_b_mean - 2*a_to_b_std) > (b_to_a_mean + 2*b_to_a_std):
                return 1, a_to_b_mean
            elif (b_to_a_mean - 2*b_to_a_std) > (a_to_b_mean + 2*a_to_b_std):
                return -1, b_to_a_mean
            else:
                return 0, max(a_to_b_mean, b_to_a_mean)
                
        except Exception as e:
            print(f"LiNGAM failed on {A.name} vs {B.name}: {str(e)}")
            return 0, 0

    def build_causal_graph(self, df):
      """Build causal graph with enhanced transitive reduction"""
      df = self.preprocess_data(df)
      numeric_cols = df.select_dtypes(include=[np.number]).columns
    
      # Clear existing graph
      self.graph = nx.DiGraph()
    
      # Phase 1: Initial edge detection
      for cola, colb in combinations(numeric_cols, 2):
        if cola == colb:
            continue
        corr = df[cola].corr(df[colb])
        if abs(corr) < 0.2:  # More stringent correlation threshold
            continue
            
        direction, strength = self.infer_causal_direction(df[cola], df[colb])
        
        if direction == 1:
            self.graph.add_edge(cola, colb, weight=strength, correlation=corr)
        elif direction == -1:
            self.graph.add_edge(colb, cola, weight=strength, correlation=corr)

      # Phase 2: Network refinement
      self._remove_weak_edges(threshold=0.1)
      self._reduce_transitive_edges()
    
      return self.graph

    def _remove_weak_edges(self, threshold=0.1):
        """Remove edges with low causal strength"""
        to_remove = [(u, v) for u, v, d in self.graph.edges(data=True) 
                    if d['weight'] < threshold]
        self.graph.remove_edges_from(to_remove)
        
    def _reduce_transitive_edges(self):
      """Improved transitive reduction using networkx algorithm"""
      try:
        import networkx as nx
        if not nx.is_directed_acyclic_graph(self.graph):
            # If graph is not a DAG, we need to make it one
            # This is a simple approach - you might need more sophisticated cycle handling
            self.graph = nx.DiGraph([(u, v) for u, v in self.graph.edges() if u != v])
        self.graph = nx.algorithms.dag.transitive_reduction(self.graph)
      except Exception as e:
        print(f"Warning: Could not perform transitive reduction: {str(e)}")
    
    def plot_interactive_graph(self):
        """Create interactive plot using Plotly"""
        pos = nx.spring_layout(self.graph, seed=42)
        
        edge_x = []
        edge_y = []
        edge_text = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_text.append(
                f"{edge[0]} → {edge[1]}<br>"
                f"Strength: {self.graph.edges[edge]['weight']:.2f}<br>"
                f"Correlation: {self.graph.edges[edge]['correlation']:.2f}"
            )

        node_x = [pos[k][0] for k in pos]
        node_y = [pos[k][1] for k in pos]
        node_text = list(pos.keys())

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#888'),
            hoverinfo='text',
            text=edge_text,
            mode='lines')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=25,
                color=[],
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                      )
        
        fig.show()

# Usage example
df = pd.read_csv("corrpy/Titanic-Dataset.csv")
analyzer = EnhancedCorrPy()
G = analyzer.build_causal_graph(df)
analyzer.plot_interactive_graph()