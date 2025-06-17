# HabitBreaker

Help with personal bad habit using Yolo11 object detection model.


## 📘 HabitBreaker – Interrupt Unconscious Phone Usage

**Purpose:**
*HabitBreaker* is a lightweight watchdog system designed to detect and interrupt unconscious bad habits — specifically **using your phone while idle**, even when your computer is still on.

---

## 🔁 Workflow Overview (see images above):

1. **Idle Detection**

   * System continuously monitors keyboard and mouse activity.
   * If **no input is detected for a set duration** (e.g., 180 seconds), it assumes you're idle and triggers behavior monitoring.
![image](https://github.com/user-attachments/assets/9d560784-e75c-4585-a2c6-3c8116f93593)

2. **Person Detection**

   * Once idle, the webcam activates and **runs YOLOv11 object detection**.
   * Only when a **person is confirmed present**, further analysis proceeds.
   * If no person is detected within 3 minutes, monitoring ends silently.
![image](https://github.com/user-attachments/assets/0eb351b4-a280-4141-af3b-d29cf3213979)

3. **Prohibited Object Monitoring**

   * While the person is present, the system scans for **specific distraction items** (e.g., `"cell phone"`, `"remote"`).
   * As soon as such an object is detected:

     * 🔔 A control action is triggered immediately (configurable: lock screen, alert, block, etc.)
     * 💥 Monitoring halts; no need to wait for full duration.

4. **Interrupt On Activity**

   * If you return to your keyboard/mouse before a violation is detected, the system **instantly stops monitoring** and resets.
![image](https://github.com/user-attachments/assets/8b29ba92-3ab7-41c3-99de-fc840d17d682)

---

## 📌 Notes

* 💻 **Computer usage (typing, clicking) is fully excluded** from detection scope. Only idle moments are evaluated.
* 🧠 HabitBreaker targets subtle behavioral slippage — moments when you're “just checking” your phone out of habit.
* 🔒 Designed to run quietly in the background and intervene **only when needed**.


---

Want a version with diagram or badge for GitHub? Say the word — I’ll package it clean.
