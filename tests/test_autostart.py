from desktop_sidebar.windows_autostart import enable_autostart, is_autostart_enabled


def test_autostart_no_crash_on_posix():
    # On non-Windows platforms these are no-ops and must not raise
    res = enable_autostart(False)
    assert res is False
    assert is_autostart_enabled() is False
