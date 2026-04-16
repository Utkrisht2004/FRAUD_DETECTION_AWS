import gradio as gr
import requests

# 🚨 DOUBLE CHECK THIS URL: It must be the BACKEND (ac34...) URL, not the Frontend (a1ee...) URL
API_URL = "http://ac348f0ea3fd04688907b4d8572a1b24-1164067965.ap-south-1.elb.amazonaws.com/predict"

def predict_transaction(*args):
    keys = [
        "TransactionAmt", "ProductCD", "card1", "card2", "card3", "card5",
        "addr1", "addr2", "dist1", "C1", "C2", "C6", "C9", "C11", "C13", "D1", "D4", "D10"
    ]
    # Build the payload
    data_payload = {keys[i]: args[i] for i in range(len(keys))}
    
    try:
        response = requests.post(API_URL, json={"data": data_payload}, timeout=10)
        result = response.json()
        
        # If the API returned an error (422 or 500), 'is_fraud' won't be there
        if "is_fraud" not in result:
            return "❌ API Rejection", f"The API returned this instead: {result}"
            
        verdict = "🚨 FRAUDULENT" if result["is_fraud"] else "✅ LEGITIMATE"
        analytics = f"Confidence: {result['confidence']}% | Threshold: {result.get('threshold_used', 'N/A')}"
        return verdict, analytics
    except Exception as e:
        return "❌ Connection Error", f"Could not reach the Backend API: {str(e)}"

css = """
body { background-color: #0a0f1e; }
.gradio-container { background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 100%) !important; color: #e0e6f0; }
h1 { color: #00d4ff !important; text-align: center !important; }
"""

with gr.Blocks(title="IEEE Fraud Detection", css=css) as app:
    gr.Markdown("# 🛡️ REAL-TIME FRAUD DETECTION")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 💳 Transaction Details")
            with gr.Row():
                transaction_amt = gr.Number(label="Transaction Amount ($)", value=100.0)
                # FIX: Dropdown ensures the data is sent as a STRING ("W"), not a number
                product_cd = gr.Dropdown(["W", "H", "C", "S", "R"], label="Product Code", value="W")
            with gr.Row():
                card1 = gr.Number(label="Card 1", value=9500); card2 = gr.Number(label="Card 2", value=360.0)
            with gr.Row():
                card3 = gr.Number(label="Card 3", value=150.0); card5 = gr.Number(label="Card 5", value=226.0)
            with gr.Row():
                addr1 = gr.Number(label="Address 1", value=299.0); addr2 = gr.Number(label="Address 2", value=87.0); dist1 = gr.Number(label="Dist", value=0.0)

            gr.Markdown("### 📊 Features")
            with gr.Row():
                c1 = gr.Number(value=1.0); c2 = gr.Number(value=1.0); c6 = gr.Number(value=1.0)
            with gr.Row():
                c9 = gr.Number(value=1.0); c11 = gr.Number(value=1.0); c13 = gr.Number(value=1.0)
            with gr.Row():
                d1 = gr.Number(value=0.0); d4 = gr.Number(value=0.0); d10 = gr.Number(value=0.0)

        with gr.Column(scale=1):
            gr.Markdown("### 🔍 Analysis Result")
            output_verdict = gr.Textbox(label="Verdict")
            output_analytics = gr.Textbox(label="Model Analytics")
            predict_btn = gr.Button("🔍 PREDICT", variant="primary")

    all_inputs = [transaction_amt, product_cd, card1, card2, card3, card5,
                  addr1, addr2, dist1, c1, c2, c6, c9, c11, c13, d1, d4, d10]
    
    predict_btn.click(fn=predict_transaction, inputs=all_inputs, outputs=[output_verdict, output_analytics])

app.launch(server_name="0.0.0.0", server_port=7860)