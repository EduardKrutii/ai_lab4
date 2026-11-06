import sys
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL_NAME = "qwen2.5:1.5b"

def generate_flashcards(text):
    system_prompt = (
        "Ти професійний асистент для студентів. Твоє завдання - створювати навчальні картки (Flashcards) "
        "з наданого тексту. Формат відповіді має бути суворим:\n"
        "Питання: [Тут питання]\nВідповідь: [Тут коротка відповідь]\n\n"
        "Створи стільки карток, скільки головних ідей є в тексті. Не пиши ніяких вступних слів."
        "Відповідай ТІЛЬКИ українською мовою. Формат відповіді має бути суворим: лише одне Питання і лише одна Відповідь."
    )
    
    print("\nАналізую текст та генерую картки (чекайте)...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=800,
            stream=True
        )
        
        print("\n=== ВАШІ КАРТКИ ===")
        for chunk in response:
            if chunk.choices[0].delta.content:
                # Виводимо текст по мірі генерації
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n===================\n")
        
    except Exception as e:
        print(f"\nПомилка з'єднання: {e}")
        print("Переконайтеся, що Ollama запущена (команда: ollama serve) та модель завантажена.")

def main():
    print("AI-Генератор навчальних карток запущено!")
    print(f"Використовується модель: {MODEL_NAME}")
    print("Введіть текст конспекту (або 'вихід' для завершення):\n")
    
    while True:
        try:
            user_input = input("Текст: ")
            if user_input.lower() in ['вихід', 'exit', 'quit']:
                print("Завершення роботи. Хай щастить на іспитах!")
                break
            if not user_input.strip():
                continue
                
            generate_flashcards(user_input)
            
        except KeyboardInterrupt:
            print("\nЗавершення роботи.")
            sys.exit(0)

if __name__ == "__main__":
    main()