from piccolo.columns import Varchar
from piccolo.table import Table


class RandomTable(Table):
    name = Varchar()
