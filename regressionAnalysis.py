import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.linear_model import RidgeCV
from sklearn.feature_selection import SelectFromModel
from time import time
from sklearn.feature_selection import SequentialFeatureSelector

