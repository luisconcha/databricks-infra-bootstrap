# Databricks notebook source
# MAGIC %md
# MAGIC ## 0. Desabilitar a retenção de objetos removidos
# MAGIC
# MAGIC Este bootstrap é um ambiente descartável de laboratório. Antes do teardown, vamos verificar e desabilitar a retenção de managed tables removidas.
# MAGIC Cada verificação é executada separadamente para preservar sua saída.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0.1 Catalog

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE CATALOG EXTENDED bootstrap_dev;
# MAGIC
# MAGIC -- Verificar o período de recuperação configurado atualmente no Catalog.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0.2 Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE SCHEMA EXTENDED bootstrap_dev.bronze;
# MAGIC
# MAGIC -- Verificar se o Schema bronze possui configuração própria de recuperação
# MAGIC -- ou se utiliza a configuração herdada do Catalog.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0.3  alterar retenção

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER CATALOG bootstrap_dev RETAIN DROPPED TO 0 HOURS;
# MAGIC
# MAGIC -- Desabilita a recuperação para managed tables removidas posteriormente
# MAGIC -- neste Catalog descartável.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0.4 confirmar Catalog

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE CATALOG EXTENDED bootstrap_dev;
# MAGIC
# MAGIC -- Resultado esperado: Recovery Period Hours = 0.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0.5 confirmar Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE SCHEMA EXTENDED bootstrap_dev.bronze;
# MAGIC
# MAGIC -- Resultado esperado: Recovery Period Hours = 0.
# MAGIC -- Confirma que o Schema bronze está com retenção efetiva de 0 horas
# MAGIC -- antes da remoção da managed table.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Remover os objetos criados no Schema bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS bootstrap_dev.bronze.sales_2021;
# MAGIC
# MAGIC -- Remove a managed table após a retenção ter sido configurada em 0 horas.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bootstrap_dev.bronze;
# MAGIC
# MAGIC -- Resultado esperado: sales_2021 não deve mais aparecer.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP VOLUME IF EXISTS bootstrap_dev.bronze.raw;
# MAGIC
# MAGIC -- Remove o objeto External Volume do Unity Catalog.
# MAGIC -- Os arquivos externos em bronze/raw não são removidos por este comando.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN bootstrap_dev.bronze;
# MAGIC
# MAGIC -- Resultado esperado: o Volume raw não deve mais aparecer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Remover o Schema criado pelo bootstrap

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP SCHEMA IF EXISTS bootstrap_dev.bronze;
# MAGIC
# MAGIC -- Remove o Schema bronze após a exclusão de seus objetos.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN bootstrap_dev;
# MAGIC
# MAGIC -- Resultado esperado: o Schema bronze não deve mais aparecer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Remover o Schema default

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP SCHEMA IF EXISTS bootstrap_dev.default;
# MAGIC
# MAGIC -- Remove o Schema default criado automaticamente com o Catalog.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN bootstrap_dev;
# MAGIC
# MAGIC -- Resultado esperado: deve permanecer apenas information_schema.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Remover o Catalog

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP CATALOG IF EXISTS bootstrap_dev;
# MAGIC
# MAGIC -- Remove o Catalog após a exclusão de todos os Schemas criados pelo bootstrap.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;
# MAGIC
# MAGIC -- Resultado esperado: bootstrap_dev não deve mais aparecer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Remover a External Location e a Storage Credential

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP EXTERNAL LOCATION IF EXISTS el_bootstrap_bronze_dev_005;
# MAGIC
# MAGIC '''
# MAGIC -- Resultado observado:
# MAGIC -- a remoção pode falhar com UC_EXTERNAL_LOCATION_OP_NOT_ALLOWED
# MAGIC -- enquanto existir uma dependent managed table.
# MAGIC
# MAGIC -- Mesmo com `Recovery Period Hours = 0`, a External Location pode permanecer
# MAGIC -- temporariamente bloqueada por uma managed table já removida.
# MAGIC -- Não utilizar `FORCE` como procedimento padrão.
# MAGIC -- Tentar novamente após a conclusão da limpeza interna.
# MAGIC '''

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP STORAGE CREDENTIAL IF EXISTS sc_bootstrap_dev_005;
# MAGIC
# MAGIC '''
# MAGIC -- Resultado observado:
# MAGIC -- a remoção é bloqueada enquanto a External Location depender
# MAGIC -- desta Storage Credential.
# MAGIC -- Não utilizar `FORCE` como procedimento padrão.
# MAGIC '''