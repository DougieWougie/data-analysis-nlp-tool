"""Session management service for handling user analysis sessions."""
import uuid
from pathlib import Path
import tempfile
import shutil
from typing import Optional


class SessionService:
    """Manages analysis sessions with temporary storage."""

    def __init__(self, base_temp_dir: Optional[str] = None):
        """
        Initialize session service.

        Args:
            base_temp_dir: Base directory for temporary files. Uses system temp if None.
        """
        self.base_temp_dir = Path(base_temp_dir or tempfile.gettempdir()) / "data_analysis_sessions"
        self.base_temp_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self) -> str:
        """
        Create a new analysis session.

        Returns:
            Session ID (UUID string)
        """
        session_id = str(uuid.uuid4())
        session_dir = self._get_session_dir(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_id

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its associated files.

        Args:
            session_id: The session UUID

        Returns:
            True if session was deleted, False if it didn't exist
        """
        session_dir = self._get_session_dir(session_id)
        if session_dir.exists():
            shutil.rmtree(session_dir)
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: The session UUID

        Returns:
            True if session exists
        """
        return self._get_session_dir(session_id).exists()

    def get_session_path(self, session_id: str) -> Path:
        """
        Get the filesystem path for a session.

        Args:
            session_id: The session UUID

        Returns:
            Path to the session directory
        """
        return self._get_session_dir(session_id)

    def _get_session_dir(self, session_id: str) -> Path:
        """Get session directory path."""
        return self.base_temp_dir / session_id
