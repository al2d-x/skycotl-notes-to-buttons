# Sky: Notes → Buttons

Turn a song you downloaded from **Sky Music** into a clean, easy-to-read **button chart** for an Xbox controller.  
You give the app an **HTML file** from <https://sky-music.github.io/>, it reads the notes, and it exports an HTML page that shows, bar by bar, **which buttons to press** (A, B, X, Y, D-pad, LT/RT/LB/RB, sticks) and when to **Rest**.

> Fan-made tool. Not affiliated with that website or the game developer.

---

## Download & Install (Windows)

1. Go to the **Releases** page and download the latest ZIP.
2. **Extract** the ZIP anywhere (e.g., your Desktop).
3. Double-click **`SkyNotesToButtons.exe`** to start.

No extra setup needed.

---

## How to Use

1. On <https://sky-music.github.io/> pick a song and **download/save the HTML** for it.
 <img width="1248" height="731" alt="image" src="https://github.com/user-attachments/assets/56b8c6df-7436-4b1d-af52-e946cf0b8fa1" />
 <img width="725" height="127" alt="image" src="https://github.com/user-attachments/assets/0e9ff297-415d-4b9f-9533-80e98ff4956f" />
 <img width="1540" height="899" alt="image" src="https://github.com/user-attachments/assets/1208cd85-a269-49e5-a2dd-f9192ffa1838" />

 
2. Open **Sky: Notes → Buttons**.
3. Click **Browse…** next to **Input HTML** and pick the file you saved.
4. Click **Browse…** next to **Export to** and choose where to save the result.
5. Press **Start**.
6. When it’s done, you can open the exported HTML in your browser.

### Output
- You get an **HTML file**.  
- If an accompanying **`ui/` folder** appears next to it, **keep it together** with the HTML when you move or upload the file (it contains the button images).

### Zoom
- Use **CTRL + Mouse Wheel** or **CTRL + + / −** in your browser to make the buttons bigger or smaller.

---

## FAQ

### “Why is the download ~40 MB?”
It’s a packaged Python app (PyInstaller). It includes the Python runtime and libraries so you don’t have to install anything. That’s normal size for a small Python GUI app.

### “Can’t you make it smaller?”
Maybe later. Shrinking means carefully excluding libraries and testing a lot; easy to break things. Stability first. 🙂

### “Why does the UI look simple?”
Because function > fashion. I’m a backend person. The UI is intentionally minimal so it’s fast and clear.

### “Why only Xbox buttons?”
The first version targets the Xbox layout. Because i have an xbox controller. I might add other layouts later.  
If you are adventurous, you can **replace the PNG images** in the `ui/` folder with your own, but **keep the same file names** (e.g., `A.png`, `LT.png`).

### “It looks too small / too big.”
Use **CTRL + Mouse Wheel** or **CTRL + + / −** in your browser.

---

## Notes & Tips

- The app looks for the notes under a special section in the HTML (`<div id="transcript">`). If the file is not from the Sky Music site or it’s edited, it may not parse.
- If a bar has no notes, you'll see **“Rest”** in that bar.
- Works offline once you have the HTML file.

---

## License & Credits

- Fan tool for **Sky: Children of the Light** players.
- Not affiliated with the game or the Sky Music website.
- Code is open for learning and personal use.
