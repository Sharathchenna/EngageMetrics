import streamlit as st
from typing import Optional
import requests

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "266a92da-f25d-4350-a70c-ec9984ba99fa"
FLOW_ID = "ad67d18e-ed45-425f-8380-4b5400c22da8"
APPLICATION_TOKEN = "<ENTER YOUR APPLICATION TOKEN>"
TWEAKS = {
    "ChatInput-9vauS": {},
    "ChatOutput-TojAu": {},
    "OpenAIModel-SPpeb": {},
    "File-pcWQi": {},
    "AstraDB-H0bkV": {},
    "OpenAIEmbeddings-59oyL": {},
    "Prompt-4Mipb": {},
    "ParseData-fWDBv": {},
    "AstraDB-Rk1Mh": {},
    "OpenAIEmbeddings-diXrs": {},
    "SplitText-Qz9ua": {}
}

# Function to run the flow
def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None
) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Streamlit UI
st.title("Your Personal Social Media Analyst")
st.subheader("Enter your query and get insights!")

# Input fields
message = st.text_area("Prompt", placeholder="Enter your prompt here...")
endpoint = FLOW_ID
output_type = "chat"
input_type = "chat"

# Run button
if st.button("Analyse"):
    if not message.strip():
        st.error("Input Message cannot be empty!")
    else:
        with st.spinner("Running the flow..."):
            response = run_flow(
                message=message,
                endpoint=endpoint,
                output_type=output_type,
                input_type=input_type,
                tweaks=TWEAKS,
                application_token=APPLICATION_TOKEN
            )
        
        if "error" in response:
            st.text("Something went wrong!, Try again later.")
            print(f"Error: {response['error']}")
        else:
            st.success("Flow executed successfully!")
            try:
                # Extract the final output text
                final_output = (
                    response.get("outputs", [{}])[0]
                    .get("outputs", [{}])[0]
                    .get("results", {})
                    .get("message", {})
                    .get("text", "No final text found.")
                )
                st.markdown(f"### Final Output:\n\n{final_output}")
            except Exception as e:
                st.error(f"Unexpected response structure: {e}")
                st.text("Unable to process the output.")