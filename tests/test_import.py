def test_main_importable():
    import desktop_sidebar
    assert callable(desktop_sidebar.main)
