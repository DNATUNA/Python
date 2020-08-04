import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import schedule

def PytrendJob():
    pytrend = TrendReq(tz=540)

    todayDate = datetime.now().strftime('%Y-%m-%d')
    lastWeekDate = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    period = lastWeekDate + ' ' + todayDate

    pytrend.build_payload(kw_list=['쿠팡', '11번가'], geo='KR')
    dataCrawling = pytrend.interest_over_time()

    csvFileName = todayDate + '.csv'

    data = pd.DataFrame(dataCrawling)[['쿠팡', '11번가']]

    data['쿠팡증감률'] = data['쿠팡'].diff().fillna(0).astype(int)
    data['11번가증감률'] = data['11번가'].diff().fillna(0).astype(int)

    data.to_csv(csvFileName, index=True)
    print(todayDate + ": Google Trends Crawling ok…")

schedule.every(10).seconds.do(PytrendJob)
while True:
    schedule.run_pending()
