# 📱 Phone Detector (aka Productivity Destroyer Detector)

Ever sat down to study or work and thought:
*"I will NOT touch my phone today."*

Yeah... same.

So I built this.

---

## 🤖 What is this?

This is a Python-powered system that:

* Watches you through your webcam 👀
* Uses a base YOLO model that can detect many object classes (not just phones)
* Alerts you with the built-in Windows alert sound when configured conditions are met 🔊

Basically, it's your digital discipline partner... but way less forgiving.

---

## 🚀 Features

* Real-time camera detection (no lag... no escape)
* Uses YOLO (yes, the cool AI model, not the meme... well, both)
* Current model can recognize multiple object types from COCO classes
* Plays the native Windows alert sound when you're caught 📢
* Doesn't spam sound like an idiot (only triggers once per detection)

---

## 🧠 How it works (simple version)

```
Camera -> AI sees object(s) -> target condition is met -> plays Windows alert sound
```

---

## 🛠️ Setup

### 1. Install dependencies

```bash
pip install opencv-python ultralytics
```

(We skipped pygame because it likes to ruin lives)

---

### 2. Run it

```bash
python phone_alert.py
```

---

## 🎮 Controls

* Press **ESC** -> Exit (run away from your mistakes)

---

## ⚠️ Warning

* This WILL expose your lack of self-control
* Works best in good lighting
* May cause guilt, shame, and productivity
* Custom phone-only training is still pending; right now detection uses the general pretrained model

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

