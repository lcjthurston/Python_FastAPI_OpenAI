import openai

openai.api_type = "azure"
openai.api_base = "https://ai-hubprojectai485604242543.services.ai.azure.com/models"
openai.api_key = "6mliRVBGRptosgveyENNCq0355fVaLOg1aa3XgZsodXDiBaJz14CJQQJ99BFACHYHv6XJ3w3AAAAACOGAFGz"
openai.api_version = "2023-05-15"

response = openai.Embedding.create(
    input="This is a sample text that I would like you to try content embeedding on ... blah blah blah",
    engine="embedding-model"
)

embedding = response['data'][0]['embedding']
