import argparse

import config
import gradio as gr
from audio_to_text import transcribe
from dotenv import load_dotenv
from image_to_text import image_to_command
from langsmith import traceable
from sender import (
    get_settings,
    reset_settings,
    send_commands,
    send_status,
    set_settings,
)
from text_to_command import text_to_command

STATUS_RECORDING_STARTED = "recording_started"
STATUS_AUDIO_TO_TEXT_STARTED = "audio_to_text_started"
STATUS_TEXT_TO_COMMAND_STARTED = "text_to_command_started"
STATUS_IMAGE_TO_TEXT_STARTED = "image_to_text_started"

load_dotenv()


@traceable(name="handler_text_input")
def handler_text_input(text: str):
    send_status(STATUS_TEXT_TO_COMMAND_STARTED)
    commands = text_to_command(text)
    response = send_commands(commands)
    status = response.get("status")
    return commands, status


@traceable(name="handler_audio_input")
def handler_audio_input(audio_file):
    send_status(STATUS_AUDIO_TO_TEXT_STARTED)
    success, text = transcribe(audio_file)
    if success:
        yield text, None, "文字起こし完了", render_lamps(["s", "u", "u"])
        send_status(STATUS_TEXT_TO_COMMAND_STARTED)
        commands = text_to_command(text)
        yield text, commands, "コマンド生成完了", render_lamps(["s", "s", "u"])
        response = send_commands(commands)
        status = response.get("status")
        yield text, commands, status, render_lamps(["s"] * 3)
    else:
        yield (
            text,
            None,
            "文字起こしに失敗しました。終了します",
            render_lamps(["e", "u", "u"]),
        )


def handler_button_get_settings():
    response = get_settings()
    settings = response.get("settings")
    return (
        response.get("status"),
        settings.get("drive_speed"),
        settings.get("cm_per_sec"),
        settings.get("turn_speed"),
        settings.get("degree_per_sec"),
    )


def handler_button_set_settings(drive_speed, cm_per_sec, turn_speed, degree_per_sec):
    dict_settings = {
        "drive_speed": drive_speed,
        "cm_per_sec": cm_per_sec,
        "turn_speed": turn_speed,
        "degree_per_sec": degree_per_sec,
    }
    response = set_settings(dict_settings)
    return response.get("status")


def handler_button_reset_settings():
    response = reset_settings()
    settings = response.get("settings")
    return (
        response.get("status"),
        settings.get("drive_speed"),
        settings.get("cm_per_sec"),
        settings.get("turn_speed"),
        settings.get("degree_per_sec"),
    )


def handler_button_drive_forward_sec():
    response = send_commands([{"action": {"type": "forward", "drive_sec": 1}}])
    return response.get("status")


def handler_button_drive_reverse_sec():
    response = send_commands([{"action": {"type": "reverse", "drive_sec": 1}}])
    return response.get("status")


def handler_button_turn_left_sec():
    response = send_commands(
        [{"action": {"type": "turn", "direction": "left", "turn_sec": 1}}]
    )
    return response.get("status")


def handler_button_turn_right_sec():
    response = send_commands(
        [{"action": {"type": "turn", "direction": "right", "turn_sec": 1}}]
    )
    return response.get("status")


def handler_button_image_input(im):
    send_status(STATUS_IMAGE_TO_TEXT_STARTED)
    with open(im["composite"], "rb") as f:
        img_bytes = f.read()
    yield None, "画像読込完了", render_lamps(["s", "u", "u"])
    commands = image_to_command(img_bytes)
    yield commands, "コマンド生成完了", render_lamps(["s", "s", "u"])
    response = send_commands(commands)
    status = response.get("status")
    yield commands, status, render_lamps(["s"] * 3)


def render_lamps(status: list[str]) -> str:
    colors = ["gray"] * len(status)
    color_map = {"s": "limegreen", "u": "gray", "e": "red"}
    for i, s in enumerate(status):
        colors[i] = color_map[s]

    html = "<div style='display: flex; gap: 10px;'>"
    for color in colors:
        html += f"<div style='width: 20px; height: 20px; border-radius: 50%; background: {color};'></div>"  # noqa: E501
    html += "</div>"
    return html


def start_recording_handler():
    send_status(STATUS_RECORDING_STARTED)


