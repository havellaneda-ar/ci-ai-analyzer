import os
import requests

def get_logs(run_id, repo):
    token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/logs"
    response = requests.get(url, headers=headers, allow_redirects=True)
    return response.text[:4000]  # limitamos para no pasarnos de tokens

def analyze_with_ai(logs):
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Eres un experto en CI/CD. Analizá errores de pipelines y dá soluciones concretas y cortas en español."
            },
            {
                "role": "user",
                "content": f"Este pipeline falló. Analizá el error y decí qué lo causó y cómo fixearlo:\n\n{logs}"
            }
        ]
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers=headers
    )
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    repo = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]

    print("📥 Bajando logs...")
    logs = get_logs(run_id, repo)

    print("🤖 Analizando con AI...")
    analysis = analyze_with_ai(logs)

    print("\n--- AI Analysis ---")
    print(analysis)