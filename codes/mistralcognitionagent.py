from mistralai import Mistral


def agentclassification(query):
    api_key = "S1pZGonHlgCIFMUzm3Y6O5jShDbJegMl"

    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    response = client.agents.complete(
                agent_id= "ag:becb4bf0:20241012:redirection:8e1c095d",
                messages = [
                    {
                        "role": "user",
                        "content": query
                    },
                ]
            )
    result = response.choices[0].message.content
    return print(result)
