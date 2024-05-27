from piccolo.columns import Varchar, Integer, Timestamp, Real, Boolean, ForeignKey, UUID
from piccolo.table import Table

import uuid


class PotentialOrdersFromEstimate(Table):
  orderID = UUID(primary_key=True, default=uuid.uuid4, unique=True)
  orderValue = Real()
  printTime = Real()
  orderDate = Timestamp()
  filamentUsed = Real()
  filamentType = Varchar()
  discordName = Varchar()
  contacted = Boolean()
  filament = ForeignKey(references="FilamentsStock")

# class FilamentMaterials(Table):
#   material = Varchar()
#   printTemperature = Integer()
#   bedTemperature = Integer()
#   difficultyIndex = Real()
#   timeIndex = Real()
#   multiplier = Real()

class FilamentsStock(Table):
  # filamentType = ForeignKey(references="FilamentMaterials")
  filamentStock = Integer()
  filamentInfinite = Boolean()
  filamentPrice = Real()
  filamentName = Varchar()
  filamentDescription = Varchar()
  active = Boolean()