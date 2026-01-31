from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from PySide6 import QtCore, QtWidgets, QtGui

from ..timefmt import format_time, format_date

COMMON_TIMEZONES = [
    "UTC",
    "Europe/London",
    "Europe/Berlin",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Asia/Kolkata",
    "Australia/Sydney",
]


class ClockWidget(QtWidgets.QWidget):
    """A single clock showing time (12-hour with am/pm) and date (DD/MM/YY).

    Usage:
        cw = ClockWidget(label="London", tz_name="Europe/London")
    """

    def __init__(self, label: str | None = None, tz_name: str | None = None, parent=None):
        super().__init__(parent)
        self.label_text = label or tz_name or "Local"
        self.tz_name = tz_name

        self._init_ui()
        self.update_time()

        # Update once every 1 second to keep AM/PM and minutes accurate
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.update_time)
        self._timer.start()

    def _init_ui(self):
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(6)

        header = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel(self.label_text)
        self.title_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = self.title_label.font()
        font.setPointSize(10)
        self.title_label.setFont(font)

        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.remove_btn = QtWidgets.QPushButton("✕")
        self.remove_btn.setFixedSize(20, 20)
        self.remove_btn.setToolTip("Remove clock")
        self.remove_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        header.addWidget(self.title_label)
        header.addItem(spacer)
        header.addWidget(self.remove_btn)

        v.addLayout(header)

        # Big time label
        self.time_label = QtWidgets.QLabel("--:--am")
        time_font = self.time_label.font()
        time_font.setPointSize(24)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        v.addWidget(self.time_label)

        # Small date label
        self.date_label = QtWidgets.QLabel("--/--/--")
        date_font = self.date_label.font()
        date_font.setPointSize(10)
        self.date_label.setFont(date_font)
        self.date_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        v.addWidget(self.date_label)

    def update_time(self):
        now = self._now()
        time_text = format_time(now)
        date_text = format_date(now)

        self.time_label.setText(time_text)
        self.date_label.setText(date_text)

    def _now(self) -> datetime:
        if self.tz_name:
            try:
                tz = ZoneInfo(self.tz_name)
                return datetime.now(tz)
            except Exception:
                # Fallback to naive local time
                return datetime.now()
        return datetime.now()
