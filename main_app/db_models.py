from piccolo.columns import Varchar, Integer, Timestamp, Real, Boolean, ForeignKey
from piccolo.table import Table


class PotentialOrdersFromEstimate(Table):
  orderValue = Real()
  printTime = Real()
  orderDate = Timestamp()
  filamentUsed = Real()
  filamentType = Varchar()
  discordName = Varchar()
  contacted = Boolean()
  filament = ForeignKey(references="FilamentsStock")

class FilamentMaterials(Table):
  material = Varchar()
  printTemperature = Integer()
  bedTemperature = Integer()
  difficultyIndex = Real()
  timeIndex = Real()
  multiplier = Real()

class FilamentsStock(Table):
  filamentType = ForeignKey(references="FilamentMaterials")
  filamentStock = Integer()
  filamentInfinite = Boolean()
  filamentPrice = Real()
  filamentName = Varchar()
  filamentDescription = Varchar()
  active = Boolean()
