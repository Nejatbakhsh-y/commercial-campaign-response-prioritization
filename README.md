# Commercial Campaign Response Prediction and Outreach Prioritization

## Business Problem

Commercial teams often run marketing campaigns using email, phone calls, direct mail, digital ads, or sales representative outreach. However, outreach resources are limited. Contacting every customer equally can waste budget, reduce conversion efficiency, and increase customer fatigue.

The main business question of this project is:

**Which customers are most likely to respond to a commercial campaign, and how should the business prioritize outreach actions?**

This project uses customer and campaign data to predict the probability that each customer will respond to a campaign. The goal is not only to build an accurate machine learning model, but also to translate model outputs into commercial decisions such as customer ranking, outreach prioritization, and campaign resource allocation.

## Dataset

This project uses the UCI Bank Marketing Dataset, a real-world dataset related to direct marketing campaigns conducted by a Portuguese banking institution.

The dataset contains customer demographic information, previous campaign information, contact history, and economic context variables. The main objective is to predict whether a customer subscribed to a term deposit after a marketing campaign.

### Dataset Source

- Source: UCI Machine Learning Repository
- Dataset: Bank Marketing Dataset
- Selected file: bank-additional-full.csv
- Number of records: 41,188
- Target variable: y

### Target Variable

The target variable is:

**y = whether the customer subscribed to a term deposit**

This project treats `y` as the campaign-response outcome:

- `yes` = customer responded positively to the campaign
- `no` = customer did not respond positively to the campaign

For modeling, this target will be converted into a binary response variable:

- `1` = subscribed / positive response
- `0` = not subscribed / negative response

### Dataset Citation


Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

## Business Objective

The objective is to build a decision-support analytics framework that helps a business:

- Identify customers with the highest likelihood of campaign response
- Rank customers by predicted response probability
- Segment customers into high, medium, and low outreach priority groups
- Improve campaign efficiency by focusing resources on higher-value opportunities
- Support marketing and sales teams with actionable recommendations


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


## Target Variable

The target variable is campaign response:

- `response = 1`: customer responded to the campaign
- `response = 0`: customer did not respond

 This is a binary classification problem, but the business value comes from ranking customers and prioritizing outreach actions.

## Commercial Decision Focus

This project focuses on commercial decision-making, not only model accuracy.

The model output will be used to answer:

| Business Decision | Project Output |
|---|---|
| Who should be contacted first? | Ranked customer list |
| Which customers are high priority? | Response probability segments |
| How should outreach resources be allocated? | High/medium/low priority groups |
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





