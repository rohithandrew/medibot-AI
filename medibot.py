import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model("gpt-4o-mini", model_provider="openai")

def emergency_assistance_loop():
    print("\nEmergency Assistance Mode - type 'quit' to exit this mode.")
    conversation_history = ""
    question_phase = True 

    while True:
        user_input = input("\nDescribe the emergency or respond: ").strip()
        if user_input.lower() == "quit":
            print("Exiting Emergency Assistance mode.")
            break

        conversation_history += f"User: {user_input}\n"

        if question_phase:
            prompt = f"""
You are a medical AI assistant handling an emergency situation.

Instructions:
- Ask only 2 or 3 specific, concise questions based on the user's latest input to understand the situation.
- After asking these questions (in one response), do not proceed further before getting user answers.
- Format your response as a short list of questions.

Conversation so far:
{conversation_history}
Bot:
"""
            response = model.invoke(prompt)
            print("\nBot response:")
            print(response.content)
            conversation_history += f"Bot: {response.content}\n"

            question_phase = False
        else:
            prompt = f"""
You are a medical AI assistant analyzing an emergency situation based on all information gathered.

Instructions:
- Provide a detailed response comprising 3 paragraphs:
  1. Explanation of the current issue based on user inputs.
  2. Possible risks or complications that might arise if untreated.
  3. Preventive measures and immediate actions the user should take.

Conversation so far:
{conversation_history}
User: {user_input}
Bot:
"""
            response = model.invoke(prompt)
            print("\nBot response:")
            print(response.content)
            conversation_history += f"Bot: {response.content}\n"

def iot_vitals_analysis(spO2, temperature):
    prompt = f"Patient SpO2: {spO2}%, Temperature: {temperature}°C.\n" \
             "Analyze these vitals, identify abnormalities, and advise what to do for patient safety."
    response = model.invoke(prompt)
    return response.content

def main():
    print("Medical Assistant Bot")

    while True:
        print("\nChoose mode:")
        print("1 - Emergency Assistance")
        print("2 - Vital Signs Monitoring")
        print("Q - Quit")
        mode = input("Enter mode number (or Q to quit): ").strip().lower()

        if mode == "q":
            print("Exiting. Stay safe!")
            break

        elif mode == "1":
            emergency_assistance_loop()

        elif mode == "2":
            print("\nVital Signs Monitoring Mode - type 'quit' to exit this mode.")
            while True:
                user_spo2 = input("Enter SpO2 (%) (or 'quit' to exit): ").strip()
                if user_spo2.lower() == "quit":
                    print("Exiting Vital Signs Monitoring mode.")
                    break
                user_temp = input("Enter Temperature (°C): ").strip()
                if user_temp.lower() == "quit":
                    print("Exiting Vital Signs Monitoring mode.")
                    break

                try:
                    spO2_val = float(user_spo2)
                    temp_val = float(user_temp)
                except ValueError:
                    print("Invalid numeric input for SpO2 or temperature. Please try again.")
                    continue

                bot_response = iot_vitals_analysis(spO2_val, temp_val)
                print("\nBot response:")
                print(bot_response)

        else:
            print("Invalid mode choice. Please select 1, 2, or Q.")

if __name__ == "__main__":
    main()