from config.config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
def summarize_chats(chats_df, prompt):
    content = "\n".join(chats_df["message"].tolist())
    final_prompt = f"{prompt}\n\nChat Data:\n{content}"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant summarizing WhatsApp chats."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.5,
        max_tokens=600
    )
    return response.choices[0].message.content