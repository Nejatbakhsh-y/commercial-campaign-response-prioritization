# Commercial Analytics AI: Campaign Propensity, Lift Analysis, and Next-Best-Action Prioritization

## Business Problem

Commercial teams often run marketing campaigns through email, phone calls, direct mail, digital outreach, or sales representative follow-up. However, outreach resources are limited. Contacting every customer with the same level of effort can waste budget, reduce conversion efficiency, and increase customer fatigue.

The core business question of this project is:

**Which customers are most likely to respond to a commercial campaign, and how should the business prioritize outreach actions?**

This project uses real campaign-response data to predict customer response probability, rank customers by commercial propensity, evaluate lift, and translate model outputs into practical next-best-action recommendations for sales and marketing decision support.

---

## Business Objective

The objective is to build a commercial analytics decision-support framework that helps a business:

- Identify customers with the highest likelihood of campaign response
- Rank customers by predicted response probability
- Segment customers into high, medium, low, and deprioritized outreach groups
- Evaluate how much the model improves targeting compared with random selection
- Recommend next-best commercial actions based on propensity segments
- Improve campaign efficiency by focusing resources on higher-propensity customers
- Support sales and marketing teams with actionable recommendations

This project is designed as a commercial analytics AI prototype rather than a standard classification notebook. It connects predictive modeling with customer prioritization, lift analysis, and business-facing decision support.

---

## Dataset Description

This project uses the **UCI Bank Marketing Dataset**, a real-world dataset related to direct marketing campaigns conducted by a Portuguese banking institution.

The dataset contains customer demographic information, campaign contact information, previous campaign history, and economic context variables.

The target variable is:

```text
y = whether the customer subscribed to a term deposit
```

For this project, the target variable is interpreted as a campaign-response outcome:

- `yes` = customer responded positively to the campaign
- `no` = customer did not respond positively to the campaign

Although the original dataset is from a banking campaign, the workflow is applicable to broader commercial analytics problems such as lead scoring, customer prioritization, marketing targeting, sales outreach optimization, and campaign resource allocation.

---

## Why `duration` Was Removed

The original dataset includes a variable named `duration`, which measures the length of the customer contact.

This variable was removed from the predictive modeling process because it creates **target leakage**.

In a real campaign setting, the business must score customers before contacting them. At that point, call duration is not yet known. Including `duration` would allow the model to use information that becomes available only after the campaign interaction has occurred.

Keeping `duration` would likely inflate model performance and make the results unrealistic for real-world campaign planning.

Therefore, `duration` was excluded so the model better reflects a realistic pre-campaign scoring workflow.

---

## Modeling Approach

The project follows a structured machine learning workflow:

1. Load the campaign dataset
2. Preprocess numerical and categorical variables
3. Remove leakage-prone variables such as `duration`
4. Encode categorical variables
5. Split the data into training and testing sets
6. Train baseline and machine learning models
7. Evaluate model performance
8. Generate customer-level propensity scores
9. Convert scores into commercial priority segments
10. Calculate lift by decile
11. Generate next-best-action recommendations
12. Save business-facing outputs
13. Present results in a Streamlit dashboard

The modeling approach includes:

| Model | Purpose |
|---|---|
| Logistic Regression | Interpretable baseline model |
| Random Forest | Nonlinear model for customer response patterns |
| Gradient Boosting | Strong predictive model for campaign response prediction |

The final model is selected based on predictive performance, ranking quality, and business usefulness.

---

## Evaluation Metrics

The model is evaluated using both standard machine learning metrics and business-focused campaign metrics.

Standard model evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

Because campaign response problems are often imbalanced, accuracy alone is not sufficient. Ranking quality is especially important because the business goal is to identify which customers should be contacted first.

ROC-AUC is used to evaluate how well the model separates likely responders from likely non-responders across different probability thresholds.

---

## Example Model Performance

The training script automatically generates model metrics and saves them to:

```text
outputs/model_metrics.json
```

Example model output:

```json
{
  "model_name": "Gradient Boosting Classifier",
  "accuracy": 0.9011,
  "precision": 0.6728,
  "recall": 0.2371,
  "f1_score": 0.3506,
  "roc_auc": 0.8091,
  "training_records": 32950,
  "test_records": 8238,
  "target_response_rate": 0.1127
}
```

