import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = """Você é a Brain, uma assistente virtual especializada em educação financeira da plataforma Dinhero. 
Seu objetivo é ajudar os usuários com dúvidas sobre:
- Conteúdos dos cursos da plataforma
- Conceitos de educação financeira
- Dúvidas gerais sobre finanças pessoais
- Investimentos básicos
- Controle financeiro e orçamento

Seja sempre educada, clara e objetiva. Use uma linguagem acessível e exemplos práticos quando possível.
Se a pergunta não for relacionada a finanças, gentilmente redirecione o usuário para tópicos financeiros."""


def chat_with_brain(message: str, conversation_history: list = None):
    try:
        contents = []
        
        contents.append(types.Content(
            role='user',
            parts=[types.Part(text=SYSTEM_PROMPT)]
        ))
        contents.append(types.Content(
            role='model',
            parts=[types.Part(text="Entendido! Estou pronta para ajudar com dúvidas sobre educação financeira.")]
        ))
        
        if conversation_history:
            for item in conversation_history:
                role = 'user' if item['role'] == 'user' else 'model'
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part(text=item['content'])]
                ))
        
        contents.append(types.Content(
            role='user',
            parts=[types.Part(text=message)]
        ))
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=1024,
            )
        )
        
        return {
            'success': True,
            'response': response.text,
            'model': 'gemini-2.0-flash-exp'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'response': 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.'
        }


def get_welcome_message():
    return {
        'role': 'assistant',
        'content': 'Olá! Eu sou a Brain, sua assistente de educação financeira! 💡 Estou aqui para te ajudar com dúvidas sobre os conteúdos da plataforma ou questões gerais sobre finanças. Como posso te ajudar hoje?'
    }
