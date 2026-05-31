import streamlit as st
from datetime import datetime
import random

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Bank App", page_icon="🏦", layout="centered")

# -----------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------
if "account_created" not in st.session_state:
    st.session_state.account_created = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "balance" not in st.session_state:
    st.session_state.balance = 0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "wrong_attempts" not in st.session_state:
    st.session_state.wrong_attempts = 0

if "account_locked" not in st.session_state:
    st.session_state.account_locked = False


# -----------------------------------
# FUNCTION TO CHECK ACCOUNT LOCK
# -----------------------------------
def check_lock():
    if st.session_state.wrong_attempts >= 3:
        st.session_state.account_locked = True


# -----------------------------------
# ACCOUNT LOCKED SCREEN
# -----------------------------------
if st.session_state.account_locked:
    st.title("🔒 ACCOUNT LOCKED")
    st.error("Too many wrong PIN attempts.")
    st.warning("Your account has been locked.")
    st.stop()


# -----------------------------------
# ACCOUNT CREATION PAGE
# -----------------------------------
if not st.session_state.account_created:

    st.title("🏦 Create Bank Account")

    name = st.text_input("Enter Full Name")
    address = st.text_area("Enter Address")
    mobile = st.text_input("Enter 10-digit Mobile Number")
    pin = st.text_input("Create 4-digit PIN", type="password")
    deposit = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create Account"):

        if len(mobile) != 10 or not mobile.isdigit():
            st.error("❌ Enter valid 10-digit mobile number")

        elif len(pin) != 4 or not pin.isdigit():
            st.error("❌ PIN must be exactly 4 digits")

        else:
            st.session_state.name = name
            st.session_state.address = address
            st.session_state.mobile = mobile
            st.session_state.pin = pin
            st.session_state.balance = deposit

            # Generate 12-digit account number
            st.session_state.account_number = random.randint(
                100000000000,
                999999999999
            )

            st.session_state.account_created = True

            # Add first transaction
            st.session_state.transactions.append(
                f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Account created with ₹{deposit}"
            )

            st.success("✅ Account Created Successfully!")

            # Refresh page immediately
            st.rerun()


# -----------------------------------
# LOGIN PAGE
# -----------------------------------
elif not st.session_state.logged_in:

    st.title("🏦 Login")

    login_name = st.text_input("Enter Name")
    login_pin = st.text_input(
        "Enter 4-digit PIN",
        type="password"
    )

    if st.button("Login"):

        if (
            login_name == st.session_state.name
            and login_pin == st.session_state.pin
        ):

            st.session_state.logged_in = True
            st.success("✅ Login Successful")

            # Refresh immediately
            st.rerun()

        else:

            st.session_state.wrong_attempts += 1
            check_lock()

            remaining = 3 - st.session_state.wrong_attempts

            st.error(
                f"❌ Invalid Name or PIN. Attempts left: {remaining}"
            )


# -----------------------------------
# HOME PAGE
# -----------------------------------
elif st.session_state.logged_in:

    st.title("🏦 BANK OF BANK")

    st.markdown("### 👤 Account Details")

    st.write(f"**Name:** {st.session_state.name}")
    st.write(
        f"**Account Number:** {st.session_state.account_number}"
    )

    # -----------------------------------
    # SIDEBAR MENU
    # -----------------------------------
    st.sidebar.title("📌 Menu")

    option = st.sidebar.radio(
        "Select Option",
        [
            "Deposit",
            "Withdraw",
            "Check Balance",
            "Transaction History",
            "Logout"
        ]
    )

    # -----------------------------------
    # DEPOSIT
    # -----------------------------------
    if option == "Deposit":

        st.subheader("💵 Deposit Money")

        amount = st.number_input(
            "Enter amount to deposit",
            min_value=1
        )

        if st.button("Deposit"):

            st.session_state.balance += amount

            st.session_state.transactions.append(
                f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Deposited ₹{amount}"
            )

            st.success("✅ Amount deposited successfully")


    # -----------------------------------
    # WITHDRAW
    # -----------------------------------
    elif option == "Withdraw":

        st.subheader("💸 Withdraw Money")

        amount = st.number_input(
            "Enter amount to withdraw",
            min_value=1
        )

        entered_pin = st.text_input(
            "Enter PIN",
            type="password"
        )

        if st.button("Withdraw"):

            if entered_pin == st.session_state.pin:

                if amount <= st.session_state.balance:

                    st.session_state.balance -= amount

                    st.session_state.transactions.append(
                        f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Withdrawn ₹{amount}"
                    )

                    st.success(
                        "✅ Amount withdrawn successfully"
                    )

                else:
                    st.error("❌ Insufficient balance")

            else:

                st.session_state.wrong_attempts += 1
                check_lock()

                remaining = 3 - st.session_state.wrong_attempts

                st.error(
                    f"❌ Wrong PIN. Attempts left: {remaining}"
                )


    # -----------------------------------
    # CHECK BALANCE
    # -----------------------------------
    elif option == "Check Balance":

        st.subheader("📊 Account Balance")

        entered_pin = st.text_input(
            "Enter PIN to view balance",
            type="password"
        )

        if st.button("Check Balance"):

            if entered_pin == st.session_state.pin:

                st.metric(
                    "Current Balance",
                    f"₹{st.session_state.balance}"
                )

            else:

                st.session_state.wrong_attempts += 1
                check_lock()

                remaining = 3 - st.session_state.wrong_attempts

                st.error(
                    f"❌ Wrong PIN. Attempts left: {remaining}"
                )


    # -----------------------------------
    # TRANSACTION HISTORY
    # -----------------------------------
    elif option == "Transaction History":

        st.subheader("📜 Transaction History")

        entered_pin = st.text_input(
            "Enter PIN to view transactions",
            type="password"
        )

        if st.button("View Transactions"):

            if entered_pin == st.session_state.pin:

                if st.session_state.transactions:

                    for t in st.session_state.transactions[::-1]:
                        st.write(t)

                else:
                    st.info("No transactions yet")

            else:

                st.session_state.wrong_attempts += 1
                check_lock()

                remaining = 3 - st.session_state.wrong_attempts

                st.error(
                    f"❌ Wrong PIN. Attempts left: {remaining}"
                )


    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    elif option == "Logout":

        st.session_state.logged_in = False

        st.success("✅ Logged out successfully")

        st.rerun()


