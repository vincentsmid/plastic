from piccolo.columns import Varchar, Integer, Timestamp, Real, Boolean, ForeignKey
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

class FilamentsStock(Table):
  filamentID = Integer(primary_key=True)
  filamentType = ForeignKey(references=FilamentMaterials)
  filamentStock = Integer()
  filamentInfinite = Boolean()
  filamentPrice = Real()
  filamentName = Varchar()
  filamentDescription = Varchar()

class FilamentMaterials(Table):
  filamentMaterial = Varchar(primary_key=True)
  printTemperature = Integer()
  bedTemperature = Integer()
  difficultyIndex = Real()
  timeIndex = Real()
  multiplier = Real()