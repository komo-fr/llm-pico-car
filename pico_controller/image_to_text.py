import base64
import json
from typing import Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langsmith import traceable
from prompts.image_to_command import IMAGE_TO_COMMAND_PROMPT


@traceable(name="image_to_command")
def image_to_command(img_bytes: bytes) -> List[Dict[str, str | int]]:
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    messages = [
        SystemMessage(content=IMAGE_TO_COMMAND_PROMPT),
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,"
                        + base64.b64encode(img_bytes).decode()
                    },
                },
            ]
        ),
    ]

    # 実行
    response = llm(messages)

    instructions = response.content
    instructions = json.loads(instructions)
    return instructions


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    path = "pico_controller/images/test.png"
    with open(path, "rb") as f:
        img_bytes = f.read()

    instructions = image_to_command(img_bytes)
    print(instructions)
