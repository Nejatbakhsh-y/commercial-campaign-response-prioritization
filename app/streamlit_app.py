from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Commercial Campaign Response Dashboard",
    layout="wide"
)

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "processed"
REPORTS_DIR = ROOT_DIR / "reports"


def load_csv(possible_paths):
    for path in possible_paths:
        if path.exists():
            return pd.read_csv(path), path
    return pd.DataFrame(), None


def normalize_name(name):
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def find_column(df, possible_names):
    if df is None or df.empty:
        return None

    normalized_columns = {normalize_name(col): col for col in df.columns}

    for name in possible_names:
        key = normalize_name(name)
        if key in normalized_columns:
            return normalized_columns[key]

    for col in df.columns:
        col_key = normalize_name(col)
        for name in possible_names:
            if normalize_name(name) in col_key:
                return col

    return None


def find_actual_response_column(df):
    if df is None or df.empty:
        return None

    exact_names = [
        "y",
        "actual_response",
        "campaign_response",
        "response",
        "responded",
        "subscribed",
        "target"
    ]

    normalized_columns = {normalize_name(col): col for col in df.columns}

    for name in exact_names:
        key = normalize_name(name)
        if key in normalized_columns:
            return normalized_columns[key]

    return None


def convert_response_to_binary(series):
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    normalized = series.astype(str).str.strip().str.lower()

    positive_values = {"yes", "y", "true", "1", "responded", "subscribed"}
    negative_values = {"no", "n", "false", "0", "not_responded", "not subscribed"}

    return normalized.map(
        lambda value: 1 if value in positive_values else 0 if value in negative_values else None
    )


def format_percentage(value):
    if value is None or pd.isna(value):
        return "Not available"
    return f"{value:.2%}"


def display_file_status(file_status):
    status_df = pd.DataFrame(file_status)
    st.dataframe(status_df, width="stretch")


# ============================================================
# Load Files
# ============================================================

priority_df, priority_path = load_csv(
    [
        DATA_DIR / "next_best_action_recommendations.csv",
        DATA_DIR / "customer_priority_segments.csv",
        DATA_DIR / "selected_top_5000_customers.csv",
        DATA_DIR / "customer_propensity_scores.csv",
        REPORTS_DIR / "next_best_action_recommendations.csv",
        REPORTS_DIR / "customer_priority_recommendations.csv",
    ]
)

propensity_df, propensity_path = load_csv(
    [
        DATA_DIR / "customer_propensity_scores.csv",
        DATA_DIR / "baseline_customer_response_scores.csv",
        REPORTS_DIR / "customer_propensity_scores.csv",
    ]
)

metrics_df, metrics_path = load_csv(
    [
        DATA_DIR / "model_performance_metrics.csv",
        REPORTS_DIR / "model_performance_metrics.csv",
        REPORTS_DIR / "model_metrics.csv",
        REPORTS_DIR / "classification_metrics.csv",
    ]
)

lift_df, lift_path = load_csv(
    [
        DATA_DIR / "lift_by_decile.csv",
        REPORTS_DIR / "lift_by_decile.csv",
        REPORTS_DIR / "decile_lift_table.csv",
    ]
)

feature_importance_df, feature_importance_path = load_csv(
    [
        DATA_DIR / "feature_importance.csv",
        DATA_DIR / "feature_importance_business_interpretation.csv",
        REPORTS_DIR / "feature_importance.csv",
        REPORTS_DIR / "top_predictive_features.csv",
    ]
)


# ============================================================
# Dashboard Header
# ============================================================

st.title("Commercial Campaign Response Dashboard")

st.markdown(
    """
This dashboard translates campaign-response model outputs into business-facing insights:
customer prioritization, model performance, lift analysis, feature importance, and next-best-action recommendations.
"""
)


# ============================================================
# Sidebar Filters
# ============================================================

st.sidebar.header("Dashboard Filters")

filtered_priority_df = priority_df.copy()

segment_col = find_column(
    filtered_priority_df,
    [
        "commercial_priority_segment",
        "priority_segment",
        "segment",
        "customer_segment"
    ]
)

probability_col = find_column(
    filtered_priority_df,
    [
        "predicted_response_probability",
        "response_probability",
        "predicted_probability",
        "propensity_score",
        "probability",
        "score"
    ]
)

