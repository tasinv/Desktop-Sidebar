"""Windows autostart helpers.

Functions are safe to import on non-Windows platforms (they will simply return False).
"""
from __future__ import annotations

import sys
from typing import Optional


def enable_autostart(enable: bool, name: str = "DesktopSidebar", executable: Optional[str] = None) -> bool:
    """Enable/disable autostart on Windows by writing to HKCU Run key.

    Returns True on success, False otherwise (including non-Windows).
    """
    if not sys.platform.startswith("win"):
        return False

    try:
        import winreg
        if executable is None:
            # If frozen (pyinstaller) use sys.executable (the exe), otherwise run the python -m module
            if getattr(sys, "frozen", False):
                executable = f'"{sys.executable}"'
            else:
                executable = f'"{sys.executable}" -m desktop_sidebar'

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        if enable:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, executable)
        else:
            try:
                winreg.DeleteValue(key, name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def is_autostart_enabled(name: str = "DesktopSidebar") -> bool:
    """Return True if the autostart entry exists (Windows)."""
    if not sys.platform.startswith("win"):
        return False
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False
