import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class SurgicalCalculator:
    """
    This is a class for calculating the outcomes of surgical lists.
    """
    weeks_epi: int
    weeks_surg: int
    time_resumption: int
    baseline_demand: int
    surg_demand: float
    surg_cap: float
    multi_cap_limitation: float
    weekly_prop_increase_cap: float
    num_weeks_run_over: int
    prop_waiting_dying_covid: float
    prop_waiting_dying_baseline: float
    data: list
    data_two: list

    def __init__(self, weeks_epi: int, weeks_surg: int, time_resumption: int, baseline_demand: int,
                 surg_demand: float, surg_cap: float, multi_cap_limitation: float, weekly_prop_increase_cap: float,
                 num_weeks_run_over: int, prop_waiting_dying_covid: float, prop_waiting_dying_baseline: float) -> None:
        """
        The constructor for the SurgicalCalculator class.

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
        """
        self.weeks_epi = weeks_epi
        self.weeks_surg = weeks_surg
        self.time_resumption = time_resumption
        self.baseline_demand = baseline_demand
        self.surg_demand = surg_demand
        self.surg_cap = surg_cap
        self.multi_cap_limitation = multi_cap_limitation
        self.weekly_prop_increase_cap = weekly_prop_increase_cap
        self.num_weeks_run_over = num_weeks_run_over
        self.prop_waiting_dying_covid = prop_waiting_dying_covid
        self.prop_waiting_dying_baseline = prop_waiting_dying_baseline
        # TODO: more descriptive names for these data variables below
        self.data = []
        self.data_two = []
        self.final_df = None

    @property
    def tb(self) -> int:
        """
        Calculates something (needs clarification).

        :return: something (needs clarification)
        """
        return self.time_resumption + self.weeks_surg

    @property
    def y(self) -> float:
        """
        Calculates something (needs clarification).

        :return: something (needs clarification)
        """
        return 1 + (2 * (1 - self.surg_demand) * self.weeks_surg) / (self.tb - self.weeks_surg)

    @property
    def m(self) -> float:
        """
        Calculates something (needs clarification).

        :return: something (needs clarification)
        """
        return (1 - self.y) / (self.tb - self.weeks_surg)

    @property
    def c(self) -> float:
        """
        Calculates something (needs clarification).

        :return: something (needs clarification)
        """
        return self.y - (self.m * self.weeks_surg)

    def first_process(self) -> None:
        """
        Does something (needs clarification).

        :return: None
        """
        # TODO: two variables below run the risk of being referenced before assignment
        n = None
        c_calculated = None

        for i in range(0, self.num_weeks_run_over + 1):
            # TODO => rename I for something more descriptive

            if i <= self.weeks_surg:
                n = self.surg_demand * self.baseline_demand

            if (i > self.weeks_surg) and (i <= self.tb):
                n = ((self.m * i) + self.c) * self.baseline_demand

            if i > self.tb:
                n = self.baseline_demand

            if i <= self.weeks_surg:
                c_calculated = self.surg_cap * self.baseline_demand

            if i > self.weeks_surg:
                c_calculated = self.surg_cap * self.baseline_demand + (self.weekly_prop_increase_cap * (i - self.weeks_surg) * self.baseline_demand)
                if c_calculated >= self.baseline_demand * self.multi_cap_limitation:
                    c_calculated = self.baseline_demand * self.multi_cap_limitation

            p = (i, n, c_calculated)
            self.data.append(p)

    def second_process(self) -> None:
        df1 = pd.DataFrame(self.data)
        df1.columns = ['WEEK', 'N', 'C']
        df_rec = pd.DataFrame(columns=['ID', 'WAIT'])

        # TODO: the variable below runs the risk of being referenced before assignment
        deaths = None

        for i in range(0, self.num_weeks_run_over + 1):

            n = int(df1.loc[df1['WEEK'] == i, 'N'])
            c = int(df1.loc[df1['WEEK'] == i, 'C'])

            df_week = pd.DataFrame(columns=['ID', 'WAIT'])
            df_week['ID'] = list(np.arange(1, n + 1, 1))
            df_week['ID'] = df_week['ID'].astype(str)
            df_week['ID'] = str(i) + '_' + df_week['ID']
            df_week['WAIT'] = 0

            df_rec = pd.concat([df_rec, df_week])
            df_rec = df_rec.sort_values('WAIT', ascending=False)
            df_rec['ORDER'] = list(np.arange(1, len(df_rec) + 1, 1))
            df_rec = df_rec.loc[df_rec['ORDER'] > c]
            del df_rec['ORDER']
            df_rec['WAIT'] = df_rec['WAIT'] + 1

            # Remaining patients without removing CR
            pat_rem_a = len(df_rec)

            if i <= self.weeks_epi:
                cov_risk = self.prop_waiting_dying_covid
            else:
                cov_risk = 0

            if len(df_rec > 0):
                deaths = np.random.binomial(len(df_rec), (cov_risk + self.prop_waiting_dying_baseline))
                drop_indices = np.random.choice(df_rec.index, deaths, replace=False)
                df_rec = df_rec.drop(drop_indices)

            # Remaining patients after removing CR
            pat_rem_b = len(df_rec)

            if pat_rem_b == 0:
                mean_wait = 0
            else:
                mean_wait = np.mean(df_rec['WAIT'])

            out = (i, n, c, pat_rem_a, deaths, pat_rem_b, mean_wait)
            self.data_two.append(out)

    def fire(self) -> pd.DataFrame:
        """
        Fires both processes in order to calculate the outcomes.

        :return: (DataFrame) calculations
        """
        # TODO: this is done like this so if the processes can run side by side we can thread them
        self.first_process()
        self.second_process()
        df_out = pd.DataFrame(self.data_two, columns=['WEEK', 'NEW_DEMAND', 'CAPACITY', 'REMAINING_NO_CR', 'DEATHS',
                                                      'REMAINING_CR', 'MEAN_WAIT'])
        self.final_df = df_out
        return df_out

    def plot(self) -> None:
        """
        Plots the results.

        :return: None
        """
        plt.figure(figsize=(12, 8))
        plt.plot(self.final_df['WEEK'], self.final_df['NEW_DEMAND'], color='#164077')
        plt.plot(self.final_df['WEEK'], self.final_df['CAPACITY'], color='#b62f3a')
        plt.ylim(bottom=0)
        plt.ylim(top=1.1 * np.max(list(self.final_df['NEW_DEMAND']) + list(list(self.final_df['CAPACITY']))))
        plt.ylabel('Activity per Week', fontsize=14)
        plt.xlabel('Weeks from today', fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

        plt.figure(figsize=(12, 8))
        plt.plot(self.final_df['WEEK'], self.final_df['REMAINING_CR'], color='#164077')
        plt.ylim(bottom=0)
        plt.ylim(top=1.1 * np.max(list(self.final_df['REMAINING_CR'])))
        plt.ylabel('Patients Remaining', fontsize=14)
        plt.xlabel('Weeks from today', fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

        plt.figure(figsize=(12, 8))
        plt.plot(self.final_df['WEEK'], self.final_df['MEAN_WAIT'], color='#164077')
        plt.ylim(bottom=0)
        plt.ylim(top=1.1 * np.max(list(self.final_df['MEAN_WAIT'])))
        plt.ylabel('Average Wait Time (weeks)', fontsize=14)
        plt.xlabel('Weeks from today', fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

