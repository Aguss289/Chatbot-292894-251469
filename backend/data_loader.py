import pandas as pd
from pathlib import Path
from typing import List, Dict


CHUNK_SIZE = 500 # caracteres (ajustable)


def read_excel(path: str) -> Dict[str, pd.DataFrame]:
	xls = pd.ExcelFile(path)
	dfs = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
	return dfs


def row_to_text(row: pd.Series, table_name: str) -> str:
	# Convierte una fila a texto legible
	parts = [f"Tabla: {table_name}"]
	for c, v in row.items():
		parts.append(f"{c}: {v}")
	return " | ".join(parts)


def dataframe_to_documents(df: pd.DataFrame, table_name: str) -> List[dict]:
	docs = []
	for _, r in df.iterrows():
		text = row_to_text(r, table_name)
		docs.append({"page_content": text, "metadata": {"table": table_name}})
	return docs


def chunk_text(text: str, size: int = CHUNK_SIZE):
	for i in range(0, len(text), size):
		yield text[i:i+size]


def build_documents_from_excel(path: str) -> List[dict]:
	dfs = read_excel(path)
	all_docs = []
	for name, df in dfs.items():
		docs = dataframe_to_documents(df, name)
		# opcional: chunkear textos extensos
		expanded = []
		for d in docs:
			txt = d["page_content"]
			if len(txt) > CHUNK_SIZE:
				for chunk in chunk_text(txt):
					expanded.append({"page_content": chunk, "metadata": d["metadata"]})
			else:
				expanded.append(d)
		all_docs.extend(expanded)
	return all_docs


if __name__ == "__main__":
	import os
	path = os.getenv("DATASET_PATH", "F:/ORT/8vo Semestre/SISTEMA SOPORTE DECISION/Obligatorio IA/TrabajoFinalPowerBI_v2 (1).xlsx")
	docs = build_documents_from_excel(path)
	print(f"Documentos generados: {len(docs)}")