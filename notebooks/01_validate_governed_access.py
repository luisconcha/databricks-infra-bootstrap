# Databricks notebook source
# MAGIC %md
# MAGIC ## 1. Ler o arquivo pelo External Volume

# COMMAND ----------

# Path representa o arquivo armazenado fisicamente em: bronze/raw/sales_2021.csv
volume_path = "/Volumes/bootstrap_dev/bronze/raw/sales_2021.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(volume_path)
)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar uma managed table
# MAGIC Com o DataFrame `df` criado na etapa anterior, executar:

# COMMAND ----------

table_name = "bootstrap_dev.bronze.sales_2021"

(df.write.format("delta").mode("overwrite").saveAsTable(table_name))

print(f"Managed table criada: {table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Consultar a managed table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bootstrap_dev.bronze.sales_2021;
# MAGIC
# MAGIC -- isso confirma que a tabela pode ser acessada pelo namespace de três níveis do Unity Catalog: catalog.schema.table
# MAGIC -- neste bootstrap: bootstrap_dev.bronze.sales_2021

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Confirmar que a tabela é MANAGED

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED bootstrap_dev.bronze.sales_2021;
# MAGIC
# MAGIC -- No resultado, localizar a propriedade: "Type    MANAGED"
# MAGIC -- A validação confirma que sales_2021 não é apenas uma referência ao CSV existente em "raw/" trata-se de uma managed table criada e administrada pelo Unity Catalog.