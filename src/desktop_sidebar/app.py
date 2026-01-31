import sys


def main(argv=None):
    """Start the sidebar GUI. Use `--no-gui` for headless/testing."""
    if argv is None:
        argv = sys.argv[1:]

    if "--no-gui" in argv:
        return 0

    try:
        from PySide6 import QtWidgets, QtCore
    except Exception as exc:
        print("PySide6 is required to run the GUI. Install with: pip install -r requirements.txt")
        raise

    app = QtWidgets.QApplication(sys.argv)

    from .widgets.clock_widget import ClockWidget, COMMON_TIMEZONES
    from .config import load_clocks, save_clocks

    w = QtWidgets.QWidget()
    w.setWindowTitle("Desktop Sidebar")
    # Make it frameless and always on top
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    w.setFixedWidth(300)
    w.setFixedHeight(520)

    # Position near the top-right of the primary screen
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    w.move(rect.width() - w.width() - 10, 10)

    main_layout = QtWidgets.QVBoxLayout(w)
    main_layout.setContentsMargins(6, 6, 6, 6)
    main_layout.setSpacing(8)

    # Controls: Add clock
    controls = QtWidgets.QHBoxLayout()
    add_btn = QtWidgets.QPushButton("+ Add Clock")
    add_btn.setToolTip("Add a new clock (select timezone)")
    controls.addWidget(add_btn)
    main_layout.addLayout(controls)

    # Scroll area for clocks
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    container = QtWidgets.QWidget()
    self_clocks_layout = QtWidgets.QVBoxLayout(container)
    self_clocks_layout.setContentsMargins(0, 0, 0, 0)
    self_clocks_layout.setSpacing(8)
    scroll.setWidget(container)
    main_layout.addWidget(scroll)

    # Load persisted clocks or create a default local clock
    clocks = load_clocks()
    if not clocks:
        clocks = [{"label": "Local", "tz": None}]

    clock_widgets = []

    def add_clock(label: str | None, tz_name: str | None):
        cw = ClockWidget(label=label, tz_name=tz_name)
        clock_widgets.append(cw)
        self_clocks_layout.addWidget(cw)

        # wiring to remove
        def remove():
            cw.setParent(None)
            clock_widgets.remove(cw)
            # persist
            persist()

        cw.remove_btn.clicked.connect(remove)
        persist()

    def persist():
        # Save label and tz (tz can be None)
        tosave = [{"label": c.label_text, "tz": c.tz_name} for c in clock_widgets]
        save_clocks(tosave)

    # Populate initial clocks
    for entry in clocks:
        add_clock(entry.get("label"), entry.get("tz"))

    # Add clock dialog
    def on_add():
        dlg = QtWidgets.QDialog(w)
        dlg.setWindowTitle("Add Clock")
        dlg_layout = QtWidgets.QFormLayout(dlg)

        label_edit = QtWidgets.QLineEdit(dlg)
        tz_combo = QtWidgets.QComboBox(dlg)
        tz_combo.addItems(COMMON_TIMEZONES)
        tz_combo.setEditable(True)  # allow typing custom IANA name

        dlg_layout.addRow("Label:", label_edit)
        dlg_layout.addRow("Timezone:", tz_combo)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        dlg_layout.addRow(btns)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)

        if dlg.exec() == QtWidgets.QDialog.Accepted:
            label = label_edit.text().strip() or None
            tz = tz_combo.currentText().strip() or None
            add_clock(label, tz)

    add_btn.clicked.connect(on_add)

    # ---------------------------
    # System tray + Windows autostart
    # ---------------------------
    try:
        from PySide6 import QtGui, QtWidgets as QtWidgets2
        from pathlib import Path
        from .windows_autostart import enable_autostart, is_autostart_enabled

        # Try to load bundled asset icon, fallback to a system icon
        icon_path = Path(__file__).resolve().parents[1] / "assets" / "icon.svg"
        if icon_path.exists():
            icon = QtGui.QIcon(str(icon_path))
        else:
            icon = app.style().standardIcon(QtWidgets2.QStyle.SP_ComputerIcon)

        tray = QtWidgets2.QSystemTrayIcon(icon, app)
        tray.setToolTip("Desktop Sidebar")

        menu = QtWidgets2.QMenu()

        open_act = menu.addAction("Open")
        minimise_act = menu.addAction("Minimise (tray icon)")
        close_act = menu.addAction("Close")

        def show_window():
            w.show()
            try:
                w.raise_()
                w.activateWindow()
            except Exception:
                pass

        def hide_window():
            # Hide entirely so other programs can cover the area
            w.hide()

        def close_app():
            tray.hide()
            app.quit()

        open_act.triggered.connect(show_window)
        minimise_act.triggered.connect(hide_window)
        close_act.triggered.connect(close_app)

        # Double-click toggles
        def on_tray_activated(reason):
            # Activate on double click
            if reason == QtWidgets2.QSystemTrayIcon.DoubleClick:
                if w.isVisible():
                    hide_window()
                else:
                    show_window()

        tray.activated.connect(on_tray_activated)
        tray.setContextMenu(menu)
        tray.show()

        # Enable autostart on Windows (silent) so it starts with Windows 11
        try:
            if enable_autostart(True):
                # Optionally show message once on first-run
                if is_autostart_enabled():
                    tray.showMessage("Desktop Sidebar", "Enabled auto-start with Windows.", icon)
        except Exception:
            # ignore failures (non-Windows or permissions)
            pass
    except Exception:
        # If system tray isn't available or imports fail, continue without it
        pass

    w.show()
    return app.exec()
