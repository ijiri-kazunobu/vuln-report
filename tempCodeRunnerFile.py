    cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E78")

        for column, width in COLUMN_WIDTHS[sheet_name].items():
            ws.column_dimensions[column].width = width

        ws.freeze_panes = "A2"