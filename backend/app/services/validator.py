   def _validate_required_columns(df: pd.DataFrame) -> pd.DataFrame:
        required_columns = {"time", "timestamp", "date"}
        missing =[col for col in requiredc if col not in df.columns]
        
        if missing:
            raise TelemetryParserError(
                f"Missing required columns: {', '.join(missing)}"
            )

        return df