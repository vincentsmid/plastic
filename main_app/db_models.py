from piccolo.columns import Varchar, Integer, Timestamp, Real, Boolean, ForeignKey, UUID
from piccolo.table import Table

import uuid


class FilamentsStock(Table):
    filamentID = UUID(primary_key=True, default=uuid.uuid4, unique=True)
    filamentPriceMultiplier = Real()
    filamentMaterial = Varchar()
    filamentColor = Varchar()
    filamentDescription = Varchar()
    filamentPicture = Varchar()
    available = Boolean()


class ItemForSale(Table):
    itemID = UUID(primary_key=True, default=uuid.uuid4, unique=True)
    itemName = Varchar()
    itemPrice = Real()
    itemDescription = Varchar()
    itemModel = Varchar()
    itemPicure = Varchar()
    available = Boolean()


class SpecialSale(Table):
    saleID = UUID(primary_key=True, default=uuid.uuid4, unique=True)
    saleLink = Varchar()
    saleText = Varchar()
    active = Boolean()


class PotentialOrdersFromEstimate(Table):
    orderID = UUID(primary_key=True, default=uuid.uuid4, unique=True)
    orderValue = Real()
    printTime = Real()
    orderDate = Timestamp()
    filamentUsed = Real()
    mail = Varchar()
    contacted = Boolean()
    filament = ForeignKey(references=FilamentsStock)
