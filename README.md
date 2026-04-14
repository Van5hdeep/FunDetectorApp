# 📱 Phone Detector (aka Productivity Destroyer Detector)

Ever sat down to study or work and thought:
*"I will NOT touch my phone today."*

Yeah... same.

So I built this.

---

## 🤖 What is this?

This is a Python-powered system that:

* Watches you through your webcam 👀
* Detects when a **phone** appears
* Immediately **snitches on you with a sound alert** 🔊

Basically, it's your digital discipline partner... but way less forgiving.

---

## 🚀 Features

* Real-time camera detection (no lag... no escape)
* Uses YOLO (yes, the cool AI model, not the meme... well, both)
* Draws a box around your phone like it's a criminal
* Plays a custom alert sound when you're caught 📢
* Doesn't spam sound like an idiot (only triggers once per detection)

---

## 🧠 How it works (simple version)

```
Camera -> AI sees phone -> "AHA GOT YOU" -> plays sound
```

---

## 🛠️ Setup

### 1. Install dependencies

```bash
pip install opencv-python ultralytics
```

(We skipped pygame because it likes to ruin lives)

---

### 2. Add your sound

* Convert your audio to `alert.wav`
* Put it in the same folder as the script

---

### 3. Run it

```bash
python main.py
```

---

## 🎮 Controls

* Press **ESC** -> Exit (run away from your mistakes)

---

## ⚠️ Warning

* This WILL expose your lack of self-control
* Works best in good lighting
* May cause guilt, shame, and productivity

---

## 🔥 Future Ideas

* Detect phone near face -> EXTRA loud alert
* Play different sounds (e.g., "bro really??")
* Auto-lock your screen (ultimate betrayal)

---

## 🧑‍💻 Why I built this

Because discipline is hard...
and sometimes you need a machine to yell at you.

---

## 🏁 Final Note

If this catches you using your phone...

Just remember:

> The code didn't fail you.
> You failed the code.

---

Good luck staying focused 😈