def launch_gradio():
    with gr.Blocks() as demo:
        with gr.Row(variant="default"):
            with gr.Column(variant="default", scale=1):
                gr.Markdown("### 📝 🎤 🖼 Pico Controller")

            with gr.Column(variant="default", scale=4):
                progress_lamps = gr.HTML(
                    label="処理ランプ", value=render_lamps(["u"] * 3)
                )

        with gr.Tab("テキスト指示"):
            # 部品の定義
            text_input = gr.Textbox(
                label="指示を入力", placeholder="前にちょっと進んで、止まって"
            )
            text_send_button = gr.Button("送信", variant="primary")
            text_status_output = gr.Textbox(label="送信ステータス")
            text_commands_output = gr.JSON(label="生成されたコマンド")
            # クリックイベントの設定
            text_send_button.click(
                handler_text_input,
                inputs=text_input,
                outputs=[text_commands_output, text_status_output],
            )

        with gr.Tab("音声指示"):
            # 部品の定義
            audio_input = gr.Audio(
                sources=["microphone"], type="filepath", format="wav"
            )
            with gr.Row():
                audio_send_button = gr.Button("送信", variant="primary")
                audio_reset_button = gr.Button("リセット", variant="secondary")

            audio_transcript_output = gr.Textbox(label="文字起こし結果")
            audio_status_output = gr.Textbox(label="送信ステータス")
            audio_commands_output = gr.JSON(label="生成されたコマンド")

            # クリックイベントの設定
            audio_send_button.click(
                handler_audio_input,
                inputs=audio_input,
                outputs=[
                    audio_transcript_output,
                    audio_commands_output,
                    audio_status_output,
                    progress_lamps,
                ],
            )
            audio_reset_button.click(
                fn=lambda: (None, "", None, ""),
                inputs=[],
                outputs=[
                    audio_input,
                    audio_transcript_output,
                    audio_commands_output,
                    audio_status_output,
                ],
            )
            audio_input.start_recording(fn=start_recording_handler)
            audio_input.stop_recording(
                fn=handler_audio_input,
                inputs=audio_input,
                outputs=[
                    audio_transcript_output,
                    audio_commands_output,
                    audio_status_output,
                    progress_lamps,
                ],
            )

        with gr.Tab("画像指示"):
            # 部品の定義
            with gr.Row():
                image_input = gr.ImageEditor(
                    type="filepath",
                    crop_size="1:1",
                    format="png",
                    brush=gr.Brush(colors=["black"], default_size=10),
                )
                image_send_button = gr.Button("送信", variant="primary")

            image_status_output = gr.Textbox(label="送信ステータス")
            image_commands_output = gr.JSON(label="生成されたコマンド")
            # クリックイベントの設定
            image_send_button.click(
                handler_button_image_input,
                inputs=image_input,
                outputs=[image_commands_output, image_status_output, progress_lamps],
            )

        with gr.Tab("設定"):
            # 部品の定義
            gr.Markdown("### Step 1｜現在の設定を読み込む")
            with gr.Row():
                settings_get_button = gr.Button("現在の設定を取得", variant="primary")

            # ---- Step 2 ----
            gr.HTML("<hr>")
            gr.Markdown("### Step 2｜1秒間動かして、実際に進む距離や回転角度を測定する")
            with gr.Row("1秒間の動作"):
                drive_forward_sec_button = gr.Button(
                    "直進 ↑", variant="secondary", scale=0
                )
                drive_reverse_sec_button = gr.Button(
                    "後進 ↓", variant="secondary", scale=0
                )
                turn_left_sec_button = gr.Button(
                    "左回転 ←", variant="secondary", scale=0
                )
                turn_right_sec_button = gr.Button(
                    "右回転 →", variant="secondary", scale=0
                )

            # ---- Step 3 ----
            gr.HTML("<hr>")
            gr.Markdown("""### Step 3｜Step 2で測定した値を `実測：1秒で進む距離` と `実測：1秒で回転する角度` に入力して設定する
⚠️ `直進速度` / `回転速度` を変える場合は、設定後にStep 2からやり直してください""")  # noqa: E501
            with gr.Row():
                with gr.Column():
                    # 直進に関する設定
                    cm_per_sec_input = gr.Number(
                        label="実測: 1秒で進む距離（cm_per_sec）",
                        placeholder=10,
                        interactive=True,
                    )
                    drive_speed_input = gr.Number(
                        label="直進速度（drive_speed）",
                        placeholder=20,
                        interactive=True,
                    )

                with gr.Column():
                    # 回転に関する設定
                    degree_per_sec_input = gr.Number(
                        label="実測: 1秒で回転する角度（degree_per_sec）",
                        placeholder=6 / 5,
                        interactive=True,
                    )
                    turn_speed_input = gr.Number(
                        label="回転速度（turn_speed）", placeholder=80, interactive=True
                    )
                with gr.Column():
                    settings_set_button = gr.Button("設定", variant="primary")
                    settings_reset_button = gr.Button("リセット", variant="secondary")
            gr.HTML("<hr>")
            gr.Markdown("### 出力結果")
            with gr.Row():
                settings_status_output = gr.Textbox(label="ステータス")

            # クリックイベントの設定
            settings_get_button.click(
                handler_button_get_settings,
                outputs=[
                    settings_status_output,
                    drive_speed_input,
                    cm_per_sec_input,
                    turn_speed_input,
                    degree_per_sec_input,
                ],
            )

            settings_set_button.click(
                handler_button_set_settings,
                inputs=[
                    drive_speed_input,
                    cm_per_sec_input,
                    turn_speed_input,
                    degree_per_sec_input,
                ],
                outputs=[settings_status_output],
            )

            settings_reset_button.click(
                handler_button_reset_settings,
                outputs=[
                    settings_status_output,
                    drive_speed_input,
                    cm_per_sec_input,
                    turn_speed_input,
                    degree_per_sec_input,
                ],
            )

            drive_forward_sec_button.click(
                handler_button_drive_forward_sec, outputs=[settings_status_output]
            )
            drive_reverse_sec_button.click(
                handler_button_drive_reverse_sec, outputs=[settings_status_output]
            )
            turn_left_sec_button.click(
                handler_button_turn_left_sec, outputs=[settings_status_output]
            )
            turn_right_sec_button.click(
                handler_button_turn_right_sec, outputs=[settings_status_output]
            )

    demo.launch(server_name="0.0.0.0", share=True)


def main():
    # mode = os.getenv("MODE", "cli")
    mode = "gradio"

    if mode == "gradio":
        launch_gradio()
    else:
        text = input("指示: ")
        commands = text_to_command(text)
        response = send_commands(commands)
        status = response.get("status")
        print("送信されたコマンド:", commands)
        print("レスポンス:", status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="mockモードで起動する")
    args = parser.parse_args()
    config.setup(use_mock=args.mock)

    main()