if not filtered_priority_df.empty and segment_col is not None:
    available_segments = sorted(filtered_priority_df[segment_col].dropna().unique())

    selected_segments = st.sidebar.multiselect(
        "Select Priority Segment",
        available_segments,
        default=available_segments
    )

    filtered_priority_df = filtered_priority_df[
        filtered_priority_df[segment_col].isin(selected_segments)
    ]

if not filtered_priority_df.empty and probability_col is not None:
    filtered_priority_df[probability_col] = pd.to_numeric(
        filtered_priority_df[probability_col],
        errors="coerce"
    )

    min_score = float(filtered_priority_df[probability_col].min())
    max_score = float(filtered_priority_df[probability_col].max())

    selected_range = st.sidebar.slider(
        "Select Propensity Score Range",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score)
    )

    filtered_priority_df = filtered_priority_df[
        filtered_priority_df[probability_col].between(selected_range[0], selected_range[1])
    ]


# ============================================================
# 1. Overall Campaign Response Rate
# ============================================================

st.header("1. Overall Campaign Response Rate")

analysis_df = propensity_df.copy()
if analysis_df.empty:
    analysis_df = priority_df.copy()

response_col = find_actual_response_column(analysis_df)
response_rate = None

if response_col is not None:
    response_binary = convert_response_to_binary(analysis_df[response_col])
    response_rate = response_binary.mean()

col1, col2, col3 = st.columns(3)

col1.metric("Overall Response Rate", format_percentage(response_rate))
col2.metric("Total Customers", f"{len(priority_df):,}" if not priority_df.empty else "Not available")
col3.metric("Filtered Customers", f"{len(filtered_priority_df):,}" if not filtered_priority_df.empty else "Not available")

if response_rate is None:
    st.info(
        "Actual response rate could not be calculated because no actual response column was found. "
        "Expected examples: y, actual_response, response, campaign_response."
    )


# ============================================================
# 2. Model Performance Metrics
# ============================================================

st.header("2. Model Performance Metrics")

if metrics_df.empty:
    st.warning("Model performance metrics file was not found yet.")
    st.info("Expected file example: data/processed/model_performance_metrics.csv or reports/model_performance_metrics.csv")
else:
    st.dataframe(metrics_df, width="stretch")


# ============================================================
# 3. Customer Priority Distribution
# ============================================================

st.header("3. Customer Priority Distribution")

if filtered_priority_df.empty:
    st.warning("Customer priority file was not found or contains no records.")
elif segment_col is None:
    st.warning("No customer priority segment column was found.")
    st.dataframe(filtered_priority_df.head(20), width="stretch")
else:
    segment_counts = (
        filtered_priority_df[segment_col]
        .value_counts()
        .reset_index()
    )
    segment_counts.columns = ["Priority Segment", "Customer Count"]

    st.bar_chart(segment_counts.set_index("Priority Segment"))
    st.dataframe(segment_counts, width="stretch")


# ============================================================
# 4. Lift by Decile
# ============================================================

st.header("4. Lift by Decile")

if not lift_df.empty:
    st.dataframe(lift_df, width="stretch")
else:
    lift_source_df = analysis_df.copy()

    lift_probability_col = find_column(
        lift_source_df,
        [
            "predicted_response_probability",
            "response_probability",
            "predicted_probability",
            "propensity_score",
            "probability",
            "score"
        ]
    )

    lift_response_col = find_actual_response_column(lift_source_df)

    if lift_probability_col is None or lift_response_col is None:
        st.warning("Lift-by-decile file was not found and could not be calculated from available columns.")
    else:
        temp = lift_source_df[[lift_probability_col, lift_response_col]].copy()
        temp[lift_probability_col] = pd.to_numeric(temp[lift_probability_col], errors="coerce")
        temp["response_binary"] = convert_response_to_binary(temp[lift_response_col])
        temp = temp.dropna()

        if temp.empty:
            st.warning("Lift-by-decile could not be calculated because valid probability and response values were not available.")
        else:
            temp = temp.sort_values(lift_probability_col, ascending=False)
            temp["decile"] = pd.qcut(
                temp[lift_probability_col].rank(method="first", ascending=False),
                10,
                labels=list(range(1, 11))
            )

            overall_rate = temp["response_binary"].mean()

            calculated_lift = (
                temp.groupby("decile", observed=True)
                .agg(
                    customers=("response_binary", "count"),
                    responders=("response_binary", "sum"),
                    response_rate=("response_binary", "mean")
                )
                .reset_index()
            )

            calculated_lift["lift"] = calculated_lift["response_rate"] / overall_rate

            st.bar_chart(calculated_lift.set_index("decile")["lift"])
            st.dataframe(calculated_lift, width="stretch")