For this project, ROC-AUC and lift analysis are especially important because the business goal is to rank customers by likelihood of response, not only to classify customers as responders or non-responders.

---

## Lift Analysis

Lift analysis evaluates whether the model improves campaign targeting compared with random customer selection.

Customers are sorted by predicted response probability and divided into deciles. The response rate in each decile is compared with the overall campaign response rate.

Lift analysis helps answer practical business questions such as:

- Are the highest-scored customers more likely to respond?
- How much better is the top customer group compared with the average customer?
- Can the business improve campaign efficiency by focusing on top-ranked customers?
- Which customer groups should be prioritized when outreach capacity is limited?

A strong lift in the top deciles indicates that the model can help prioritize outreach more effectively.

The lift analysis output is saved as:

```text
outputs/lift_by_decile.csv
```

---

## Customer Propensity Scores

The model generates a predicted response probability for each customer.

Example:

| Customer ID | Propensity Score |
|---:|---:|
| 10452 | 0.84 |
| 20931 | 0.55 |
| 35120 | 0.27 |
| 18411 | 0.08 |

These scores represent the estimated likelihood that each customer will respond positively to the campaign.

The customer propensity score output is saved as:

```text
outputs/customer_propensity_scores.csv
```

---

## Commercial Priority Segmentation

Propensity scores are converted into business-friendly customer segments.

| Propensity Score | Segment | Business Meaning |
|---:|---|---|
| 0.70 and above | High Priority | Strong candidate for immediate outreach |
| 0.40 to 0.69 | Medium Priority | Good candidate for targeted follow-up |
| 0.20 to 0.39 | Low Priority | Suitable for low-cost nurture campaign |
| Below 0.20 | Deprioritized | Do not prioritize in the current campaign |

This segmentation makes the model output easier for business users to interpret and apply.

---

## Next-Best-Action Logic

Each customer segment is mapped to a recommended commercial action.

| Segment | Recommended Action |
|---|---|
| High Priority | Priority sales outreach |
| Medium Priority | Targeted marketing follow-up |
| Low Priority | Low-cost nurture campaign |
| Deprioritized | Exclude from current campaign |

Example output:

| Customer ID | Probability | Segment | Next Best Action |
|---:|---:|---|---|
| 10452 | 0.84 | High Priority | Priority sales outreach |
| 20931 | 0.55 | Medium Priority | Targeted marketing follow-up |
| 35120 | 0.27 | Low Priority | Low-cost nurture campaign |
| 18411 | 0.08 | Deprioritized | Exclude from current campaign |

The next-best-action output is saved as:

```text
outputs/next_best_actions.csv
```

This step converts machine learning predictions into operational recommendations for marketing and sales teams.

---

## Explainability

The project includes feature importance analysis to identify which variables contribute most to campaign response prediction.

Important drivers may include:

- Previous campaign outcome
- Contact type
- Customer job category
- Education
- Age
- Number of campaign contacts
- Prior contact history
- Campaign timing
- Economic context variables

Explainability is important because commercial teams need to understand why certain customers are prioritized. It also supports model governance, business trust, and responsible use of predictive analytics.

The feature importance output is saved as:

```text
outputs/feature_importance.csv
```

Important dataset note: the UCI Bank Marketing Additional dataset does not include a `balance` variable. Therefore, balance is not used as a feature in this project version.

---

## Project Outputs

This project produces five main analytical outputs:

| Output File | Description |
|---|---|
| `outputs/model_metrics.json` | Model performance metrics including accuracy, precision, recall, F1 score, ROC-AUC, training records, test records, and target response rate |
| `outputs/customer_propensity_scores.csv` | Customer-level predicted response probabilities and priority segments |
| `outputs/lift_by_decile.csv` | Lift analysis showing how effectively the model ranks high-response customers |
| `outputs/next_best_actions.csv` | Recommended outreach action for each customer based on propensity segment |
| `outputs/feature_importance.csv` | Top predictive features driving campaign response |

