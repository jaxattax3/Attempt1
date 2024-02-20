import matplotlib.pyplot as plt
import pandas as pd
import os

def convert_k_notation_to_number(input_string):
    """Converts a string with 'k' notation to a number."""
    if input_string.lower().endswith('k'):
        return float(input_string[:-1]) * 1000
    else:
        return float(input_string)

def get_career_info(career_name, mode):
    """Collects income, expenses, and optionally investment details for a given career."""
    print(f"Enter information for {career_name}:")
    yearly_income = convert_k_notation_to_number(input("Yearly income: "))
    yearly_expenses = convert_k_notation_to_number(input("Yearly expenses: "))
    info = {"yearly_income": yearly_income, "yearly_expenses": yearly_expenses}
    if mode == "advanced":
        investment_percent = float(input("What percent of leftover money is invested in %: ")) / 100
        if investment_percent > 0:
            average_roi = float(input("What is the average ROI in %: ")) / 100
            info.update({"investment_percent": investment_percent, "average_roi": average_roi})
    return info

# Initial setup: mode selection and career information input
mode = input("Choose mode (simple or advanced): ").lower()
career1_name = input("Enter the name for Career 1: ")
career1_info = get_career_info(career1_name, mode)
career2_name = input("Enter the name for Career 2: ")
career2_info = get_career_info(career2_name, mode)
years_separated_by = int(input("Years separated by: "))

# Adjusting start years based on user input
career1_start_year = 1 if years_separated_by <= 0 else 1 + years_separated_by
career2_start_year = 1 if years_separated_by >= 0 else 1 - years_separated_by

careers = {career1_name: career1_info, career2_name: career2_info}
total_money = {}

# Financial calculations
for career, info in careers.items():
    start_year = career1_start_year if career == career1_name else career2_start_year
    years_to_calculate = 60 - (start_year - 1)
    leftover_money = [info["yearly_income"] - info["yearly_expenses"]]
    for year in range(1, years_to_calculate):
        if mode == "advanced" and "investment_percent" in info:
            invested_amount = leftover_money[-1] * info["investment_percent"]
            roi_amount = invested_amount * info["average_roi"]
            new_leftover = leftover_money[-1] + (info["yearly_income"] - info["yearly_expenses"]) + roi_amount - invested_amount
        else:
            new_leftover = leftover_money[-1] + (info["yearly_income"] - info["yearly_expenses"])
        leftover_money.append(new_leftover)
    prepend_zeros = [0] * (start_year - 1)
    total_money[career] = pd.Series(prepend_zeros + leftover_money).cumsum()

# Plotting
plt.figure(figsize=(10, 6))
for career in total_money:
    years_plot = range(1, len(total_money[career]) + 1)
    plt.plot(years_plot, total_money[career], label=career)

plt.title("Total Money Over 60 Years")
plt.xlabel("Year")
plt.ylabel("Total Money")
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.legend()
plt.show()

# Spreadsheet creation
user_decision = input("Would you like a spreadsheet to show each year how much the individual has for each career side by side? (yes/no): ").lower()

if user_decision == 'yes':
    file_name = input("What do you want the file to be called? (please include '.xlsx' at the end): ")

    # Ensure the directory exists
    directory = os.path.dirname(file_name)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Create a single DataFrame with one column for each career
    years = range(1, 61)
    combined_data = {
        career1_name: total_money[career1_name].reindex(years, fill_value=0),
        career2_name: total_money[career2_name].reindex(years, fill_value=0)
    }
    combined_df = pd.DataFrame(combined_data, index=years)
    combined_df.index.name = "Year"
    combined_df.columns = [career1_name, career2_name]

    # Save the DataFrame to an Excel file
    combined_df.to_excel(file_name, sheet_name='Career Comparison')

    print(f"The spreadsheet has been saved as '{file_name}' in the current working directory.")
else:
    print("No spreadsheet will be created.")
