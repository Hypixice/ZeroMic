<div align="center">
  <img src="https://x19.fp.ps.netease.com/file/69f5fc8dfcc7c18f65647c58EUpGTLbr07" width="128" height="128" alt="ZeroMic Logo">
  <h1>ZeroMic</h1>
  <p><strong>No App Required (Mobile) · Portable Single-Binary (PC) · Modern MD3 UI</strong></p>
  <p>Transform your smartphone into a High-Fidelity wireless microphone for your PC instantly.</p>
  
  <p>
    <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=flat-square" alt="Platform">
    <img src="https://img.shields.io/badge/License-GPLv3-green?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/Built%20with-Python%20%7C%20WebRTC-yellow?style=flat-square" alt="Tech">
  </p>

  <p>
    <b>English</b> | <a href="./README_zh.md">简体中文</a>
  </p>
</div>

---

## 📖 Introduction

**ZeroMic** is a minimalist, cross-platform wireless microphone transmission tool. 

Whether your desktop lacks a dedicated mic or you need high-quality voice input for gaming (Discord, KOOK) or online meetings, ZeroMic has you covered. Simply run the desktop client and access the local URL via your mobile browser—no app installation required. 

Powered by **WebRTC P2P technology**, audio data is streamed directly within your local network (LAN) **without passing through external servers**, ensuring maximum privacy and millisecond-level latency.

## ✨ Key Features

- **🚀 Out-of-the-Box:** Packaged as a single executable. No installation, no complicated setup—just double-click and go.
- **🔧 Auto-Driver Config:** Automatically creates and configures virtual audio devices without manual intervention.
- **🐧 True Cross-Platform:** Native support for Windows, Linux, and macOS from a single codebase.
- **⚡ Ultra-Low Latency:** WebRTC-powered LAN streaming provides a near-wired audio experience.
- **🎨 Modern Design:** Sleek Dark Mode with MD3 (Material Design 3) aesthetics, responsive interactions, and clear status feedback.
- **🧹 Clean Uninstall:** Built-in cleanup feature ensures no driver residue or registry bloat is left behind.

## 🚀 Quick Start

### Prerequisites
- A PC running Windows 10+, Linux (PulseAudio/PipeWire), or macOS.
- Your phone and PC must be connected to the **same Local Area Network (Wi-Fi)**.

### Usage Steps
1. Download the executable for your platform from the [Releases](https://github.com/hypixice/ZeroMic/releases) page.
2. **Windows**: Right-click and **Run as Administrator**. **Linux/macOS**: Run directly (no root required).
3. On first launch, ZeroMic will automatically set up the virtual audio device. (Windows may take 10-20s for driver setup; Linux/macOS is near-instant).
4. Once configured, a URL (e.g., `https://192.168.x.x:5000`) will be displayed on the PC client.
5. Enter this URL in your mobile browser (Safari, Chrome, or Edge recommended).
6. In your game or voice chat software, set the **Microphone Input Device** to the virtual device created by ZeroMic.
7. Start talking!

## 🛠️ Developer Guide (Build from Source)

```bash
# 1. Clone the repository
git clone [https://github.com/hypixice/ZeroMic.git](https://github.com/hypixice/ZeroMic.git)
cd ZeroMic

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-windows.txt

# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt

# 3. Build Executable
# Windows
.\build.bat

# Linux / macOS
./build.sh
```
The packaged binary will be located in the `dist/` directory.

## ⚠️ FAQ

**Q: Mobile browser shows "Connection is not private"?**
A: This occurs because we use a self-signed certificate for LAN HTTPS (a mandatory requirement for WebRTC). Click "Advanced" -> "Proceed to..." in your browser to continue.

**Q: Why did my PC sound stop working after setup? (Windows)**
A: Windows sometimes sets the new virtual device as the default "Speaker". Click the volume icon in your taskbar and manually switch back to your original speakers/headphones.

**Q: "pactl command not found" on Linux?**
A: Ensure PulseAudio or PipeWire is installed. Most desktop distros include them. If missing: `sudo apt install pulseaudio-utils` (Debian/Ubuntu) or `sudo pacman -S pulseaudio` (Arch).

**Q: Error when clicking "Uninstall Driver"? (Windows)**
A: Ensure the software is running with **Administrator privileges**. It is recommended to restart your PC after uninstallation to completely clear the audio routing cache.

## 📄 License
This project is licensed under the [GPL-3.0 License](LICENSE). You are free to use, modify, and distribute the code, provided that all derivative works remain open-source under the same license.

---
*Created with ❤️ by Hypixice Studio.*
