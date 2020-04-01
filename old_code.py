# 1. Number of weeks of epidemic
# 2. Number of weeks of surgical / referral shutdown
# 3. Time taken from resumption to refer missed cases
# 4. Baseline demand / capacity

# 5. Demand for surgery as a proportion of baseline during service limitation
# 6. Surgical capacity as a proportion of baseline during service limitation
# 7. Multiple for increased capacity after service limitation
# 8. Weekly proportional increase in capacity after service limitation
# 9. Number of weeks to run over

# 10. Proportion of waiting list dying weekly due to COVID-19
# 11. Proportion of waiting list dying weekly due to baseline age-specific competing risks


# EXAMPLE PARAMETERS:
# dem_cap(12,16,52,200,0.7,0.3,1.1,0.05,208,0.001,0.0005)

def dem_cap(te, to, tend, baseline, xd, xc, rx, rr, W, covid, cr):
    import pandas as pd
    import numpy as np

    tb = tend + to
    out = []

    Y = 1 + (2 * (1 - xd) * to) / (tb - to)
    m = (1 - Y) / (tb - to)
    c = Y - (m * to)

    for i in range(0, W + 1):

        if i <= to:
            N = xd * baseline
        if (i > to) & (i <= tb):
            N = ((m * i) + c) * baseline
        if i > tb:
            N = baseline

        if i <= to:
            C = xc * baseline
        if i > to:
            C = xc * baseline + (rr * (i - to) * baseline)
            if C >= baseline * (rx):
                C = baseline * (rx)

        p = (i, N, C)
        out.append(p)

    df1 = pd.DataFrame(out)
    df1.columns = ['WEEK', 'N', 'C']

    df_rec = pd.DataFrame(columns=['ID', 'WAIT'])

    out_list = []

    for i in range(0, W + 1):

        N = int(df1.loc[df1['WEEK'] == i, 'N'])
        C = int(df1.loc[df1['WEEK'] == i, 'C'])

        df_week = pd.DataFrame(columns=['ID', 'WAIT'])
        df_week['ID'] = list(np.arange(1, N + 1, 1))
        df_week['ID'] = df_week['ID'].astype(str)
        df_week['ID'] = str(i) + '_' + df_week['ID']
        df_week['WAIT'] = 0

        df_rec = pd.concat([df_rec, df_week])
        df_rec = df_rec.sort_values('WAIT', ascending=False)
        df_rec['ORDER'] = list(np.arange(1, len(df_rec) + 1, 1))
        df_rec = df_rec.loc[df_rec['ORDER'] > C]
        del df_rec['ORDER']
        df_rec['WAIT'] = df_rec['WAIT'] + 1

        # Remaining patients without removing CR
        pat_rem_a = len(df_rec)

        if i <= te:
            cov_risk = covid
        else:
            cov_risk = 0

        if len(df_rec > 0):
            deaths = np.random.binomial(len(df_rec), (cov_risk + cr))
            drop_indices = np.random.choice(df_rec.index, deaths, replace=False)
            df_rec = df_rec.drop(drop_indices)

        # Remaining patients after removing CR
        pat_rem_b = len(df_rec)

        if pat_rem_b == 0:
            mean_wait = 0
        else:
            mean_wait = np.mean(df_rec['WAIT'])

        out = (i, N, C, pat_rem_a, deaths, pat_rem_b, mean_wait)
        out_list.append(out)

    return pd.DataFrame(out_list, columns=['WEEK', 'NEW_DEMAND', 'CAPACITY',
                                             'REMAINING_NO_CR', 'DEATHS', 'REMAINING_CR', 'MEAN_WAIT'])


if __name__ == "__main__":
    test = dem_cap(12, 16, 52, 200, 0.7, 0.3, 1.1, 0.05, 208, 0.001, 0.0005)
    print(test.head)

