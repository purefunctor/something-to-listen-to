"""Rich terminal frontend using `rich`."""

from rich import box, print
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text

table = Table(expand=True, box=box.SQUARE, style="green")
table.add_column(Text("RAINY NIGHT IN TALINN", justify="center"))
table.add_row("[bold]Artist:[/bold] Ludwig Goransson")
table.add_row("[bold]Length:[/bold] 8m00s")
table.add_row(
    "[bold]Album:[/bold] Tenet (Original Motion Picture Soundtrack) [Deluxe Edition]"
)

columns = Columns(
    [
        table,
        table,
        table,
        table,
    ],
    width=35,
)

print(Align(columns, "center"))
