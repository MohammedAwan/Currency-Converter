import requests
import streamlit as st

#Function to get available currency list
def cur_list():
    url = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.min.json'
    try:
        response = requests.get(url)
        cur_list = []
        for i in response.json():
            cur_list.append(response.json()[i])
        return cur_list , response.json()
    except Exception as e:
        print("Error while getting list",e)

#Function to get current rates
def get_rate(cur_code):
    url = f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{cur_code}.json'
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return 0    

#Function to convert currency name to currency code
def nameToCode(name, dict):
    for i in dict:
        if dict[i] == name:
            return i

#Function to convert rates
def convert(currency_dict):
    
    from_code = nameToCode(st.session_state.from_code, currency_dict)
    to_code = nameToCode(st.session_state.to_code, currency_dict)
    from_amount = st.session_state.from_amount
    rates = get_rate(from_code)
    if rates == 0:
        print("Could not fetch rates")
    elif to_code in rates[from_code]:
        new_amount = round(rates[from_code][to_code] * from_amount, 2)
        st.session_state.converted_amount = new_amount
        print("Conversion successful")
    

def main():
    st.title("Currency Converter")
    
    # Initializing Session state
    if 'from_code' not in st.session_state:
        st.session_state.from_code = 'Indian Rupee'
        st.session_state.from_amount = 1
        st.session_state.to_code = 'US Dollar'
        
    # Fetching available currency list
    currency_list, currency_dict = cur_list()
    
    # Input boxes
    left,right = st.columns([1,2])
    with left:
        from_currency = st.selectbox(label = "Select Currency", options= currency_list, key = 'from_code',on_change = convert(currency_dict))
        to_currency = st.selectbox(label = "To Currency", options= currency_list, key = 'to_code',on_change = convert(currency_dict))
    with right:
        amount = st.number_input(label="Enter Amount", min_value = 0, key='from_amount',on_change = convert(currency_dict) )
        converted = st.number_input(label="Converted Amount", key ='converted_amount' )

if __name__ == '__main__':
    main()