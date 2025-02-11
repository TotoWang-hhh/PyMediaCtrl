# PyMediaCtrl
A tray media controller for Windows written with Python, fixed &amp; modified from older version from 2yrs before.

**2023~2025 by rgzz666**

Modified in 2025, removed cover art and fixed basic function, made some small changes and translated UI into English.

Do not try to learn from this piece of sh*t or change/fix anything. Fixed it only because it is at least useful.

For more info and references, see the [original post](https://www.cnblogs.com/TotoWang/p/py_music_ctrl.html) ([Archived @ 2025/02/09](http://web.archive.org/save/https://www.cnblogs.com/TotoWang/p/py_music_ctrl.html)).

## List of changes made on this program

- Fixed basic function (Use `winri-*`(`pywinrt` on GitHub) instead of Microsoft official deprecated winrt).
- Removed cover art.
- Added white tray icon (for dark taskbar theme).
- Use system dark mode flag instead of apps dark mode flag when detecting the appearance of the taskbar.
- Added the ability to auto choose dark / light icon.
- Changed `change_icon()` and moved part of it into `set_icon()`.
- Added text scrolling when the text is too long.
- Changed the text to left-aligned which was centered before.
- Translated the program into English.
- Changed font to English `Arial` instead of Chinese `等线`(Deng Xian).
- Made the controls window topmost.
- Added the ability to hide the controls when clicking the tray icon while the window is opened.
- Changed the content of play / pause button to an image.
- Removed unecessary imports.

