import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Perplexity (OpenAI-compatible)
api_key = os.getenv("PERPLEXITY_API_KEY")
if api_key and api_key != "your_perplexity_api_key_here":
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    model_name = "sonar"
else:
    client = None
    model_name = None

def get_python_help(query: str, dataset_context: str = "") -> str:
    """
    Analyzes the query and returns a helpful response about Python syntax or modules using Perplexity.
    """
    if not client:
        return """
### Perplexity API Key Missing
Please set your `PERPLEXITY_API_KEY` in the `.env` file to enable the AI.
"""

    system_prompt = """
    You are an expert Machine Learning Assistant. 
    Your goal is to provide clear, concise, and high-quality guidance on Python for Machine Learning.

    Rules:
    1. **Persona**: Act as a Senior ML Engineer. Prioritize libraries like Pandas, NumPy, Scikit-learn, PyTorch, TensorFlow, and Matplotlib.
    2. **Best Practices**: ALWAYS recommend the most efficient and standard approach (e.g., "Use vectorization instead of loops"). Explain *why* it is the best way.
    3. **Math Support**: When explaining algorithms, use LaTeX formatting for mathematical formulas (enclose in $$ for display mode or $ for inline).
    4. **Deep Learning & Visualization**: 
       - You are an expert in Neural Networks (CNNs, RNNs, Transformers).
       - When asked about architectures, use **Mermaid.js** diagrams to visualize them. Use the `mermaid` code block.
    5. **Full Programs**: If the user asks to "create a program" or "solve a task", provide the **COMPLETE, RUNNABLE** Python code in a single block. Do not give partial snippets unless asked.
    6. **Data Preprocessing**: You are an expert in data cleaning:
       - **Null Values**: Always check `df.isnull().sum()` first. Recommend `SimpleImputer` for numeric columns or `fillna` for simple cases.
       - **Imbalanced Data**: Recommend `SMOTE` from `imblearn` or `class_weight='balanced'` in sklearn models.
       - **Encoding**: Use `LabelEncoder` for target variables, `OneHotEncoder` or `pd.get_dummies` for features.
    7. **Scope**: Focus on Python ML/Data Science.
    """
    
    full_query = query
    if dataset_context:
        full_query = f"CONTEXT: The user is working with this dataset:\n{dataset_context}\n\nUse these columns and structure in your code.\n\nQUERY: {query}"
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"### AI Error\nAn error occurred while contacting the AI: {str(e)}"
