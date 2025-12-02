from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GROQAPIKEY"),
    base_url="https://api.groq.com/openai/v1",
)



def webTranslation(latinText):
    response = client.responses.create(
        input=f"Latin to English translation for: {latinText}",
        model="openai/gpt-oss-20b",
    )
    return response.output_text


print(f"Latin: Maxima pars Graium Saturno et maxime Athenae conficiunt sacra, quae Cronia esse iterantur ab illis, eumque diem celebrant: per agros urbesque fere omnes exercent epulas laeti famulosque procurant quisque suos; nosterque itidem est mos traditus illinc iste, ut cum dominis famuli epulentur ibidem. \nEnglish: {webTranslation("Maxima pars Graium Saturno et maxime Athenae conficiunt sacra, quae Cronia esse iterantur ab illis, eumque diem celebrant: per agros urbesque fere omnes exercent epulas laeti famulosque procurant quisque suos; nosterque itidem est mos traditus illinc iste, ut cum dominis famuli epulentur ibidem.")}")