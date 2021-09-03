import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


import statsmodels.api as sm
from scipy.stats import spearmanr, pearsonr, shapiro

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
import shap

from sklearn.metrics import roc_auc_score, confusion_matrix, plot_roc_curve,\
    plot_confusion_matrix, recall_score, precision_score, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_selection import SequentialFeatureSelector
import random
from datetime import datetime, date

def select_features(model, n_features, y, X, scoring=None):
    results = []
    for n in range(1, n_features):
        print(f'Running for {n} features')
        cv = KFold(n_splits=5, shuffle=False)  # Note - we want to check stability over time, do not shuffle
        selector = SequentialFeatureSelector(n_features_to_select=n, n_jobs=-1, direction='forward', cv=cv,
                                             estimator=model,
                                             scoring=scoring
                                             )
        selector.fit(X, y)
        support = selector.get_support()
        features = list(X.columns[support])

        print(f'Selected features: {features}')
        X_selected = X[features]
        score = cross_val_score(model, X_selected, y, cv=cv, scoring=scoring)
        print(f'Fit summary: {np.mean(score)} ({min(score)} to {max(score)})')
        results.append({'n': n, 'cv_score': np.mean(score), 'features': features})

    return pd.DataFrame(results)


def split_train_test(data, predictors, target, shuffle=True, test_size=0.3):
    '''target/predictors split, scaling, train/test split'''
    target = [target]
    X = data[predictors]
    y = data[target]

    X_train, X_eval, y_train, y_eval = train_test_split(X, y, test_size=test_size, random_state=1992, shuffle=shuffle)

    return (X_train, X_eval, y_train, y_eval)



def plot_histogram(feature_name, df):
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    sns.histplot(x=feature_name, data=df, ax=ax[0])
    ax[0].set_title(
        f"{feature_name} has \n mean {round(df[feature_name].mean(), 1)}, stdev {round(df[feature_name].std(), 1)}, CV is {round(df[feature_name].std() / df[feature_name].mean(), 1)}")
    try:
        pp = sm.ProbPlot(df[feature_name], fit=True)
    except RuntimeError:
        print(f"Dropped {df[feature_name].isna().sum()} missing observations")
        df = df.loc[df[feature_name].notnull()]
        pp = sm.ProbPlot(df[feature_name], fit=True)

    qq = pp.qqplot(marker='.', markerfacecolor='#0597E4', markeredgecolor='#0597E4', alpha=1, ax=ax[1])
    sm.qqline(qq.axes[1], line='45', fmt='k--')

    stat, p = shapiro(df[feature_name])
    alpha = 0.05

    if p > alpha:
        ax[1].set_title(f"{feature_name} \n is Normal")
    else:
        ax[1].set_title(f"{feature_name} \n is NOT Normal")

    plt.tight_layout()

def plot_shap_metrics(model, data, predictors, target, shuffle=True, export_dir=None):
    '''running models on predictors'''

    cv = KFold(shuffle=shuffle, n_splits=5, random_state=111)
    X_all = data[predictors]
    y_all = data[[target]]
    y_evals = None

    # For covariance only - use all data
    scaler = StandardScaler()
    scaler.fit(X_all)
    masker = shap.maskers.Impute(data=scaler.transform(X_all))

    shap_values = None
    shap_x_indexes = None

    for train_index, eval_index in cv.split(X_all):
        X_train, X_eval = X_all.iloc[train_index], X_all.iloc[eval_index]
        y_train, y_eval = y_all.iloc[train_index], y_all.iloc[eval_index]

        pipe = Pipeline([
            ('standard_scaling', StandardScaler()),
            ('regression', model)
        ])

        pipe.fit(X_train, y_train[target])
        y_pred = pipe.predict(X_eval)
        y_eval['y_pred'] = y_pred
        y_eval['abs_diff'] = np.abs(y_eval[target] - y_eval['y_pred'])
        if y_evals is None:
            y_evals = y_eval
        else:
            y_evals = pd.concat([y_evals, y_eval])

        explainer = shap.LinearExplainer(pipe.named_steps['regression'], masker=masker)
        split_shap_values = explainer.shap_values(pipe.named_steps['standard_scaling'].transform(X_eval))
        if shap_values is None:
            shap_values = np.array(split_shap_values)
            shap_x_indexes = eval_index
        else:
            shap_values = np.concatenate((shap_values, np.array(split_shap_values)))
            shap_x_indexes = np.concatenate((shap_x_indexes, eval_index), axis=0)

    fig, ax = plt.subplots(1, 1, figsize=(25, 10))
    plt.subplot(1, 1, 1)
    shap.summary_plot(shap_values, X_all.iloc[list(shap_x_indexes)], max_display=10, show=False, plot_size=None)

    if export_dir is not None:
        plt.savefig(f'{export_dir}/shap_metrics_on_{date.today()}.png')