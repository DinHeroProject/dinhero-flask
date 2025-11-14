import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

MAX_OUTPUT_TOKENS = int(os.getenv('BRAIN_MAX_TOKENS', 1024)) 
MAX_HISTORY_MESSAGES = int(os.getenv('BRAIN_MAX_HISTORY', 8))

SYSTEM_PROMPT = """Você é a Brain, uma assistente virtual especializada em educação financeira da plataforma Dinhero. 
Seu objetivo é ajudar os usuários com dúvidas sobre:
- Conteúdos dos cursos da plataforma
- Conceitos de educação financeira
- Dúvidas gerais sobre finanças pessoais
- Investimentos básicos
- Controle financeiro e orçamento

Seja sempre educada, clara e objetiva. Use uma linguagem acessível e exemplos práticos quando possível.
IMPORTANTE: Mantenha suas respostas concisas e diretas, sem ser prolixo.
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
            limited_history = conversation_history[-MAX_HISTORY_MESSAGES:] if len(conversation_history) > MAX_HISTORY_MESSAGES else conversation_history
            
            for item in limited_history:
                role = 'user' if item['role'] == 'user' else 'model'
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part(text=item['content'])]
                ))
        
        # Adiciona a mensagem atual
        contents.append(types.Content(
            role='user',
            parts=[types.Part(text=message)]
        ))
        
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=MAX_OUTPUT_TOKENS, 
            )
        )
        
        return {
            'success': True,
            'response': response.text,
            'model': 'gemini-2.5-flash-lite'
        }
        
    except Exception as e:
        print(e)
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
