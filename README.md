# Sky: Notes → Buttons

Turn a song you downloaded from **Sky Music** into a clean, easy-to-read **button chart** for controllers (Xbox / PlayStation / Switch) or **keyboard**.
You give the app an **HTML file** from [https://sky-music.github.io/](https://sky-music.github.io/), it reads the notes, and it exports a page that shows, bar by bar, **which buttons to press** and when to **Rest**.

> Fan-made tool for **Sky: Children of the Light**. Not affiliated with the website or game developers.
> Works **offline** once you have the HTML file.

---

## ✨ What’s new in 2.0

* **Multiple layouts (profiles):** Xbox, PlayStation, Switch, and Keyboard (EN/DE).
* **Profile validation:** quickly see if a profile is missing icons.
* **Help inside the app:** About, Profile naming, How to add a profile, and Licenses.
* **Version menu:** opens the GitHub Releases page (no auto-update, no internet checks).
* **Cleaner export:** simple, readable HTML with icon fallbacks if images are missing.

---

## 📥 Download & Install (Windows)

1. Go to **Releases** and download the latest ZIP.
   [https://github.com/al2d-x/skycotl-notes-to-buttons/releases](https://github.com/al2d-x/skycotl-notes-to-buttons/releases)
2. **Extract** the ZIP anywhere (e.g., Desktop).
3. Double-click **`SkyNotesToButtons.exe`** to start.
   *No extra setup needed.*

> Some antivirus tools flag small indie EXEs. This one is clean. The code is public—feel free to review it.

---

## 🚀 Quick Start

1. On [https://sky-music.github.io/](https://sky-music.github.io/) pick a song and **download/save the HTML** for it.
<img width="1450" height="759" alt="image" src="https://github.com/user-attachments/assets/6a463d7f-c2d3-468f-8c91-c09195502b9f" />
<img width="589" height="133" alt="image" src="https://github.com/user-attachments/assets/41d8edeb-2e17-4e6f-b6f9-ffae0e37822d" />
<img width="1545" height="723" alt="image" src="https://github.com/user-attachments/assets/d9ea97e8-6217-4699-aa5f-6266bc3149ae" />

3. Open **Sky: Notes → Buttons**.
4. Click **Browse…** next to **Input HTML** and pick the file you saved.
5. Choose an **icon profile** (e.g., Xbox, PS, Switch, Keyboard).
6. Click **Browse…** next to **Export to** and choose where to save.
7. Press **Start**.
8. When it’s done, open the exported HTML in your browser.

**Zoom the chart:** use **CTRL + Mouse Wheel** or **CTRL + + / −** in your browser.

---

## 🗂️ Output

* You get one **HTML file** with a tidy grid of bars.
* Each bar shows a vertical stack of button icons (or a **Rest** label).
* If icon files aren’t found, the app shows **text badges** (fallback), so the chart is still usable.

> Tip: If you move the exported HTML elsewhere and your icons disappear, export again near your **`sntb-ui/`** icon folders, or copy the relevant profile folder along with the HTML (keeping the same structure).

---

## 🎛 Profiles (Layouts)

Choose from built-in profiles (examples):

* `xbox_kenny`, `xbox_zacksly`, `xbox_unknown`
* `ps_kenny`, `ps_zacksly`
* `switch_zacksly`
* `keyboard_eng_kenny`, `keyboard_ger_kenny`

### Add your own profile

1. In the app: **Help → Open profiles folder** (this points to `sntb-ui/`).
2. Create a new subfolder (its name becomes the profile name in the app).
3. Add **`1.png … 15.png`** (top-left to bottom-right notes ingame).
4. In the app: **Help → Validate selected profile** to check for missing/out-of-range files.

---

## ❓ FAQ

**Why is the download ~40 MB?**
The EXE bundles Python and libraries so you don’t have to install anything. That size is normal for a small Python GUI app.

**Does it auto-update?**
No. The app shows **Help → Version…** which **opens the Releases page** in your browser. No internet checks, no automatic downloads.

**It looks too small / too big.**
Use **CTRL + Mouse Wheel** (or **CTRL + + / −**) in your browser.

**My song didn’t parse.**
The Sky Music site has a few HTML formats. This app expects notes under `<div id="transcript">`. If a saved file is different or incomplete, parsing can fail. Try another copy of the song or open an issue with the HTML attached.

**The icons don’t show.**
Make sure the exported HTML can find the profile images. Export next to your `sntb-ui/` folder, or keep the profile folder with the HTML. If images are missing, the app shows **text labels** as a fallback.

**profile for my ps6 are missing.**
Do it yourself
---

## 🔒 Privacy

* Works **offline**.
* The app **never uploads** your files anywhere.
* Licenses for icon sets are included and viewable under **Help → Licenses**.

---

## 🛠️ Build from Source (advanced)

If you don’t want the EXE, you can run from source:

```powershell
# In PowerShell
git clone https://github.com/al2d-x/skycotl-notes-to-buttons.git
cd skycotl-notes-to-buttons
py -3.12 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m main
```

> If `requirements.txt` isn’t present, install dependencies shown in the repo (e.g., `beautifulsoup4`, optionally `ttkbootstrap`), then run `python -m main`.

---

## 🧭 Roadmap

* User  “print-friendly” export
* Better handling of alternate Sky Music HTML formats and Exports from other websites

Have ideas? Open an **Issue**!
---

## 📜 License & Credits

* This is a fan tool for **Sky: Children of the Light** players.
* Not affiliated with thatgamecompany or the Sky Music website.
* Icon sets and their licenses are credited under **Help → Licenses** in the app (and in `/docs/licenses/`).

  * Kenney Input Prompts (CC0)
  * Zacksly Icons (CC BY 3.0)
  * Additional sets noted where used

---

## 💬 Support

* Found a bug or a song that won’t parse?
  Please open an **Issue** with:

  * The **input HTML** (attach the file)
  * A short description (what you expected vs. what happened)
  * If relevant, your chosen **profile** and the exported HTML result

Thanks for trying **Sky: Notes → Buttons**! 🎶🎮
