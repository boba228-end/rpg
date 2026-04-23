from mistralai.client import Mistral
import os
meseges = [
    {
            "content": "ты находишся в 2d игре в мире спиритов(летающие огоньки)."
            "ты являешся мудрецом которому будут задовать вопросы. отвечай в стиле мудрого мага.не используй силволов не из алфовита или знаком препинания",
            "role": "system"
    }
          ]
def вопрос_ответ(vopros):
    meseges.append(
        {
                "content": vopros,
                "role": "user",
        }
    )
    with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", "4UjwANcuou3liWHT3BVZWpibKW15Vyan"),
    ) as mistral:

        res = mistral.chat.complete(model="mistral-small-latest", messages=meseges, stream=False)

        # Handle response
        otvet = res.choices[0].message.content
        meseges.append(
            {
                "content": otvet,
                "role": "assistant",
        }
        )
        print(res.choices[0].message.content)
        return(otvet)
вопрос_ответ("что такое кресло")