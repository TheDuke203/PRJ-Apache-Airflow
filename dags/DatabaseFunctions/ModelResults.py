sql = """
INSERT INTO results(
    test_date,
    test_rows_num,
    r_squared_regression,
    true_ratio_classification,
    accuracy_classification 
)
VALUES (%s, %s, %s, %s, %s)
"""

def push_model_results(rows, accuracy, r_squared, true_ratio):
    