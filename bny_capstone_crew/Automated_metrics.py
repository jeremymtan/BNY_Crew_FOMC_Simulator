import json
from collections import Counter
import numpy as np
import glob

meeting_code = "24_9"

code2date = {
    "23_2": "Feb 2023",
    "23_5": "May 2023",
    "23_7": "July 2023",
    "24_3": "March 2024",
    "24_9": "September 2024",
    "24_11": "November 2024",
    "24_12": "December 2024",
    "25_3": "March 2025",
}
code2vote = {
    "23_2": ["0.25%", "+0.25", "0.25", "+0.25"],
    "23_5": ["0.25%", "+0.25", "0.25", "+0.25"],
    "23_7": ["0.25%", "+0.25", "0.25", "+0.25"],
    "24_3": ["0.00%", "-0.00%", "+0.00%", "0.00", "-0.00", "+0.00"],
    "24_9": ["-0.50%", "-0.50"],
    "24_11": ["-0.25%", "-0.25"],
    "24_12": ["-0.25%", "-0.25"],
    "25_3": ["0.00%", "-0.00%", "+0.00%", "0.00", "-0.00", "+0.00"],
}

code2pred = {
    "23_2": [
        "3.00%-3.25%",
        "3.00%",
        "3.25%",
        "3.00-3.25%",
        "3.00",
        "3.25",
        "3.00-3.25",
        "2.50%-2.75%",
        "2.50%",
        "2.75%",
        "2.50-2.75%",
        "2.50",
        "2.75",
        "2.50-2.75",
    ],
    "23_5": [
        "2.75%-3.00%",
        "2.75%",
        "3.25%",
        "2.75-3.00%",
        "2.75",
        "3.25",
        "2.75-3.00",
        "3.00%-3.25%",
        "3.00%",
        "3.00-3.25%",
        "3.00",
        "3.00-3.25",
        "2.75%-3.25%",
        "2.75-3.25%",
        "2.75-3.25",
    ],
    "23_7": [
        "3.25%-3.50%",
        "3.25%",
        "3.50%",
        "3.25-3.50%",
        "3.25",
        "3.50",
        "3.25-3.50",
        "3.00%-3.25%",
        "3.00%",
        "3.00-3.25%",
        "3.00",
        "3.00-3.25",
        "3.00%-3.50%",
        "3.00-3.50%",
        "3.00-3.50",
    ],
    "24_3": [
        "3.75%-4.00%",
        "3.75%",
        "4.00%",
        "3.75-4.00%",
        "3.75",
        "4.00",
        "3.75-4.00",
    ],
    "24_9": [
        "3.25%-3.50%",
        "3.25%",
        "3.50%",
        "3.25-3.50%",
        "3.25",
        "3.50",
        "3.25-3.50",
    ],
    "24_11": [
        "3.25%-3.50%",
        "3.25%",
        "3.50%",
        "3.25-3.50%",
        "3.25",
        "3.50",
        "3.25-3.50",
    ],
    "24_12": [
        "3.75%-4.00%",
        "3.75%",
        "4.00%",
        "3.75-4.00%",
        "3.75",
        "4.00",
        "3.75-4.00",
    ],
    "25_3": [
        "3.75%-4.00%",
        "3.75%",
        "4.00%",
        "3.75-4.00%",
        "3.75",
        "4.00",
        "3.75-4.00",
    ],
}
meeting_date = code2date[meeting_code]
correct_vote = code2vote[meeting_code]
correct_pred = code2pred[meeting_code]

# Step 1: Get a list of all JSON files
json_files = glob.glob("rate_summary*.json")  # Adjust pattern to match your file names

# Step 2: Read all JSON files into a list
rate_summaries = []


for file in json_files:
    with open(file, "r") as f:
        data = json.load(f)
        rate_summaries.append(data)  # Append each JSON object to the list


# Dictionary to store votes by member
votes_by_member = {}
predictions_by_member = {}
all_votes = []
all_preds = []
all_dates = []
all_metrics = []

# Loop through each JSON object
for summary in rate_summaries:
    for vote in summary["rate_votes"]:
        member = vote["member"]
        vote_value = vote["vote"]

        # Initialize list if member not in dictionary
        if member not in votes_by_member:
            votes_by_member[member] = []

        # Append vote to the corresponding member
        votes_by_member[member].append(vote_value)
        all_votes.append(vote_value)
    for prediction in summary["rate_predictions"]:
        member = prediction["member"]
        prediction_value = prediction["prediction"]

        # Initialize list if member not in dictionary
        if member not in predictions_by_member:
            predictions_by_member[member] = []

        # Append vote to the corresponding member
        predictions_by_member[member].append(prediction_value)
        all_preds.append(prediction_value)
    all_dates.append(summary["exact_historical_dates_referenced"])
    all_metrics.append(summary["exact_metrics_mentioned"])

vote_agreement_rates = []
prediction_agreement_rates = []

for member in votes_by_member:
    vote_counts = Counter(votes_by_member[member])
    # Get the most common value and its count
    most_common_value, count = vote_counts.most_common(1)[0]
    vote_agreement_rates.append(100 * count / len(votes_by_member[member]))
    # Do the same for predictions
    prediction_counts = Counter(predictions_by_member[member])
    # Get the most common value and its count
    most_common_value, count = prediction_counts.most_common(1)[0]
    prediction_agreement_rates.append(100 * count / len(predictions_by_member[member]))


# print(vote_agreement_rates)
avg_vote_agreement = np.mean(vote_agreement_rates)
print(f"Meeting Date: {meeting_date}")
print(f"average agreement rate for votes: {avg_vote_agreement}%")
# print(prediction_agreement_rates)
avg_prediction_agreement = np.mean(prediction_agreement_rates)
print(
    f"average agreement rate for predictions: {np.round(avg_prediction_agreement,2)}%"
)
print(
    f"total agreement rate: {np.round(np.mean([avg_vote_agreement,avg_prediction_agreement]),2)}%"
)
correct_vote_pct = (
    100 * sum([vote in correct_vote for vote in all_votes]) / len(all_votes)
)
print(f"correct rate vote percentage = {correct_vote_pct}%")
correct_pred_pct = (
    100 * sum([pred in correct_pred for pred in all_preds]) / len(all_preds)
)
print(f"correct rate prediction percentage = {correct_pred_pct}%")
print(f"total accuracy = {(correct_pred_pct + correct_vote_pct)*0.5}%")
print()
print("All dates mentioned:")
for dates in all_dates:
    print(dates)

print()
print("All metrics mentioned:")
for metrics in all_metrics:
    print(metrics)
