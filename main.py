"""
main.py
Command line interface
Created by Miguel Alejandre / @Maskeit
"""
import os
from utils.utils import (
    generar_embeddings,
    eliminar_indice,
    listar_indices,
    buscar_pregunta,
    mostrar_info_indice,
    eliminar_vector_por_id,
    eliminar_vector_por_metadata,
    eliminar_todos_los_vectores,
    generar_embeddings_a_txt,
    cargar_indice
)

def menu():
    global index
    print("=== CONFIGURACIÓN INICIAL ===")
    index_name = input("Nombre del índice Pinecone a usar o crear: ")
    index = cargar_indice(index_name)
    if index is None:
        return

    while True:
        print("\n=== MENÚ VANTIVA EMBEDDINGS ===")
        print("1. Generar embeddings de un PDF")
        print("2. Eliminar índice de Pinecone")
        print("3. Listar índices existentes")
        print("4. Buscar pregunta (demo)")
        print("5. Salir")
        print("6. Eliminar vector por ID o metadato")
        print("7. Limpiar todos los vectores del índice")
        print("8. Mostrar información del índice")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            ruta = input("Ruta al archivo PDF: ")
            generar_embeddings(index, ruta)
        elif opcion == '2':
            eliminar_indice(index_name)
        elif opcion == '3':
            listar_indices()
        elif opcion == '4':
            pregunta = input("Escribe tu pregunta: ")
            buscar_pregunta(index, pregunta)
        elif opcion == '5':
            print("Saliendo...")
            break
        elif opcion == '6':
            clave = input("¿Eliminar por ID o metadato? (id/metadata): ")
            if clave == 'id':
                vector_id = input("ID del vector a eliminar: ")
                eliminar_vector_por_id(index, vector_id)
            elif clave == 'metadata':
                campo = input("Nombre del campo de metadata (e.g. 'text'): ")
                valor = input("Valor del campo a eliminar: ")
                eliminar_vector_por_metadata(index, campo, valor)
            else:
                print("Opción inválida.")
        elif opcion == '7':
            confirmar = input("¿Seguro que quieres borrar TODOS los vectores? (si/no): ")
            if confirmar.lower() == "si":
                eliminar_todos_los_vectores(index)
        elif opcion == '8':        
            mostrar_info_indice(index)
        elif opcion == '9':
            ruta = input("Ruta al archivo PDF: ")
            generar_embeddings_a_txt(ruta, "salida.txt")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()