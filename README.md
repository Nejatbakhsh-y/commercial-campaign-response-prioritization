# Commercial Campaign Response Prediction and Outreach Prioritization

## Business Problem

Commercial teams often run marketing campaigns using email, phone calls, direct mail, digital ads, or sales representative outreach. However, outreach resources are limited. Contacting every customer equally can waste budget, reduce conversion efficiency, and increase customer fatigue.

The main business question of this project is:

**Which customers are most likely to respond to a commercial campaign, and how should the business prioritize outreach actions?**

This project uses customer and campaign data to predict the probability that each customer will respond to a campaign. The goal is not only to build an accurate machine learning model, but also to translate model outputs into commercial decisions such as customer ranking, outreach prioritization, and campaign resource allocation.

## Business Objective

The objective is to build a decision-support analytics framework that helps a business:

- Identify customers with the highest likelihood of campaign response
- Rank customers by predicted response probability
- Segment customers into high, medium, and low outreach priority groups
- Improve campaign efficiency by focusing resources on higher-value opportunities
- Support marketing and sales teams with actionable recommendations

## Dataset

This project uses the UCI Bank Marketing Dataset, a real-world dataset related to direct marketing campaigns conducted by a Portuguese banking institution.

The dataset contains customer demographic information, previous campaign information, contact history, and economic context variables. The main objective is to predict whether a customer subscribed to a term deposit after a marketing campaign.

### Dataset Source

| Item | Description |
|---|---|
| Source | UCI Machine Learning Repository |
| Dataset | Bank Marketing Dataset |
| Selected file | bank-additional-full.csv |
| Number of records | 41,188 |
| Target variable | y |

### Dataset Citation

Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

## Target Variable

The target variable is:

**y = whether the customer subscribed to a term deposit**

This project treats `y` as the campaign-response outcome:

- `yes` = customer responded positively to the campaign
- `no` = customer did not respond positively to the campaign

For modeling, this target is converted into a binary response variable:

- `1` = subscribed / positive response
- `0` = not subscribed / negative response

This is a binary classification problem, but the business value comes from ranking customers and prioritizing outreach actions.

## Project Workflow

1. Define the business problem
2. Load and understand the dataset
3. Clean and prepare the data
4. Perform exploratory data analysis
5. Engineer useful commercial features
6. Build baseline and machine learning models
7. Evaluate model performance
8. Rank customers by predicted response probability
9. Create outreach priority segments
10. Translate results into business recommendations

## Step 3: Data Understanding

After loading the UCI Bank Marketing Dataset, the project performs an initial data understanding analysis to connect the raw data to the commercial campaign objective.

This step examines:

- Number of customer records
- Overall campaign response rate
- Numerical and categorical variables
- Missing and `unknown` values
- Campaign-related variables
- Previous campaign outcomes
- Response differences across customer groups
- Response differences across contact types
- Relationship between repeated contacts and customer response

The main business goal of this step is to understand which customer and campaign characteristics are associated with higher response rates before building predictive models.

## Baseline Modeling

This project trains three baseline machine learning models to predict customer campaign response:

| Model | Purpose |
|---|---|
| Logistic Regression | Interpretable baseline model |
| Random Forest | Nonlinear model for complex customer behavior |
| Gradient Boosting | Strong predictive model for campaign response prediction |

The models are first trained as baseline classifiers and then evaluated using both machine learning metrics and commercial targeting metrics.

Because campaign response is an imbalanced classification problem, the project emphasizes ranking-oriented and business-focused evaluation rather than accuracy alone. Metrics such as ROC-AUC, lift, cumulative gain, and precision at top customer segments are especially useful for prioritizing outreach.

The recommended final model candidate is selected based on predictive performance and business usefulness. In this type of commercial analytics problem, Random Forest or Gradient Boosting is usually preferred because they can capture nonlinear response patterns.

### Modeling Note

The `duration` variable is excluded from predictive modeling because it is only known after a customer contact occurs. Including this variable would create data leakage and would not reflect a realistic pre-campaign scoring scenario. The model is designed to support outreach prioritization before the campaign action is taken.

## Model Performance Evaluation

The trained models are evaluated using both standard machine learning metrics and commercial analytics metrics.

Standard model evaluation metrics include:

- ROC-AUC
- Accuracy
- Precision
- Recall
- F1 score
- Confusion matrix

Because this is a commercial analytics project, the evaluation also includes business-focused targeting metrics:

- Top-decile lift
- Precision at top 10%
- Precision at top 20%
- Cumulative gain
- Response rate by propensity group

These metrics help determine whether the model can improve campaign targeting and outreach prioritization. The goal is not only to predict campaign response accurately, but also to identify which customers should be prioritized when marketing or sales resources are limited.

The commercial evaluation answers practical business questions such as:

| Business Question | Evaluation Output |
|---|---|
| How well does the model distinguish responders from non-responders? | ROC-AUC |
| How accurate are the model classifications? | Accuracy, precision, recall, and F1 score |
| How many correct and incorrect predictions are made? | Confusion matrix |
| Are the highest-scored customers more likely to respond? | Precision at top 10% and top 20% |
| How much better is model-based targeting than random targeting? | Top-decile lift |
| How many responders can be captured by targeting a smaller customer group? | Cumulative gain |
| Which customer groups should receive outreach priority? | Response rate by propensity group |

This evaluation connects machine learning performance directly to commercial decision-making. It shows whether the model can help a business rank customers, prioritize outreach, and allocate campaign resources more efficiently.

## Customer Propensity Scoring

The final selected model is used to generate a predicted response probability for each customer.

This predicted probability represents the likelihood that a customer will respond positively to the campaign. Customers are then sorted from highest to lowest predicted probability to create a ranked outreach list.

The output file is saved as:

`data/processed/customer_propensity_scores.csv`

The propensity score output includes:

- Customer ID
- Predicted response probability
- Actual response outcome
- Customer rank

This step converts the machine learning model into a practical commercial decision-support tool by helping the business prioritize customers with the highest likelihood of campaign response.

## Commercial Decision Focus

This project focuses on commercial decision-making, not only model accuracy.

The model output is used to answer:

| Business Decision | Project Output |
|---|---|
| Who should be contacted first? | Ranked customer list |
| Which customers are high priority? | Response probability segments |
| How should outreach resources be allocated? | High, medium, and low priority groups |
| How can campaign efficiency improve? | Lift and gain analysis |
| What factors drive response? | Feature importance and explainability |

## Expected Business Impact

The expected business impact is to help a company improve campaign targeting, reduce wasted outreach, increase response rates, and allocate marketing or sales resources more efficiently.

Instead of treating all customers equally, the business can use predicted response probabilities to prioritize customers most likely to respond. This supports better commercial decision-making by helping teams focus outreach efforts on higher-potential opportunities.

Expected benefits include:

- Higher campaign response efficiency
- Better use of sales and marketing resources
- Reduced unnecessary customer contact
- Improved customer prioritization
- More data-driven campaign planning
- Clearer connection between machine learning outputs and business actions

## Repository Structure

```text
commercial-campaign-response-prioritization/
│
├── README.md
├── data/
│   ├── raw/
│   │   └── bank-additional-full.csv
│   └── processed/
│       └── customer_propensity_scores.csv
│
├── notebooks/
│   ├── 01_business_problem_and_data_understanding.ipynb
│   └── 02_baseline_modeling.ipynb
│
├── reports/
│   └── figures/
│
├── src/
├── requirements.txt
└── .gitignore
