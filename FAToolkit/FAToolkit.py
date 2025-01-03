import requests
import json
import os
import uuid
from typing import Dict


class flutterwave:
    def __init__(self, secret_key: str, threshold_amount: float):
        """
        Initializes the FlutterwavePayment class with the provided API secret key and threshold amount.
        """
        self.secret_key = secret_key
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        self.thresholdAmount = threshold_amount
        self.transferURL = "https://api.flutterwave.com/v3/transfers"
        self.accountResolveURL = "https://api.flutterwave.com/v3/accounts/resolve"
        self.transferStatusURL = "https://api.flutterwave.com/v3/transfers"
        self.walletBalanceURL = "https://api.flutterwave.com/v3/payout-subaccounts/"

    def getTransferStatus(self, transactionReference: str) -> dict:
        """
        Retrieves the status of a bank transfer using Flutterwave's API.

        This function checks the current status of a transfer transaction 
        using the unique transaction reference. It communicates with Flutterwave's 
        API to fetch detailed information about the transfer.

        Parameters:
            transactionReference (str): 
                A unique identifier for the transaction, typically generated 
                when initiating the transfer. This is used to track the transaction.

        Returns:
            dict: 
                A dictionary containing the response from Flutterwave's transfer status API. 
                Key components of the response include:
                - `status` (str): The status of the request (e.g., "success", "failed").
                - `message` (str): A description of the request's result.
                - `data` (list, optional): If successful, this contains a list of transactions 
                matching the reference, with each transaction containing:
                    - `id` (int): Unique identifier for the transaction.
                    - `reference` (str): The transaction reference.
                    - `status` (str): The current status of the transaction 
                    (e.g., "SUCCESSFUL", "FAILED", "PENDING").
                    - `complete_message` (str): A detailed message about the transaction's state.
                    - `amount` (float): The amount transferred.

        Process:
            1. Constructs the API URL using the provided transaction reference.
            2. Makes a GET request to Flutterwave's transfer status endpoint.
            3. Parses the JSON response and returns it as a dictionary.
            
        Notes:
            - Handle network errors, timeouts, or invalid responses gracefully in the calling code.
        """
        status = "PENDING"
        url = f"{self.transferStatusURL}?reference={transactionReference}"
        while status == "PENDING":
            transferStatusResponse = json.loads(requests.get(url, headers= self.headers).text)
            status = transferStatusResponse['data'][0]['status'] 
        return transferStatusResponse

    def resolveAccount(self, accountNumber: str, bankCode: str) -> dict:
        """
        Resolves a bank account using Flutterwave's API.

        This function verifies the validity of a bank account by checking the provided 
        account number and bank code against Flutterwave's account resolution service. 
        It returns detailed information about the account, including the account holder's 
        name and status.

        Parameters:
            accountNumber (str): 
                The bank account number to be resolved. This should be a valid account 
                number associated with the specified bank code.
            bankCode (str): 
                The unique code identifying the bank where the account is held. This is 
                typically a numeric or alphanumeric code (e.g., "044" for Access Bank in Nigeria).

        Returns:
            dict: 
                A dictionary containing the response from Flutterwave's account resolution API. 
                This includes:
                - `status` (str): Indicates the success or failure of the resolution request 
                (e.g., "success", "failed").
                - `message` (str): A message describing the result of the resolution attempt.
                - `data` (dict, optional): If the resolution is successful, this contains 
                detailed information about the account, such as:
                    - `account_number` (str): The validated account number.
                    - `account_name` (str): The name of the account holder.

        Process:
            1. Prepares the payload with the `accountNumber` and `bankCode`.
            2. Makes a POST request to Flutterwave's account resolution endpoint.
            3. Parses the JSON response and returns it as a dictionary.

        Notes:
            - Handle potential network errors or invalid responses gracefully in the calling code.
        """
        
        resolutionPayload = {
            "account_number": accountNumber,
            "account_bank": bankCode
        }
        accountResolveResponse = json.loads(requests.post(self.accountResolveURL, json=resolutionPayload, headers= self.headers).text)
        return accountResolveResponse

    def makePaymentWithBankTransfer(self, recipientAccountNumber: str, recipientBankCode: str, userWalletID: str, transactionNarration: str, amountToTransfer: float) -> Dict[str, object]:
        
        """
        Initiates a bank transfer payment using Flutterwave's API.

        This function enables transferring funds from the user's wallet
        to a recipient's bank account. It handles key aspects such as validating the transfer 
        amount, resolving the recipient's account details, and performing the transfer through 
        a secure API call. The function ensures robust error handling to provide detailed feedback 
        in case of any failure during the process.

        The process flow includes:
        1. Validating the `amountToTransfer` to ensure it does not exceed the defined 
        `thresholdAmount`.
        2. Resolving the recipient's bank account using their account number and bank code 
        to verify the account details.
        3. Constructing the transfer payload, including details like the user's 
        wallet ID and a unique transaction reference (`tx_ref`).
        4. Making a POST request to Flutterwave's API with the prepared payload.
        5. Validating the response to determine the success or failure of the transfer 
        and providing appropriate feedback to the caller.

        Parameters:
            recipientAccountNumber (str): 
                The recipient's bank account number, used to identify the target account 
                for the transfer. Must be a valid account number in the recipient's bank.
            recipientBankCode (str): 
                The bank code corresponding to the recipient's bank. This is typically 
                a unique identifier for banks in Nigeria (e.g., "044" for Access Bank).
            userWalletID (str): 
                The ID of the user's wallet to debit the transfer amount. The wallet ID must be a valid 
                subaccount identifier within the Flutterwave system.
            transactionNarration (str): 
                A brief description or note about the transaction, which appears in the 
                transaction history and provides context for the transfer (e.g., "Payment for services").
            amountToTransfer (float): 
                The amount to be transferred in Nigerian Naira (NGN). Must be a positive value 
                not exceeding the defined `thresholdAmount`.

        Returns:
            dict: 
                A dictionary containing the outcome of the transaction. It includes:
                - `status` (str): Indicates whether the transfer was "SUCCESSFUL" or "FAILED".
                - `reason` (str): A detailed explanation for the outcome, providing reasons 
                for failure or confirmation of success.
                - `moreInfo` (dict/str): Additional information related to the transaction, 
                such as response data from Flutterwave's API, or an empty string if no further 
                details are available.

        Error Handling:
            - If the transfer amount exceeds the maximum limit, the function immediately 
            returns a failure response with an appropriate message.
            - If the recipient's account cannot be resolved (e.g., invalid account number 
            or bank code), the function provides a failure response with the error details 
            from the account resolution API.
            - If the transfer request fails due to network or API issues, the function 
            captures and relays the failure reason from the Flutterwave API.
            - If the transfer is successful but the subsequent status verification indicates 
            a failure, the function returns detailed failure information, including the 
            complete error message.

        Use Case Example:
            This function can be used in financial platforms or wallets that need to 
            integrate Flutterwave's transfer functionality. For example, a user initiates 
            a transfer of NGN 1,500 to another user with a narration such as "Loan repayment".
        """
        
        
        tx_ref = str(uuid.uuid1())
        
        if (amountToTransfer > self.thresholdAmount):
            return({
                'status': 'FAILED',
                'reason': f'the amount to send is above the maximum transfer amount allowed, try an amount less than {self.thresholdAmount}',
                'moreInfo': ''
            })
        
        resolveAccountResponse = self.resolveAccount(accountNumber = recipientAccountNumber,bankCode = recipientBankCode)
        
        if (resolveAccountResponse['status'] == "success" and resolveAccountResponse['data']['account_number'] == recipientAccountNumber):
            beneficiaryName =  resolveAccountResponse['data']['account_name']
            transferPayload = {
                        "account_bank": recipientBankCode,
                        "account_number": recipientAccountNumber,
                        "amount": amountToTransfer,
                        "currency": "NGN",
                        "beneficiary_name": beneficiaryName,
                        "debit_subaccount": userWalletID,
                        "reference": tx_ref,
                        "debit_currency": "NGN",
                        "narration": transactionNarration
                        }
            transferResponse = json.loads(requests.post(self.transferURL, json=transferPayload, headers=self.headers).text)
            
            if (transferResponse['status'] == "success"):
                transferStatusResponse = self.getTransferStatus(tx_ref)['data'][0]
                if (transferStatusResponse['status'] == "FAILED"):
                    return({
                            'status': 'FAILED',
                            'reason': transferStatusResponse['complete_message'],
                            'moreInfo': transferStatusResponse
                            })
                elif (transferStatusResponse['status'] == "SUCCESSFUL"):
                    return({
                            'status': 'SUCCESSFUL',
                            'reason': transferStatusResponse['complete_message'],
                            'moreInfo': transferResponse['data']
                            })
            else:
                return({
                        'status': 'FAILED',
                        'reason': transferResponse['message'],
                        'moreInfo': transferResponse['data']
                        })   
            
        else:
            return({
                    'status': 'FAILED',
                    'reason': resolveAccountResponse['message'],
                    'moreInfo': ""
                    })
        
    def getWalletBalance(self, userWalletID: str) -> dict:
        
        """
        Retrieves the balance of a user's wallet in NGN currency.

        This method uses the Flutterwave API to fetch the wallet balance for a specified 
        user wallet ID. It returns the balance details or an error response.

        Parameters:
            user_wallet_id (str): The unique identifier for the user's wallet.

        Returns:
            dict: A dictionary containing the wallet balance details, including the status
                and data. If the request fails, the dictionary will include the error
                message and additional information.
        """
        url = f"{self.walletBalanceURL}{userWalletID}/balances?currency=NGN"
        walletBalanceResponse = json.loads(requests.get(url, headers= self.headers).text)
        return walletBalanceResponse