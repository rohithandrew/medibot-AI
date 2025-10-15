import os
from dotenv import load_dotenv
import pywhatkit
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model("gpt-4o-mini", model_provider="openai")

ALERT_NUMBER = "+7010722108"

def send_whatsapp_alert(message, phone_number=ALERT_NUMBER):
    try:
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
        print("Alert message sent successfully.")
    except Exception as e:
        print("An error occurred while sending the alert message:", e)

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
- Do NOT use any markdown formatting (such as asterisks, hashes, backticks, or dashes) in your answer. Use only plain text with complete sentences and normal paragraphs.
- Ask only 2 or 3 specific, concise questions based on the user's latest input to understand the situation.
- After asking these questions (in one response), do not proceed further before getting user answers.
- Format your response as a short list of questions, with each question as a plain sentence.

Conversation so far:
{conversation_history}
Bot: """
            response = model.invoke(prompt)
            print("\nBot response:")
            print(response.content)
            conversation_history += f"Bot: {response.content}\n"

            question_phase = False
        else:
            prompt = f"""
You are a medical AI assistant analyzing an emergency situation based on all information gathered.

Instructions:
- Do NOT use any markdown formatting (such as asterisks, hashes, backticks, or dashes) in your answer. Use only plain text with complete sentences and normal paragraphs.
- Provide a detailed response comprising 3 paragraphs:
  1. Explanation of the current issue based on user inputs.
  2. Possible risks or complications that might arise if untreated.
  3. Preventive measures and immediate actions the user should take.

Conversation so far:
{conversation_history}
User: {user_input}
Bot:  """
            response = model.invoke(prompt)
            print("\nBot response:")
            print(response.content)
            conversation_history += f"Bot: {response.content}\n"

def analyze_critical_condition(spO2, temperature, heart_rate):
    abnormalities = []
    if spO2 < 95:
        abnormalities.append(f"SpO2 is low at {spO2}%, indicating potential hypoxemia.")
    if temperature < 36.1 or temperature > 37.2:
        abnormalities.append(f"Temperature is abnormal at {temperature}°C, which could indicate fever or hypothermia.")
    if heart_rate < 60:
        abnormalities.append(f"Heart rate is low at {heart_rate} bpm (bradycardia).")
    elif heart_rate > 100:
        abnormalities.append(f"Heart rate is high at {heart_rate} bpm (tachycardia).")
    return abnormalities

def iot_vitals_analysis(spO2, temperature, heart_rate):
    prompt = (
        f"The patient has the following vital signs:\n"
        f"SpO2: {spO2}%\n"
        f"Temperature: {temperature}°C\n"
        f"Heart Rate (ECG): {heart_rate} bpm\n"
        "Instructions:\n"
        "- Analyze each vital sign individually, making sure to check for:\n"
        "  * Normal SpO2 (95-100%).\n"
        "  * Normal temperature (36.1°C to 37.2°C).\n"
        "  * Normal heart rate 60–100 bpm. Below 60 is bradycardia, above 100 is tachycardia.\n"
        "- Identify if any value is abnormal and describe what this may indicate for the patient's health.\n"
        "- Advise on what should be done for patient safety.\n"
        "- Do NOT use any markdown formatting (such as asterisks, hashes, backticks, or dashes) in your answer. Use only plain text with complete sentences and normal paragraphs."
    )
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
                user_hr = input("Enter Heart Rate (bpm) (or 'quit' to exit): ").strip()
                if user_hr.lower() == "quit":
                    print("Exiting Vital Signs Monitoring mode.")
                    break

                try:
                    spO2_val = float(user_spo2)
                    temp_val = float(user_temp)
                    hr_val = float(user_hr)
                except ValueError:
                    print("Invalid input for SpO2, temperature, or heart rate. Please try again.")
                    continue

                bot_response = iot_vitals_analysis(spO2_val, temp_val, hr_val)
                print("\nBot response:")
                print(bot_response)

                abnormalities = analyze_critical_condition(spO2_val, temp_val, hr_val)
                if abnormalities:
                    alert_message = (
                        "Critical Alert! Patient vitals show abnormalities:\n" + "\n".join(abnormalities)
                    )
                    send_whatsapp_alert(alert_message)

        else:
            print("Invalid mode choice. Please select 1, 2, or Q.")


if __name__ == "__main__":
    main()