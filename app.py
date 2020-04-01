from flask import Flask, render_template
from calculator import SurgicalCalculator
from old_code import dem_cap

app = Flask(__name__)


@app.route("/calculate/<weeks_epi>/<weeks_surg>/<time_resumption>/<baseline_demand>/<surg_demand>/<surg_cap>/<multi_cap_limitation>/<weekly_prop_increase_cap>/<num_weeks_run_over>/<prop_waiting_dying_covid>/<prop_waiting_dying_baseline>/")
def calculate(weeks_epi, weeks_surg, time_resumption, baseline_demand, surg_demand, surg_cap, multi_cap_limitation,
              weekly_prop_increase_cap, num_weeks_run_over, prop_waiting_dying_covid, prop_waiting_dying_baseline):
    """
    Calculation API for projections.

    :param weeks_epi: (int) Number of weeks of epidemic
    :param weeks_surg: (int) Number of weeks of surgical / referral shutdown
    :param time_resumption: (int) Time taken from resumption to refer missed cases
    :param baseline_demand: (int) Baseline demand / capacity
    :param surg_demand: (float) Demand for surgery as a proportion of baseline during service limitation
    :param surg_cap: (float) Surgical capacity as a proportion of baseline during service limitation
    :param multi_cap_limitation: (float) Multiple for increased capacity after service limitation
    :param weekly_prop_increase_cap: (float) Weekly proportional increase in capacity after service limitation
    :param num_weeks_run_over: (int) Number of weeks to run over
    :param prop_waiting_dying_covid: (float) Proportion of waiting list dying weekly due to COVID-19
    :param prop_waiting_dying_baseline: (float) Proportion of waiting list dying weekly due to baseline age-specific competing risks

    :return: (JSON) containing lists of calculation
    """
    weeks_epi = int(weeks_epi)
    weeks_surg = int(weeks_surg)
    time_resumption = int(time_resumption)
    baseline_demand = int(baseline_demand)
    surg_demand = float(surg_demand)
    surg_cap = float(surg_cap)
    multi_cap_limitation = float(multi_cap_limitation)
    weekly_prop_increase_cap = float(weekly_prop_increase_cap)
    num_weeks_run_over = int(num_weeks_run_over)
    prop_waiting_dying_covid = float(prop_waiting_dying_covid)
    prop_waiting_dying_baseline = float(prop_waiting_dying_baseline)

    # out_come = dem_cap(
    #     weeks_epi,
    #     weeks_surg,
    #     time_resumption,
    #     baseline_demand,
    #     surg_demand,
    #     surg_cap,
    #     multi_cap_limitation,
    #     weekly_prop_increase_cap,
    #     num_weeks_run_over,
    #     prop_waiting_dying_covid,
    #     prop_waiting_dying_baseline
    # )

    calc = SurgicalCalculator(weeks_epi=weeks_epi, weeks_surg=weeks_surg, time_resumption=time_resumption,
                              baseline_demand=baseline_demand, surg_demand=surg_demand, surg_cap=surg_cap,
                              multi_cap_limitation=multi_cap_limitation,
                              weekly_prop_increase_cap=weekly_prop_increase_cap, num_weeks_run_over=num_weeks_run_over,
                              prop_waiting_dying_covid=prop_waiting_dying_covid,
                              prop_waiting_dying_baseline=prop_waiting_dying_baseline)
    # calc.fire()
    return {
        "WEEK": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "NEW_DEMAND": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "CAPACITY": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "REMAINING_CR": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "MEAN_WAIT": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    }
    # return {
    #     "WEEK": list(calc.final_df["WEEK"]),
    #     "NEW_DEMAND": list(calc.final_df["NEW_DEMAND"]),
    #     "CAPACITY": list(calc.final_df["CAPACITY"]),
    #     "REMAINING_CR": list(calc.final_df["REMAINING_CR"]),
    #     "MEAN_WAIT": list(calc.final_df["MEAN_WAIT"]),
    # }
    # return {
    #     "WEEK": list(out_come["WEEK"]),
    #     "NEW_DEMAND": list(out_come["NEW_DEMAND"]),
    #     "CAPACITY": list(out_come["CAPACITY"]),
    #     "REMAINING_CR": list(out_come["REMAINING_CR"]),
    #     "MEAN_WAIT": list(out_come["MEAN_WAIT"])
    # }


@app.route('/test')
def test():
    return "Hello World!"


@app.route('/')
def home():
    return render_template("main.html")

# http://127.0.0.1:5000/calculate/14/5/8/4/3/0.6/0.6/0.5/0.7/0.4/0.8/

# http://127.0.0.1:5000/calculate/12/16/52/200/0.7/0.3/1.1/0.05/208/0.001/0.0005


if __name__ == '__main__':
    app.run()
