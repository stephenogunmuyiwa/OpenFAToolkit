"""

OpenFAToolkit (Open Finance Agent Toolkit) is an open-source framework for adding fintech tools such as wallets, being able to make bill payments, or send money accross several channels, to your AI agent.
# Quick Example with Google Gemini & Flutterwave wallet

  >>> import google.generativeai as genai
  >>> from dotenv import load_dotenv
  >>> from FAToolkit import flutterwave
  >>> import os
  >>> load_dotenv()

  >>> genai.configure(api_key= os.getenv('GEMINI_API_KEY'))
  >>> flw = flutterwave(secret_key=os.getenv('FLW_SEC_KEY'), threshold_amount=1000)

  >>> generation_config = {
                          "temperature": 1,
                          "top_p": 0.95,
                          "top_k": 40,
                          "max_output_tokens": 8192,
                          "response_mime_type": "text/plain",
                        }

  >>> model = genai.GenerativeModel(
                              model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              system_instruction = "you are a finance agent that can help users make bank trasfers, and check wallet balances",
                              tools=[flw.makePaymentWithBankTransfer, flw.getWalletBalance]
                              )
  >>> chat_session = model.start_chat(
                                      enable_automatic_function_calling=True,
                                      history = []
                                      )
  >>> response = chat_session.send_message("I want to make a transfer of 1000 naira to this account number <receipentAccountNumber>, the bank code is <receipentBankCode> my walletID is <userWalletID> for his barbing service but before you make the transfer tell me how much I have in my wallet")
  >>> print(response.text)
"""

from .FAToolkit import flutterwave

__all__ = ['flutterwave']
