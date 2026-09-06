# Databricks notebook source
# MAGIC %md
# MAGIC ## Validação do baseline de segurança
# MAGIC
# MAGIC Este notebook valida os objetos de governança criados no Unity Catalog.
# MAGIC
# MAGIC > Ajuste os nomes de `Storage Credential` e `External Location` conforme a execução atual do bootstrap. Nesta execução de validação foram usados `sc_bootstrap_dev_005` e `el_bootstrap_bronze_dev_005`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Listar Storage Credentials

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW STORAGE CREDENTIALS;
# MAGIC
# MAGIC -- Resultado esperado:
# MAGIC -- localizar a Storage Credential criada nesta execução do bootstrap.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Inspecionar a Storage Credential

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE STORAGE CREDENTIAL sc_bootstrap_dev_005;
# MAGIC
# MAGIC -- Resultado esperado:
# MAGIC -- confirmar que a credential utiliza Azure Managed Identity
# MAGIC -- e está associada ao Access Connector usado nesta execução.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Inspecionar a External Location

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTERNAL LOCATION el_bootstrap_bronze_dev_005;
# MAGIC
# MAGIC -- Resultado esperado:
# MAGIC -- confirmar a URL do ADLS e a Storage Credential associada.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Verificar grants da External Location

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANTS ON EXTERNAL LOCATION el_bootstrap_bronze_dev_005;
# MAGIC
# MAGIC -- Resultado:
# MAGIC -- exibe privilégios explicitamente concedidos sobre a External Location.
# MAGIC -- Nenhuma linha significa que não há grants explícitos retornados por esta consulta.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Verificar grants da Storage Credential

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANTS ON STORAGE CREDENTIAL sc_bootstrap_dev_005;
# MAGIC
# MAGIC -- Resultado:
# MAGIC -- exibe privilégios explicitamente concedidos sobre a Storage Credential.
# MAGIC -- Nenhuma linha significa que não há grants explícitos retornados por esta consulta.