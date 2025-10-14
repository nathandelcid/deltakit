import requests
import uuid
import os
import platform


class PackageAnalytics:
    """Analytics tracker that uses a proxy server for GA4"""

    def __init__(self, proxy_url):
        """
        Initialize analytics tracker

        Args:
            proxy_url: Your proxy server URL (e.g., 'https://your-project.up.railway.app')
        """
        self.proxy_url = proxy_url.rstrip('/')  # Remove trailing slash if present
        self.track_endpoint = f"{self.proxy_url}/track"

        # Generate or load a persistent client ID
        self.client_id = self._get_client_id()

        # Check if telemetry is disabled
        self.enabled = not self._is_disabled()

    def _get_client_id(self):
        """Generate a unique client ID for this user"""
        # You could persist this in a config file for consistency
        return str(uuid.uuid4())

    def _is_disabled(self):
        """Check if user has disabled telemetry"""
        # Respect common do-not-track environment variables
        if os.environ.get("DO_NOT_TRACK", "").lower() in ("1", "true"):
            return True
        if os.environ.get("ANALYTICS_DISABLED", "").lower() in ("1", "true"):
            return True
        # Check if running in CI
        if os.environ.get("CI", "").lower() in ("1", "true"):
            return True
        return False

    def track_event(self, event_name, params=None):
        """
        Send an event via the proxy to GA4

        Args:
            event_name: Name of the event (e.g., 'package_imported', 'function_called')
            params: Dictionary of event parameters
        """
        if not self.enabled:
            return

        if params is None:
            params = {}

        # Add system information to parameters
        params.update(
            {
                "python_version": platform.python_version(),
                "os": platform.system(),
                "os_version": platform.release(),
            }
        )

        payload = {
            "client_id": self.client_id,
            "event_name": event_name,
            "params": params,
        }

        try:
            # Use a short timeout and don't block on failure
            requests.post(
                self.track_endpoint,
                json=payload,
                timeout=2,
            )
        except Exception:
            # Silently fail - don't break the user's code if analytics fails
            pass
