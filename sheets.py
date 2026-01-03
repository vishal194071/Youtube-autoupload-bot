import pandas as pd
from auth import SheetAuth

SPREADSHEET_ID = "1Uq3BZafl5oCwNB-NNlX9eQUIq8whx2ht20dsI37Q8-w"
SHEET_NAME = "sheet1"


class SpreadSheet:
    def __init__(
        self,
        sheet_service,
        spreadsheet_id=SPREADSHEET_ID,
        sheet_name=SHEET_NAME
    ):
        """
        sheet_service   = SheetAuth.get_service()
        spreadsheet_id  = default spreadsheet ID
        sheet_name      = default sheet tab name
        """
        self.sheet = sheet_service
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    # --------------------------------------------------
    # Internal helper (use defaults if not provided)
    # --------------------------------------------------
    def _resolve(self, spreadsheet_id, sheet_name):
        return (
            spreadsheet_id or self.spreadsheet_id,
            sheet_name or self.sheet_name
        )

    # --------------------------------------------------
    # Load Sheet → DataFrame
    # --------------------------------------------------
    def load_df(self, spreadsheet_id=None, sheet_name=None):
        spreadsheet_id, sheet_name = self._resolve(
            spreadsheet_id, sheet_name
        )

        result = self.sheet.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1:Z"
        ).execute()

        values = result.get("values", [])
        if not values:
            return pd.DataFrame()

        header = values[0]
        rows = values[1:]
        rows = [row + [""] * (len(header) - len(row)) for row in rows]

        return pd.DataFrame(rows, columns=header)
    
    def videosToUpload(self):
        df = self.load_df()
        ready_df = df[df["status"] == "ready"]
        return ready_df.to_dict(orient="records")
    
    def update_status_by_metadata(
        self,
        metadata,
        match_key="status",
        new_status="done"
    ):
        
        print(f"{metadata}\n match_key: {match_key} new_status:{new_status} ")

        if not metadata:
            raise ValueError("Empty metadata object")

        if match_key not in metadata:
            raise ValueError(f"Metadata must contain '{match_key}'")

        # 1️⃣ Load entire sheet as JSON
        sheet_json = self.sheet_to_json_object()

        if not sheet_json:
            raise ValueError("Sheet is empty")

        headers = list(sheet_json[0].keys())

        if "status" not in headers:
            raise ValueError("Sheet must contain 'status' column")

        if match_key not in headers:
            raise ValueError(f"Sheet must contain '{match_key}' column")

        status_col_letter = chr(ord("A") + headers.index("status"))

        # 2️⃣ Find matching row
        for index, row in enumerate(sheet_json):
            if row.get(match_key) == metadata.get(match_key):
                sheet_row_number = index + 2  # header offset
                status_cell = f"{status_col_letter}{sheet_row_number}"

                self.update_cell(
                    cell=status_cell,
                    value=new_status
                )

                print(
                    f"✅ Updated status → {new_status} "
                    f"for {match_key}={metadata.get(match_key)}"
                )
                return

        # 3️⃣ If no row matched
        raise ValueError(
            f"No matching row found where {match_key}={metadata.get(match_key)}"
        )


    # --------------------------------------------------
    # Sheet → JSON Object
    # --------------------------------------------------
    def sheet_to_json_object(self, spreadsheet_id=None, sheet_name=None):
        df = self.load_df(spreadsheet_id, sheet_name)
        return df.to_dict(orient="records")

    # --------------------------------------------------
    # Append rows
    # --------------------------------------------------
    def append_rows(self, rows, spreadsheet_id=None, sheet_name=None):
        spreadsheet_id, sheet_name = self._resolve(
            spreadsheet_id, sheet_name
        )

        # ---- Normalize input to List[List[Any]] ----
        if isinstance(rows, dict):
            rows = [[*rows.values()]]

        elif isinstance(rows, list):
            # single row like ["a","b","c"]
            if rows and not isinstance(rows[0], list):
                rows = [rows]

        else:
            raise TypeError(
                "rows must be dict, list, or list of lists"
            )

        self.sheet.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": rows}
        ).execute()


    # --------------------------------------------------
    # Append DataFrame
    # --------------------------------------------------
    def append_df(self, df, spreadsheet_id=None, sheet_name=None):
        self.append_rows(
            df.values.tolist(),
            spreadsheet_id,
            sheet_name
        )

    # --------------------------------------------------
    # Update single cell
    # --------------------------------------------------
    def update_cell(self, cell, value, spreadsheet_id=None, sheet_name=None):
        spreadsheet_id, sheet_name = self._resolve(
            spreadsheet_id, sheet_name
        )

        self.sheet.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!{cell}",
            valueInputOption="USER_ENTERED",
            body={"values": [[value]]}
        ).execute()

    # --------------------------------------------------
    # Overwrite entire sheet
    # --------------------------------------------------
    def overwrite_with_df(self, df, spreadsheet_id=None, sheet_name=None):
        spreadsheet_id, sheet_name = self._resolve(
            spreadsheet_id, sheet_name
        )

        values = [df.columns.tolist()] + df.values.tolist()

        self.sheet.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1",
            valueInputOption="USER_ENTERED",
            body={"values": values}
        ).execute()

    # --------------------------------------------------
    # Find rows by column
    # --------------------------------------------------
    def find_rows(self, column, value, spreadsheet_id=None, sheet_name=None):
        df = self.load_df(spreadsheet_id, sheet_name)
        return df[df[column] == value]
