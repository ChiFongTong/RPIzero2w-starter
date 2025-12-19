# Raspberry Pi Zero 2 W 快速上手教學 (Raspberry Pi OS Lite)
*撰寫人:T90，2025/12/19。*

這份教學將引導你如何在 Raspberry Pi Zero 2 W 上安裝 Raspberry Pi OS Lite (64-bit)，並透過 Windows 或 MAC 進行遠端開發，最後部署一個 ChatGPT CLI 應用程式。

## **本教學的終端機指令在 Windows 或 MAC 環境都幾乎一致，請放心服用。**

## 1. 系統安裝與設定 (Raspberry Pi Imager)

我們使用官方工具將作業系統燒錄到 MicroSD 卡，並預先設定好 WiFi 與 SSH。請準備好 MicroSD 卡及讀卡機，並插入到電腦中備用。

1.  下載並安裝 [Raspberry Pi Imager](https://www.raspberrypi.com/software/)。(本教學使用之版本為v2.0.0)

2.  **選擇裝置 (Select your Raspberry Pi device)**:選擇 `Raspberry Pi Zero 2 W`。

3.  **選擇作業系統 (Choose Operating system)**:
    *   因為 **`Pi Zero 2w`** 的記憶體只有512mb，剛好足夠運行桌面環境(GUI)，但若同時執行其他任務則非常勉強，故我們選擇無桌面環境(CLI)來進行使用。
    *   點選 **`Raspberry Pi OS (other)`** 。
    *   選擇 **`Raspberry Pi OS Lite (64-bit)`** (無桌面環境，CLI操作)。

4.  **選擇儲存裝置 (Choose your Storage device)**:選擇你的 MicroSD 卡。如無可選項，請檢查SD卡是否已被電腦識別，並回到第一步。
    
    *   勾選 **`Exclude system drives`** 用於清除sd卡內原有系統
5.  **自訂義配置 (Customisation)**:
    *   **Customisation 分頁**:
        *   設定 **Hostname** (主機名稱)，例如: **`rpi-zero`**。
        
        *   設定 **Localisation** (地區)，例如: **Capital city** : **`Taipie(Tawian)`**，**Time zone** : **`Asia/Taipei`**，**keyboard** : **`tw`**。

        *   設定 **User** (使用者)，例如 : **Username** : **`pi`**，**Password** : **`raspberry`**。
            *   請牢記你的**Hostname**、**Username**、**Password**，我們會在後續遠端連線(SSH)中經常使用
        
        *   設定 **Wi-Fi**，輸入你的 WiFi 名稱 (SSID) 與密碼。
            *   也可以 **`skip`** ，但我們會在後續遠端連線(SSH)，故請填寫。
            *   注意查看RPI的WiFi頻段支援， **`Pi Zero 2w`** 只能使用2.4Ghz
        
        *   設定 **SSH authentication**:
            *   勾選 **Enable SSH**，選擇 **`Use password authentication`**。
        
        *   設定 **Raspberry Pi Connect**
            *   **Disable**即可。這是樹莓派官方開發的遠端連線，若有需要可勾選。

6.  設定完成後點擊 **Next**，檢查所有配置項，然後點擊 **Write** 開始下載映像並燒錄。
     *  燒錄完成並將 SD 卡插入 Raspberry Pi 並接電。
     *  首次開機需等待約 3-5 分鐘，若在燒錄時有設定WiFi，會自動連接。
     *  你可以觀察板上的黃綠色LED燈是否閃爍，當它不再閃爍，長亮時即開機完成。



## 2. SSH 連線
1.  確定您的電腦與RPI在同一區域網絡中。
2.  在 Windows 開啟 **PowerShell** 或 **命令提示字元 (CMD)**。
3.  輸入以下指令連線 (請將 **`pi`** 換成你設定的帳號，**`rpi-zero`** 換成你設定的主機名稱):
    ```powershell
    ssh pi@rpi-zero.local
    ```
4.  第一次連線會詢問指紋確認，輸入 **`yes`**。
5.  輸入密碼登入，輸入時密碼會看不見，是正常情況。



## 3. 撰寫 Python Hello World

登入後，我們先用最簡單的方式寫一個 Python 程式。

1.  使用 **`nano`** 編輯器建立檔案:
    ```bash
    nano helloworld.py
    ```
2.  輸入以下程式碼:
    ```python
    print("Hello World...")
    ```
3.  存檔並離開:按 **`Ctrl + O`** (存檔) -> **`Enter`** -> **`Ctrl + X`** (離開)。
4.  執行程式:
    ```bash
    python helloworld.py
    ```
    *你應該會看到終端機印出 "Hello World..."。*



## 4. 建立 Hello Website 並執行

接著我們建立一個簡單的網頁，並用 Python 內建的 HTTP Server 讓它跑起來。

1.  建立資料夾並進入:
    ```bash
    mkdir hello_website
    cd hello_website
    ```
2.  建立 **`index.html`**:
    ```bash
    nano index.html
    ```
3.  貼上以下 HTML 內容:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello from Raspberry Pi</title>
    </head>
    <body>
        <h1>Hello World from Raspberry Pi Zero 2 W!</h1>
        <p>這是跑在樹莓派上的網站</p>
    </body>
    </html>
    ```
4.  存檔並離開:按 **`Ctrl + O`** (存檔) -> **`Enter`** -> **`Ctrl + X`** (離開)。
5.  使用 Python 啟動網頁伺服器 (Port 8000或自訂):
    ```bash
    python -m http.server 8000
    ```
6.  在 Windows 的瀏覽器輸入 `http://rpi-zero.local:8000`，即可看到網頁，`rpi-zero`改為您設定的Hostname。
    *(按 `Ctrl + C` 可停止伺服器)*



## 5. 使用 rsync 部署 AI Chat CLI

最後，我們將電腦上的 `AI_chat_CLI` 專案傳送到 Raspberry Pi 並執行。

### 步驟 A: 傳送檔案 (在 Windows 端執行)

請確保你的 Windows 有安裝 `rsync` (可透過 Git Bash 或 WSL 使用)。如果沒有，也可以使用 `scp`。

在專案根目錄 (`RPI_start` 資料夾) 開啟終端機:
**(請換成你的 User@Hostname)**
```bash
# 使用 rsync (推薦)
rsync -avz -e ssh ./AI_chat_CLI pi@rpi-zero.local:~/

# 或者使用 scp (Windows PowerShell 內建)
scp -r .\AI_chat_CLI pi@rpi-zero.local:~/
```

### 步驟 B: 安裝依賴與執行 (在 Raspberry Pi 端執行)

1.  回到 Raspberry Pi 的 SSH視窗，進入資料夾:
    ```bash
    cd ~/AI_chat_CLI
    ```
2.  建立 Python 虛擬環境 (建議做法，避免汙染系統環境):
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  安裝 OpenAI 套件:
    ```bash
    pip install openai
    ```
4.  設定 API Key 並執行:
    ```bash
    # 設定環境變數 (請換成你的 Key)
    export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxx"

    # 執行程式
    python main.py
    ```

現在，你可以在 Raspberry Pi 的終端機上與 ChatGPT 對話了！