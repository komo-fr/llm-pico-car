"""Internationalization resources for Pico Controller."""

import gradio as gr

i18n = gr.I18n(
    ja={
        # App header
        "app_title": "📝 🎤 🖼 Pico Controller",
        "progress_lamps_label": "処理ランプ",
        # Tabs
        "tab_text": "テキスト指示",
        "tab_audio": "音声指示",
        "tab_image": "画像指示",
        "tab_settings": "設定",
        # Common labels
        "send_button": "送信",
        "reset_button": "リセット",
        "status_label": "送信ステータス",
        "commands_label": "生成されたコマンド",
        # Text tab
        "text_input_label": "指示を入力",
        "text_input_placeholder": "前にちょっと進んで、止まって",
        # Audio tab
        "transcript_label": "文字起こし結果",
        # Image tab (uses common labels)
        # Settings tab
        "settings_step1": "Step 1｜現在の設定を読み込む",
        "settings_get_button": "現在の設定を取得",
        "settings_step2": "Step 2｜1秒間動かして、実際に進む距離や回転角度を測定する",
        "settings_1sec_operation": "1秒間の動作",
        "drive_forward": "直進 ↑",
        "drive_reverse": "後進 ↓",
        "turn_left": "左回転 ←",
        "turn_right": "右回転 →",
        "settings_step3": "Step 3｜Step 2で測定した値を `実測：1秒で進む距離` と `実測：1秒で回転する角度` に入力して設定する\n⚠️ `直進速度` / `回転速度` を変える場合は、設定後にStep 2からやり直してください",
        "cm_per_sec_label": "実測: 1秒で進む距離（cm_per_sec）",
        "drive_speed_label": "直進速度（drive_speed）",
        "degree_per_sec_label": "実測: 1秒で回転する角度（degree_per_sec）",
        "turn_speed_label": "回転速度（turn_speed）",
        "settings_button": "設定",
        "output_result": "出力結果",
        "status_output_label": "ステータス",
        # Status messages
        "transcription_complete": "文字起こし完了",
        "command_generation_complete": "コマンド生成完了",
        "transcription_failed": "文字起こしに失敗しました。終了します",
        "image_loaded": "画像読込完了",
    },
    en={
        # App header
        "app_title": "📝 🎤 🖼 Pico Controller",
        "progress_lamps_label": "Progress Status",
        # Tabs
        "tab_text": "Text Input",
        "tab_audio": "Voice Input",
        "tab_image": "Image Input",
        "tab_settings": "Settings",
        # Common labels
        "send_button": "Submit",
        "reset_button": "Reset",
        "status_label": "Processing Status",
        "commands_label": "Generated Commands",
        # Text tab
        "text_input_label": "Enter instruction",
        "text_input_placeholder": "Go straight and move a little to the right",
        # Audio tab
        "transcript_label": "Transcription Result",
        # Image tab (uses common labels)
        # Settings tab
        "settings_step1": "Step 1 | Load current settings.",
        "settings_get_button": "Get Current Settings",
        "settings_step2": "Step 2 | Move for 1 second and measure actual distance and rotation angle.",
        "settings_1sec_operation": "1-second operation",
        "drive_forward": "Forward ↑",
        "drive_reverse": "Reverse ↓",
        "turn_left": "Turn Left ←",
        "turn_right": "Turn Right →",
        "settings_step3": "Step 3 | Configure settings using values measured in Step 2.\n⚠️ If you change the drive speed or turn speed, please repeat from Step 2 after configuring.",
        "cm_per_sec_label": "Measured: Distance per second (cm_per_sec)",
        "drive_speed_label": "Drive speed (drive_speed)",
        "degree_per_sec_label": "Measured: Rotation angle per second (degree_per_sec)",
        "turn_speed_label": "Turn speed (turn_speed)",
        "settings_button": "Apply Settings",
        "output_result": "Output Result",
        "status_output_label": "Status",
        # Status messages
        "transcription_complete": "Transcription complete",
        "command_generation_complete": "Command generation complete",
        "transcription_failed": "Transcription failed. The process has been stopped.",
        "image_loaded": "Image loaded",
    },
)