# ============================================================
# 5. Top Predictive Features
# ============================================================

st.header("5. Top Predictive Features")

if feature_importance_df.empty:
    st.warning("Feature-importance file was not found.")
else:
    feature_col = find_column(
        feature_importance_df,
        [
            "feature",
            "variable",
            "feature_name",
            "predictor"
        ]
    )

    importance_col = find_column(
        feature_importance_df,
        [
            "importance",
            "feature_importance",
            "permutation_importance",
            "absolute_importance",
            "coefficient"
        ]
    )

    if feature_col is None or importance_col is None:
        st.warning("Feature-importance table was found, but feature and importance columns were not detected.")
        st.dataframe(feature_importance_df.head(20), width="stretch")
    else:
        temp = feature_importance_df[[feature_col, importance_col]].copy()
        temp[importance_col] = pd.to_numeric(temp[importance_col], errors="coerce")
        temp = temp.dropna()
        temp["absolute_importance"] = temp[importance_col].abs()

        top_features = (
            temp.sort_values("absolute_importance", ascending=False)
            .head(10)
        )

        st.bar_chart(top_features.set_index(feature_col)["absolute_importance"])
        st.dataframe(top_features, width="stretch")


# ============================================================
# 6. Next-Best-Action Table
# ============================================================

st.header("6. Next-Best-Action Table")

if filtered_priority_df.empty:
    st.warning("Next-best-action table could not be displayed because the customer-priority file is missing.")
else:
    customer_id_col = find_column(
        filtered_priority_df,
        [
            "customer_id",
            "id",
            "client_id"
        ]
    )

    action_col = find_column(
        filtered_priority_df,
        [
            "next_best_action",
            "recommended_action",
            "action",
            "business_action"
        ]
    )

    display_columns = []

    for col in [customer_id_col, probability_col, segment_col, action_col]:
        if col is not None and col not in display_columns:
            display_columns.append(col)

    if display_columns:
        display_df = filtered_priority_df[display_columns].copy()
    else:
        display_df = filtered_priority_df.copy()

    if probability_col is not None and probability_col in display_df.columns:
        display_df = display_df.sort_values(probability_col, ascending=False)

    st.dataframe(display_df, width="stretch")


# ============================================================
# 7. Downloadable Customer-Priority File
# ============================================================

st.header("7. Downloadable Customer-Priority File")

if filtered_priority_df.empty:
    st.warning("No customer-priority records are available for download.")
else:
    csv_data = filtered_priority_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Customer-Priority File",
        data=csv_data,
        file_name="customer_priority_dashboard_export.csv",
        mime="text/csv"
    )


# ============================================================
# Input File Status
# ============================================================

st.header("Dashboard Input File Status")

file_status = [
    {
        "Dashboard Input": "Customer Priority / Next-Best-Action File",
        "Status": "Found" if priority_path else "Missing",
        "File Path": str(priority_path) if priority_path else "Not found"
    },
    {
        "Dashboard Input": "Customer Propensity File",
        "Status": "Found" if propensity_path else "Missing",
        "File Path": str(propensity_path) if propensity_path else "Not found"
    },
    {
        "Dashboard Input": "Model Performance Metrics File",
        "Status": "Found" if metrics_path else "Missing",
        "File Path": str(metrics_path) if metrics_path else "Not found"
    },
    {
        "Dashboard Input": "Lift by Decile File",
        "Status": "Found" if lift_path else "Missing",
        "File Path": str(lift_path) if lift_path else "Not found or calculated dynamically"
    },
    {
        "Dashboard Input": "Feature Importance File",
        "Status": "Found" if feature_importance_path else "Missing",
        "File Path": str(feature_importance_path) if feature_importance_path else "Not found"
    }
]

display_file_status(file_status)
