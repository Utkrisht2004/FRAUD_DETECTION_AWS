import gradio as gr
import requests

# ─────────────────────────────────────────
# CONFIGURATION - POINT TO YOUR EKS BACKEND
# ─────────────────────────────────────────
API_URL = "http://ac348f0ea3fd04688907b4d8572a1b24-1164067965.ap-south-1.elb.amazonaws.com/predict"

def predict_transaction(*args):
    # Convert the 18 inputs into the JSON format your API expects
    # (Mapping the UI fields to the dictionary keys)
    keys = [
        "TransactionAmt", "ProductCD", "card1", "card2", "card3", "card5",
        "addr1", "addr2", "dist1", "C1", "C2", "C6", "C9", "C11", "C13", "D1", "D4", "D10"
    ]
    data_payload = {keys[i]: args[i] for i in range(len(keys))}
    
    try:
        response = requests.post(API_URL, json={"data": data_payload}, timeout=10)
        result = response.json()
        
        verdict = "🚨 FRAUDULENT" if result["is_fraud"] else "✅ LEGITIMATE"
        prob_pct = result["confidence"]
        risk = "🔴 HIGH" if prob_pct > 70 else "🟡 MEDIUM" if prob_pct > 30 else "🟢 LOW"

        return f"""
        ## {verdict} TRANSACTION
        **Fraud Probability:** {prob_pct}%
        **Risk Level:** {risk}
        **Threshold:** {result.get('threshold_used', 'N/A')}
        """
    except Exception as e:
        return f"### ❌ Error\nCould not connect to API. Details: {str(e)}"

# ─────────────────────────────────────────
# HER STYLING & UI LAYOUT (UNTOUCHED)
# ─────────────────────────────────────────
css = """
body { background-color: #0a0f1e; }
.gradio-container {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 100%) !important;
    font-family: 'Segoe UI', sans-serif;
    color: #e0e6f0;
}
h1 { color: #00d4ff !important; text-align: center !important; letter-spacing: 2px; }
"""

with gr.Blocks(title="IEEE Fraud Detection", css=css) as app:
    gr.Markdown("# 🛡️ REAL-TIME FRAUD DETECTION\n### IEEE-CIS Dataset — EKS Cloud Production")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 💳 Transaction Details")
            with gr.Row():
                transaction_amt = gr.Number(label="Transaction Amount ($)", value=100.0)
                product_cd = gr.Number(label="Product Code", value=1)
            with gr.Row():
                card1 = gr.Number(label="Card 1", value=9500)
                card2 = gr.Number(label="Card 2", value=360.0)
            with gr.Row():
                card3 = gr.Number(label="Card 3", value=150.0)
                card5 = gr.Number(label="Card 5", value=226.0)
            with gr.Row():
                addr1 = gr.Number(label="Billing Address 1", value=299.0)
                addr2 = gr.Number(label="Billing Address 2", value=87.0)
                dist1 = gr.Number(label="Distance 1", value=0.0)

            gr.Markdown("### 📊 Count & Time Features")
            with gr.Row():
                c1 = gr.Number(label="C1", value=1.0)
                c2 = gr.Number(label="C2", value=1.0)
                c6 = gr.Number(label="C6", value=1.0)
            with gr.Row():
                c9 = gr.Number(label="C9", value=1.0)
                c11 = gr.Number(label="C11", value=1.0)
                c13 = gr.Number(label="C13", value=1.0)
            with gr.Row():
                d1 = gr.Number(label="D1 (Days)", value=0.0)
                d4 = gr.Number(label="D4 (Days)", value=0.0)
                d10 = gr.Number(label="D10 (Days)", value=0.0)

        with gr.Column(scale=1):
            gr.Markdown("### 🔍 Analysis Result")
            output = gr.Markdown(value="*Enter details and click Predict.*")
            predict_btn = gr.Button("🔍 PREDICT", variant="primary")

    all_inputs = [transaction_amt, product_cd, card1, card2, card3, card5,
                  addr1, addr2, dist1, c1, c2, c6, c9, c11, c13, d1, d4, d10]
    
    predict_btn.click(fn=predict_transaction, inputs=all_inputs, outputs=output)

app.launch(server_name="0.0.0.0", server_port=7860)