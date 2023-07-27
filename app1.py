import streamlit as st
import pandas as pd
from datetime import date
import uuid

st.title("Enter Details for Invoice")
# Get the current date for the invoice
invoice_date = date.today()
# Generate a unique invoice number using UUID
invoice_num = str(uuid.uuid4().int)[:8]
# Get user input for customer details
name = st.text_input('Your Name')
phno = st.text_input('Enter your Phone Number')
email = st.text_input('Enter Your Email-ID')
ad = st.text_area("Billing Address")
# Get the number of items and their details for the invoice
num_items = st.number_input('Number of items', min_value=0, step=1)
data = []
for i in range(num_items):
    item = st.text_input(f'Item {i+1}')
    price = st.number_input(f'Price of item {i+1}', min_value=0)
    quantity = st.number_input(f'Quantity of item {i+1}', min_value=0)
    total = price * quantity
    data.append([item, price, quantity, total])
# Create a DataFrame from the invoice item data
df = pd.DataFrame(data, columns=['item', 'price', 'quantity', 'total'])
# Display the invoice item table
st.table(df)
stotal = df['total'].sum()
# Get the mode of payment from the user
mop = st.selectbox('Mode of Payment', ['Cash', 'Credit Card', 'Debit Card', 'UPI'])
feedback = st.text_input('Feedback')

# If the "Print Invoice" button is clicked
if st.button('Print Invoice'):
    # Check if all required fields are filled
    if not name or not phno or not email or not ad or not num_items:
        st.error("Please fill in all the required fields.")
    else:
        # Create a DataFrame to store the invoice details
        invoice_data = {
            'Customer_Name': [name],
            'Phone_No': [phno],
            'EmailID': [email],
            'Address': [ad],
            'Invoice_Number': [invoice_num],
            'Invoice_Date': [invoice_date],
            'Total_Bill_Amount': [stotal],
            'MOP': [mop],
            'Feedback': [feedback]
        }

        # Append item details to the invoice_data dictionary
        for i, (item, price, quantity, total) in enumerate(data):
            invoice_data[f'Item_{i+1}'] = [item]
            invoice_data[f'Price_{i+1}'] = [price]
            invoice_data[f'Quantity_{i+1}'] = [quantity]

        # Create a DataFrame from the invoice_data dictionary
        df_invoice = pd.DataFrame(invoice_data)

        # Save the invoice data to an Excel file
        excel_filename = f"Invoice_{invoice_num}.xlsx"
        df_invoice.to_excel(excel_filename, index=False)

        # Display the invoice details in a formatted manner using Markdown
        st.markdown(f"### Invoice Data Saved as Excel:")
        st.write(df_invoice)

        # Create a download button for the Excel file
        with open(excel_filename, "rb") as f:
            bytes_data = f.read()
        st.download_button(label="Download Excel File", data=bytes_data, file_name=excel_filename)

