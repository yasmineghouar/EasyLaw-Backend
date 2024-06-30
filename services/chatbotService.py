from configparser import ConfigParser
from cohere.errors import BadRequestError
from langchain_community.embeddings import CohereEmbeddings
from pinecone import Pinecone
import cohere

cohere_secret_key = 'MKrHkdAkUcRog6etmHbEaWTEaigKT4PrASSD8xz5'
pinecone_secret_key = 'a62d3c42-a144-4c53-ae2b-8587e92e6f9e'
pinecone_index_name = 'chatboteasylaw'

def cohere_specialized_call(message):
    """
    Fonction pour effectuer un appel spécialisé à Cohere.

    Args:
        message (str): La requête de l'utilisateur.

    Returns:
        str: La réponse générée en utilisant le contexte récupéré de Pinecone.
    """
    # Initialisation de l'API Cohere
    co = cohere.Client(cohere_secret_key)
    embeddings = CohereEmbeddings(cohere_api_key=cohere_secret_key)

    # Embedding du message
    query = embeddings.embed_query(message)

    # Initialisation de l'index Pinecone
    pc = Pinecone(api_key=pinecone_secret_key)
    index = pc.Index(pinecone_index_name)

    # Requête Pinecone avec le vecteur du message
    results = index.query(
        vector=query,
        top_k=2,
        include_metadata=True,
    )

    if not results.matches:
        response = co.generate(
            prompt=f"""أنت روبوت دردشة متخصص في تقديم الإجابات على الاستفسارات المتعلقة بالقضايا القانونية الجزائرية.
            اكتب ردًا على الاستفسار التالي: {message}""",
            model='command-xlarge-nightly',
            max_tokens=800,
            temperature=0.2,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
    else:
        response = co.generate(
            prompt=f"""أنت روبوت دردشة متخصص في تقديم الإجابات على الاستفسارات المتعلقة بالقضايا القانونية الجزائرية.
            اكتب ردًا على الاستفسار التالي: {message}. {results} وهذه هي الردود التي يجب أن تستوحي منها:""",
            model='command-xlarge-nightly',
            max_tokens=800,
            temperature=0.2,
            stop_sequences=[],
            return_likelihoods='NONE'
        )

    return response.generations[0].text
