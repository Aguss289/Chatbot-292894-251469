# pyright: reportCallIssue=false

import pandas as pd
from typing import List, Mapping, cast


CHUNK_SIZE = 500  # caracteres (ajustable)


def read_excel(path: str) -> Mapping[str, pd.DataFrame]:
	xls = pd.ExcelFile(path)
	dfs = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
	return cast(Mapping[str, pd.DataFrame], dfs)


def create_summary_documents(dfs: Mapping[str, pd.DataFrame]) -> List[dict]:
	"""Crea UN SOLO documento con TODA la información necesaria"""
	docs = []
	
	if 'Ventas' in dfs and 'Productos' in dfs and 'Clientes' in dfs:
		df_ventas = dfs['Ventas']
		df_prod = dfs['Productos']
		df_cli = dfs['Clientes']
		
		# Merge completo
		ventas_full = df_ventas.merge(df_prod, on='IdProducto').merge(df_cli, on='IdCliente')
		ventas_full['Total'] = ventas_full['Cantidad'] * ventas_full['Precio']
		ventas_full['FechaVenta'] = pd.to_datetime(ventas_full['FechaVenta'])
		ventas_full['Año'] = ventas_full['FechaVenta'].dt.year
		ventas_full['Mes'] = ventas_full['FechaVenta'].dt.month
		ventas_full['MesAño'] = ventas_full['FechaVenta'].dt.strftime('%Y-%m')
		
		# UN SOLO DOCUMENTO COMPLETO
		doc_completo = f"""=== BASE DE DATOS COMPLETA DE VENTAS ===

1. RESUMEN GENERAL:
Total ventas: {len(df_ventas)}
Ingresos totales: ${ventas_full['Total'].sum():,.2f}
Ticket promedio: ${ventas_full['Total'].mean():.2f}
Unidades vendidas: {int(ventas_full['Cantidad'].sum())}

2. PRODUCTOS ({len(df_prod)} productos):
Categorías: {', '.join(df_prod['Categoria'].unique())}
Producto más vendido (unidades): {ventas_full.groupby('NombreProducto')['Cantidad'].sum().idxmax()} ({int(ventas_full.groupby('NombreProducto')['Cantidad'].sum().max())} unidades)
Producto más vendido (ingresos): {ventas_full.groupby('NombreProducto')['Total'].sum().idxmax()} (${ventas_full.groupby('NombreProducto')['Total'].sum().max():,.2f})

Top 10 productos por ventas:
{ventas_full.groupby('NombreProducto').agg({'Cantidad': 'sum', 'Total': 'sum'}).sort_values(by='Total', ascending=False).head(10).to_string()}

Ventas por categoría:
{ventas_full.groupby('Categoria')['Total'].sum().sort_values(ascending=False).to_string()}

3. CLIENTES ({len(df_cli)} clientes):
Ciudades: {', '.join(df_cli['Ciudad'].unique())}
Cliente con más compras: {ventas_full.groupby('NombreCliente')['IdVenta'].count().idxmax()} ({int(ventas_full.groupby('NombreCliente')['IdVenta'].count().max())} compras)
Cliente con más ingresos: {ventas_full.groupby('NombreCliente')['Total'].sum().idxmax()} (${ventas_full.groupby('NombreCliente')['Total'].sum().max():,.2f})

Top 10 clientes:
{ventas_full.groupby('NombreCliente').agg({'IdVenta': 'count', 'Total': 'sum'}).sort_values(by='Total', ascending=False).head(10).to_string()}

Ventas por ciudad:
{ventas_full.groupby('Ciudad').agg({'IdVenta': 'count', 'Total': 'sum'}).sort_values(by='Total', ascending=False).to_string()}

4. ANÁLISIS TEMPORAL:
VENTAS POR AÑO (número de transacciones):
- Año 2023: {len(ventas_full[ventas_full['Año'] == 2023])} ventas
- Año 2024: {len(ventas_full[ventas_full['Año'] == 2024])} ventas

Detalle por año:
{ventas_full.groupby('Año').agg({'IdVenta': 'count', 'Total': 'sum', 'Cantidad': 'sum'}).to_string()}

Ventas por mes (YYYY-MM, número de transacciones):
{ventas_full.groupby('MesAño').agg({'IdVenta': 'count', 'Total': 'sum'}).sort_index().to_string()}

5. DETALLES POR AÑO 2023:
{f"Transacciones: {len(ventas_full[ventas_full['Año'] == 2023])}" if 2023 in ventas_full['Año'].values else "No hay datos de 2023"}
{f"Ingresos: ${ventas_full[ventas_full['Año'] == 2023]['Total'].sum():,.2f}" if 2023 in ventas_full['Año'].values else ""}
{f"Top 3 productos 2023: {ventas_full[ventas_full['Año'] == 2023].groupby('NombreProducto')['Total'].sum().sort_values(ascending=False).head(3).to_dict()}" if 2023 in ventas_full['Año'].values else ""}

6. DETALLES POR AÑO 2024:
{f"Transacciones: {len(ventas_full[ventas_full['Año'] == 2024])}" if 2024 in ventas_full['Año'].values else "No hay datos de 2024"}
{f"Ingresos: ${ventas_full[ventas_full['Año'] == 2024]['Total'].sum():,.2f}" if 2024 in ventas_full['Año'].values else ""}
{f"Top 3 productos 2024: {ventas_full[ventas_full['Año'] == 2024].groupby('NombreProducto')['Total'].sum().sort_values(ascending=False).head(3).to_dict()}" if 2024 in ventas_full['Año'].values else ""}

NOTA: Los datos NO incluyen información sobre vendedores, canales de venta, formas de pago ni locales/sucursales específicos. Solo se tiene información de productos, clientes (con ciudades) y fechas de venta."""
		
		docs.append({"page_content": doc_completo, "metadata": {"type": "complete", "priority": "highest"}})
	
	return docs


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
		docs.append({"page_content": text, "metadata": {"table": table_name, "type": "detail"}})
	return docs


def chunk_text(text: str, size: int = CHUNK_SIZE):
	for i in range(0, len(text), size):
		yield text[i:i+size]


def build_documents_from_excel(path: str) -> List[dict]:
	dfs = read_excel(path)
	
	# SOLO crear documentos de resumen - NO documentos individuales
	# Esto hace que el sistema sea mucho más rápido y preciso
	print("[INFO] Generando documentos de resumen optimizados...")
	summary_docs = create_summary_documents(dfs)
	print(f"[INFO] Total de documentos: {len(summary_docs)}")
	
	return summary_docs


if __name__ == "__main__":
	import os
	default_path = os.path.join(os.path.dirname(__file__), "..", "TrabajoFinalPowerBI_v2 (1).xlsx")
	path = os.getenv("DATASET_PATH", default_path)
	docs = build_documents_from_excel(path)
	print(f"Documentos generados: {len(docs)}")