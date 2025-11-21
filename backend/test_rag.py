"""
Script de prueba para verificar el sistema RAG
Ejecutar: python test_rag.py
"""

import os
from dotenv import load_dotenv
from data_loader import build_documents_from_excel
from rag_pipeline import build_qa

# Cargar variables de entorno
load_dotenv("env")

def test_data_loading():
    """Prueba 1: Verificar que se carga el Excel correctamente"""
    print("\n" + "="*60)
    print("PRUEBA 1: Carga de datos desde Excel")
    print("="*60)
    
    dataset_path = os.getenv("DATASET_PATH", "../TrabajoFinalPowerBI_v2 (1).xlsx")
    
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Dataset no encontrado en {dataset_path}")
        return False
    
    print(f"✅ Dataset encontrado: {dataset_path}")
    
    try:
        docs = build_documents_from_excel(dataset_path)
        print(f"✅ Documentos generados: {len(docs)}")
        
        if len(docs) > 0:
            print(f"\n📄 Ejemplo de documento:")
            print(f"   Contenido: {docs[0]['page_content'][:200]}...")
            print(f"   Metadata: {docs[0]['metadata']}")
            return True
        else:
            print("❌ ERROR: No se generaron documentos")
            return False
            
    except Exception as e:
        print(f"❌ ERROR al cargar datos: {e}")
        return False

def test_vectorstore():
    """Prueba 2: Verificar que existe el vectorstore"""
    print("\n" + "="*60)
    print("PRUEBA 2: Vectorstore FAISS")
    print("="*60)
    
    vectorstore_dir = os.getenv("VECTORSTORE_DIR", "../vectorstore")
    
    if not os.path.exists(vectorstore_dir):
        print(f"❌ ERROR: Vectorstore no encontrado en {vectorstore_dir}")
        print(f"   Ejecuta primero: python embeddings_builder.py")
        return False
    
    faiss_file = os.path.join(vectorstore_dir, "index.faiss")
    pkl_file = os.path.join(vectorstore_dir, "index.pkl")
    
    if os.path.exists(faiss_file) and os.path.exists(pkl_file):
        print(f"✅ Vectorstore encontrado en {vectorstore_dir}")
        print(f"   - index.faiss: {os.path.getsize(faiss_file):,} bytes")
        print(f"   - index.pkl: {os.path.getsize(pkl_file):,} bytes")
        return True
    else:
        print(f"❌ ERROR: Archivos del vectorstore incompletos")
        return False

def test_openai_key():
    """Prueba 3: Verificar que la API key de OpenAI está configurada"""
    print("\n" + "="*60)
    print("PRUEBA 3: Configuración OpenAI")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no configurada en backend/env")
        return False
    
    if api_key.startswith("sk-"):
        print(f"✅ API Key configurada: {api_key[:15]}...{api_key[-4:]}")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"✅ Modelo configurado: {model}")
        return True
    else:
        print("❌ ERROR: API Key no parece válida (debe empezar con 'sk-')")
        return False

def test_rag_pipeline():
    """Prueba 4: Verificar que el pipeline RAG funciona"""
    print("\n" + "="*60)
    print("PRUEBA 4: Pipeline RAG Completo")
    print("="*60)
    
    try:
        print("🔄 Inicializando pipeline RAG...")
        qa = build_qa()
        print("✅ Pipeline RAG inicializado correctamente")
        
        # Prueba con una pregunta simple
        test_question = "¿Qué información tienes disponible?"
        print(f"\n🤔 Pregunta de prueba: '{test_question}'")
        print("🔄 Consultando al sistema RAG...")
        
        answer = qa.run(test_question)
        
        print(f"\n✅ Respuesta obtenida:")
        print(f"   {answer[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR en pipeline RAG: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*60)
    print("🧪 TEST SUITE - Sistema RAG Chatbot")
    print("="*60)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Carga de datos", test_data_loading()))
    results.append(("Vectorstore FAISS", test_vectorstore()))
    results.append(("Configuración OpenAI", test_openai_key()))
    
    # Solo probar RAG si las pruebas anteriores pasaron
    if all(r[1] for r in results):
        results.append(("Pipeline RAG", test_rag_pipeline()))
    else:
        print("\n⚠️ Saltando prueba de RAG (pruebas anteriores fallaron)")
        results.append(("Pipeline RAG", None))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    for name, result in results:
        if result is True:
            status = "✅ PASÓ"
        elif result is False:
            status = "❌ FALLÓ"
        else:
            status = "⏭️ OMITIDA"
        print(f"{status:12} - {name}")
    
    # Resultado final
    passed = sum(1 for _, r in results if r is True)
    total = len([r for r in results if r[1] is not None])
    
    print("\n" + "="*60)
    if passed == total:
        print(f"✅ TODAS LAS PRUEBAS PASARON ({passed}/{total})")
        print("="*60)
        print("\n🎉 El sistema está listo para usar!")
        print("\nPróximos pasos:")
        print("  1. Inicia el backend: uvicorn app:app --reload")
        print("  2. Inicia el frontend: cd ../frontend && npm run dev")
        print("  3. Abre http://localhost:5173 en tu navegador")
    else:
        print(f"⚠️ ALGUNAS PRUEBAS FALLARON ({passed}/{total} pasaron)")
        print("="*60)
        print("\nRevisa los errores arriba y corrige antes de continuar.")
    
    print()

if __name__ == "__main__":
    main()

