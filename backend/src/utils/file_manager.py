"""File management utilities for storing and loading datasets."""
from pathlib import Path
from typing import BinaryIO
import pandas as pd


class FileManager:
    """Handles file storage operations for datasets."""

    @staticmethod
    def save_uploaded_file(file: BinaryIO, destination: Path) -> Path:
        """
        Save an uploaded file to disk.

        Args:
            file: File object to save
            destination: Path where the file should be saved

        Returns:
            Path to the saved file
        """
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as f:
            content = file.read()
            f.write(content)
        return destination

    @staticmethod
    def load_dataframe(file_path: Path) -> pd.DataFrame:
        """
        Load a pandas DataFrame from a file with smart format detection.

        Args:
            file_path: Path to the CSV or Excel file

        Returns:
            Loaded DataFrame

        Raises:
            ValueError: If file format is not supported
        """
        suffix = file_path.suffix.lower()

        # Try CSV first
        if suffix == ".csv":
            return pd.read_csv(file_path)

        # For .xlsx files, use openpyxl
        elif suffix == ".xlsx":
            try:
                return pd.read_excel(file_path, engine="openpyxl")
            except Exception as e:
                # If it fails, it might be a misnamed text file
                raise ValueError(f"Failed to read .xlsx file. It may be corrupted or not a valid Excel file: {str(e)}")

        # For .xls files, try xlrd first, then fallback to text formats
        elif suffix == ".xls":
            try:
                return pd.read_excel(file_path, engine="xlrd")
            except Exception as xlrd_error:
                # The file might be a text file with .xls extension
                # Try both TSV and CSV, keep the one with more columns
                tsv_df = None
                csv_df = None

                # Try reading as tab-separated (TSV)
                try:
                    tsv_df = pd.read_csv(file_path, sep="\t")
                    if len(tsv_df) == 0 or len(tsv_df.columns) == 0:
                        tsv_df = None
                except Exception:
                    pass

                # Try reading as comma-separated (CSV)
                try:
                    csv_df = pd.read_csv(file_path, sep=",")
                    if len(csv_df) == 0 or len(csv_df.columns) == 0:
                        csv_df = None
                except Exception:
                    pass

                # Return the dataframe with more columns (better parse)
                if tsv_df is not None and csv_df is not None:
                    return tsv_df if len(tsv_df.columns) > len(csv_df.columns) else csv_df
                elif tsv_df is not None:
                    return tsv_df
                elif csv_df is not None:
                    return csv_df

                # All attempts failed
                raise ValueError(
                    f"Failed to read .xls file. It appears to be neither a valid Excel file "
                    f"nor a valid text file (CSV/TSV). Please ensure your file is properly formatted. "
                    f"Original error: {str(xlrd_error)}"
                )

        else:
            raise ValueError(f"Unsupported file format: {suffix}. Please upload .csv, .xlsx, or .xls files.")

    @staticmethod
    def save_dataframe(df: pd.DataFrame, file_path: Path) -> Path:
        """
        Save a DataFrame to disk.

        Args:
            df: DataFrame to save
            file_path: Path where the file should be saved

        Returns:
            Path to the saved file (may differ if .xls was converted to .xlsx)
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            df.to_csv(file_path, index=False)
        elif suffix == ".xlsx":
            df.to_excel(file_path, index=False, engine="openpyxl")
        elif suffix == ".xls":
            # xlrd cannot write, so convert .xls to .xlsx when saving
            new_file_path = file_path.with_suffix(".xlsx")
            df.to_excel(new_file_path, index=False, engine="openpyxl")
            # Remove old .xls file if it exists
            if file_path.exists():
                file_path.unlink()
            return new_file_path
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
        return file_path

    @staticmethod
    def delete_file(file_path: Path) -> bool:
        """
        Delete a file.

        Args:
            file_path: Path to the file to delete

        Returns:
            True if file was deleted, False if it didn't exist
        """
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    @staticmethod
    def get_dataset_path(session_dir: Path, filename: str = "dataset.csv") -> Path:
        """
        Get the standard path for a dataset file.

        Args:
            session_dir: Session directory
            filename: Name of the dataset file

        Returns:
            Path to the dataset file
        """
        return session_dir / filename
