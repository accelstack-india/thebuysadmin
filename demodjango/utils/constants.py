import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')
today = datetime.datetime.now(ist)

DASHBOARD_CONTROLLER = "DASHBOARD_CONTROLLER"
DASHBOARD_STATS = "DASHBOARD_STATS"
TRADE_LIST = "TRADE_LIST"
USER_DATA = "USER_DATA"
USER_NOTIFICATION = "USER_NOTIFICATION"