These outputs make the project title accurate:

**Campaign Propensity** is represented by `customer_propensity_scores.csv`.

**Lift Analysis** is represented by `lift_by_decile.csv`.

**Next-Best-Action Prioritization** is represented by `next_best_actions.csv`.

**Explainability** is represented by `feature_importance.csv`.

**Model Evaluation** is represented by `model_metrics.json`.

The project may also generate an additional supporting file:

```text
outputs/model_performance_metrics.csv
```

This file is a supplemental tabular version of model performance results.

---

## Business Value

This project demonstrates how machine learning can improve commercial campaign execution.

Potential business value includes:

- Better customer targeting
- Higher campaign response efficiency
- More efficient sales and marketing resource allocation
- Reduced unnecessary customer contact
- Improved campaign return on investment
- Stronger prioritization of high-propensity customers
- More transparent decision-making through explainable model outputs
- Actionable customer-level recommendations instead of only technical model metrics

The main value of the project is not only predicting campaign response, but also converting predictions into clear business actions.

---

## Responsible AI Note

This project is intended as a decision-support tool, not a fully automated decision-making system.

Responsible AI considerations include:

- Removing leakage-prone variables such as `duration`
- Evaluating model performance beyond accuracy
- Reviewing feature importance for business reasonableness
- Avoiding over-reliance on sensitive or potentially unfair variables
- Using predictions to support human decision-making
- Monitoring model performance if applied to new campaign data
- Ensuring that customer outreach strategies remain fair, transparent, and compliant with relevant business policies

The model should be reviewed by business, analytics, and governance stakeholders before any real-world deployment.

---

## Project Structure

```text
commercial-analytics-campaign-ai/
│
├── data/
│   └── README.md
│
├── notebooks/
│   └── commercial_campaign_eda.ipynb
│
├── src/
│   ├── load_data.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── score_customers.py
│   └── generate_next_best_action.py
│
├── outputs/
│   ├── model_metrics.json
│   ├── model_performance_metrics.csv
│   ├── customer_propensity_scores.csv
│   ├── lift_by_decile.csv
│   ├── next_best_actions.csv
│   └── feature_importance.csv
│
├── app/
│   └── streamlit_app.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Requirements

The main Python packages used in this project include:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- jupyter
- notebook
- streamlit

Install the requirements with:

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

Run the following commands from the project root folder.

### 1. Install required packages

```powershell
pip install -r requirements.txt
```

### 2. Run the project scripts

```powershell
python .\src\load_data.py
python .\src\preprocess_data.py
python .\src\train_model.py
python .\src\score_customers.py
python .\src\generate_next_best_action.py
```

These scripts generate the main output files in the `outputs/` folder.

### 3. Verify project outputs

```powershell
Get-ChildItem outputs
```

You should see the following main files:

```text
customer_propensity_scores.csv
lift_by_decile.csv
next_best_actions.csv
feature_importance.csv
model_metrics.json
```

### 4. Run the Streamlit dashboard

```powershell
streamlit run app/streamlit_app.py
```

---

## Streamlit Dashboard

The project includes a Streamlit dashboard that translates machine learning outputs into business-facing campaign insights.

The dashboard includes:

- Overall campaign response rate
- Model performance metrics
- Customer priority distribution
- Lift analysis by decile
- Top predictive features
- Next-best-action recommendation table
- Downloadable customer-priority output

Run the dashboard with:

```powershell
streamlit run app/streamlit_app.py
```

---

## Final Project Output

The final project produces:

- A real-data commercial analytics workflow
- Machine learning models for campaign response prediction
- Model performance evaluation
- Customer propensity scores
- Lift analysis by decile
- Commercial priority segments
- Next-best-action recommendations
- Feature importance and explainability outputs
- A Streamlit dashboard for business-facing review

This project demonstrates how machine learning can be used not only for prediction, but also for commercial prioritization, campaign lift analysis, resource allocation, model explainability, and business decision support.

---

## What I did!

Developed a real-data commercial analytics AI prototype using campaign-response data to predict customer propensity, evaluate lift, rank outreach priority, and generate next-best-action recommendations for sales and marketing decision support.
