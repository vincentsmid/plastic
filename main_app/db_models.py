from piccolo.columns import Varchar, Integer, Timestamp, Real, Boolean
from piccolo.table import Table


class PotentialOrdersFromEstimate(Table):
    orderID = Integer(primary_key=True)
    orderValue = Varchar()
    printTime = Real()
    orderDate = Timestamp()
    filamentUsed = Real()
    filamentType = Varchar()
    discordName = Varchar()
    contacted = Boolean()
