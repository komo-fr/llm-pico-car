import json
from typing import Dict, List, Literal

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from matplotlib import colors as mcolors
from prompts.text_to_command_prompt import TEXT_TO_COMMAND_PROMPT


def move(
    direction: Literal["forward", "reverse", "left", "right"], distance: int
) -> str:
    """directionの方向に、distanceの距離だけ移動する"""
    print(f"移動しました: {direction} {distance}")


@traceable(name="text_to_command")
def text_to_command(text: str) -> List[Dict[str, str | int]]:
    prompt = ChatPromptTemplate(
        [
            ("system", TEXT_TO_COMMAND_PROMPT),
            ("human", "指示: {text}"),
        ]
    )

    llm = init_chat_model(model="gpt-4.1", temperature=0)

    chain = prompt | llm
    result = chain.invoke({"text": text})
    instructions = result.content
    instructions = json.loads(instructions)
    instructions = _add_led_rgb(instructions)
    return instructions


def _add_led_rgb(commands: List[Dict[str, str | int]]) -> List[Dict[str, str | int]]:
    """
    コマンドを変換する
    """
    converted_commands = []
    for command in commands:
        if "led" in command:
            if command["led"]["color"] == "off":
                command["led"]["rgb"] = (0, 0, 0)
            else:
                rgb_float = mcolors.to_rgb(str(command["led"]["color"]))
                rgb_int = tuple(int(round(c * 255)) for c in rgb_float)
                command["led"]["rgb"] = rgb_int

        converted_commands.append(command)

    return converted_commands
