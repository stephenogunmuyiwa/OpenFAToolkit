<div align="center">
AI Agents can do Finance

[Docs](https://github.com/stephenohunmuyiwa/OpenFAToolkit/README.md) | [Examples](https://github.com/stephenohunmuyiwa/OpenFAToolkit/tree/python/examples) | [Twitter](https://x.com/stephenogunmuy1)

OpenFAToolkit is a free open source software, MIT licensed, built on the APIs of [Flutterwave](https://www.flutterwave.com) | [Paystack](https://www.paystack.com)

</div>

## OpenFAToolkit

OpenFAToolkit (Open Finance Agent Toolkit) is an open-source framework for adding fintech tools such as wallets, being able to make bill payments, or send money accross several channels, to your AI agent.

**Problem**:

Making agents perform financial transactions is tedious. The ecosystem is heavily fragmented, spanning 5+ popular agent development frameworks, multiple programming languages, and dozens of different fintech APIs and banking architectures.
For developers without expertise in using fintech APIs, being able to add finance caoablilities to your agents seems like an impossible task.

**Solution**:

OpenFAToolkit solves this by providing an open-source, all inclusive framework that makes it super easy to add fianac capabilities to your agents.

- **For agent developers**: OpenFAToolkit offers an always-growing catalog of ready made finance actions (sending money, paying bills, checking balance, ...) that can be imported as tools into your existing agent. It works with the most popular agent frameworks (Langchain, Openai, Gemini, etc), Typescript and Python, and many fintech wallet providers (Flutterwave, Paystack, ...).

### Key features

1. **Works Everywhere**: Compatible with Langchain, Openai, Gemini, and more.
2. **Wallet Agnostic**: Supports all fintech wallet providers (Flutterwave, Paystack, ...).
3. **Customizable & Open Sourced**: Use or add more tools for any finance functionality (sending money, checking wallet balance, etc) and analysis .

![OpenFAT](https://github.com/stephenogunmuyiwa/OpenFAToolkit/blob/python/assets/cover1.png?raw=true)

### How it works

OpenFAT plugs into your agents tool calling capabilities adding all the functions your agent needs to interact with the Fintech Wallts.

High-level, here's how it works:

#### Set up your environment variables

```.env
FLW_SEC_KEY ="########################################"
PAYSTK_SEC_KEY ="########################################"
GEMINI_API_KEY = "######################################"
```

#### Import from the Toolkit the fintech service you want

```python
import google.generativeai as genai
from dotenv import load_dotenv
from FAToolkit import flutterwave
import os
load_dotenv()

genai.configure(api_key= os.getenv('GEMINI_API_KEY'))
flw = flutterwave(secret_key=os.getenv('FLW_SEC_KEY'))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
```

#### Connect it to your agent framework of choice

```python
model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction = "you are a finance agent that can help users make bank trasfers, and check wallet balances",
            tools=[flw.makePaymentWithBankTransfer, flw.getWalletBalance]
            )
chat_session = model.start_chat(
    enable_automatic_function_calling=True,
    history = []
    )
response = chat_session.send_message("I want to make a transfer of 1000 naira to this account number <receipentAccountNumber>, the bank code is <receipentBankCode> my walletID is <userWalletID> for his barbing service but before you make the transfer tell me how much I have in my wallet")
print(response.text)
```

See [here](https://github.com/stephenohunmuyiwa/OpenFAToolkit/tree/python/examples) for more examples.
