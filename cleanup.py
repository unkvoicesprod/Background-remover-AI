import os
import shutil

def clean_project():
    """
    Remove arquivos de relatório, análise e caches que não são 
    necessários para a execução do programa principal.
    """
    # Arquivos gerados por análises técnicas anteriores (não usados pelo app)
    files_to_remove = [
        "STATUS_VISUAL.txt",
        "README_ANALISE.md",
        "RESUMO_EXECUTIVO.md",
        "DETALHES_CORRECOES.md",
        "RELATORIO_ANALISE.md",
        "MANUTENCAO.md"
        # "validate.py" # Descomente esta linha se quiser remover também o validador
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Iniciando limpeza em: {base_dir}")
    print("-" * 40)

    for filename in files_to_remove:
        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removido: {filename}")
            except Exception as e:
                print(f"❌ Erro ao remover {filename}: {e}")
        else:
            pass # Arquivo já não existe

    # Limpeza de cache do Python (__pycache__)
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if d == "__pycache__":
                try:
                    shutil.rmtree(os.path.join(root, d))
                    print(f"✅ Cache limpo em: {os.path.relpath(root, base_dir)}")
                except Exception: pass

    print("-" * 40)
    print("Limpeza concluída!")

if __name__ == "__main__":
    clean_project()