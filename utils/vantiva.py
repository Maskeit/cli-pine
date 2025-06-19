"""
vantiva-cli.py
Command line interface
Created by Miguel Alejandre / @Maskeit
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import re
from pinecone import Pinecone

os.environ['PINECONE_API_KEY'] = "pcsk_2a3MQz_otCFT2VN4UbsCafCGJdh3Qh9wrpFCM2R7AGAq536bqRvx5EGwMUmuPhrASGeHa"
INDEX_NAME = "taller"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
pinecone = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pinecone.Index(INDEX_NAME)

# Limpia texto de saltos o espacios raros
def limpiar_texto(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# Metodo para generar embeddings
def generar_embeddings(ruta_pdf):
    print(f"Generando embeddings de {ruta_pdf}...")
    loader = PyPDFLoader(ruta_pdf)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    texts = []
    for chunk in chunks:
        texto_limpio = limpiar_texto(chunk.page_content)
        texts.append(texto_limpio)
    vectors = embeddings.embed_documents(texts)

    pinecone_vectors = [
        {"id": f"chunk-{i}", "values": vec, "metadata": {"text": texts[i]}}
        for i, vec in enumerate(vectors)
    ]
    index.upsert(vectors=pinecone_vectors)
    print("Embeddings generados y subidos.")

# Elimina un indice completo cuidado porque tambien elimina los vectores!!
def eliminar_indice(nombre):
    pinecone.delete_index(nombre)
    print(f"Índice '{nombre}' eliminado.")

# Muestra informacion de todos los indices de pinecone
def listar_indices():
    indices = pinecone.list_indexes()
    print("Índices en Pinecone:")
    for i in indices:
        print(f" - {i}")
        
# muestra la infor de un solo indice pedido
def mostrar_info_indice():
    try:
        info = pinecone.describe_index(index=INDEX_NAME)
        print(f"Información del índice :")
        for k, v in info.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Error al obtener información del índice : {e}")

def buscar_pregunta(pregunta):
    query_vec = embeddings.embed_query(pregunta)
    res = index.query(vector=query_vec, top_k=3, include_metadata=True)
    for match in res['matches']:
        print(f"\n[Score: {match['score']:.2f}]")
        print(match['metadata']['text'])


# elimina un vector por id
def eliminar_vector_por_id(vector_id):
    index.delete(ids=[vector_id])
    print(f"Vector con ID '{vector_id}' eliminado.")

# elimina un vector por metadata
def eliminar_vector_por_metadata(campo, valor):
    filtro = {campo: {"$eq": valor}}
    index.delete(filter=filtro)
    print(f"Vectores con {campo} = '{valor}' eliminados.")

# elimina todos los vectores, limpia la BDV
def eliminar_todos_los_vectores():
    index.delete(delete_all=True)
    print("Todos los vectores han sido eliminados del índice.")

    
# Nueva función para generar y guardar chunks limpios en un archivo .txt
def generar_embeddings_a_txt(ruta_pdf, nombre_salida="debug_chunks.txt"):
    print(f"Generando y guardando chunks de {ruta_pdf} en {nombre_salida}...")
    loader = PyPDFLoader(ruta_pdf)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    with open(nombre_salida, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            texto_limpio = limpiar_texto(chunk.page_content)
            f.write(f"=== CHUNK {i} ===\n{texto_limpio}\n\n")
    print(f"Chunks guardados localmente en {nombre_salida}.")