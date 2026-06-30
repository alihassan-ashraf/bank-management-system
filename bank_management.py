import streamlit as st


class BankManagementSystem:

    def create_account(self, accounts, account_no, name, phone, balance):
        account = {
            "Account No": account_no,
            "Name": name,
            "Phone": phone,
            "Balance": balance
        }
        accounts.append(account)

    def search_account(self, accounts, account_no):
        for account in accounts:
            if account["Account No"] == account_no:
                return account
        return None

    def deposit_money(self, account, amount):
        account["Balance"] = account["Balance"] + amount

    def withdraw_money(self, account, amount):
        if amount <= account["Balance"]:
            account["Balance"] = account["Balance"] - amount
            return True
        else:
            return False

    def delete_account(self, accounts, account_no):
        account = self.search_account(accounts, account_no)

        if account is not None:
            accounts.remove(account)
            return True
        else:
            return False


bank = BankManagementSystem()

st.set_page_config(page_title="Bank Management System", page_icon="🏦")

st.title("🏦 Bank Management System")
st.write("A simple Python Streamlit app to manage bank accounts and transactions.")

if "accounts" not in st.session_state:
    st.session_state.accounts = []

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Create Account",
        "View All Accounts",
        "Search Account",
        "Deposit Money",
        "Withdraw Money",
        "Check Balance",
        "Delete Account",
        "Bank Summary"
    ]
)

if menu == "Create Account":
    st.subheader("Create New Account")

    account_no = st.text_input("Enter Account Number")
    name = st.text_input("Enter Customer Name")
    phone = st.text_input("Enter Phone Number")
    balance = st.number_input("Enter Initial Balance", min_value=0.0, value=0.0)

    if st.button("Create Account"):
        if account_no == "" or name == "" or phone == "":
            st.warning("Please fill all fields.")
        else:
            existing_account = bank.search_account(st.session_state.accounts, account_no)

            if existing_account is not None:
                st.error("Account number already exists.")
            else:
                bank.create_account(st.session_state.accounts, account_no, name, phone, balance)
                st.success("Account created successfully!")

elif menu == "View All Accounts":
    st.subheader("All Bank Accounts")

    if len(st.session_state.accounts) == 0:
        st.info("No accounts available.")
    else:
        st.table(st.session_state.accounts)

elif menu == "Search Account":
    st.subheader("Search Account")

    account_no = st.text_input("Enter Account Number to Search")

    if st.button("Search"):
        account = bank.search_account(st.session_state.accounts, account_no)

        if account is not None:
            st.success("Account found!")
            st.write("Account No:", account["Account No"])
            st.write("Name:", account["Name"])
            st.write("Phone:", account["Phone"])
            st.write("Balance:", account["Balance"])
        else:
            st.error("Account not found.")

elif menu == "Deposit Money":
    st.subheader("Deposit Money")

    account_no = st.text_input("Enter Account Number")
    amount = st.number_input("Enter Amount to Deposit", min_value=0.0, value=0.0)

    if st.button("Deposit"):
        account = bank.search_account(st.session_state.accounts, account_no)

        if account is not None:
            if amount > 0:
                bank.deposit_money(account, amount)
                st.success("Amount deposited successfully!")
                st.write("Updated Balance:", account["Balance"])
            else:
                st.warning("Amount must be greater than zero.")
        else:
            st.error("Account not found.")

elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")

    account_no = st.text_input("Enter Account Number")
    amount = st.number_input("Enter Amount to Withdraw", min_value=0.0, value=0.0)

    if st.button("Withdraw"):
        account = bank.search_account(st.session_state.accounts, account_no)

        if account is not None:
            if amount > 0:
                result = bank.withdraw_money(account, amount)

                if result:
                    st.success("Amount withdrawn successfully!")
                    st.write("Updated Balance:", account["Balance"])
                else:
                    st.error("Insufficient balance.")
            else:
                st.warning("Amount must be greater than zero.")
        else:
            st.error("Account not found.")

elif menu == "Check Balance":
    st.subheader("Check Balance")

    account_no = st.text_input("Enter Account Number")

    if st.button("Check Balance"):
        account = bank.search_account(st.session_state.accounts, account_no)

        if account is not None:
            st.success("Account found!")
            st.write("Account Holder:", account["Name"])
            st.write("Current Balance:", account["Balance"])
        else:
            st.error("Account not found.")

elif menu == "Delete Account":
    st.subheader("Delete Account")

    account_no = st.text_input("Enter Account Number to Delete")

    if st.button("Delete"):
        deleted = bank.delete_account(st.session_state.accounts, account_no)

        if deleted:
            st.success("Account deleted successfully!")
        else:
            st.error("Account not found.")

elif menu == "Bank Summary":
    st.subheader("Bank Summary")

    total_accounts = len(st.session_state.accounts)
    total_balance = 0

    for account in st.session_state.accounts:
        total_balance = total_balance + account["Balance"]

    st.write("Total Accounts:", total_accounts)
    st.write("Total Bank Balance:", total_balance)
